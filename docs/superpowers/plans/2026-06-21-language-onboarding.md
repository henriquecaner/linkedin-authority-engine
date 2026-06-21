# Persistent Language Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `/init`'s first question a language choice (Brazilian Portuguese / English) that persists in `authority-context.md` and drives generation, interaction, and scoring across all flows forever.

**Architecture:** Pure markdown-playbook change. `/init` gains a step 0 (language question) and writes `language: pt|en` to the profile frontmatter. The `authority-context` read protocol and the four flow commands gain a Gate 2 instruction to read that field, operate in-language, and pass `--lang <pt|en>` to the two Python scripts (which already accept it). No Python changes.

**Tech Stack:** Markdown commands + skills (read by Claude at runtime); the `pytest tests/test_plugin_structure.py` structural gate.

## Global Constraints

- **Stored token is `pt` or `en`** (verbatim scorer vocabulary). Never store `pt-BR`/`Portuguese`. No `pt-BR → pt` mapping anywhere.
- **`language: pt` always means Brazilian Portuguese (pt-BR).** Every in-language instruction must say **"Brazilian Portuguese (pt-BR)"** explicitly — "você" (never "tu"), Brazilian vocabulary/spelling/idiom — never bare "Portuguese" and never European Portuguese.
- **Fallback:** a profile with no `language` field → omit `--lang` (scorer defaults to `auto`) and infer language from the conversation. No pre-existing consumer breaks.
- **Both scripts get `--lang`:** `validate_specs.py` AND `score_post.py`. Not just the scorer.
- **No translation of skill/command files** (they are internal English instructions); only *output* is in-language. **No Python changes. No new unit tests** for playbook behavior.
- Plugin version stays `1.1.0`. `test_plugin_structure` asserts command frontmatter (`description` + `argument-hint`) and skill frontmatter (`description`) + body > 200 chars — preserve all frontmatter.
- Languages offered: Brazilian Portuguese (pt-BR) and English only.

---

## Task 1: Onboarding — capture and persist the language

**Files:**
- Modify: `linkedin-authority-engine/commands/init.md`
- Modify: `linkedin-authority-engine/skills/discovery-script/SKILL.md`
- Modify: `linkedin-authority-engine/skills/authority-context/SKILL.md`
- Modify: `linkedin-authority-engine/skills/authority-context/references/authority-context-template.md`
- Test: `tests/test_plugin_structure.py` (existing — must stay green)

**Interfaces:**
- Produces: the `language: pt|en` frontmatter key in the generated `authority-context.md`, consumed by Task 2's flows.

- [ ] **Step 1: Rewrite the `## Steps` section of `init.md` to add the language question (step 1) and write the field (step 6)**

In `linkedin-authority-engine/commands/init.md`, replace the entire `## Steps` block (currently steps 1–6) with:

```markdown
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
```

- [ ] **Step 2: Add the in-language note to `discovery-script/SKILL.md`**

In `linkedin-authority-engine/skills/discovery-script/SKILL.md`, immediately after the line `Ask one question at a time (or in short blocks). Do not move past a section until the \`*\` fields are covered.`, add a new paragraph:

```markdown
Conduct the interview in the language chosen in step 1 of `init` (the `language` token). When it is `pt`, ask every question in **Brazilian Portuguese (pt-BR)** — "você", Brazilian vocabulary and spelling, never European Portuguese. The question wording below is the English reference; translate it to the chosen language as you go.
```

- [ ] **Step 3: Add the `language` field + read rule to `authority-context/SKILL.md`**

In `linkedin-authority-engine/skills/authority-context/SKILL.md`:

(a) In the `## Files` section, change the `authority-context.md` bullet to note the frontmatter:

```markdown
- `authority-context.md` — living profile (13 sections) with a frontmatter that includes `last_updated`, `version`, and `language` (`pt` = Brazilian Portuguese / pt-BR, or `en`). Template in `references/authority-context-template.md`.
```

(b) In `## Gate 2 — Read (generation)`, append to the end of that section's paragraph:

