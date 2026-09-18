# LinkedIn Authority Engine

> Plugin for **Claude Code** and **Claude Cowork** that turns a founder's expertise into authority on LinkedIn. Posts tuned for the 360Brew algorithm, with a living client profile and memory that learns every session.

[![version](https://img.shields.io/badge/version-1.5.0-black)](./linkedin-authority-engine/.claude-plugin/plugin.json)
[![skills](https://img.shields.io/badge/skills-23-2ea44f)](./linkedin-authority-engine/skills)
[![platform](https://img.shields.io/badge/Claude%20Code%20%7C%20Cowork-plugin-blue)](https://thelevr.com)
[![algorithm](https://img.shields.io/badge/360Brew-v3.5%20Q1%202026-orange)](./linkedin-authority-engine/skills/360brew-algorithm/SKILL.md)
[![license](https://img.shields.io/badge/license-proprietary-lightgrey)](#license)

By **[LEVEL TECH](https://thelevel.com.br)** · product page: **[thelevr.com](https://thelevr.com)**

---

## The problem

You're an expert and no one on LinkedIn knows it. Maybe you've already tried: posted for months, got two likes (one from your business partner), and stopped. Or you paid an agency that gave you back "awareness" and a polished report, with zero meetings on the calendar.

The bottleneck was never knowledge. It's that you didn't have a system to take what you know and ship it in the format the LinkedIn algorithm rewards, week after week, without turning you into a full-time content creator.

## What the plugin does

You talk to Claude in plain language. The plugin reads your authority profile and does what the request needs: sharpen your positioning, plan a month of posts, draft and grade a single post, or audit your profile copy. Whatever it writes comes out in your voice and gets checked against the LinkedIn algorithm, not vague best practices. Every result feeds a memory, so the next session starts closer to you.

As of v1.3.0 it covers the whole loop, not just the writing:

| Stage | Just ask, or run | Powered by |
|---|---|---|
| **Strategy** | "define my niche", "build my content pillars", "plan my next 4 weeks" | `niche-definer`, `audience-persona`, `content-pillars`, `content-calendar` |
| **Produce** | `/guided`, "turn this into a post", "turn this into a carousel", "fix my CTA" | `guided`, `repurposer`, `story-extractor`, `carousel-builder`, `cta-optimizer` |
| **Score & ship** | `/score`, `/rewrite` | `score_post.py`, `humanizer-linkedin`, `post-publication-protocol` |
| **Audit** | "audit my profile", "read my analytics" | `profile-optimizer`, `analytics-interpreter` |

What sets it apart from a generic text generator:

- **Tuned for 360Brew.** Format, timing, hook, and CTA get checked against the LinkedIn algorithm reference (v3.5, Q1 2026), not generic advice.
- **A living client profile.** `authority-context.md` holds who you are, your voice, your topics, and your numbers, so the content comes out yours, not off a template. The strategy skills write back into it as your positioning sharpens.
- **Self-enriching memory.** Patterns that work get saved as learnings, so the plugin gets sharper on your case each session, through three write-back "doors."
- **Portuguese and English.** Scoring and validation run on both. A shared library (`postlib.py`) is the single source of truth for the PT/EN matchers and the 360Brew specs; force a language with `--lang pt|en` or let it auto-detect.

## A typical session

You don't memorize commands. You say what you want, and the right skill loads on its own.

"Help me figure out what to be known for" pulls up `niche-definer`, which sharpens your positioning and writes it into your profile. "Plan my next month" builds a four-week calendar off your pillars. "Turn this podcast transcript into a post" hands it to `repurposer`, runs it through the humanizer and the score, and saves the result. "Audit my profile" reads your headline and About and hands back rewrites. The slash commands (`guided`, `rewrite`, `thread`, `score`) are still there when you want the structured post workflow.

---

## Installation & Quickstart

### Option A: Google Antigravity (Native IDE / CLI)

1. Clone or open this repository in **Antigravity**.
2. Antigravity automatically detects the [`.agents/`](file:///.agents) directory, loading all rules, subagents, and skills natively.
3. Start the onboarding in chat:
   > *"Quero fazer o onboarding de autoridade"* or *"iniciar setup"*
4. The engine conducts a discovery interview and creates your `authority-context.md` and `memory/` substrate.

### Option B: Claude Code / Cowork Plugin

```bash
# 1. add the local marketplace
/plugin marketplace add /path/to/linkedin-authority-engine

# 2. install the plugin
/plugin install linkedin-authority-engine

# 3. create the client profile (onboarding)
/linkedin-authority-engine:init
```

After `init`, use `/linkedin-authority-engine:linkedin` to see the mode menu.

---

## Commands

| Command | What it does |
|---|---|
| `init` | Onboarding. Runs the discovery interview and creates `authority-context.md`, `memory/` and `outputs/posts/`. Accepts `--refresh` to update the profile. |
| `linkedin` | Central menu. Shows the modes and the strategy/produce/audit skills, and routes to the chosen one. A good starting point. |
| `guided` | Creates a post from scratch in a 7-step workflow: category → objective → angle → structure → type → hook → body → CTA. |
| `rewrite` | Optimizes an existing post into two versions (conservative and bold), with a 360Brew diagnosis, humanizer and comparative score. |
| `thread` | Builds a series of 3-7 posts on a topic, with a planned architecture (hook, authority, educational, story, conversion). |
| `score` | Evaluates and humanizes a finished post. Runs technical validation, humanizer and a grade across the 6 dimensions, with a verdict: publish / adjust / rework. |

Beyond the commands, 10 **workflow skills** (strategy, production, audits) load when you ask for them in plain language. They are listed under [Skills](#skills-22).

---

## How it works under the hood

```
authority-context.md  ─┐
memory/                ─┤──►  reads profile + winning patterns
                        │
                  ┌─────▼─────────────────────────────────┐
                  │  generation (guided / rewrite / thread)│
                  │  structure → hook → body → CTA         │
                  └─────┬─────────────────────────────────┘
                        │
                  humanizer-linkedin   (takes the AI look out)
                        │
                  score_post.py        (6 360Brew dimensions)
                        │
                  post-publication-protocol (90 critical min)
                        │
                  write-back ──►  memory/  (self-enrichment)
```

The strategy skills (`niche-definer`, `audience-persona`, `content-pillars`) close a second loop: they write their result back into `authority-context.md` through the **Gate 3-S** protocol (propose → diff → confirm → version bump), so the profile that feeds every post keeps getting sharper.

### Skills (22)

The plugin's intelligence lives in the skills. Each one is a reference Claude loads when it needs it. Twelve are knowledge bases the commands draw on:

| Skill | Function |
|---|---|
| `360brew-algorithm` | Full algorithm reference: format, timing, metrics and scoring. |
| `authority-context` | Read/write protocol for the client's memory substrate. The 3 self-enrichment doors. |
| `hooks` | A bank of 147 hooks by type (proof, authority, transformation, contrarian, confession…). |
| `copywriting-structures` | 8 frameworks (AIDA, PAS, BAB, FAB, Star-Story-Solution, APP, HSO, Storytelling) and a selection guide. |
| `content-types` | A catalog of 22 post types by objective. |
| `templates-by-category` | Ready templates for 7 categories, with placeholders and examples. |
| `ctas` | A bank of CTAs by objective (saves, leads, engagement, sales…). |
| `style-and-tone` | 360Brew formatting guide, authenticity and a voice checklist. |
| `humanizer-linkedin` | Pipeline that removes AI writing patterns — surgery, not demolition. |
| `post-publication-protocol` | The 90 critical minutes after publishing: signals, actions and mistakes that kill reach. |
| `visual-brief` | Visual brief for the post with technical specs and ready prompts for image generation. |
| `discovery-script` | The `init` interview script (internal use). |

The other 10 are **workflow skills** (added in v1.3.0). They carry their own steps and trigger when you ask in plain language, no slash command:

- **Strategy:** `niche-definer`, `audience-persona`, `content-pillars`, `content-calendar` — the first three write their result back into the authority profile after you confirm.
- **Production:** `repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`.
- **Audits:** `profile-optimizer`, `analytics-interpreter`.

### Agents (2)

- **`linkedin-strategist`** — content strategy and angle decisions.
- **`humanizer-linkedin`** — final pass that takes the AI signature out of the text.

### Scripts (3 CLIs + 1 shared library)

Python tools the commands call. Scoring and validation are **multilingual (PT + EN)**: matching runs against both languages by default, so the scorer works on Portuguese and English posts. Use `--lang pt|en` to force one language.

```bash
python scripts/score_post.py <post.txt> [--objective authority|sales|engagement] [--lang auto|pt|en]
python scripts/suggest_hooks.py --category <cat> --objective <obj> [--topic "..."]
python scripts/validate_specs.py <post.txt> [--lang auto|pt|en]
```

`postlib.py` is the shared library both `score_post.py` and `validate_specs.py` import — the single source of truth for the PT/EN matchers and the 360Brew specs.

### Hook

A `SessionStart` shows a banner pointing to `init` when no profile exists in the project yet.

---

## Repository structure

```
authority-engine/
├── linkedin-authority-engine/   # the plugin (product)
│   ├── .claude-plugin/          # plugin.json + marketplace.json
│   ├── commands/                # 6 commands
│   ├── skills/                  # 22 skills
│   ├── agents/                  # 2 agents
│   ├── scripts/                 # 3 CLI scripts + postlib.py (shared lib)
│   └── hooks/                   # SessionStart hook
│
├── tests/                       # pytest suite (plugin structure + scripts)
└── docs/                        # supporting documentation
```

---

## Tests

```bash
# from the repo root
pytest
```

The suite covers the plugin structure (`test_plugin_structure.py`, including the workflow skills and an anti-Taplio-coupling guard), the script behavior via CLI including PT/EN scoring (`test_scripts_cli.py`), and the shared matcher library (`test_postlib.py`).

---

## Roadmap

- [x] Multilingual scoring (PT + EN)
- [x] Workflow skills — strategy, production, profile & analytics (v1.3.0)
- [ ] Self-serve launch — first for the warm audience already waiting for the product
- [ ] Multi-language operation end-to-end, including generation and ES
- [ ] Publication on the public plugin marketplace

---

## License

Proprietary © LEVEL TECH. Contact: caner@thelevel.com.br
