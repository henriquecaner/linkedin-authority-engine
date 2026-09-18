---
name: score
description: Score Mode of the LinkedIn Authority Engine — evaluates and humanizes a finished post, running technical validation, humanizer and a score across the 6 dimensions with a final verdict (publish / adjust / rework). Use when the user has a finished post and wants to know if it's ready to publish.
---

# Score skill
## Gate 2 — Read the substrate (required, automatic)

Before evaluating:

1. Load the `authority-context` skill.
2. Read `authority-context.md` (full profile) and every file in `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Apply: tone of voice, content pillars, real credentials, editorial constraints as additional evaluation criteria.
4. If `topic-performance.md` has a real baseline for the profile, use it for relative comparison in the score.
5. **Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → conduct the evaluation and interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.

If no post is provided as an argument, ask: "Paste the post you want to evaluate."

---

## Partial pipeline (SCORE MODE)

> Skips generation and the visual brief, goes straight to evaluation. No post-publication protocol (unless explicitly requested).

### Stage A — Technical validation

Run `${PLUGIN_ROOT}/scripts/validate_specs.py` on the post:

```bash
python ${PLUGIN_ROOT}/scripts/validate_specs.py post.txt --lang <pt|en>
```

> Se os scripts não executarem (ChatGPT web, sem runtime local), aplique a checagem manual abaixo.
>
> **Manual checklist — no-runtime fallback** (same numbers as `postlib.py`):
> - Length: 1250–2500 characters (warning zone 1000–3000).
> - Paragraphs: at least 14 (warning at 10); paragraphs are blocks split by a blank line.
> - Average word length: at most 5 letters (warning at 6).
> - At most 19 words per paragraph; a paragraph with 150 or more characters is dense — split it.
> - At most 2 hashtags; zero links in the body (links go in the first comment).
> - Score across 6 dimensions with these weights: Saves Potential 30%, Hook 20%, Algorithm 20%, Structure 15%, CTA 10%, Data 5%.
> - Verdict bands: score ≥9 publish, 7–8.9 adjust, score <7 rework.


Present the result:

```
TECHNICAL VALIDATION:
🚨 Critical errors: [link in body, too many hashtags, ...]
⚠️  Warnings: [dense paragraphs, complex words, ...]
✅ Specs OK: [what's within the parameters]
```

If there are critical errors, ask whether the user wants to fix them before humanizing. If yes, fix; if no, continue and record the errors in the final score.

### Stage B — Humanizer LinkedIn

Run the `humanizer-linkedin` skill on the post. Present a compact diff (max 5 changed items) with the substitutions made.

### Stage C — Final score

Run `${PLUGIN_ROOT}/scripts/score_post.py` on the humanized post:

```bash
python ${PLUGIN_ROOT}/scripts/score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>
```

> Se os scripts não executarem (ChatGPT web, sem runtime local), aplique a checagem manual abaixo.
>
> **Manual checklist — no-runtime fallback** (same numbers as `postlib.py`):
> - Length: 1250–2500 characters (warning zone 1000–3000).
> - Paragraphs: at least 14 (warning at 10); paragraphs are blocks split by a blank line.
> - Average word length: at most 5 letters (warning at 6).
> - At most 19 words per paragraph; a paragraph with 150 or more characters is dense — split it.
> - At most 2 hashtags; zero links in the body (links go in the first comment).
> - Score across 6 dimensions with these weights: Saves Potential 30%, Hook 20%, Algorithm 20%, Structure 15%, CTA 10%, Data 5%.
> - Verdict bands: score ≥9 publish, 7–8.9 adjust, score <7 rework.


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
- **Score < 7/10:** "Rework. [Point out the critical problems and suggest using Rewrite Mode (the `rewrite` skill).]"

---

## Gate 3 — Write-back to the substrate

After the evaluation, following the instructions of the `authority-context` skill:

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
