# Design — Plugin `linkedin-authority-engine`

> **Data:** 2026-06-17 · **Autor:** Henrique Caner (LEVEL TECH) + Claude
> **Status:** design aprovado em brainstorm; pronto para revisão antes do plano de implementação.
> **Escopo deste doc:** arquitetura completa do produto (6 módulos) + spec detalhado do **v1 (Fundação + Motor de Posts)**.

---

## 1. Contexto e objetivo

Hoje o produto existe como **uma skill empacotada** (`Skill-old/virall-linkedin-content.skill`): um `SKILL.md` (V4.0) + 16 references + 3 scripts Python, focada em criar posts de LinkedIn otimizados pro algoritmo 360Brew. Para funcionar bem, ela depende de um **projeto Claude montado à mão + instruções de projeto** (o perfil do cliente, hoje escrito a partir do template `Instrucoes_Projeto_Template_v2.md` após uma entrevista de discovery).

Esse é o produto que a LEVEL TECH vai vender: **LinkedIn Authority Engine** — vendido self-serve (Gold R$ 2.997 + continuity R$ 297/mês) pro founder B2B instalar e rodar no próprio LinkedIn, e também usado pela LEVEL em modo agência multi-cliente.

**Objetivo:** transformar a skill num **plugin** para **Claude Code e Claude Cowork**, mais profundo, denso, contextual e **auto-enriquecedor** — eliminando a montagem manual de "projeto + instruções".

### Definição operacional de "auto-enriquece" (decidido)
Três mecanismos, que juntos formam **um único substrato de memória**:
1. **Memória de cliente acumulativa** — perfil vivo por cliente que cresce a cada sessão.
2. **Base de conhecimento que evolui** — padrões vencedores capturados viram conhecimento reutilizável por cliente.
3. **Feedback loop de performance** — performance real dos posts ajusta hooks, temas e scoring.

(Web research ao vivo foi **descartado** para v1.)

---

## 2. Modelo de uso e distribuição (decidido)

- **Primário:** vendido self-serve. Cliente instala o plugin e roda na própria conta Claude (inferência na conta dele → custo ~R$ 0 pra LEVEL).
- **Secundário:** LEVEL usa multi-cliente (uma pasta/projeto por cliente).
- **Substrato de memória:** **híbrido local-first** (decisão C). Arquivos locais na pasta do cliente são a fonte de verdade e sempre funcionam sem setup. **Unabyss (MCP)** é enriquecimento **opcional** quando presente (LEVEL tem; cliente self-serve não precisa).

### Linha plugin vs serviço (explícita)
Estão **no plugin:** geração de conteúdo, onboarding, scoring, memória local.
**NÃO estão no plugin** (são o serviço/entrega humana): Slack connect, call de onboarding do Platinum, suporte assistido. O spec não promete que o plugin faça o que o serviço faz.

---

## 3. Decomposição do produto (6 módulos) e build order

| # | Módulo | Natureza | Build order |
|---|--------|----------|-------------|
| 1 | **Fundação** — esqueleto do plugin + substrato de memória (3 portas) + `/init` onboarding | núcleo | **v1** |
| 2 | **Motor de Posts** — 4 modos + pipeline + scripts + 360Brew (porta e aprofunda a skill atual) | núcleo | **v1** |
| 3 | **Feedback Loop de Performance** — registra post → performance → ajusta hooks/temas/scoring | substrato (porta write-back) | v1.x |
| 4 | **Motor de Lead Magnets** — 1-4/mês, 3 arquétipos | conteúdo | v2 |
| 5 | **Ingestão de Transcrição + agente HeyGen** — Caminho B do onboarding, discovery automatizado por avatar | onboarding/infra | futuro |
| 6 | **Cadência/Calendário** — operação 20-30 posts/mês | orquestração | v2 |

**Fora de escopo (brainstorm próprio, se um dia):** automação de comentários agindo no LinkedIn (ToS, sem API sancionada). Decidido: não trabalhar agora.

**v1 = Módulos 1 + 2.** Entregável: plugin instalável que o cliente usa de verdade (posts + onboarding + memória). É o MVP vendável da semana.

---

## 4. Arquitetura do plugin (v1)

Espelha o `hormozi-gtm` (molde provado já em uso pela LEVEL): `plugin.json` + `commands/` + `skills/` + `agents/` + `hooks/` + `scripts/` + `reference/`.

