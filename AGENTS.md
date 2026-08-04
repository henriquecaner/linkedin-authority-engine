# Repository Guidelines

## Project Overview

**LinkedIn Authority Engine** is a plugin for Claude Code / Claude Cowork (v1.3.0, LEVEL TECH), not an application. It turns a founder's expertise into LinkedIn authority posts tuned to the "360Brew" algorithm reference, backed by a living client profile and self-enriching memory.

Most of the repo is markdown (commands, skills, agents) that Claude reads at runtime. The only executable code is a small Python CLI suite for scoring and validation.

Two artifact sets live here; the distinction matters when editing:

- **Plugin source** — `linkedin-authority-engine/`. This ships to users; edits change product behavior.
- **Consumer state** — `authority-context.md`, `memory/`, `outputs/posts/`. These are created *inside a user's project* by `/init`; the instances at the repo root are sample/dev data, not plugin source.

## Architecture & Data Flow

**Runtime model:** no server, no persistent process. Each slash command is a markdown playbook that Claude executes.

**The Gates pattern** — every generation/scoring command (`guided`, `rewrite`, `thread`, `score`) is structured as gates. New commands must follow the same scaffold or the memory loop breaks:

1. **Gate 1** — existence check: no `authority-context.md` → route to `/init`.
2. **Gate 2** — read the substrate: load `authority-context.md` + all of `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`) as constraints.
3. **Gate 3** — write-back: append findings to `memory/` (the "self-enrichment doors").

**Post pipeline:** read profile/memory → generate (structure → hook → body → CTA) → `humanizer-linkedin` (mandatory before scoring for any externally-facing post) → `score_post.py` (6 dimensions) → `post-publication-protocol` → write-back to `memory/`. The strategy trio (`niche-definer`, `audience-persona`, `content-pillars`) writes results back into `authority-context.md` via the **Gate 3-S** protocol: propose → diff → confirm → version bump.

**Skills split** (22 total in `linkedin-authority-engine/skills/`):

- **12 knowledge bases** the commands load on demand: `360brew-algorithm`, `authority-context`, `hooks`, `copywriting-structures`, `content-types`, `templates-by-category`, `ctas`, `style-and-tone`, `humanizer-linkedin`, `post-publication-protocol`, `visual-brief`, `discovery-script`.
- **10 self-invoking workflow skills** (v1.3.0): strategy (`niche-definer`, `audience-persona`, `content-pillars`, `content-calendar`), production (`repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`), audits (`profile-optimizer`, `analytics-interpreter`). Each carries When-to-trigger / Inputs / Process / Output sections and auto-invokes from plain-language requests.

**Python scoring layer:**

- `scripts/postlib.py` is the single source of truth: `SPECS` (char limits, paragraph minimums) and the PT/EN regex matchers. `score_post.py` and `validate_specs.py` both import it.
- **3-way sync, no enforcement:** `postlib.SPECS` ↔ `WEIGHTS` in `score_post.py` (saves 30%, hook 20%, algorithm 20%, structure 15%, cta 10%, data 5%) ↔ the Metrics section of `skills/360brew-algorithm/SKILL.md`. Changing one requires manually updating all three.
- **Multilingual matching is union-based, not detection-based.** `--lang auto` (default) matches text against BOTH PT and EN pattern sets simultaneously; `detect_language()` is for reporting only and never gates matching. When adding a pattern, add it to both the `_*["pt"]` and `_*["en"]` dicts and keep labels canonical so union matching dedupes (see `_SAVES`, `_CTA`, `_PUNISHED`, `_AI_CLICHE_HOOKS` in `postlib.py`).

**Hook:** `hooks/hooks.json` defines a `SessionStart` banner that points the user to `/init` when no profile exists.

## Key Directories

| Path | Purpose |
|---|---|
| `linkedin-authority-engine/.claude-plugin/` | `plugin.json` + `marketplace.json` manifests (version duplicated in both) |
| `linkedin-authority-engine/commands/` | 6 slash commands: `init`, `linkedin`, `guided`, `rewrite`, `thread`, `score` |
| `linkedin-authority-engine/skills/` | 22 skills, each at `skills/<name>/SKILL.md` |
| `linkedin-authority-engine/agents/` | 2 agents: `linkedin-strategist`, `humanizer-linkedin` |
| `linkedin-authority-engine/scripts/` | 3 CLIs + `postlib.py` shared library |
| `linkedin-authority-engine/hooks/` | `hooks.json` (SessionStart hook) |
| `tests/` | pytest suite + `fixtures/` (paired PT/EN sample posts) |
| `docs/superpowers/` | Design history and roadmap specs/plans (not plugin source) |
| `gtm/`, `archive/`, `CLAUDE.local.md` | Gitignored local GTM/strategy front. Never commit |

## Development Commands

```bash
# Tests — pytest is the only runner; run from the repo root
pytest                                                    # full suite
pytest tests/test_postlib.py                              # single file
pytest tests/test_scripts_cli.py::test_score_post_runs    # single test

# Python CLIs (in the plugin they're called via ${CLAUDE_PLUGIN_ROOT}/scripts/)
python linkedin-authority-engine/scripts/score_post.py <post.txt> [--objective authority|sales|engagement] [--lang auto|pt|en] [--json] [--compact]
python linkedin-authority-engine/scripts/validate_specs.py <post.txt> [--lang auto|pt|en]
python linkedin-authority-engine/scripts/suggest_hooks.py --category <cat> --objective <obj> [--topic "..."] [--seed N]

# Install in Claude Code
/plugin marketplace add /path/to/linkedin-authority-engine
/plugin install linkedin-authority-engine
/linkedin-authority-engine:init
```

