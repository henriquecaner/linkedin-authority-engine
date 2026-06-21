# Design — Persistent language choice in `/init`

> Data: 2026-06-21 · Status: aprovado para plano · Plugin: `linkedin-authority-engine`

## Problem

The plugin has no explicit language setting. Output language is implicit — Claude infers it from the conversation — and the commands call `score_post.py` / `validate_specs.py` with the default `--lang auto` (union PT+EN). A user who wants the engine to operate in Brazilian Portuguese "forever" has no way to lock that in.

## Goal

Make the **first question** of `/init` a language choice. The choice persists in `authority-context.md` (the substrate every Gate 2 already reads), so all flows — generation, interaction, and scoring — operate in that language from then on, without re-asking.

## Decisions (locked)

- **Languages offered:** **Brazilian Portuguese (pt-BR)** and English only — aligned with the scorer's real matchers (`--lang pt|en`). No third language (would degrade scoring; out of scope).
- **The Portuguese register is always Brazilian (pt-BR), never European Portuguese.** Generation and interaction use Brazilian register: "você" (not "tu"), Brazilian vocabulary, spelling, and idiom. Every in-language instruction in the touched files says **"Brazilian Portuguese (pt-BR)"** explicitly — not bare "Portuguese" — so the model never drifts to pt-PT.
- **Stored value = scorer token, not display label.** The frontmatter stores `language: pt` or `language: en` (verbatim scorer vocabulary; the scorer has no pt-BR/pt-PT distinction). Within this plugin, `language: pt` **always means Brazilian Portuguese** — it is the only Portuguese variant offered. The string "Português (Brasil)" appears only in the `/init` prompt. No `pt-BR → pt` mapping anywhere.
- **Generated profile:** section labels in **English** (stable structure the gates read), client data in the chosen language. The plugin's own skill/command files stay English (internal instructions); only *output* is in-language.
- **`/init --refresh` may change the language** of an existing profile (just rewrites the field).
- **No translation of skill files. No unit tests for playbook behavior.** (YAGNI.)

## Architecture

### Persistence

Single source of truth: a `language` key in the `authority-context.md` frontmatter. Written only by `init.md` step 5 (the sole frontmatter write site — confirmed: the template has no YAML head; `last_updated`/`version` are added at generation time). Value is `pt` or `en`.

### `/init` flow change

A new **step 0** runs before the discovery script is loaded:

```
Before we start — which language should this engine work in?
  1) Português (Brasil)    2) English
```

The answer (a) sets the language for the **entire interview** (Claude conducts discovery in that language), and (b) is recorded as `language: <pt|en>` in the frontmatter at step 5. The `discovery-script` skill gains a one-line note: conduct the interview in the language chosen in step 0.

### Propagation to flows (Gate 2)

Each flow reads `language` from the profile and operates in it. Touch-list:

| File | Generate in-language | Interact in-language | Pass `--lang` to |
|---|---|---|---|
| `commands/guided.md` | yes | yes | `score_post.py` + `validate_specs.py` |
| `commands/rewrite.md` | yes | yes | `score_post.py` + `validate_specs.py` |
| `commands/thread.md` | yes | yes | `score_post.py` + `validate_specs.py` |
| `commands/score.md` | — | yes | `score_post.py` + `validate_specs.py` |
| `commands/linkedin.md` | — | menu/profile-check in-language when a profile exists | — |

Both scripts accept `--lang`; both calls get it, not just the scorer. The value passed is the profile's `language` token verbatim (`pt` or `en`).

`linkedin.md` renders its menu/profile-check in the profile's language **only when a profile exists**. When no profile exists yet (the "run `/init`" message), the language is unknown, so it stays in English — the language question hasn't been asked yet.

### Fallback (backward-compatibility) — non-negotiable

A profile with **no** `language` field (every consumer who ran `/init` before this change) → today's behavior: omit `--lang` (scorer defaults to `auto`, Claude infers the language). No pre-existing consumer breaks. There is no sample `authority-context.md` in this repo, so nothing in-repo needs the field.

### Supporting files

- `skills/authority-context/references/authority-context-template.md` — document the `language` frontmatter field (labels stay EN; note that data is filled in the chosen language).
- `skills/authority-context/SKILL.md` — note the EN-labels/in-language-data rule and the `language` field.
- `commands/init.md` — step 0 (language question) + write `language` at step 5 + `--refresh` may rewrite it.
- `skills/discovery-script/SKILL.md` — conduct the interview in the step-0 language.

## Touched files

`commands/init.md`, `commands/guided.md`, `commands/rewrite.md`, `commands/thread.md`, `commands/score.md`, `commands/linkedin.md`, `skills/discovery-script/SKILL.md`, `skills/authority-context/SKILL.md`, `skills/authority-context/references/authority-context-template.md`.

**Not touched:** scorer/validator Python (already accept `--lang`); WEIGHTS/SPECS; plugin version; the 11 other skills.

## Testing

The surface is markdown playbooks. Gate: `pytest tests/test_plugin_structure.py` stays green (frontmatter + body checks on the touched skills/commands), plus a manual walkthrough: `/init` choosing Português → confirm `language: pt` written → `/guided` generates in PT and the scorer is invoked with `--lang pt`. No new unit tests for playbook behavior.

## Risks & mitigations

- **Token drift (`pt-BR` vs `pt`)** → store the scorer token directly; display label only in the prompt.
- **Undefined state on old profiles** → explicit fallback to `auto`/omit `--lang`.
- **A flow silently skipped** → the touch-list table is the checklist; each flow confirms generate + interact + `--lang`.

## Sequencing

1. **Task A — Onboarding:** `init.md` step 0 + write field, `discovery-script` note, `authority-context` template + SKILL.
2. **Task B — Propagation:** the 4 flows + `linkedin.md` + the fallback rule.
