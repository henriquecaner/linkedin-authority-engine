---
name: linkedin-authority-engine:rewrite
description: Rewrite Mode of the LinkedIn Authority Engine — optimizes an existing post into two versions (conservative and bold), with a 360Brew diagnosis, humanizer and comparative score.
---

# /linkedin-authority-engine:rewrite

## Gate 2 — Read the substrate (required, automatic)

Before any analysis or generation:

1. Load the `linkedin-authority-engine:authority-context` skill.
2. Read `authority-context.md` (full profile) and every file in `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Apply: tone of voice, content pillars, real credentials, editorial constraints.
4. Prioritize winning patterns from `winning-hooks.md` and `topic-performance.md`.
5. Validate on each generated version: "Does this sound like how this client would talk?"
6. **Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → generate every post and conduct the interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.

If no post is provided as an argument, ask: "Paste the post you want to optimize."

---

## REWRITE STEP 1 — Diagnosis

Run `/Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/validate_specs.py` on the original post and analyze it against the 360Brew specs (load `linkedin-authority-engine:360brew-algorithm` for the full reference).

Present the diagnosis:

```
DIAGNOSIS:
Estimated score: X/10
🚨 Critical problems: [e.g., link in body, too many hashtags]
⚠️  Important: [e.g., weak hook, generic CTA]
✅ What works: [the post's strong points]
```

---

## REWRITE STEP 2 — Focus

Ask: "Main focus of the rewrite? (a) Hook, (b) Reach/specs, (c) CTA, (d) Everything"

Wait for the answer before generating the versions.

---

## REWRITE STEP 3 — Generate 2 versions

Based on the diagnosis and the chosen focus, generate:

- **Version A (Conservative):** Keeps the original voice and structure, fixes only the technical problems identified. Uses the credentials and tone from the profile loaded in Gate 2.
- **Version B (Bold):** Stronger hook (use the `linkedin-authority-engine:hooks` skill), restructures for maximum impact (use `linkedin-authority-engine:copywriting-structures`), maximizes Saves Potential.

For the CTAs of both versions, use the `linkedin-authority-engine:ctas` skill, aligning to the post's objective.

---

## REWRITE STEP 4 — Finalization pipeline on both + comparison

> Correct order: humanize first, then show the comparative score. Otherwise the user chooses based on a score that will change.

### Stage A — Technical validation

Run `/Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/validate_specs.py` on each version. Fix errors before advancing.

### Stage B — Humanizer LinkedIn

Run the `linkedin-authority-engine:humanizer-linkedin` skill on each version (A and B). Present a compact diff per version (max 5 items).

### Stage C — Final score

Run `/Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/score_post.py` on each humanized version:

```bash
python /Users/henriquecaner/Documents/GitHub/linkedin-content-caner/.agents/scripts/score_post.py post.txt --lang <pt|en> --objective <authority|sales|engagement>
```

Present the final comparison:

| Metric | Original | Version A (humanized) | Version B (humanized) |
|--------|----------|------------------------|------------------------|
| Score | X/10 | X/10 | X/10 |
| Saves Potential | X/10 | X/10 | X/10 |
| Hook | X/10 | X/10 | X/10 |
| Algorithm | X/10 | X/10 | X/10 |

The user picks the preferred version (or asks for a mix). With the chosen version:

### Stage D — Visual brief

Run the `linkedin-authority-engine:visual-brief` skill on the chosen version.

### Stage E — Post-publication protocol

Run the `linkedin-authority-engine:post-publication-protocol` skill.

1. Generate the **ready-to-paste first comment** to drop in right after publishing: link (if any) + extra context + 1 question that invites 3+ sentence replies.
2. Deliver the summary of the critical 90 minutes.

---

## Gate 3 — Write-back to the substrate

After approval of the final version, following the instructions of the `linkedin-authority-engine:authority-context` skill:

1. Append to `memory/winning-hooks.md`: date, hook pattern of the chosen version (if the hook improved), type, category, objective, final score. (Columns `times used`, `average performance`, `keep/kill` stay empty until v1.x.)
2. Append to `memory/topic-performance.md`: date, topic, pillar, post type, score. (Performance columns stay empty until v1.x.)
3. Append to `memory/learnings.md`: what was changed in the rewrite, which version was chosen and why, constraints applied.
4. If the user rejected one of the versions, record the reason in `memory/learnings.md`.

---

## Save the final post

Save the final post (chosen, humanized version) to:

```
outputs/posts/<YYYYMMDD>-<slug>-v1.md
```

If a previous version of the same slug already exists, increment the number (v2, v3...).
