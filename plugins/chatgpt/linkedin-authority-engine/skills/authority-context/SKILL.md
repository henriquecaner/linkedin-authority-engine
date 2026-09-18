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
- `outputs/strategy/` — non-post strategy artifacts (content calendars, profile audits, analytics reports) named `<YYYYMMDD>-<artifact>.md`. Created on demand by the strategy/profile/analytics skills.

## Gate 1 — Write (onboarding)
`init` writes `authority-context.md`. See the `init` skill. Path U additionally seeds `memory/voice-profile.md` from the measured post corpus (seeding contract in `references/memory-schemas.md`); seeding does not open Gate 3 write-back.

## Gate 2 — Read (generation)
Before generating any post: read `authority-context.md` (core theme, 3 pillars, ICP, voice, constraints, YES/NO territories) and `memory/` (prioritize hooks/topics with a positive verdict). If Unabyss is present, pull real performance (optional — enrichment via Unabyss MCP when present; not required in v1). Also read the `language` frontmatter field and operate in it: `pt` → generate and interact in **Brazilian Portuguese (pt-BR)** ("você", Brazilian vocabulary/spelling, never European Portuguese); `en` → English; and pass it as `--lang <pt|en>` to `validate_specs.py` and `score_post.py`. If the field is absent, omit `--lang` and infer the language from the conversation.

## Gate 3 — Write-back (end of session)

Write-back has two modes. Pick by what the skill produced.

### Gate 3-M — Memory append (default)
Append (never overwrite): `winning-hooks.md` (approved hooks + category/objective/score), `topic-performance.md` (topic/pillar/type/score) and `learnings.md` (what worked, voice adjustments, rejections). `voice-profile.md` is READ-ONLY in v1 (read in Gate 2, writing arrives in v1.x) — Gate 1 onboarding seeding is the only exception, and it does not open Gate 3 write-back. Columns and schemas in `references/memory-schemas.md`. Used by every generation/scoring skill and by `analytics-interpreter`.

### Gate 3-S — Profile section write-back (strategy skills only)
Used by `niche-definer`, `audience-persona`, and `content-pillars` when their output durably refines the client profile. Unlike Gate 3-M, this **mutates structured sections of `authority-context.md` in place** (e.g. §2 Positioning, §4 Audience, §11 Content instruction). That is destructive, so it is never silent. Follow this exact sequence — it mirrors how `init --refresh` updates stale fields "while preserving the rest":

1. **Propose.** Draft the new content for the target section only.
2. **Diff.** Show the user the old section vs. the proposed section, side by side. Touch nothing else.
3. **Confirm.** Wait for an explicit yes. If the user edits the proposal, write the edited version. If no, stop — do not write.
4. **Replace in place — at field granularity.** Rewrite only the target fields. Every other section, **and every sibling field inside the same section**, plus the frontmatter `language`, stay byte-for-byte untouched. Replacing a whole `# N.` block would clobber a sibling skill's fields, so target the specific fields, not the section wholesale. **Field ownership across the strategy skills:**
   - **§2 Positioning** — `niche-definer` owns the *core authority theme* + *value proposition*; `content-pillars` owns the *3 content pillars*. Each leaves the other's fields untouched.
   - **§4 Audience (ICP)** — `audience-persona` owns it (the `## Profile 1` persona body), and preserves any `## Profile 2` the user set up. `niche-definer` does **not** write §4; it hands the audience off to `audience-persona`.
   - **§11 Content instruction** — `content-pillars` may write the *Priority themes* list only; it must leave the `Content mix` table (a `*` critical field owned by `init`/objective calibration) byte-for-byte.
   (Verified by dry-run: a §2 core-theme rewrite left the 3 pillars and a §4 `## Profile 2` subsection byte-identical.)
5. **Bump + log.** Increment `version` in the frontmatter (e.g. `1.0 → 1.1`), set `last_updated` to today, and append a dated note to `memory/learnings.md`: `**<YYYY-MM-DD>:** updated authority-context §N (<section>) via <skill> — <one-line reason>`.

Guardrails: never overwrite a `*` critical field with a vaguer version; if a proposal would empty a field the user filled, flag it instead of writing. **Never write a region that was not shown in the confirmed diff** — a single confirmation may cover more than one field or section (e.g. `content-pillars` touching §2 and §11) only when every touched region appears in that diff. No silent or unshown writes, ever.

## Guardrails
Apply the constraints from section 9 of the profile (forbidden words, confidential information, sensitivities) and respect the NO territories from section 8.