## Code Conventions & Common Patterns

- **Language:** plugin content is written in English. Reply to the user in their language. Session language for generated posts comes from the `language:` field in `authority-context.md` frontmatter (`pt` → Brazilian Portuguese, "você" form; pass `--lang <pt|en>` to both `validate_specs.py` and `score_post.py`).
- **Output naming:** posts save to `outputs/posts/<YYYYMMDD>-<slug>-v1.md`, bumping to `v2`/`v3` when the slug exists. Non-post strategy artifacts (calendars, profile audits, analytics reports) save to `outputs/strategy/<YYYYMMDD>-<artifact>.md` and do NOT run the post finalization pipeline.
- **Versioning:** the version string is duplicated in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Bump both together.
- **Frontmatter contracts** (enforced by `tests/test_plugin_structure.py`): commands need `description:` and `argument-hint:`; agents need `name:` and `description:`; skill bodies must be substantial (>200 chars). `commands/guided.md` is the canonical example of the Gates scaffold.
- **Humanizer pass:** prose for humans (post copy, READMEs, marketing) must pass through `humanizer-linkedin` (in-plugin) before saving or showing. Skip for code, configs, commit messages, and short status updates.
- **No Taplio coupling:** workflow skills must not reference Taplio (guarded by `test_workflow_skills_have_no_taplio_coupling`).
- **Python style:** stdlib only (`re`, `argparse`, `json`, `pathlib`, `random`, `sys`). Each script has a module docstring with usage, snake_case functions, a `main()` behind `if __name__ == "__main__":`, and no third-party imports. Scorer feedback lines are prefixed `[+]` (good), `[o]` (moderate), `[X]` (problem).

## Important Files

| File | Why it matters |
|---|---|
| `linkedin-authority-engine/.claude-plugin/plugin.json` | Plugin manifest; version `1.3.0` (mirrored in `marketplace.json`) |
| `linkedin-authority-engine/scripts/postlib.py` | Single source of truth: `SPECS` + all PT/EN matchers |
| `linkedin-authority-engine/scripts/score_post.py` | `WEIGHTS` + the 6 dimension scorers; `--json`/`--compact` output modes |
| `linkedin-authority-engine/skills/360brew-algorithm/SKILL.md` | Algorithm reference; Metrics section must stay in sync with `SPECS`/`WEIGHTS` |
| `linkedin-authority-engine/skills/authority-context/SKILL.md` | Read/write protocol for the memory substrate; `references/` holds memory schemas |
| `linkedin-authority-engine/commands/guided.md` | Reference implementation of Gates + pipeline |
| `linkedin-authority-engine/hooks/hooks.json` | SessionStart hook definition |
| `tests/conftest.py` | `plugin_dir` fixture used by all tests |
| `CLAUDE.md` | Authoritative repo guidance; this file complements it |

## Runtime/Tooling Preferences

- **Python 3.14** via the local `.venv/` at the repo root (gitignored, already present). There is no `requirements.txt`/`pyproject.toml`: scripts are stdlib-only; pytest is the single third-party dependency.
- **No Node/JS stack.** There is no `package.json` anywhere; do not introduce one.
- **Run everything from the repo root.** This preserves the memory namespace, `.claude/settings.json` permissions, and the SessionStart hook. GTM tooling (`/hormozi-gtm:*`) treats `gtm/` as its project root, never the repo root (see `CLAUDE.local.md`).
- `.claude/settings.json` enables dev-time plugins (superpowers, plugin-dev, frontend-design); `.claude/settings.local.json` is machine-local and gitignored.
- **CI is Claude-driven only** (`.github/workflows/`): `claude.yml` responds to `@claude` mentions on issues/PRs; `claude-code-review.yml` auto-reviews PRs. CI does NOT run pytest; the local suite is the quality gate.
- `*.zip` is gitignored; `linkedin-authority-engine-v1.3.0.zip` at the root is a packaged build artifact, not source.

## Testing & QA

- **Framework:** bare pytest, no config file (no `pytest.ini`/`pyproject.toml`), run from the repo root. 53 tests, ~1s.
- **Coverage by file:**
  - `tests/test_plugin_structure.py` — structure guards: manifest keys, command/agent frontmatter, all 22 skills present with substantial bodies, discovery-script question count, no Taplio coupling, no stale skill references.
  - `tests/test_scripts_cli.py` — exercises the CLIs as subprocesses (`[sys.executable, script, ...]`) against the paired PT/EN fixtures in `tests/fixtures/`, asserting on `--json` output: language autodetect, PT/EN score parity, punished-hook flagging, `--lang` override, `--seed` determinism. This validates the real CLI contract, not just imported functions.
  - `tests/test_postlib.py` — direct unit tests of the matcher library (word-anchoring against false positives, accent-insensitive matching, canonical-label dedupe under union matching).
- **Expectations:** when adding or changing a matcher pattern or a `SPECS`/`WEIGHTS` value, cover both languages with fixture-based tests and keep `pytest` green from the repo root before considering the change done.
