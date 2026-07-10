# Design — /connect: publicação via Composio + loop de performance via browser

**Status:** draft (2026-07-10) · **Target version:** 1.4.0

## Context

Hoje o pipeline do plugin termina em `outputs/posts/`. Publicar, comentar na golden hour, coletar performance e agendar são passos manuais do usuário. Avaliamos integrar o [Composio](https://docs.composio.dev) (toolkit LinkedIn, 22 tools via MCP hospedado HTTP) e uma revisão crítica derrubou o desenho ingênuo (embarcar `.mcp.json` no plugin). Achados que moldam este design:

1. **A URL do MCP do Composio é por sessão/usuário**, gerada via SDK (`composio.create(user_id, mcp=True)` → URL + headers de auth). Não há URL fixa para embarcar. TTL/estabilidade da URL não é documentado — tratado aqui como efêmero por segurança.
2. **`.mcp.json` embarcado cobraria de 100% dos usuários** por uma feature opcional: server tentando conectar em toda sessão + 22 tools (incluindo delete post e ad targeting) no contexto de toda sessão. Inaceitável.
3. **A API do LinkedIn não expõe o que o loop de memória precisa.** `GET_MY_INFO` retorna nome/headline/foto; não existe tool para listar posts próprios; `GET_SHARE_STATS` é organizacional (scope `rw_organization_admin`, que o LinkedIn proíbe de combinar com `w_member_social`). Impressões e alcance de perfil pessoal só existem na UI.
4. **O app OAuth compartilhado do Composio vive de 429.** Uso real exige app próprio do usuário no LinkedIn Developer Portal (produto "Share on LinkedIn", self-serve, scope `w_member_social`).
5. **A LP (copy honesta v5) afirma que o plugin não publica/agenda.** Este design muda isso — a LP só muda depois da feature funcionando.

**Decisão de arquitetura: híbrida.** Composio é o braço de **escrita** (publicar, comentar, imagem, agendar — onde API é obrigatória). O **browser logado do usuário** é a fonte de **leitura** (analytics semanais, discovery de perfil/posts históricos — onde a API não entrega e a UI entrega). O write-back de URNs + a rotina de leitura fecham, pela primeira vez sem input manual, o loop de auto-enriquecimento de `memory/`.

## Fora de escopo

- Analytics via API (impossível para perfil pessoal — ver Context §3).
- Publicação como organização (`w_organization_social`): v1 é conta pessoal, o ICP do produto.
- Alternativa sem Composio (chamar `POST /rest/posts` direto de um script): reavaliá-la só se o Composio falhar no piloto. O custo dominante (app LinkedIn do usuário) é idêntico nos dois caminhos; o Composio paga seu custo com OAuth flow + storage/refresh de token.
- Qualquer mudança na LP/GTM (Frente 1) — depende de piloto validado.

## Componentes

### 1. Skill `linkedin-connection` + comando `/connect` (onboarding opt-in)

Workflow skill no padrão v1.3.0 (When to trigger / Inputs / Process / Output). Roda depois do `/init`, nunca como pré-requisito. Passos que ela guia:

1. Criar conta no Composio e pegar a API key.
2. Criar app no LinkedIn Developer Portal com o produto "Share on LinkedIn" (passo honesto: ~15-20 min, guia com screenshots em `docs/connect-setup.md`). Colar client id/secret no auth config do Composio.
3. Conectar a conta LinkedIn (OAuth via Composio connected account).
4. Rodar `scripts/composio_connect.py` (novo CLI, mesma suite de `scripts/`):
   - lê `COMPOSIO_API_KEY` do ambiente;
   - cria **ou retoma** (`composio.use`) uma sessão com `mcp=True`, **restrita a 4 tools**: `LINKEDIN_CREATE_LINKED_IN_POST`, `LINKEDIN_CREATE_COMMENT_ON_POST`, `LINKEDIN_INITIALIZE_IMAGE_UPLOAD`, `LINKEDIN_REGISTER_IMAGE_UPLOAD`;
   - persiste `session_id` em `memory/connection.md` (para retomar em vez de recriar);
   - imprime o comando `claude mcp add --transport http linkedin-composio <url> --header ...` pronto para o usuário executar.
5. Smoke test: `GET_MY_INFO` (nome/headline) confirma a conexão e grava headline em `authority-context.md` §1 se o campo estiver vazio (único "discovery" que a API permite — expectativa calibrada).

A config MCP fica no **projeto do usuário**, não no plugin. Quem não roda `/connect` não vê nada disso. URL expirada = erro recuperável: a skill instrui rodar o script de novo (retoma sessão, regenera URL, `claude mcp add` atualiza).

### 2. Skill `publisher` (publicar + golden hour)

Gate 1 (contexto existe) → Gate 2 (lê `memory/`) → checa conexão (`memory/connection.md` + tool disponível; sem conexão → rota para `/connect` ou entrega o post para publicação manual, como hoje).

Fluxo: recebe um arquivo de `outputs/posts/` finalizado (pipeline completo já rodado — humanizer + score) → **mostra o post e pede confirmação explícita** (publicar é externo e irreversível na prática; nunca publicar sem confirmação, inclusive quando disparado por rotina agendada — rotina publica só o que foi pré-aprovado com data marcada) → publica → publica o primeiro comentário (protocolo dos 5 minutos do `post-publication-protocol`) → **Gate 3: grava URN + data + slug em `memory/published-posts.md`** (arquivo novo, append-only) → entrega o restante do protocolo de 90 minutos para execução humana (responder comentários não é automatizável nem desejável automatizar).

### 3. Agendamento

Sem infra própria. `/publish` aceita "agende para terça 9h": cria um scheduled agent (Claude Code cron / Cowork routine) que dispara a skill `publisher` sobre o arquivo pré-aprovado. O post agendado já passou pela confirmação humana no momento do agendamento; a rotina não gera nem altera conteúdo.

### 4. Skill `performance-collector` (rotina semanal, via browser)

O elo que faz a integração valer. Sem Composio — usa o browser logado do usuário (claude-in-chrome / aside-browser):

1. Abre a página de analytics do LinkedIn do próprio perfil.
2. Cruza com `memory/published-posts.md` (URNs/datas) para atribuir números a posts específicos.
3. **Gate 3: write-back em `memory/topic-performance.md` e `winning-hooks.md`** — mesmo formato que o `analytics-interpreter` já usa, para que ele consuma esses dados sem mudança.
4. Sugere rodar `analytics-interpreter` quando houver 4+ semanas de dados.

Agendável como rotina semanal. Degrada explicitamente: sem browser conectado, pede o paste manual (comportamento atual do `analytics-interpreter`).

## Riscos e pré-requisitos

| Risco | Mitigação |
|---|---|
| TTL da URL de sessão Composio não documentado | Pedir confirmação escrita ao suporte Composio **antes da Wave 2**; design já assume efemeridade (retomada via `session_id`) |
| Seletores da UI de analytics do LinkedIn mudam | `performance-collector` lê a página semanticamente (não seletores fixos) e degrada para paste manual |
| Comportamento de `claude mcp add` + env vars no Cowork | Validar na Wave 1; se divergir, documentar caminho Cowork separado |
| Publicação indevida por rotina | Regra dura: rotina só publica arquivo pré-aprovado; nunca gera/edita conteúdo |
| Onboarding de 15-20 min assusta | `/connect` é opcional e o plugin inteiro funciona sem ele; docs com screenshots |

## Waves

- **0** — Confirmação escrita do Composio sobre vida útil da sessão/URL. Sem isso, parar.
- **1** — Protótipo manual (fora do plugin): sessão Composio criada à mão, `claude mcp add` no projeto dev, publicar 1 post de teste + 1 comentário na conta do próprio Henrique. Valida contrato das tools, rate limits do app próprio, e o fluxo no Cowork.
- **2** — `scripts/composio_connect.py` + testes pytest (contrato CLI, sem rede — mock do SDK) + skill `linkedin-connection` + `docs/connect-setup.md`.
- **3** — Skill `publisher` + `memory/published-posts.md` + gate de confirmação + write-back.
- **4** — Agendamento (scheduled agent disparando `publisher` sobre arquivo pré-aprovado).
- **5** — Skill `performance-collector` + integração com `analytics-interpreter`.
- **6** — Integração: menu `linkedin.md`, README, CLAUDE.md, bump 1.4.0 (plugin.json + marketplace.json). Só então avaliar mudança de claims na LP.

## Verification

- `pytest` verde, incluindo testes novos do `composio_connect.py` (contrato CLI via subprocess, padrão do repo).
- Piloto real: 2 posts publicados via `publisher` na conta do Henrique, URNs gravados em `memory/published-posts.md`, primeiro comentário publicado.
- Rotina agendada dispara e publica um post pré-aprovado sem intervenção; um post NÃO aprovado nunca publica.
- `performance-collector` roda contra o perfil real e grava números coerentes em `topic-performance.md`; com browser desconectado, degrada para paste manual sem erro.
- Instalação limpa do plugin **sem** rodar `/connect`: nenhum warning de MCP, nenhuma tool Composio no contexto.
- `grep -ri "composio" linkedin-authority-engine/.claude-plugin/` volta vazio (nada de Composio na config embarcada do plugin).
