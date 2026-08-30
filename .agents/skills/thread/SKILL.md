---
name: linkedin-authority-engine:thread
description: Thread Mode of the LinkedIn Authority Engine — builds a series of 3-7 posts on a topic, with a planned architecture (hook, authority, educational, story, conversion).
---

# /linkedin-authority-engine:thread

## Gate 2 — Read the substrate (required, automatic)

Before any generation:

1. Load the `linkedin-authority-engine:authority-context` skill.
2. Read `authority-context.md` (full profile) and every file in `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Apply: tone of voice, content pillars, real credentials, editorial constraints across every post in the series.
4. Prioritize winning patterns: approved hooks in `winning-hooks.md`, high-performing topics in `topic-performance.md`.
5. Ensure voice consistency and narrative progression across the posts.
6. **Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → generate every post and conduct the interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.

---

## THREAD STEP 1 — Define the series

If not provided via argument, collect:
- Central theme of the series
- Objective (Authority / Sales / Engagement)
- Desired number of posts (3-7)
- Intended cadence (e.g., daily, every other day, weekly)

---

## THREAD STEP 2 — Series architecture

Generate the post architecture adapted to the chosen number:

```
POST 1 — SERIES HOOK (Hook/Contrarian)
  → Introduces the theme, builds anticipation, promises value

POST 2 — AUTHORITY PROOF
  → Real credential + context that justifies the theme

POST 3 — EDUCATIONAL/HOW-TO
  → Actionable practical value, high Saves Potential

POST 4 — STORY/BEHIND THE SCENES
  → Emotional connection, real behind-the-scenes

POST 5 — CONVERSION/CTA
  → Close with an offer, lead magnet or next step
```

Adapt to the number of posts (e.g., for 3 posts, condense into Hook + Educational + Conversion).

Use real profile credentials to anchor each post to the person's positioning.

Present the architecture and wait for approval before generating.

---

## THREAD STEP 3 — Starting point

Ask: "Would you rather generate all the posts at once or one at a time (guided workflow)?"

- "All at once": generate the entire series sequentially.
- "One at a time": generate the first, wait for approval, then the next.

---

## THREAD STEP 4 — Generation + pipeline per post

For **each post** in the series:

1. Generate the post following the 360Brew specs (load `linkedin-authority-engine:360brew-algorithm`):
   - 1,250-2,500 characters
   - 14+ short paragraphs (max ~19 words each)
   - No links in the body, no generic hashtags
   - Re-hook mid-post
   - Use a hook suited to the post type (skill `linkedin-authority-engine:hooks`)
   - CTA aligned with the objective (skill `linkedin-authority-engine:ctas`)

2. Run the full **Finalization pipeline**:

   **Stage A — Technical validation**

   ```bash
   python /Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/validate_specs.py post.txt --lang <pt|en>
   ```

   Fix errors before advancing.

   **Stage B — Humanizer LinkedIn**

   Run the `linkedin-authority-engine:humanizer-linkedin` skill. Present a compact diff (max 5 items).

   **Stage C — Visual brief**

   Run the `linkedin-authority-engine:visual-brief` skill.

   **Stage D — Final score**

   ```bash
   python /Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>
   ```

   **Stage E — Post-publication protocol**

   Run the `linkedin-authority-engine:post-publication-protocol` skill. Generate the ready-to-paste first comment for each post.

3. Present the post in the format:

```
━━━━━━━━━━━━━━━━━━━━━━━
POST [N]/[TOTAL] — [Type]
━━━━━━━━━━━━━━━━━━━━━━━

[Humanized text]

Humanizer: [compact diff]
Score: X.X/10 | Top 1%: X% | Top 5%: X%
Visual brief: [format + concept + AI prompt]
━━━━━━━━━━━━━━━━━━━━━━━
```

---

## THREAD STEP 5 — Publishing calendar

After generating all the posts, present the suggested calendar:

| Post | Topic | Type | Score | Suggested date | Window (BRT) |
|------|-------|------|-------|----------------|--------------|

For recommended timing by objective and day of the week, see the `linkedin-authority-engine:post-publication-protocol` skill.

---

## Gate 3 — Write-back to the substrate

After approval of the series, following the instructions of the `linkedin-authority-engine:authority-context` skill:

1. Append to `memory/winning-hooks.md`: per approved hook in the series — date, hook pattern, type, category, objective, score. (Columns `times used`, `average performance`, `keep/kill` stay empty until v1.x.)
2. Append to `memory/topic-performance.md`: per post in the series — date, topic, pillar, post type, score. (Performance columns stay empty until v1.x.)
3. Append to `memory/learnings.md`: what worked in the architecture, what was adjusted, patterns identified.
4. If any post was rejected or rewritten, record the reason in `memory/learnings.md`.

---

## Save the final posts

Save each approved post to:

```
outputs/posts/<YYYYMMDD>-<post-slug>-v1.md
```

If a previous version of the same slug already exists, increment the number (v2, v3...).
