---
description: Score Mode of the LinkedIn Authority Engine — evaluates and humanizes a finished post, running technical validation, humanizer and a score across the 6 dimensions with a final verdict (publish / adjust / rework). Use when the user has a finished post and wants to know if it's ready to publish.
argument-hint: "[post to evaluate]"
---

# /linkedin-authority-engine:score

## Gate 2 — Read the substrate (required, automatic)

Before evaluating:

1. Load the `linkedin-authority-engine:authority-context` skill.
2. Read `authority-context.md` (full profile) and every file in `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Apply: tone of voice, content pillars, real credentials, editorial constraints as additional evaluation criteria.
4. If `topic-performance.md` has a real baseline for the profile, use it for relative comparison in the score.
5. **Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → conduct the evaluation and interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.

If no post is provided as an argument, ask: "Paste the post you want to evaluate."

---

## Partial pipeline (SCORE MODE)

> Skips generation and the visual brief, goes straight to evaluation. No post-publication protocol (unless explicitly requested).

### Stage A — Technical validation

Run `${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py` on the post:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt --lang <pt|en>
```

Present the result:

```
TECHNICAL VALIDATION:
🚨 Critical errors: [link in body, too many hashtags, ...]
⚠️  Warnings: [dense paragraphs, complex words, ...]
✅ Specs OK: [what's within the parameters]
```

If there are critical errors, ask whether the user wants to fix them before humanizing. If yes, fix; if no, continue and record the errors in the final score.

### Stage B — Humanizer LinkedIn

Run the `linkedin-authority-engine:humanizer-linkedin` skill on the post. Present a compact diff (max 5 changed items) with the substitutions made.

### Stage C — Final score

Run `${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py` on the humanized post:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>
```

If the objective was not provided, infer it from the post content or ask.

Present the report across the 6 dimensions:

| Dimension | Weight | Score | Note |
|-----------|--------|-------|------|
| Saves Potential | 30% | X/10 | ... |
| Hook | 20% | X/10 | ... |
| Algorithm | 20% | X/10 | ... |
| Structure | 15% | X/10 | ... |
| CTA | 10% | X/10 | ... |
| Data | 5% | X/10 | ... |
| **Total** | 100% | **X.X/10** | |

If `topic-performance.md` has a real baseline, present the comparison: "Average for this profile: X.X/10 — this post is X% above/below."

### Final verdict

Based on the score:

- **Score ≥ 9/10:** "Publish. Post ready."
- **Score 7-8.9/10:** "Adjust. [Point out 1-2 specific improvements with the highest impact on the score.]"
- **Score < 7/10:** "Rework. [Point out the critical problems and suggest using Rewrite Mode (`/linkedin-authority-engine:rewrite`).]"

---

## Gate 3 — Write-back to the substrate

After the evaluation, following the instructions of the `linkedin-authority-engine:authority-context` skill:

1. Append to `memory/topic-performance.md`: date, topic, pillar, post type, score. (Performance columns stay empty until v1.x.)
2. Append to `memory/learnings.md`: the main findings of the evaluation, errors found, patterns that hurt the score.
3. If the hook is strong (Hook dimension score ≥ 8/10), append to `memory/winning-hooks.md`: date, hook pattern, type, category, objective, score. (Columns `times used`, `average performance`, `keep/kill` stay empty until v1.x.)

---

## Save the evaluated post

Save the post in its humanized version (post-Stage B) to:

```
outputs/posts/<YYYYMMDD>-<slug>-v1.md
```

If a previous version of the same slug already exists, increment the number (v2, v3...).