```markdown
 Also read the `language` frontmatter field and operate in it: `pt` → generate and interact in **Brazilian Portuguese (pt-BR)** ("você", Brazilian vocabulary/spelling, never European Portuguese); `en` → English; and pass it as `--lang <pt|en>` to `validate_specs.py` and `score_post.py`. If the field is absent, omit `--lang` and infer the language from the conversation.
```

- [ ] **Step 4: Document the `language` field in the template**

In `linkedin-authority-engine/skills/authority-context/references/authority-context-template.md`, immediately after the `> **Primary skill:** ...` line near the top, add:

```markdown
>
> **Frontmatter:** when generated, this file carries a YAML frontmatter with `last_updated`, `version`, and `language` (`pt` = Brazilian Portuguese / pt-BR, or `en`). Section labels stay in English; the client's data is written in the chosen language.
```

- [ ] **Step 5: Verify structure is intact**

Run: `.venv/bin/python -m pytest tests/test_plugin_structure.py -q`
Expected: PASS (init/discovery-script/authority-context frontmatter + bodies intact).

- [ ] **Step 6: Commit**

```bash
git add linkedin-authority-engine/commands/init.md linkedin-authority-engine/skills/discovery-script/SKILL.md linkedin-authority-engine/skills/authority-context/SKILL.md linkedin-authority-engine/skills/authority-context/references/authority-context-template.md
git commit -m "$(printf 'feat(init): language choice (pt-BR/en) as first onboarding question, persisted to profile\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 2: Propagation — flows read the field and pass `--lang`

**Files:**
- Modify: `linkedin-authority-engine/commands/guided.md`
- Modify: `linkedin-authority-engine/commands/rewrite.md`
- Modify: `linkedin-authority-engine/commands/thread.md`
- Modify: `linkedin-authority-engine/commands/score.md`
- Modify: `linkedin-authority-engine/commands/linkedin.md`
- Test: `tests/test_plugin_structure.py` (existing)

**Interfaces:**
- Consumes: the `language: pt|en` frontmatter key written by Task 1.

The canonical Gate 2 language item (referred to below as **[LANG-ITEM]**) is:

```markdown
**Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → generate every post and conduct the interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.
```

- [ ] **Step 1: Add [LANG-ITEM] to `guided.md` Gate 2**

In `linkedin-authority-engine/commands/guided.md`, the Gate 2 list ends at item `5. Validate internally on each generation: ...`. Add a new item `6.` with the [LANG-ITEM] text above.

- [ ] **Step 2: Add `--lang` to `guided.md` script calls**

In `guided.md`, update the two command blocks:
- Stage A: `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt` → `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt --lang <pt|en>`
- Stage D: `python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objective <authority|sales|engagement>` → `python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>`

- [ ] **Step 3: Add [LANG-ITEM] to `rewrite.md` Gate 2 and `--lang` to its calls**

In `linkedin-authority-engine/commands/rewrite.md`:
- Gate 2 list ends at item `5. Validate on each generated version: ...`. Add item `6.` with [LANG-ITEM].
- Stage C command block: `python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objective <authority|sales|engagement>` → add `--lang <pt|en>` before `--objective`.
- The two inline `validate_specs.py` mentions (REWRITE STEP 1 and Stage A) have no literal `post.txt` to edit; the Gate 2 [LANG-ITEM] ("pass `--lang` to both") governs them — no per-mention edit needed.

- [ ] **Step 4: Add [LANG-ITEM] to `thread.md` Gate 2 and `--lang` to its calls**

In `linkedin-authority-engine/commands/thread.md`:
- Gate 2 list ends at item `5. Ensure voice consistency and narrative progression across the posts.`. Add item `6.` with [LANG-ITEM].
- Stage A block: `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt` → add `--lang <pt|en>`.
- Stage D block: `python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objective <authority|sales|engagement>` → add `--lang <pt|en>` before `--objective`.

- [ ] **Step 5: Add [LANG-ITEM] to `score.md` Gate 2 and `--lang` to its calls**

In `linkedin-authority-engine/commands/score.md`:
- Gate 2 list ends at item `4. If \`topic-performance.md\` has a real baseline ...`. Add item `5.` with [LANG-ITEM].
- Stage A block: `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt` → add `--lang <pt|en>`.
- Stage C block: `python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objective <authority|sales|engagement>` → add `--lang <pt|en>` before `--objective`.

