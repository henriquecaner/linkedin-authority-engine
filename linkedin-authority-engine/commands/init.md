---
description: Client onboarding. Runs the discovery interview (Path A) and creates authority-context.md in the project folder, plus memory/ and outputs/posts/. Auto-suggested when other commands run without a profile. Supports --refresh to update an existing profile.
argument-hint: "[--refresh]"
---

# /linkedin-authority-engine:init

Creates the living client profile — it replaces the manual setup of "Claude project + instructions."

## Steps

1. **Check existing context.** If `authority-context.md` already exists at the root: without `--refresh`, ask whether to review/update it; with `--refresh`, update stale fields while preserving the rest.
2. **Load the script.** Use the Skill tool to load `linkedin-authority-engine:discovery-script`. (Path A — guided in-session interview. Path B/transcript is future work.)
3. **Run the interview.** One question at a time or in short blocks. Do not close a section without covering its critical fields (`*`).
4. **Synthesize the profile.** Use the Skill tool to load `linkedin-authority-engine:authority-context` and fill `references/authority-context-template.md` with the answers. Flag gaps in `*` fields and follow up only on what is missing.
5. **Write the files** at the project root:
   - `authority-context.md` (filled profile, with `last_updated` and `version` frontmatter)
   - `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` (empty headers per the schemas)
   - `outputs/posts/.gitkeep`
6. **Confirm** by showing a summary (core theme, 3 pillars, objective, mix) and instruct: "run `/linkedin-authority-engine:guided` for your first post."

## Voice

Setup/interaction: direct, no robotic assistant tone. No humanizer here (this is not external copy).
