# Schemas for `memory/` — self-enriching substrate

Files created in the client folder. Append-only. Read during generation (Gate 2), written at the end of the session (Gate 3).

## winning-hooks.md
| date | hook pattern | type | category | objective | score | times used | avg performance | keep/kill |
|---|---|---|---|---|---|---|---|---|

**v1 fills:** date, hook pattern, type, category, objective, score. The `times used`, `avg performance` and `keep/kill` columns stay empty until v1.x (filled by manual performance entry, or via Unabyss when present).

## topic-performance.md
| date | topic | pillar | post type | score | avg reactions | avg comments | avg saves | vs baseline | verdict |
|---|---|---|---|---|---|---|---|---|---|

**v1 fills:** date, topic, pillar, post type, score. The `avg reactions`, `avg comments`, `avg saves`, `vs baseline` and `verdict` columns stay empty until v1.x.

## voice-profile.md
Dated bullets: `**YYYY-MM-DD:** voice adjustment → result → keep? (yes/no)`

**Gate 1 (seeding, allowed):** the `init` skill Path U writes dated bullets measured from the real post corpus, in the existing bullet shape with `result` = the measured value and `keep?` = `yes` for an observed baseline. One bullet per metric that has a voice consequence: mean chars, mean paragraph length, mean chars per paragraph, `avg_word_length`, emoji rate, hashtag mean, question rate, first-person rate, plus one bullet per punished or AI-cliché hook found live. The seeding block carries the header `<!-- seeded from Unipile deep discovery, YYYY-MM-DD, N posts -->` so a reader can tell measurement from a later human adjustment.

**Gate 3-M (write-back, still forbidden in v1):** no session appends this file; that arrives in v1.x. Gate 1 seeding does not open Gate 3 write-back. The file is read during generation (Gate 2) to calibrate the voice.

## learnings.md
Dated free-form entries: `**YYYY-MM-DD:** learning`

v1 records free-form entries every session (what worked, adjustments, rejections).

> Reference schema: this file is the schema of record for the Gate 3 contracts across the plugin skills. Any divergence between this file and the skills must be resolved here.
