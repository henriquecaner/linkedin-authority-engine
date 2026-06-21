---
name: authority-context
description: Read and write protocol for the client memory substrate (authority-context.md + memory/). ALWAYS use it before generating content (read the profile + winning patterns) and at the end of every generation session (write-back). Defines the 3 gates of auto-enrichment.
---

# Authority context — self-enriching substrate

The client folder is the source of truth (local-first). Unabyss (MCP) is optional enrichment when present (optional — enrichment via Unabyss MCP when present; not required in v1).

## Files
- `authority-context.md` — living profile (13 sections) with a frontmatter that includes `last_updated`, `version`, and `language` (`pt` = Brazilian Portuguese / pt-BR, or `en`). Template in `references/authority-context-template.md`.
- `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` — schemas in `references/memory-schemas.md`.
- `outputs/posts/` — versioned generated posts (`YYYYMMDD-vN`).

## Gate 1 — Write (onboarding)
`init` writes `authority-context.md`. See the `init` command.

## Gate 2 — Read (generation)
Before generating any post: read `authority-context.md` (core theme, 3 pillars, ICP, voice, constraints, YES/NO territories) and `memory/` (prioritize hooks/topics with a positive verdict). If Unabyss is present, pull real performance (optional — enrichment via Unabyss MCP when present; not required in v1). Also read the `language` frontmatter field and operate in it: `pt` → generate and interact in **Brazilian Portuguese (pt-BR)** ("você", Brazilian vocabulary/spelling, never European Portuguese); `en` → English; and pass it as `--lang <pt|en>` to `validate_specs.py` and `score_post.py`. If the field is absent, omit `--lang` and infer the language from the conversation.

## Gate 3 — Write-back (end of session)
Append (never overwrite): `winning-hooks.md` (approved hooks + category/objective/score), `topic-performance.md` (topic/pillar/type/score) and `learnings.md` (what worked, voice adjustments, rejections). `voice-profile.md` is READ-ONLY in v1 (read in Gate 2, writing arrives in v1.x). Columns and schemas in `references/memory-schemas.md`.

## Guardrails
Apply the constraints from section 9 of the profile (forbidden words, confidential information, sensitivities) and respect the NO territories from section 8.
