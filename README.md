# LinkedIn Authority Engine

> Plugin para **Claude Code** e **Claude Cowork** que transforma a expertise de um founder em autoridade no LinkedIn. Posts tunados pelo algoritmo 360Brew, com perfil de cliente vivo e memória que aprende a cada sessão.

[![versão](https://img.shields.io/badge/versão-1.0.0-black)](./linkedin-authority-engine/.claude-plugin/plugin.json)
[![plataforma](https://img.shields.io/badge/Claude%20Code%20%7C%20Cowork-plugin-blue)](https://thelevr.com)
[![algoritmo](https://img.shields.io/badge/360Brew-v3.0%20Q1%202026-orange)](./linkedin-authority-engine/skills/algoritmo-360brew/SKILL.md)
[![licença](https://img.shields.io/badge/licença-proprietary-lightgrey)](#licença)

Por **[LEVEL TECH](https://thelevel.com.br)** · página do produto: **[thelevr.com](https://thelevr.com)**

---

## O problema

Você é especialista e ninguém no LinkedIn sabe disso. Ou você já tentou: postou por meses, colheu dois likes (um do sócio) e parou. Ou pagou uma agência que devolveu "awareness" e um relatório bonito, sem uma reunião no calendário.

O gargalo nunca foi falta de conhecimento. Foi falta de um sistema que pega o que você sabe e entrega no formato que o algoritmo do LinkedIn premia — toda semana, sem você virar criador de conteúdo de tempo integral.

## O que o plugin faz

Você conversa com a Claude. O plugin lê o seu perfil de autoridade, gera o post no framework certo, tira a cara de IA do texto, dá uma nota técnica antes de publicar e ainda te entrega o protocolo dos 90 minutos seguintes à publicação. Cada post que sai bem alimenta a memória, e o próximo já nasce mais perto da sua voz.

Três coisas separam ele de um gerador de texto genérico:

- **Tunado pelo 360Brew.** Toda decisão de formato, timing, gancho e CTA é checada contra a referência do algoritmo do LinkedIn (v3.0, Q1 2026) — não contra "boas práticas" vagas.
- **Perfil de cliente vivo.** O `authority-context.md` guarda quem você é, sua voz, seus temas e seus números. O conteúdo nasce seu, não de um template.
- **Memória auto-enriquecedora.** Padrões que funcionam viram aprendizado persistente. O plugin fica melhor no seu caso a cada sessão, por três "portas" de write-back.

---

## Instalação

```bash
# 1. adiciona o marketplace local
/plugin marketplace add /caminho/para/linkedin-authority-engine

# 2. instala o plugin
/plugin install linkedin-authority-engine

# 3. cria o perfil do cliente (onboarding)
/linkedin-authority-engine:init
```

Depois do `init`, use `/linkedin-authority-engine:linkedin` para ver o menu de modos.

---

## Comandos

| Comando | O que faz |
|---|---|
| `init` | Onboarding. Conduz a entrevista de discovery e cria `authority-context.md`, `memory/` e `outputs/posts/`. Aceita `--refresh` pra atualizar o perfil. |
| `linkedin` | Menu central. Mostra os modos e roteia pro escolhido. Bom ponto de partida. |
| `guiado` | Cria um post do zero num workflow de 7 etapas: categoria → objetivo → pauta → estrutura → tipo → hook → corpo → CTA. |
| `rewrite` | Otimiza um post existente em duas versões (conservadora e bold), com diagnóstico 360Brew, humanizer e score comparativo. |
| `thread` | Monta uma série de 3-7 posts sobre um tema, com arquitetura planejada (gancho, autoridade, educativo, story, conversão). |
| `score` | Avalia e humaniza um post pronto. Roda validação técnica, humanizer e nota nas 6 dimensões, com veredicto: publicar / ajustar / retrabalhar. |

---

## Como funciona por dentro

```
authority-context.md  ─┐
memory/                ─┤──►  lê perfil + padrões vencedores
                        │
                  ┌─────▼─────────────────────────────────┐
                  │  geração (guiado / rewrite / thread)   │
                  │  estrutura → hook → corpo → CTA        │
                  └─────┬─────────────────────────────────┘
                        │
                  humanizer-linkedin   (tira a cara de IA)
                        │
                  score_post.py        (6 dimensões 360Brew)
                        │
                  protocolo-pos-publicacao (90 min críticos)
                        │
                  write-back ──►  memory/  (auto-enriquecimento)
```

### Skills (12)

A inteligência do plugin mora nas skills — cada uma é uma referência que a Claude carrega quando precisa.

| Skill | Função |
|---|---|
| `algoritmo-360brew` | Referência completa do algoritmo: formato, timing, métricas e pontuação. |
| `authority-context` | Protocolo de leitura/escrita do substrato de memória do cliente. As 3 portas de auto-enriquecimento. |
| `hooks` | Banco de 147 hooks por tipo (prova, autoridade, transformação, contrarian, confissão…). |
| `estruturas-copywriting` | 8 frameworks (AIDA, PAS, BAB, FAB, Star-Story-Solution, APP, HSO, Storytelling) e guia de escolha. |
| `tipos-conteudo` | Catálogo de 16 tipos de post por objetivo. |
| `templates-por-categoria` | Templates prontos pra 7 categorias, com placeholders e exemplos. |
| `ctas` | Banco de CTAs por objetivo (saves, leads, engajamento, vendas…). |
| `estilo-tom` | Guia de formatação 360Brew, autenticidade e checklist de voz. |
| `humanizer-linkedin` | Pipeline que remove padrões de escrita de IA — cirurgia, não demolição. |
| `protocolo-pos-publicacao` | Os 90 minutos críticos depois de publicar: sinais, ações e erros que matam alcance. |
| `brief-visual` | Brief visual do post com specs técnicas e prompts prontos pra geração de imagem. |
| `discovery-script` | Roteiro de entrevista do `init` (uso interno). |

### Agents (2)

- **`linkedin-strategist`** — estratégia de conteúdo e decisões de pauta.
- **`humanizer-linkedin`** — passe final que tira a assinatura de IA do texto.

### Scripts (3)

Ferramentas Python que os comandos chamam:

```bash
python scripts/score_post.py <post.txt> [--objetivo authority|sales|engagement]
python scripts/suggest_hooks.py --categoria <cat> --objetivo <obj> [--tema "..."]
python scripts/validate_specs.py <post.txt>
```

### Hook

Um `SessionStart` mostra um banner apontando pro `init` quando ainda não existe perfil no projeto.

---

## Estrutura do repositório

```
authority-engine/
├── linkedin-authority-engine/   # o plugin (produto)
│   ├── .claude-plugin/          # plugin.json + marketplace.json
│   ├── commands/                # 6 comandos
│   ├── skills/                  # 12 skills
│   ├── agents/                  # 2 agents
│   ├── scripts/                 # 3 scripts Python
│   └── hooks/                   # hook de SessionStart
│
├── gtm-context.md               # contexto go-to-market (ICP, oferta, voz, canais)
├── outputs/                     # entregáveis de estratégia comercial
│   ├── pricing/                 # pricing review (5 leis Hormozi)
│   └── audit/                   # audit de oferta (Value Equation)
│
├── tests/                       # suíte pytest (estrutura do plugin + scripts)
└── docs/                        # documentação de apoio
```

### A camada GTM

Além do plugin, o repo guarda o trabalho de go-to-market do produto, gerado com o plugin Hormozi GTM:

- **`gtm-context.md`** — ICP, oferta, brand voice, canais e estágio. Fonte única de contexto comercial.
- **`outputs/pricing/`** — análise de preço pelas 5 leis do Pricing Playbook.
- **`outputs/audit/`** — diagnóstico da oferta pela Value Equation.

---

## Testes

```bash
# do diretório do plugin
pytest
```

A suíte cobre a integridade da estrutura do plugin (`test_plugin_structure.py`) e o comportamento dos scripts via CLI (`test_scripts_cli.py`).

---

## Roadmap

- [ ] Lançamento self-serve (Gold + continuity) — primeiro pro warm que já espera o produto
- [ ] Página de vendas + gateway de pagamento + integração com HubSpot Sales
- [ ] Operação multi-idioma (PT / EN / ES)
- [ ] Publicação no marketplace público de plugins

---

## Licença

Proprietary © LEVEL TECH. Contato: caner@thelevel.com.br
