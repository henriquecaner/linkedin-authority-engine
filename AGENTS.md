# Repository Guidelines

## Project Overview

**LinkedIn Authority Engine** is a Claude Code / Claude Cowork plugin (v1.4.0, LEVEL TECH), not an application. It turns a founder's expertise into LinkedIn authority posts tuned to the "360Brew" algorithm reference (v3.5, Q1 2026), backed by a per-client profile (`authority-context.md`) and a memory layer that every command enriches on each run.

Almost everything here is markdown that Claude reads at runtime: 6 slash commands, 23 skills, 2 agents. The only executable code is a stdlib-only Python CLI suite (4 CLIs + `postlib.py`) for scoring, validating posts, and Unipile deep discovery, covered by an 85-test pytest suite.

Two artifact sets live in this repo; the distinction matters when editing:

- **Plugin source**: `linkedin-authority-engine/`. Ships to users; edits change product behavior.
- **Consumer state**: `authority-context.md`, `memory/`, `outputs/`. Created *inside a user's project* by `/init`. None of these exist at this repo's root today; the GTM front keeps its own copies under the gitignored `gtm/`.

`CLAUDE.md` explains the product rationale (why the Gates exist, what the pipeline protects). This file records verified mechanics: counts, flags, file layout, the test contract. Both were checked against the tree on 2026-09-11. If they ever disagree, the tree wins; fix both files instead of picking one.

## Architecture & Data Flow

**Runtime model.** No server, no persistent process. Each slash command is a markdown playbook Claude executes. `hooks/hooks.json` adds one `SessionStart` hook (matcher `startup`, type `command`) that echoes a banner pointing to `/linkedin-authority-engine:init` when no profile exists.

**The Gates pattern** (defined in `skills/authority-context/SKILL.md`). Every generation or scoring flow (`guided`, `rewrite`, `thread`, `score`, and the workflow skills) follows the same scaffold. A new command that skips a gate breaks the memory loop.

1. **Gate 1**: no `authority-context.md` in the project → route to `/init`.
2. **Gate 2**: load `authority-context.md` plus all four memory files (`memory/winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`) as constraints. Read `language:` from the profile frontmatter (`pt` → Brazilian Portuguese, "você" form; `en` → English) and pass `--lang <pt|en>` to both scripts.
3. **Gate 3-M** (memory append, the default): append, never overwrite, to `winning-hooks.md` (approved hooks; `score` mode only when Hook ≥ 8), `topic-performance.md`, `learnings.md`. `voice-profile.md` is read-only under Gate 3-M; Gate 1 Path U may seed it from a measured post corpus. Performance columns stay empty until v1.x.
4. **Gate 3-S** (profile write-back, strategy skills only: `niche-definer`, `audience-persona`, `content-pillars`): propose → diff → confirm → replace the target section in place at field granularity → bump `version` in the frontmatter and log to `memory/learnings.md`. Ownership: `niche-definer` owns §2 core theme + value proposition, `content-pillars` owns §2 pillars + §11 priority themes, `audience-persona` owns §4.

**Post pipeline** (`commands/guided.md` is the reference): Gate 2 → STEP 0-6 (category → objective → agenda → structure → type → hooks → body → CTA) → Finalization A-E:

- A: `validate_specs.py post.txt --lang <pt|en>`
- B: `humanizer-linkedin` skill (mandatory before scoring for any externally-facing post)
- C: `visual-brief` skill
- D: `score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>` (6 dimensions plus Top 1% / Top 5% probability)
- E: `post-publication-protocol` (first comment + 90-minute plan)

then Gate 3-M. Decision bands (`commands/score.md`): ≥ 9 publish, 7-8.9 adjust, < 7 rework.

**Skills split** (23 in `linkedin-authority-engine/skills/`, each exactly one `SKILL.md`; only `authority-context/` has a `references/` dir):

- **12 knowledge bases** loaded on demand: `360brew-algorithm`, `authority-context`, `hooks`, `copywriting-structures`, `content-types`, `templates-by-category`, `ctas`, `style-and-tone`, `humanizer-linkedin`, `post-publication-protocol`, `visual-brief`, `discovery-script`.
- **11 self-invoking workflow skills**, each with When-to-trigger / Inputs / Process / Output sections: strategy (`niche-definer`, `audience-persona`, `content-pillars`, `content-calendar`), production (`repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`), audits (`profile-optimizer`, `analytics-interpreter`), discovery (`linkedin-deep-discovery`, v1.4.0). The first ten shipped in v1.3.0.

