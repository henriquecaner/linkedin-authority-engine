# LinkedIn Authority Engine

Plugin for **Claude Code** and **Claude Cowork** that turns a founder's expertise into authority on LinkedIn. Posts tuned for the 360Brew algorithm, with a living client profile (`authority-context.md`) and local memory that learns every session.

By [LEVEL TECH](https://thelevel.com.br) · [thelevr.com](https://thelevr.com)

## Installation

```bash
# add the marketplace (local path or repository)
/plugin marketplace add /path/to/linkedin-authority-engine

# install the plugin
/plugin install linkedin-authority-engine

# create the client profile
/linkedin-authority-engine:init
```

After `init`, use `/linkedin-authority-engine:linkedin` for the mode menu.

## Commands

| Command | What it does |
|---|---|
| `init` | Onboarding. Runs the discovery interview and creates `authority-context.md`, `memory/` and `outputs/posts/`. Accepts `--refresh`. |
| `linkedin` | Central menu. Routes to the chosen mode. |
| `guided` | Creates a post from scratch in 7 steps (category → objective → angle → structure → type → hook → body → CTA). |
| `rewrite` | Optimizes a post into two versions (conservative and bold), with a 360Brew diagnosis, humanizer and score. |
| `thread` | A series of 3-7 posts on a topic, with a planned architecture. |
| `score` | Evaluates and humanizes a finished post: technical validation, humanizer and a grade across the 6 dimensions. |

## How it works

The plugin reads your authority profile, drafts the post in the right framework, strips out AI writing patterns, and grades it before you publish. Then it hands you the 90-minute post-publication protocol. Every post that lands feeds the local memory, so the next one starts closer to your voice.

- **23 skills** — a knowledge base the commands load on demand (360Brew algorithm reference, a bank of 147 hooks, 8 copywriting structures, 22 content types, templates by category, CTAs, style and tone, humanizer, post-publication protocol, visual brief, memory substrate, discovery script), plus 11 workflow skills you trigger by asking in plain language: `niche-definer`, `audience-persona`, `content-pillars`, `content-calendar`, `repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`, `profile-optimizer`, `analytics-interpreter`, `linkedin-deep-discovery` (Unipile-backed profile + post-corpus fetch for onboarding).
- **2 agents** — `linkedin-strategist` (strategy) and `humanizer-linkedin` (final anti-AI pass).
- **4 CLI scripts + shared lib** — `score_post.py`, `suggest_hooks.py`, `validate_specs.py`, `unipile_discovery.py` (LinkedIn profile + posts + company fetch via Unipile API v2; needs `UNIPILE_API_KEY` and a connected `UNIPILE_LINKEDIN_ACCOUNT_ID`), plus `postlib.py` (the shared, multilingual PT+EN matcher library and 360Brew specs). Scoring and validation accept `--lang auto|pt|en`.
- **1 hook** — a `SessionStart` banner pointing to `init`.

## Beyond the post

The four commands above write and grade a post. Ten skills cover the work around it. You invoke them by asking in plain language, no slash command needed.

**Strategy** — define your niche, build an audience persona, set your content pillars, plan four weeks of posts. The first three write their result back into your authority profile after you confirm the change.

**Production** — repurpose a blog, video, or tweet into a native post; pull a story out of a raw experience; fix a weak CTA; turn a framework into a carousel script.

**Audits** — audit your LinkedIn profile copy, or paste your analytics and get three moves for next month.

## Structure

```
linkedin-authority-engine/
├── .claude-plugin/   # plugin.json + marketplace.json
├── commands/         # 6 commands
├── skills/           # 23 skills
├── agents/           # 2 agents
├── scripts/          # 4 CLI scripts + postlib.py (shared lib)
└── hooks/            # SessionStart hook
```

The full repository overview (including the go-to-market layer) is in the [root README](../README.md).

## License

Proprietary © LEVEL TECH. Contact: caner@thelevel.com.br
