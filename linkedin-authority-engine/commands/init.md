---
description: Client onboarding. Runs the discovery interview (Path A) and creates authority-context.md in the project folder, plus memory/ and outputs/posts/. Auto-suggested when other commands run without a profile. Supports --refresh to update an existing profile.
argument-hint: "[--refresh]"
---

# /linkedin-authority-engine:init

Creates the living client profile — it replaces the manual setup of "Claude project + instructions."

## Steps

1. **Choose the language (ask this first).** Before anything else, ask:

   ```
   Before we start — which language should this engine work in?
     1) Português (Brasil)
     2) English
   ```

   Map the answer to a token: option 1 → `pt`, option 2 → `en`. This token is written to the profile in step 6. **`pt` means Brazilian Portuguese (pt-BR)** — conduct the rest of the interview and all future output in that register ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese). With `--refresh`, ask again and overwrite the existing `language` field if it changed.
2. **Check existing context.** If `authority-context.md` already exists at the root: without `--refresh`, ask whether to review/update it; with `--refresh`, update stale fields while preserving the rest.
3. **Load the script.** Use the Skill tool to load `linkedin-authority-engine:discovery-script`. (Path A — guided in-session interview. Path B/transcript is future work.) Conduct it in the language chosen in step 1.
4. **Run the interview.** One question at a time or in short blocks. Do not close a section without covering its critical fields (`*`).
5. **Synthesize the profile.** Use the Skill tool to load `linkedin-authority-engine:authority-context` and fill `references/authority-context-template.md` with the answers. Keep the section labels in English; write the client's data in the chosen language. Flag gaps in `*` fields and follow up only on what is missing.
6. **Write the files** at the project root:
   - `authority-context.md` (filled profile). Frontmatter must include `last_updated`, `version`, and `language` (the `pt`/`en` token from step 1):
     ```
     ---
     last_updated: <YYYY-MM-DD>
     version: 1.0
     language: pt
     ---
     ```
   - `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` (empty headers per the schemas)
   - `outputs/posts/.gitkeep`
7. **Confirm** by showing a summary (core theme, 3 pillars, objective, mix) and instruct: "run `/linkedin-authority-engine:guided` for your first post." Present the confirmation in the chosen language.

## Voice

Setup/interaction: direct, no robotic assistant tone. No humanizer here (this is not external copy).