**Python scoring layer** (`linkedin-authority-engine/scripts/`):

- `postlib.py` is the single source of truth: `SPECS` (11 keys: `chars_min` 1250, `chars_max` 2500, `chars_warning_min` 1000, `chars_warning_max` 3000, `paragraphs_min` 14, `paragraphs_warning` 10, `avg_word_length_max` 5, `avg_word_length_warning` 6, `max_words_per_paragraph` 19, `dense_paragraph_chars` 150, `hashtags_max` 2) plus every PT/EN regex matcher. `score_post.py` and `validate_specs.py` import it. `suggest_hooks.py` does not: its `HOOKS` dict mirrors `skills/hooks/SKILL.md` by hand, a second manual sync point.
- **Three-way sync, no enforcement:** `postlib.SPECS` ↔ `WEIGHTS` in `score_post.py` (`saves_potential` 0.30, `hook` 0.20, `algorithm` 0.20, `structure` 0.15, `cta` 0.10, `data` 0.05) ↔ the Metrics table in `skills/360brew-algorithm/SKILL.md`. Aligned as of 2026-09-11; change one, update the other two by hand.
- **Union matching, not detection.** `resolve_langs("auto")` returns `["pt", "en"]`; every matcher loops over both sets and dedupes by canonical label. `detect_language()` is for reporting and never gates matching. New pattern → add it to both `_*["pt"]` and `_*["en"]` with the same label (see `_SAVES`, `_CTA`, `_PUNISHED`, `_AI_CLICHE_HOOKS`). Matching is word-anchored (`_WORD_RE`) and accent-insensitive; AI clichés are checked in the first 5 lines only.

## Key Directories

|Path|Purpose|
|---|---|
|`linkedin-authority-engine/.claude-plugin/`|`plugin.json` + `marketplace.json`; version `1.4.0` duplicated in both|
|`linkedin-authority-engine/commands/`|`init`, `linkedin` (menu router), `guided`, `rewrite`, `thread`, `score`|
|`linkedin-authority-engine/skills/`|23 skills at `skills/<name>/SKILL.md`|
|`linkedin-authority-engine/agents/`|`linkedin-strategist` (`model: opus`, `effort: high`), `humanizer-linkedin` (`opus`, `medium`)|
|`linkedin-authority-engine/scripts/`|`postlib.py`, `score_post.py`, `validate_specs.py`, `suggest_hooks.py`, `unipile_discovery.py`|
|`linkedin-authority-engine/hooks/`|`hooks.json` (SessionStart banner)|
|`tests/`|pytest suite (5 files) + `fixtures/post_example.txt` (EN) and `post_example_pt.txt` (PT translation of the same post)|
|`.env.example`|Unipile credential names (`UNIPILE_API_KEY`, `UNIPILE_DSN`, …). Never commit `.env`.|
|`docs/superpowers/specs/`, `docs/superpowers/plans/`|Design history: 7 specs, 4 plans. Newest is `specs/2026-07-10-connect-publish-loop-design.md`, a v1.5.0 draft for Composio publishing. Plugin 1.4.0 is Unipile deep discovery, not that spec. Not plugin source; PT-BR and EN mixed|
|`.github/workflows/`|`claude.yml` (@claude mentions) and `claude-code-review.yml` (PR auto-review). Neither runs pytest|
|`.claude/settings.json`|Tracked dev-time plugins: superpowers, plugin-dev, frontend-design|
|`gtm/`, `archive/`, `CLAUDE.local.md`, `.claude/settings.local.json`, `.superpowers/sdd/`, `.playwright-mcp/`, `.venv/`, `.env`, `*.zip`|Local-only and gitignored (`.superpowers/sdd/` ignores itself). Never commit|
|`create-app.md`, `console-errs.txt`, `modal-checkout-lae.png`|Tracked at the root but unrelated to the plugin (landing-page / checkout debugging leftovers). Do not extend or reference them|

## Development Commands