- [ ] **Step 6: Make `linkedin.md` render in-language when a profile exists**

In `linkedin-authority-engine/commands/linkedin.md`, in the `## Profile check (required before any mode)` section, after the bullet that begins `- If it **exists**: continue with the routing below.`, add:

```markdown

When the profile exists, read its `language` frontmatter field and render the menu and all prompts in that language (`pt` → Brazilian Portuguese / pt-BR, `en` → English). When no profile exists yet, the "No profile found" message stays in English — the language has not been chosen yet.
```

- [ ] **Step 7: Verify structure is intact**

Run: `.venv/bin/python -m pytest tests/test_plugin_structure.py -q`
Expected: PASS (all five commands keep `description` + `argument-hint` frontmatter).

- [ ] **Step 8: Verify every flow got both the Gate 2 item and `--lang`**

Run:
```bash
grep -L "language" linkedin-authority-engine/commands/{guided,rewrite,thread,score,linkedin}.md
```
Expected: no output (every flow mentions `language`).

```bash
grep -c -- "--lang <pt|en>" linkedin-authority-engine/commands/guided.md linkedin-authority-engine/commands/score.md linkedin-authority-engine/commands/thread.md
```
Expected: `guided` ≥ 2, `score` ≥ 2, `thread` ≥ 2 (each has a validate + a score call).

- [ ] **Step 9: Commit**

```bash
git add linkedin-authority-engine/commands/guided.md linkedin-authority-engine/commands/rewrite.md linkedin-authority-engine/commands/thread.md linkedin-authority-engine/commands/score.md linkedin-authority-engine/commands/linkedin.md
git commit -m "$(printf 'feat(flows): read profile language, generate in-language, pass --lang to scorer/validator\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Manual verification (after both tasks)

Not automatable here (playbook behavior). Note in the PR for the user to run:
1. `/linkedin-authority-engine:init` → choose `1) Português (Brasil)` → confirm `authority-context.md` frontmatter has `language: pt` and the interview ran in pt-BR ("você", Brazilian register).
2. `/linkedin-authority-engine:guided` on that profile → the post and interaction are in pt-BR and the scorer is invoked with `--lang pt`.
3. A profile with no `language` field → flows still work, `--lang` omitted (no regression).

---

## Self-Review

**Spec coverage:**
- Languages PT-BR + EN, pt-BR register explicit → Global Constraints + [LANG-ITEM] + init step 1. ✅
- Stored token `pt`/`en`, no mapping → Global Constraints + init step 6 frontmatter. ✅
- First question in `/init` + interview in-language → Task 1 steps 1-2. ✅
- EN labels / in-language data → init step 5 + template step 4. ✅
- Persistence in frontmatter (sole write site = init) → Task 1 step 1 (step 6 block). ✅
- Propagation to guided/rewrite/thread/score + linkedin.md, both scripts get `--lang` → Task 2 steps 1-6. ✅
- Fallback for fieldless profiles → Global Constraints + [LANG-ITEM]. ✅
- `--refresh` may change language → init step 1. ✅
- No Python changes, no new unit tests, version unchanged → Global Constraints; test gate is test_plugin_structure + manual walkthrough. ✅

**Placeholder scan:** No TBD/TODO; every edit shows the exact text to insert and its anchor. The `<pt|en>` literal is intentional (it mirrors the existing `<authority|sales|engagement>` placeholder convention already in these command files — Claude substitutes at runtime). ✅

**Consistency:** [LANG-ITEM] text is identical across the four flows; the stored token (`pt`/`en`) matches the `--lang` argument and the scorer's vocabulary; "Brazilian Portuguese (pt-BR)" wording is uniform. ✅
