# Design — Update geral do plugin: taxonomia de funil + recuperação de voz

> Data: 2026-06-21 · Status: aprovado para plano · Plugin: `linkedin-authority-engine`

## Fontes

1. **Vídeo Will McTighe — "Every Type of LinkedIn Post"** (`/Users/henriquecaner/Downloads/YTDown-YouTube-Every-T.txt`). Framework de 10 tipos de post organizados por job no funil (awareness → trust → conversion).
2. **The Voice Recovery Edit — LinkedIn Post Checklist** (`/Users/henriquecaner/Downloads/linkedin-voice-check-checklist vFF.md`). Banned words, banned hooks, out-loud test, specificity check.

## Tese

"Pare de tratar cada post como se fizesse o mesmo trabalho." Posts diferentes têm jobs diferentes no funil, e o trade-off alcance × conversão é real: posts de topo (newsjacking, spectacle) ganham alcance; posts de fundo (objection, demo, lead-magnet, case-study) têm baixo alcance mas alta conversão (transcrição, linha 54: "estudos de caso recebem 10-20K views quando recebo 0,5-1M/semana, mas convertem extremamente bem").

## Escopo

Update em duas fases sequenciadas, um único design doc, implementação faseada.

- **Fase 1 — Estratégia:** refinar e expandir o catálogo `content-types`.
- **Fase 2 — Voz:** incorporar o voice checklist no `humanizer-linkedin` (qualitativo) e no scorer (programático).

**Fora de escopo desta rodada:**
- Command/skill standalone de newsjacking (entra como tipo de destaque no catálogo, não como command).
- Modo "feedback-only" de IA (o Step 4 do checklist é resolvido via princípio "surgery, not demolition", já existente).
- Bump de versão e commit das mudanças (o usuário fará depois; o scorer já está em v3.5).

---

## FASE 1 — Estratégia (taxonomia)

### Decisões travadas

- O `content-types/SKILL.md` permanece **agrupado por objetivo** (educate / inspire / engage / convert / authority), refinado tipo a tipo.
- Catálogo passa de 16 para **22 tipos** (16 refinados + 6 novos).
- O **estágio de funil** entra como **coluna no selection guide** (não como reorganização total).
- **Badge por job** (não badge uniforme "recomendado"):
  - ⚡ **Alto alcance (awareness):** Newsjacking, Spectacle
  - 💰 **Alta conversão (baixo alcance, alto ROI):** Objection, Demo, Lead-magnet, Case-study
- **Video** sai do `content-types` (é formato, não estrutura de texto) → nota em `visual-brief`.

### Mapeamento McTighe-10 → catálogo (cobertura auditável)

| # | McTighe (fase) | Destino no plugin | Badge |
|---|---|---|---|
| 1 | Newsjacking (Awareness) | **NOVO** | ⚡ |
| 2 | Relatable/Validation (Awareness) | **NOVO** (validation puro). O sub-tipo *perspective/contrarian* já é coberto por #11 Contrarian Opinion (refinado) | — |
| 3 | Educational (Awareness) | Já coberto: #10 How-to, #15 Framework, #4 Statistics, #16 Data-Driven (refinados) | — |
| 4 | Spectacle/Challenge (Awareness) | **NOVO** | ⚡ |
| 5 | Story → Lesson → Application (Trust) | Refina #9 Tell a Story | — |
| 6 | Video (Trust) | **Fora de content-types** → nota em `visual-brief`. Behind-the-scenes já é #8 | — |
| 7 | Transformation / Case-study 6-step (Conversion) | Refina #6 Before-After | 💰 |
| 8 | Objection-handling (Conversion) | **NOVO** | 💰 |
| 9 | Product-demo (Conversion) | **NOVO** | 💰 |
| 10 | Lead-magnet (Conversion) | **NOVO** | 💰 |

### Os 6 novos tipos (estrutura a documentar)

1. **Newsjacking** ⚡ — pega um evento que já tem atenção e conecta ao ângulo do autor. Estrutura: gancho na notícia → recorte pro nicho → problema específico da audiência → take. Nota de **velocidade** (janela curta; erro comum = só resumir e adicionar opinião no fim).
2. **Spectacle/Challenge** ⚡ — desafio de alto risco. 5 componentes: (1) stakes altas, (2) relevante à audiência, (3) publicar *antes* de saber o resultado, (4) valor a cada passo (documentar a jornada), (5) milestones.
3. **Objection-handling** 💰 — abre com a objeção (idealmente atribuída a alguém de peso) → resposta em ida-e-volta → reframe. Insumo vem de objeções de calls de discovery.
4. **Product-demo** 💰 — produto/serviço resolvendo um problema real em ação (não lista de features). Foco em casos de uso; peso extra se quem mostra é o fundador/CEO.
5. **Lead-magnet** 💰 — entrega algo valioso → pede comentário → move pro e-mail. Erro comum = ofertar algo de baixo valor.
6. **Relatable/Validation** — nomeia uma frustração/realidade que a audiência sente mas não articula. Distinto de Contrarian (validação vs desafio).

### 2 frameworks que refinam tipos existentes

- **Story → Lesson → Application** refina #9 *Tell a Story*: toda história fecha com a lição e (quando cabe) a aplicação prática.
- **Case-study 6-step** refina #6 *Before-After*: hook com transformação → prova visual (screenshot/mensagem) → problema relacionável → resultado específico e tangível → seu papel como **guia** (cliente é o herói) → CTA claro com urgência.

