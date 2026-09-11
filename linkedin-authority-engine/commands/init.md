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
3. **Discovery path.** Ask for the client's LinkedIn URL up front, plus up to 3 direct-competitor URLs and up to 3 positioning-reference URLs (§7 asks for exactly these, by name and URL). Then branch:
   - **Path U (deep discovery)** — a URL is available and Gate 0 passes (`python linkedin-authority-engine/scripts/unipile_discovery.py --dry-run --linkedin-url <url>` exits 0): load `linkedin-authority-engine:linkedin-deep-discovery`, run the fetches (client with `--role self`, each competitor/reference with `--role reference`, sequentially, max 6 reference profiles), then run the interview from the dossier.
   - **Path A (manual)** — no URL or no key (Gate 0 exits 2): load `linkedin-authority-engine:discovery-script` and conduct the guided in-session interview. Today's behaviour, unchanged. (Path B/transcript is future work.) Conduct it in the language chosen in step 1.
4. **Run the interview.** One question at a time or in short blocks. Do not close a section without covering its critical fields (`*`). Path U rule: for every field the dossier proposes, show the proposed value and ask for a correction, not an open question. Ask the full open question only for fields in the skill's "always ask" list, or where the dossier records a gap.
5. **Synthesize the profile.** Use the Skill tool to load `linkedin-authority-engine:authority-context` and fill `references/authority-context-template.md` with the answers. Keep the section labels in English; write the client's data in the chosen language. Flag gaps in `*` fields and follow up only on what is missing. Provenance rule: fields drafted from the dossier are marked in the confirmation summary so the user knows what they are approving. Prose fields pass the humanizer before being written.
6. **Write the files** at the project root:
   - `authority-context.md` (filled profile). Frontmatter must include `last_updated`, `version`, and `language` (the `pt`/`en` token from step 1):
     ```
     ---
     last_updated: <YYYY-MM-DD>
     version: 1.0
     language: pt
     ---
     ```
   - `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` (empty headers per the schemas; Path U seeds `memory/voice-profile.md` instead of leaving it empty — see the skill's Gate 1 seeding contract — and appends a dated entry to `memory/learnings.md`: `**<YYYY-MM-DD>:** authority-context seeded from Unipile deep discovery — <n> posts, <n> reference profiles; dossiers in outputs/discovery/`)
   - `outputs/posts/.gitkeep`
7. **Confirm** by showing a summary (core theme, 3 pillars, objective, mix) and instruct: "run `/linkedin-authority-engine:guided` for your first post." Present the confirmation in the chosen language.

## Voice

Setup/interaction: direct, no robotic assistant tone. No humanizer here (this is not external copy).