```bash
# Run everything from the repo root with the local venv (Python 3.14, pytest 9.1).
# `pytest` alone works once .venv is activated.
.venv/bin/python -m pytest                                          # 85 tests, under 1 s
.venv/bin/python -m pytest tests/test_postlib.py                    # one file
.venv/bin/python -m pytest tests/test_scripts_cli.py::test_score_post_runs

# CLIs (inside the plugin they are invoked as ${CLAUDE_PLUGIN_ROOT}/scripts/<name>.py)
.venv/bin/python linkedin-authority-engine/scripts/score_post.py <post.txt> [--objective authority|sales|engagement] [--lang auto|pt|en] [--json] [--compact]
.venv/bin/python linkedin-authority-engine/scripts/validate_specs.py <post.txt> [--lang auto|pt|en] [--json] [--quiet]
.venv/bin/python linkedin-authority-engine/scripts/suggest_hooks.py --category <career_lesson|achievement|failure|debunk|practical_tip|opinion|behind_the_scenes|other> --objective <authority|sales|engagement> [--topic "..."] [--count N] [--seed N] [--json]
.venv/bin/python linkedin-authority-engine/scripts/unipile_discovery.py --linkedin-url <url> --role self|reference [--posts N] [--out DIR] [--json] [--dry-run]

# Install into Claude Code
/plugin marketplace add /path/to/linkedin-authority-engine
/plugin install linkedin-authority-engine
/linkedin-authority-engine:init
```

Exit codes: `validate_specs.py` returns 1 when the post fails a hard spec; `score_post.py` returns 1 only when the file is missing. There is no build, lint, or format step.

## Code Conventions & Common Patterns

- **Language.** Plugin source (commands, skills, agents, scripts, READMEs) is English. Reply to the user in their language. Generated posts follow `language:` in the profile frontmatter. Design docs under `docs/superpowers/` mix PT-BR and EN; that is not a precedent for plugin source.
- **Output naming.** Posts: `outputs/posts/<YYYYMMDD>-<slug>-v1.md`, bumping to `v2`, `v3` when the slug exists. Strategy artifacts (calendars, profile audits, analytics reports): `outputs/strategy/<YYYYMMDD>-<artifact>.md`; these skip the post finalization pipeline.
- **`/init` creates** `authority-context.md` (sections `# 1.` to `# 13.`; frontmatter `last_updated`, `version`, `language`), `memory/{winning-hooks,topic-performance,voice-profile,learnings}.md` with empty headers from `skills/authority-context/references/memory-schemas.md`, and `outputs/posts/.gitkeep`. Path U (Unipile) may seed `voice-profile.md` instead of leaving it empty; that seeding is Gate 1, not Gate 3-M.
- **Versioning.** Bump `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` together. `tests/test_plugin_structure.py::test_plugin_json_valid` pins the literal `"1.4.0"`, so bump the test in the same change.
- **Frontmatter contracts** (enforced by `tests/test_plugin_structure.py`): commands need `description:` and `argument-hint:`; agents need `name:` and `description:` (both agents also set `model` and `effort`); skill bodies must exceed 200 chars. `commands/guided.md` is the canonical Gates example.
- **Adding a skill** requires adding its name to `EXPECTED_SKILLS` or `EXPECTED_WORKFLOW_SKILLS` in `tests/test_plugin_structure.py`, otherwise the suite does not guard it.
- **Humanizer pass.** Prose for humans (post copy, READMEs, marketing) goes through `humanizer-linkedin` before it is saved or shown. Skip for code, configs, commit messages, and short status updates.
- **No Taplio coupling** in workflow skills. `test_workflow_skills_have_no_taplio_coupling` rejects `taplio`, `search_inspiration`, `get_me`, `create_draft`, `utm_source`, `power up with` (case-insensitive).
- **Python style.** Stdlib only (`re`, `argparse`, `json`, `pathlib`, `random`, `sys`). Module docstring with usage, snake_case functions, `main()` behind `if __name__ == "__main__":`. Scorer feedback prefixes: `[+]` good, `[o]` moderate, `[X]` problem, `[!]` warning (today only "Multiple CTAs detected").

## Important Files