### Selection guide

Ganha coluna **Estágio (funil)** mapeando objetivo → tipos → estágio. Abertura curta com a tese "cada post faz um job" e a leitura do trade-off alcance × conversão.

---

## FASE 2 — Voz (humanizer + scorer)

### `humanizer-linkedin/SKILL.md` (camada qualitativa)

Ganha uma seção LinkedIn-específica que **não duplica** os 24 padrões do `humanizer` global:

- **17 banned hooks** com reescrita (lista completa, incluindo templates variáveis).
- **15 banned words** → say-instead (Surfaced→Found, Leveraged→Used, Utilized→Used, etc., conforme checklist).
- **Out-loud test** — leia cada frase em voz alta; reescreva o que não soa como conversa.
- **Specificity check** — vago = AI; toda história com ≥2 de {nome, número, data, lugar}.
- Nota sobre o "Step 4": o plugin gera/reescreve, então a regra "use AI só pra feedback" é honrada via o princípio existente **"surgery, not demolition"**.

### `postlib.py` + `score_post.py` (camada programática)

Split recomendado para não inflar false-positives (postlib é "anchored to avoid false positives"):

- Novo bucket **`_AI_CLICHE_HOOKS`** (EN + PT), **separado** de `_PUNISHED` (que continua sendo engagement-bait). Só **frases concretas** regex-áveis entram:

| Concreto (→ scorer EN+PT) | Template variável (→ só humanizer) |
|---|---|
| "Read that again" / "Leia isso de novo" | "Stop doing X. Do Y." |
| "Let that sink in" / "Deixa isso assentar" | "Unpopular opinion: …" |
| "What if I told you" / "E se eu te dissesse" | "Most people think X. They're wrong." |
| "Here's the truth about" / "A verdade sobre" | "I used to believe X. Then everything changed." |
| "Nobody tells you" / "Ninguém te conta" | "Not only that, but…" |
| "Unlock the power of" / "Destrave o poder de" | "Not because X. Because Y." |
| "Game-changer" / "divisor de águas" | "And here's the thing most people miss…" |
| "Here's the shift" / "Aqui está a virada" | |
| "The real question is" / "A verdadeira pergunta é" | |
| "Here's the kicker" (EN; sem PT limpo) | |

- Nova função `find_ai_cliches(text, lang)` (escaneia as primeiras linhas, como `find_punished`), com matching union PT+EN e dedupe por label canônico — mesmo padrão das demais.
- `score_hook` ganha penalidade quando detecta clichê de AI (sugestão: −1.5). Penaliza a dimensão **Hook** (clichê de hook), distinta da penalidade de bait que já existe.
- **Sem mudança nos WEIGHTS** nem nos SPECS numéricos.

### Sync (evitar drift)

A nova penalidade é documentada na seção **Metrics** do `360brew-algorithm/SKILL.md` (breakdown da dimensão Hook, banda 0-3 "punido pelo algoritmo" ganha os clichês de AI como exemplo). Mantém alinhados os três pontos: postlib / score_post / SKILL.md.

---

## Arquivos tocados

| Arquivo | Mudança |
|---|---|
| `skills/content-types/SKILL.md` | Reescrita: 22 tipos, badges por job, coluna de funil, tese de abertura |
| `skills/visual-brief/SKILL.md` | Nota: Video como formato de trust |
| `skills/humanizer-linkedin/SKILL.md` | +banned hooks (17), +banned words (15), out-loud, specificity |
| `scripts/postlib.py` | +`_AI_CLICHE_HOOKS` (EN+PT) + `find_ai_cliches()` |
| `scripts/score_post.py` | `score_hook` penaliza clichê de AI |
| `skills/360brew-algorithm/SKILL.md` | 1 linha de sync na seção Metrics (dimensão Hook) |
| `tests/test_postlib.py` | Testes de `find_ai_cliches` (EN+PT, sem false-positive) |
| `README.md` + `linkedin-authority-engine/README.md` | Atualizar contagem "16 content types" → "22" |
| `CLAUDE.md` | Atualizar referência "16 content types" → "22" |

**Não toca:** WEIGHTS do scorer, SPECS numéricos do 360brew, gates / memory loop, versão do plugin (commit/bump fica pra depois).

## Testes

- `tests/test_postlib.py`: `find_ai_cliches` detecta clichês EN e PT nas primeiras linhas; não dispara em texto limpo; dedup por label.
- Opcional: caso CLI em `tests/test_scripts_cli.py` — post com clichê de hook recebe Hook penalizado.
- Suite completa (`pytest`) deve permanecer verde (hoje: 42 passa).

## Riscos e mitigações

- **False-positive no scorer** → mitigado pelo split (só frases concretas viram regex; templates ficam no humanizer).
- **Equivalentes PT awkward** → "Here's the kicker" fica só EN; demais têm equivalente idiomático.
- **Achatar a tese com badge uniforme** → resolvido com badge por job (⚡ vs 💰).
- **Drift entre postlib/score/SKILL.md** → linha de sync explícita na seção Metrics.

## Sequenciamento

1. **Fase 1** (taxonomia) — independente do scorer; entrega valor sozinha.
2. **Fase 2** (voz) — humanizer-linkedin → postlib/score → testes → sync no SKILL.md.

Cada fase pode virar seu próprio plano de implementação.