```
linkedin-authority-engine/
├── .claude-plugin/plugin.json
├── commands/
│   ├── linkedin.md              # menu router
│   ├── init.md                  # onboarding (Caminho A)
│   ├── guiado.md                # criar do zero (7 steps)
│   ├── rewrite.md               # otimizar post existente
│   ├── thread.md                # série de posts
│   └── score.md                 # avaliar post pronto
├── skills/
│   ├── algoritmo-360brew/       # core + formatos + métricas
│   ├── hooks/                   # 147 hooks
│   ├── estruturas-copywriting/  # PAS, AIDA, BAB, HSO…
│   ├── tipos-conteudo/          # 16 tipos
│   ├── templates-por-categoria/
│   ├── ctas/
│   ├── estilo-tom/
│   ├── protocolo-pos-publicacao/
│   ├── brief-visual/
│   ├── humanizer-linkedin/      # ou reuso do humanizer global
│   ├── discovery-script/        # perguntas da entrevista (Caminho A)
│   └── authority-context/       # meta-skill: protocolo de leitura/escrita do substrato
├── agents/
│   ├── linkedin-strategist.md   # persona que segura expertise 360Brew + contexto do cliente
│   └── humanizer.md             # (ou reuso do global)
├── hooks/hooks.json             # SessionStart: carrega contexto / sugere /linkedin init
├── scripts/
│   ├── validate_specs.py        # portado da .skill (pronto)
│   ├── score_post.py            # portado (pronto)
│   └── suggest_hooks.py         # portado (pronto)
└── reference/                   # docs auxiliares compartilhados
```

### `plugin.json` (rascunho)
```json
{
  "name": "linkedin-authority-engine",
  "displayName": "LinkedIn Authority Engine",
  "version": "1.0.0",
  "description": "Sistema que transforma a expertise do founder em autoridade no LinkedIn. Posts tunados pelo algoritmo 360Brew, com perfil de cliente vivo e auto-enriquecimento. Para Claude Code e Claude Cowork.",
  "author": { "name": "LEVEL TECH", "email": "caner@thelevel.com.br" },
  "homepage": "https://thelevr.com",
  "license": "proprietary",
  "keywords": ["linkedin", "authority", "content", "360brew", "b2b", "level"]
}
```

### Portabilidade Cowork vs Code (verificado)
Claude Cowork suporta plugins desde 30/jan/2026, empacotando **skills + slash commands + sub-agents + connectors** — os mesmos primitivos do Code. Logo `commands/`, `skills/` e `agents/` funcionam nos dois sem fork.
**Hooks** (`SessionStart`) são convenção do Claude Code. No Cowork, o carregamento automático de contexto é coberto pela meta-skill `authority-context` (que instrui ler `authority-context.md` no início). **Princípio de design:** a lógica essencial vive em skills (portáveis); hooks/commands são conveniência. Nada essencial depende exclusivamente de hook.

---

## 5. Substrato de memória — o coração do auto-enriquece

Um substrato, **três portas**. As três são **desenhadas agora** (mesmo que o write-back só seja implementado plenamente em v1.x) para não retrabalhar a fundação.

### Arquivos na pasta do cliente
```
<pasta-do-cliente>/
├── authority-context.md          # perfil vivo (schema na seção 7)
├── memory/
│   ├── winning-hooks.md          # hook → vezes usado → performance média → keep/kill
│   ├── topic-performance.md      # tema → nº posts → reações/comentários/saves vs baseline → veredito
│   ├── voice-profile.md          # ajustes de voz que colaram / rejeitados
│   └── learnings.md              # aprendizados livres por cliente
└── outputs/
    └── posts/                    # posts gerados + score, versionados (YYYYMMDD-vN)
```

### Porta 1 — Escrita (onboarding)
`/linkedin init` → conduz a entrevista (Caminho A) → escreve `authority-context.md`. Substitui a montagem manual de projeto + instruções.

### Porta 2 — Leitura (geração)
**Todo** modo (guiado/rewrite/thread/score) lê `authority-context.md` + `memory/` **antes** de gerar. Efeitos:
- Hooks usam credenciais/marcadores reais do perfil.
- Temas batem com os 3 pilares e respeitam os territórios SIM/NÃO.
- Voz casa com o espectro de tom e o nível de vulnerabilidade definidos.
- Padrões em `memory/winning-hooks.md` e `topic-performance.md` têm prioridade.
- Restrições (palavras proibidas, sensibilidades, confidencial) são aplicadas como guardrails.

É o que torna o plugin **muito mais contextual** que a skill estática (que cai em defaults genéricos quando não há projeto montado).

