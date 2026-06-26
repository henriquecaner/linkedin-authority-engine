# Design — Refatorar as skills Taplio para melhorar o linkedin-authority-engine

**Status:** approved (2026-06-25) · **Target version:** 1.3.0

## Context

Recebemos um repositório externo de 17 skills LinkedIn da Taplio e o pedido de estudá-las e refatorá-las como melhoria do plugin proprietário `linkedin-authority-engine/`.

As skills Taplio trazem padrões fortes de autoria — `When to trigger` com frases literais, `Inputs to ask for (only if missing)`, `Output format` em template fechado, regras opinativas, hand-off entre skills. Mas todas são acopladas ao **Taplio MCP**: gate que bloqueia execução sem o MCP, links de signup com UTM, seção "Power up with Taplio". Nada disso pode entrar num plugin proprietário (LEVEL TECH) que usa o substrato local `authority-context.md` + `memory/`. A licença Taplio permite fork/adapt sem atribuição, então o port é limpo — desde que **todo acoplamento Taplio seja removido**.

**Reframe-chave.** As "skills" Taplio são workflows (inputs + processo + output), não bases de conhecimento. O usuário optou por empacotar as capacidades novas como **skills auto-invocáveis** (decisão "só skills", à prova de futuro vs. a direção Cowork commands→skills), o que casa com o formato-fonte.

**Gap coberto:** camada de estratégia que alimenta o perfil (moat), produção (repurpose/história/CTA/carrossel), perfil + analytics. Plugin sai de 12 → 22 skills.

**Fora de escopo:** as 4 skills de pesquisa com dados ao vivo (viral-post-analyzer, trending-topics-scanner, niche-creator-finder, swipe-file-builder) dependem de `search_inspiration`; sem dados ao vivo degradam para chute. Skills já cobertas (hook-generator, post-writer=/guided, post-performance-critic=/score) não são portadas.

## Retrofit Contract (aplicado a cada skill portada)

1. Frontmatter: `name` slug puro, `description` afiada com gatilho, EN.
2. Gate Taplio MCP → **Gate 1** (sem `authority-context.md` → `/init`, parar) + **Gate 2** (skill `authority-context` lê perfil + `memory/`, opera no `language`).
3. Tradução de tools: `get_me`→ler perfil; `search_inspiration`→"o que o usuário cola / padrões em `memory/`" (sem inventar métricas); `create_draft`→salvar em `outputs/`.
4. Pipeline de finalização (humanizer→validate→score→post-publication) só para skills de POST. Outras pulam.
5. Gate 3 write-back por tipo (3-M append-only / 3-S section write-back).
6. Deletar promo Taplio, UTM, blocos de MCP.
7. Hand-offs reescritos para `linkedin-authority-engine:<x>`.
8. Manter os ossos bons: When to trigger / Inputs / Process / Output format / Rules.

### Gate 3-S (write-back de seção do perfil) — risco principal

Skills de estratégia mutam IN-PLACE seções do `authority-context.md` (§2/§4/§11). Protocolo: **propor → mostrar diff → confirmar → substituir só a seção-alvo preservando o resto → bump `version` + nota datada em `learnings.md`**. Espelha o `--refresh` do `init.md` e o propose-then-confirm da Taplio. Lógica centralizada na skill `authority-context` (uma fonte só), reusada pelas 3 skills de estratégia.

## Mapa das 10 skills novas

| Skill | Fonte | Write-back / output |
|---|---|---|
| niche-definer | niche-definer | Gate 3-S → §2/§4 |
| audience-persona | audience-persona-builder | Gate 3-S → §4 |
| content-pillars | content-pillars-builder | Gate 3-S → §2/§11 |
| content-calendar | content-calendar-planner | `outputs/strategy/`; hand-off /guided |
| repurposer | repurposer | `outputs/posts/` (pipeline) |
| story-extractor | story-extractor | `outputs/posts/` (pipeline) |
| cta-optimizer | cta-optimizer | inline; carrega skill `ctas` |
| carousel-builder | carousel-builder | `outputs/posts/`; hand-off visual-brief |
| profile-optimizer | profile-optimizer | `outputs/strategy/` (perfil colado) |
| analytics-interpreter | analytics-interpreter | Gate 3-M → `memory/`; `outputs/strategy/` |

Cadeia de hand-off: niche-definer → audience-persona → content-pillars → content-calendar → /guided.

## Waves

- **0** — estender `authority-context` com Gate 3-S + registrar `outputs/strategy/`.
- **1** — piloto `niche-definer` + verificar write-back end-to-end.
- **2** — audience-persona, content-pillars, content-calendar.
- **3** — repurposer, story-extractor, cta-optimizer, carousel-builder.
- **4** — profile-optimizer, analytics-interpreter.
- **5** — quality pass cirúrgico nas 11 skills (description + When to trigger + hand-offs; sem reescrever conteúdo que funciona).
- **6** — integração: menu `linkedin.md` com frases-gatilho, README, CLAUDE.md (contagem + `outputs/strategy/`), bump 1.3.0 (plugin.json + marketplace.json).

## Verification

- Skills de POST: amostra passa por `validate_specs.py` + `score_post.py`.
- Skills de estratégia: write-back contra `authority-context.md` de amostra — só a seção-alvo muda, version bump, learnings note, diff mostrado.
- Regressão: `pytest` verde.
- Higiene: `grep -ri "taplio\|search_inspiration\|get_me\|create_draft\|utm_source"` nas skills novas volta vazio.
