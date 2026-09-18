# Platform ports — LinkedIn Authority Engine

One directory per platform. Copies, not a single portable source: each host has
its own manifest rules, command equivalents and script story, and a shared file
would drift against all of them at once. The Claude source stays canonical for
behavior; each port is locked to it by `tests/test_chatgpt_structure.py`
(version + skill count + no Claude-isms — extend the same guard per port).

| Platform | Directory | Manifest | Command equivalents | Scripts | Status |
|---|---|---|---|---|---|
| ChatGPT (desktop + web) | `plugins/chatgpt/linkedin-authority-engine` | `plugin.json` (`$schema` agent-plugins.org, `extensions.com.openai`) | 6 commands → 6 skills (`init`, `linkedin`, `guided`, `rewrite`, `thread`, `score`); agents folded in (`linkedin-strategist` core into `guided` + `thread`) | stdlib-only `.py`, byte-identical to source; `${PLUGIN_ROOT}`; manual checklist fallback when no local runtime | shipped 1.5.0 |
| OMP / PI | `plugins/omp-pi/linkedin-authority-engine` | TBD | TBD | TBD | planned |
| Grok | `plugins/grok/linkedin-authority-engine` | TBD | TBD | TBD | planned |
| Cursor | `plugins/cursor/linkedin-authority-engine` | TBD | TBD | TBD | planned |
| Gemini | `plugins/gemini/linkedin-authority-engine` | TBD | TBD | TBD | planned |

Repo marketplace for the desktop app: `.agents/plugins/marketplace.json`
(entry `linkedin-authority-engine` → `./plugins/chatgpt/linkedin-authority-engine`).