### Porta 3 — Write-back (enriquecimento)
Ao fim de cada sessão de geração, o plugin **anexa** ao `memory/`:
- hooks/temas usados e ângulo escolhido;
- o que o cliente aprovou vs rejeitou (sinal de voz/preferência);
- quando há performance (entrada manual via futuro `/linkedin perf`, ou Unabyss): qual post venceu vs baseline.

**Contrato de dados (definido agora, consumido pelo Feedback Loop em v1.x):**

`memory/topic-performance.md` — tabela append-only:
| tema | pilar | nº posts | reações méd | comentários méd | saves méd | vs baseline | veredito |

`memory/winning-hooks.md` — tabela append-only:
| padrão de hook | tipo | vezes usado | performance méd | keep/kill |

`memory/voice-profile.md` — bullets datados: ajuste de voz → resultado → manter?

`memory/learnings.md` — entradas livres datadas, formato `**AAAA-MM-DD:** aprendizado`.

**Unabyss (opcional):** presente → Porta 2 puxa performance real pro contexto e Porta 3 registra de volta no MCP. Ausente → tudo opera em arquivos locais; performance entra manual ou é pulada. Queries de referência: portar de `references/integracao-unabyss.md`.

---

## 6. Onboarding `/linkedin init`

### v1 — Caminho A (entrevista guiada in-session)
O plugin conduz as perguntas de discovery na própria sessão, uma de cada vez (ou em blocos curtos), e monta `authority-context.md` ao final. Para o cliente self-serve que não fez call de discovery.

Fluxo:
1. Detecta se já existe `authority-context.md` (se sim, oferece `--refresh`).
2. Roda o `discovery-script` (skill) — perguntas agrupadas pelas 13 seções do schema.
3. Sintetiza as respostas no schema (seção 7), marcando campos críticos (`*`).
4. Sinaliza lacunas em campos `*` e pede follow-up só do que faltou.
5. Escreve `authority-context.md` + inicializa `memory/` vazio + `outputs/posts/`.

**discovery-script:** reconstruído a partir do mapa de Q do `Instrucoes_Projeto_Template_v2.md` (Q1-Q18 + Q extras). Markdown versionado na skill. O `.key` original (Keynote, protobuf comprimido) não é extraível de forma limpa; o verbatim pode ser refinado depois editando a skill.

### Futuro — Caminho B (ingestão de transcrição + agente HeyGen Live Avatar)
Módulo 5. Cliente joga 1+ transcrições (ex.: Gemini meeting notes, possivelmente quebradas em N reuniões) na pasta → synthesizer mapeia transcrição → schema → perfil, com gap-flagging. A entrevista de discovery será conduzida por um **avatar interativo do Henrique via HeyGen Live Avatar** (discovery automatizado em tempo real), que gera a transcrição consumida pelo synthesizer. Fora do v1.

**Stack decidida para o Caminho B (backlog):** HeyGen **Live Avatar**.
- Produto: https://www.liveavatar.com
- Docs: https://docs.liveavatar.com
- Agent Skills (relevante — o avatar pode rodar as perguntas como skill): https://docs.liveavatar.com/docs/agent-skills
- Web SDK: https://github.com/heygen-com/liveavatar-web-sdk

Quando atacar o Módulo 5: o `discovery-script` (skill já criada no v1) vira a base das *agent skills* do avatar, garantindo paridade entre o Caminho A (in-session) e o Caminho B (avatar). O synthesizer transcrição→`authority-context.md` é compartilhado pelos dois caminhos.

---

## 7. Schema de `authority-context.md` (porta de `Instrucoes_Projeto_Template_v2.md`)

Schema canônico do perfil — 13 seções, port direto do template provado (única mudança: substituir "usar skill LinkedIn Content 3.1" por "este plugin"):

1. **Perfil do cliente** — nome, cargo, LinkedIn, tempo, experiência, região, bio, marcadores de credibilidade*, trajetória.
2. **Posicionamento e autoridade** — tema central*, 3 pilares*, proposta de valor*, mandamentos, diferenciais, histórias/cases, inéditos, crenças contrárias, "tema de palestra".
3. **Objetivos do conteúdo** — Authority/Sales/Engagement*, objetivos específicos, vitória em 90 dias*, métrica principal.
4. **Audiência-alvo (ICP)** — até 2 perfis: cargo/setor/porte/geo, dores*, transformação antes→depois*, valores, canal de origem, pergunta recorrente.
5. **Arquitetura de ofertas** — tabela de ofertas + oferta prioritária.
6. **Narrativa comercial** — discurso de venda, objeções* (cada uma vira pauta).
7. **Paisagem competitiva** — concorrentes, espaço de diferenciação, referências admiradas*.
8. **Territórios de conteúdo** — temas SIM, temas NÃO, fontes de informação*.
9. **Restrições e cuidados** — palavras proibidas*, confidencial, sensibilidades.
10. **Tom de voz e estilo** — 3 palavras, benchmark, espectro de tom, nível de vulnerabilidade*, contrarian.
11. **Instrução de conteúdo** — mix de conteúdo %*, temas prioritários, formato preferido, frequência, aprovação.
12. **Identidade visual** *(opcional)* — fontes, paleta, estilo.
13. **Notas adicionais** — psicográfico, ponto de partida digital, desafio motivador, palavras-chave da marca*, outras.

