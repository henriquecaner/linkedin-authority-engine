# Schemas for `memory/` — self-enriching substrate

Files created in the client folder. Append-only. Read during generation (Gate 2), written at the end of the session (Gate 3).

## winning-hooks.md
| date | hook pattern | type | category | objective | score | times used | avg performance | keep/kill |
|---|---|---|---|---|---|---|---|---|

**v1 fills:** date, hook pattern, type, category, objective, score. The `times used`, `avg performance` and `keep/kill` columns stay empty until v1.x (manual perf via `/linkedin perf` or Unabyss).

## topic-performance.md
| date | topic | pillar | post type | score | avg reactions | avg comments | avg saves | vs baseline | verdict |
|---|---|---|---|---|---|---|---|---|---|

**v1 fills:** date, topic, pillar, post type, score. The `avg reactions`, `avg comments`, `avg saves`, `vs baseline` and `verdict` columns stay empty until v1.x.

## voice-profile.md
Dated bullets: `**YYYY-MM-DD:** voice adjustment → result → keep? (yes/no)`

**v1: READ-ONLY.** This file is read during generation (Gate 2) to calibrate the voice. Writing voice adjustments arrives in v1.x. The absence of write-back in v1 is intentional, not a bug.

## learnings.md
Dated free-form entries: `**YYYY-MM-DD:** learning`

v1 records free-form entries every session (what worked, adjustments, rejections).

> Reference schema: this file is the schema of record for the Gate 3 contracts across the 4 plugin commands. Any divergence between this file and the commands must be resolved here.
