# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo is **not an application** — it is the source of a Claude Code / Claude Cowork **plugin** (`linkedin-authority-engine/`, v1.4.0). The plugin turns a founder's expertise into LinkedIn posts tuned for the 360Brew algorithm. Most of the "code" is markdown (commands, skills, agents) that Claude reads at runtime; the only executable code is a small Python CLI suite used for scoring/validation and Unipile deep discovery.

Two distinct artifact sets live here, and the distinction matters when editing:
- **Plugin source** (`linkedin-authority-engine/`) — what ships to users. Editing this changes product behavior.
- **Consumer state** — `authority-context.md`, `memory/`, `outputs/posts/`. These are created *inside a user's project* by `/init`. In this repo they are sample/dev instances, not plugin source.

Base language of all shipped artifacts is **English** (see README). Respond to the user in their language, but keep plugin content in EN unless told otherwise.

## Commands

```bash
# Tests (from repo root) — pytest is the only test runner
pytest                          # full suite
pytest tests/test_postlib.py    # single file
pytest tests/test_scripts_cli.py::test_score_post_runs   # single test

# Python CLIs (run from anywhere; in the plugin they're called via ${CLAUDE_PLUGIN_ROOT}/scripts/)
python linkedin-authority-engine/scripts/score_post.py <post.txt> [--objective authority|sales|engagement] [--lang auto|pt|en] [--json] [--compact]
python linkedin-authority-engine/scripts/validate_specs.py <post.txt> [--lang auto|pt|en] [--json] [--quiet]
python linkedin-authority-engine/scripts/suggest_hooks.py --category <cat> --objective <obj> [--topic "..."] [--count N] [--seed N] [--json]
python linkedin-authority-engine/scripts/unipile_discovery.py --linkedin-url <url> --role self|reference [--posts N] [--out DIR] [--json] [--dry-run]
```

There is a local `.venv/` (Python 3.14). Tests shell out to the scripts via `sys.executable` as subprocesses (see `tests/test_scripts_cli.py`), so they validate the actual CLI contract, not just imported functions.

## Architecture

### The plugin runtime model (read this before editing commands)

The plugin has no server and no persistent process. Each command is a markdown playbook Claude executes. Three structural conventions tie the commands together — preserve them when editing:

1. **The "Gates" pattern.** Every generation/scoring command (`guided`, `rewrite`, `thread`, `score`) is structured as gates:
   - **Gate 1** — existence check: if no `authority-context.md`, route to `/init`.
   - **Gate 2** — read the substrate: load `authority-context.md` + all of `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`) and apply them as constraints.
   - **Gate 3** — write-back: after the work, append findings to `memory/` (the "self-enrichment doors"). This is what makes the plugin learn per-client.
   When adding a command, follow the same gate scaffold or the memory loop breaks.

2. **The pipeline.** Generation flows: read profile/memory → generate (structure → hook → body → CTA) → `humanizer-linkedin` skill (strip AI tone) → `score_post.py` (6 dimensions) → `post-publication-protocol` → write-back. The humanizer pass before scoring is mandatory for any externally-facing post.

3. **Skills are the knowledge base — and, as of v1.3.0, also self-invoking workflows.** The 23 skills in `linkedin-authority-engine/skills/` split into two kinds: (a) *knowledge bases* the commands load on demand (hooks bank, copy frameworks, CTAs, 360Brew spec, etc.) — commands orchestrate, these hold domain knowledge; and (b) *workflow skills* (`niche-definer`, `audience-persona`, `content-pillars`, `content-calendar`, `repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`, `profile-optimizer`, `analytics-interpreter`, plus `linkedin-deep-discovery` in v1.4.0) that carry their own When-to-trigger / Inputs / Process / Output, auto-invoke from plain-language requests, and follow the same Gates scaffold. The strategy trio (`niche-definer`, `audience-persona`, `content-pillars`) writes back into `authority-context.md` via the **Gate 3-S** protocol (propose → diff → confirm → in-place section replace → version bump), defined in the `authority-context` skill. `voice-profile.md` may be seeded at Gate 1 (Path U); Gate 3-M still must not overwrite it. Change a numeric spec in one place and check whether `score_post.py` mirrors it (see below).

### The Python scoring layer

`postlib.py` is the **single source of truth** imported by both `score_post.py` and `validate_specs.py`. Key facts:
- `SPECS` (char counts, paragraph minimums, etc.) lives in `postlib.py`. The dimension `WEIGHTS` live in `score_post.py` (saves 30%, hook 20%, algorithm 20%, structure 15%, cta 10%, data 5%) and are documented as aligned with `skills/360brew-algorithm/SKILL.md`. **These three locations (postlib SPECS, score_post WEIGHTS, the SKILL.md Metrics section) must stay in sync** — there is no enforcement, so changing one requires manually updating the others.
- **Multilingual matching is union-based, not detection-based.** With `--lang auto` (default), text is matched against *both* PT and EN pattern sets simultaneously; `detect_language()` is for reporting only and never gates matching. PT/EN keyword sets are designed not to collide, and structural matches dedupe by canonical label. When adding a pattern, add it to both `_*["pt"]` and `_*["en"]` dicts and keep labels canonical so union matching doesn't double-count.

### Design docs (not plugin source)

`docs/superpowers/` (plans + specs) holds the plugin's design history and active roadmap specs. It documents how the product was built and what's next; it is not part of the shipping plugin.

## Conventions

- **Output naming:** generated posts save to `outputs/posts/<YYYYMMDD>-<slug>-v1.md`, incrementing the version suffix (`v2`, `v3`) when a slug already exists. Non-post strategy artifacts (content calendars, profile audits, analytics reports) save to `outputs/strategy/<YYYYMMDD>-<artifact>.md` and do **not** run the post finalization pipeline.
- **Versioning:** the plugin version is duplicated in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — bump both together. Current pin is `1.4.0` (Unipile deep discovery). The Composio connect-publish spec is a v1.5.0 draft, not this release.
- **Prose for humans** (READMEs, post copy, marketing) must pass through a humanizer pass (the `humanizer-linkedin` skill in-plugin, or the global `humanizer` skill) before being saved or shown. Skip for code, configs, commit messages, and short status updates.