Campos `*` são críticos: o `init` não fecha sem eles (pede follow-up).

---

## 8. Motor de Posts (porta + aprofunda a skill V4.0)

### Commands (4 modos da skill atual viram comandos)
- `/linkedin` — menu router (PRIORIDADE MÁXIMA, igual à skill).
- `/linkedin guiado [tema]` — workflow 7 steps (categoria → objetivo → pauta → estrutura → tipo → hooks → corpo → CTA).
- `/linkedin rewrite [post]` — diagnóstico → foco → 2 versões (conservadora/bold) → pipeline → comparativo.
- `/linkedin thread [tema]` — série 3-7 posts com arquitetura + calendário.
- `/linkedin score [post]` — avaliação imediata (validação → humanizer → score → veredito).

### Pipeline de finalização (compartilhado, igual à skill)
A (validação `validate_specs.py`) → B (Humanizer) → C (Brief Visual) → D (Score `score_post.py`) → E (1º comentário + protocolo pós-publicação). **Mudança v1:** todo step lê o substrato (Porta 2) e o step E grava write-back (Porta 3).

### Skills (estoura o monólito)
As 16 references → skills granulares carregadas sob demanda (melhor triggering, menos inchaço de contexto). Conteúdo portado 1:1 da `.skill`, reorganizado.

### Agents (leve — 2)
- `linkedin-strategist` — persona com expertise 360Brew + leitura do contexto do cliente; orquestra geração pesada.
- `humanizer` — reuso do global ou skill dedicada `humanizer-linkedin`.

### Scripts (portados, já prontos)
`validate_specs.py`, `score_post.py`, `suggest_hooks.py` — copiar da `.skill`, sem reescrita.

### 360Brew (conhecimento, portado)
Fórmula do outlier, specs de texto, multiplicadores de alcance, pesos de engajamento, scoring 6 dimensões, regras de hashtag/link. Tudo da skill atual.

---

## 9. Hook `SessionStart` (Claude Code)
Detecta `authority-context.md` no cwd:
- **Presente:** carrega resumo (nome, tema central, pilares, objetivo, mix) no contexto + avisa se `last_updated` > 30 dias ("contexto stale → `/linkedin init --refresh`").
- **Ausente:** sugere `/linkedin init`.

No Cowork, o mesmo efeito vem da meta-skill `authority-context`.

---

## 10. O que "deeper / denser / contextual / auto-enriquece" significa concretamente
- **Skill estática → plugin contextual:** todo output é função do perfil vivo + padrões vencedores acumulados, não de defaults genéricos.
- **Monólito → granular:** um `SKILL.md` gigante vira commands + skills focadas; o modelo carrega só o que precisa.
- **One-shot → sessão com memória:** lê contexto antes, escreve aprendizado depois.
- **Setup manual → self-bootstrap:** `/linkedin init` substitui "projeto Claude + instruções".

---

## 11. Premissas e questões em aberto
- **Premissa (verificada):** Cowork suporta plugins com skills/commands/agents. Hooks são Code-only — coberto por skill no Cowork.
- **Premissa:** scripts Python da `.skill` rodam como estão (validar no plano de implementação).
- **Aberto (v1.x):** `/linkedin perf` — comando de entrada manual de performance que alimenta a Porta 3. Contrato de dados já definido; comando entra com o Feedback Loop.
- **Aberto (futuro):** discovery-script verbatim do Keynote (refinável editando a skill).
- **Fora de escopo:** automação de comentários agindo no LinkedIn; lead magnets; cadência/calendário (v2+).

---

## 12. Próximo passo
Plano de implementação (skill `writing-plans`) cobrindo **v1 = Módulos 1 + 2**, na ordem: (a) esqueleto do plugin + `plugin.json`; (b) substrato de memória + schema `authority-context.md`; (c) `/linkedin init` Caminho A + discovery-script; (d) port do Motor de Posts (skills + commands + scripts + agents); (e) hook SessionStart; (f) teste de instalação em Code e Cowork.