|File|Why it matters|
|---|---|
|`linkedin-authority-engine/.claude-plugin/plugin.json`|Manifest keys: `name`, `displayName`, `version`, `description`, `author`, `homepage`, `license`, `keywords`|
|`linkedin-authority-engine/scripts/postlib.py`|`SPECS`, `LANGS`, `resolve_langs()`, all PT/EN matchers|
|`linkedin-authority-engine/scripts/score_post.py`|`WEIGHTS`, six `score_*` functions, `calculate_probabilities()`, `--json` / `--compact` output|
|`linkedin-authority-engine/scripts/unipile_discovery.py`|Deep discovery CLI: profile + posts + company via Unipile v2; stdlib; opener/sleep/rand injectable|
|`linkedin-authority-engine/skills/360brew-algorithm/SKILL.md`|Algorithm reference v3.5; its Metrics table must match `SPECS` / `WEIGHTS`|
|`linkedin-authority-engine/skills/authority-context/SKILL.md`|Gates 1 / 2 / 3-M / 3-S; `references/authority-context-template.md` (13 sections) and `references/memory-schemas.md`|
|`linkedin-authority-engine/commands/guided.md`|Reference implementation of Gates + pipeline|
|`linkedin-authority-engine/hooks/hooks.json`|SessionStart hook|
|`tests/conftest.py`|Single fixture `plugin_dir` → `<repo>/linkedin-authority-engine`|
|`CLAUDE.md`|Product rationale for the same architecture|

## Runtime/Tooling Preferences

- **Python 3.14** via the gitignored `.venv/` at the repo root (Homebrew `python@3.14`). No `requirements.txt`, `pyproject.toml`, `setup.cfg`, `pytest.ini`, `tox.ini`, or `Makefile`: scripts are stdlib-only and pytest is the only third-party package installed. If the venv is missing: `python3.14 -m venv .venv && .venv/bin/pip install pytest`.
- **No Node/JS stack.** No `package.json`, lockfile, or `node_modules` anywhere. Do not introduce one.
- **Run from the repo root.** This preserves the memory namespace, `.claude/settings.json` permissions, and the SessionStart hook. GTM tooling (`/hormozi-gtm:*`, enabled only in the local `.claude/settings.local.json`) treats `gtm/` as its project root, never the repo root.
- **CI is Claude-driven only.** Both workflows in `.github/workflows/` run `anthropics/claude-code-action@v1`; no workflow installs Python or runs pytest. The local suite is the quality gate.
- **Packaged builds** are `*.zip` files, gitignored. None is present in the tree right now.

## Testing & QA

- **Framework:** bare pytest, no config file. 85 tests collected (11 plugin structure + 4 agents structure + 29 postlib, 5 of them parametrized + 13 CLI + 28 unipile); 85 passed in 0.92 s on 2026-09-11.
- `tests/test_plugin_structure.py`: manifests (`version == "1.4.0"`, required keys), 10 + 11 skills from `EXPECTED_SKILLS` / `EXPECTED_WORKFLOW_SKILLS`, `authority-context` assets (template sections 1-13, four memory file names in `memory-schemas.md`), `discovery-script` coverage (11 section labels, at least 25 `?`), 6 command and 2 agent frontmatters, `hooks.json` contains `SessionStart`, Taplio guard, stale-reference guard (`LinkedIn Content \d`, `virall-linkedin-content`).
- `tests/test_scripts_cli.py`: runs each CLI as `subprocess.run([sys.executable, script, ...])` against the paired PT/EN fixtures and asserts on `--json` output: language autodetect, proof-of-work in both languages, PT/EN `saves_potential` parity, punished-hook flagging via `validate_specs.py --json`, `--lang en` suppressing PT verbs, `--seed 7` determinism. This is the real CLI contract; keep it green ahead of unit tests.
- `tests/test_postlib.py`: word-anchoring against substring false positives (`brand` does not match `ran`), PT stemming (`triplicamos`), accent-insensitive and curly-apostrophe cliché matching, canonical-label dedupe across PT+EN, the `-1.5` hook penalty for AI clichés.
- `tests/test_unipile_discovery.py`: offline Unipile client (pagination, slug→id, engagement, dry-run, credentials). No network.
- **Expectation:** any change to a matcher, `SPECS`, or `WEIGHTS` gets fixture-based coverage in both languages, and `.venv/bin/python -m pytest` stays green from the repo root before the change counts as done.
