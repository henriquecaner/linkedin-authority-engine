---
name: guided
description: Guided Mode of the LinkedIn Authority Engine — builds a post from scratch with a full 7-step workflow (category, objective, agenda, structure, type, hook, body, CTA), reading the authority profile and running through the finalization pipeline. Use when the user wants to create a new post.
---

# Guided skill
## Gate 2 — Read the substrate (required, automatic)

Before any generation:

1. Load the `authority-context` skill.
2. Read `authority-context.md` (full profile) and every file in `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Apply: tone of voice, content pillars, real credentials, editorial constraints.
4. Prioritize winning patterns: approved hooks in `winning-hooks.md`, high-performing topics in `topic-performance.md`.
5. Validate internally on each generation: "Does this sound like how this client would talk?"
6. **Language.** Read the `language` field from the `authority-context.md` frontmatter and operate in it for the whole session: `language: pt` → generate every post and conduct the interaction in **Brazilian Portuguese (pt-BR)** ("você", never "tu"; Brazilian vocabulary, spelling, and idiom; never European Portuguese); `language: en` → English. Pass the token as `--lang <pt|en>` to **both** `validate_specs.py` and `score_post.py`. If the field is absent (older profile), omit `--lang` (scorer defaults to `auto`) and infer the language from the conversation.

---

## Pipeline: STEP 0 → 1.0 → 1.1 → [1.2] → 2 → 3 → 4 → 5 → 6 → Finalization pipeline

---

### STEP 0 — Context (automatic, silent)

Already done via Gate 2 above. Confirm internally: tone, pillars and constraints loaded.

---

### STEP 1.0 — Category

Ask which post category:

The `slug` column is the exact value to pass to `suggest_hooks.py --category`.

| Option | Slug (`--category`) | What it is |
|--------|--------------------|------------|
| Career lesson | `career_lesson` | Defining moment + takeaway |
| Achievement | `achievement` | Win with numbers |
| Failure | `failure` | Mistake + lesson (vulnerability) |
| Debunk | `debunk` | Break a market myth |
| Practical tip | `practical_tip` | Something actionable |
| Opinion | `opinion` | Bold stance |
| Behind the scenes | `behind_the_scenes` | Real day-to-day |
| Other | `other` | Free topic |

---

### STEP 1.1 — Objective

Ask: "What's the main objective? Authority, Sales or Engagement?"

---

### STEP 1.2 — Agenda suggestions

> Skip if the topic came as an argument in `the `guided` skill [topic]`.

Generate **4-5 agenda ideas** (short hook-style title + one angle sentence). If `topic-performance.md` has real performance data, prioritize proven topics and cite the figure (e.g., "your post about X got 6x your average"). The user picks 1.

---

### STEP 2 — Structure

Load the `copywriting-structures` skill and suggest **2-3 frameworks** suited to the category and objective.

Quick reference:

| Structure | Flow | Best for |
|-----------|------|----------|
| PAS | Problem → Agitation → Solution | Educational posts |
| AIDA | Attention → Interest → Desire → Action | Conversion |
| BAB | Before → After → Bridge | Transformation |
| HSO | Hook → Story → Offer | Narrative + offer |
| Storytelling | Setup → Conflict → Resolution → Lesson | Emotional connection |

Additional details (FAB, Star-Story-Solution, APP): load the `copywriting-structures` skill.

The user picks 1 framework.

---

### STEP 3 — Content type

Load the `content-types` skill and suggest **3 suitable types**. Most popular: Story, How-to, Before-After, Contrarian, Mistakes. Full list in the `content-types` skill.

The user picks 1 type.

---

### STEP 4 — Hooks

Optionally run `${PLUGIN_ROOT}/scripts/suggest_hooks.py` with the category, objective and topic:

```bash
python ${PLUGIN_ROOT}/scripts/suggest_hooks.py --category <category> --objective <objective> --topic "<topic>"
```

> Se os scripts não executarem (ChatGPT web, sem runtime local), aplique a checagem manual abaixo. Skip the script and build the 3 hooks directly from the `hooks` skill with the category, objective and topic.

Also load the `hooks` skill to enrich with patterns from the full bank.

Present **3 hooks**, prioritizing (in order): Proof of Work, Authority Proof, Transformation, Tension/Contrarian, Confession/Failure.

Use real credentials from the profile loaded in Gate 2. If `winning-hooks.md` has approved hooks for this profile, prioritize them.

The user picks 1 hook.

---

### STEP 5 — Body

Generate the body following the 360Brew specs (load `360brew-algorithm` for details):

- 1,250-2,500 characters
- 14+ short paragraphs (max ~19 words each)
- Simple words (avg word length ≤5 letters)
- Specific numbers
- **Re-hook mid-post**: one sentence of tension or a twist between the development and the conclusion, to hold dwell time (>15 sec unlocks distribution)
- **No links in the body, no generic hashtags**

Base structure:

```
HOOK (1-2 lines)
↓
CONTEXT (3-4 paragraphs)
↓
DEVELOPMENT (8-10 paragraphs)
↓
CONCLUSION (2-3 paragraphs)
↓
CTA (single — STEP 6)
```

Templates by category: load `templates-by-category`.

---

### STEP 6 — CTA

Load the `ctas` skill and generate **3 options** aligned with the chosen objective.

**2026 priority:** Saves (5x likes) › Long comments (2x) › Follow › Leads.

| Objective | Priority CTA |
|-----------|--------------|
| Saves/Reference | "Save this post for when you need it" |
| Authority | "Follow me for more on [niche]" |
| Sales | "Comment [WORD] and I'll DM you" |
| Engagement | "Disagree with any point? Tell me which and why" |

> Rule: whenever the post has a framework, checklist or guide, the save CTA is the default.

The user picks **1 CTA**. Post assembled (hook + body + CTA) → run the **Finalization pipeline** below.

---

## Finalization pipeline

> Run in this exact order, without skipping steps.

**Input:** complete post (hook + body + CTA).

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


If it returns errors (link in body, too many hashtags, complex words, dense paragraphs): **fix before continuing**. Do not advance to Stage B with a technical error.

### Stage B — Humanizer LinkedIn

Run the `humanizer-linkedin` skill on the complete post. Present a compact diff (max 5 changed items).

### Stage C — Visual brief

Run the `visual-brief` skill on the humanized post. Automatically generate the brief with recommended format, visual concept and AI prompt.

### Stage D — Final score

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


Present the report across the 6 dimensions (Saves Potential 30%, Hook 20%, Algorithm 20%, Structure 15%, CTA 10%, Data 5%) + Top 1% / Top 5% classification.

If `topic-performance.md` has a real baseline for the profile, also present the comparison (relative context > absolute).

Rule: Score ≥ 9/10 to publish. Below that, point to a specific adjustment.

### Stage E — Post-publication protocol

Run the `post-publication-protocol` skill.

1. Generate the **ready-to-paste first comment** to drop in right after publishing: link (if any) + extra context + 1 question that invites 3+ sentence replies.
2. Deliver the summary of the critical 90 minutes.

---

## Gate 3 — Write-back to the substrate

After final approval of the post, following the instructions of the `authority-context` skill:

1. Append to `memory/winning-hooks.md`: date, hook pattern (if approved), type, category, objective, score obtained. (Columns `times used`, `average performance`, `keep/kill` stay empty until v1.x.)
2. Append to `memory/topic-performance.md`: date, topic, pillar, post type, score. (Performance columns stay empty until v1.x.)
3. Append to `memory/learnings.md`: what worked, what was adjusted, constraints applied.
4. If the user rejected a version, record the reason for rejection in `memory/learnings.md`.

---

## Save the final post

Save the final post (humanized version + chosen CTA) to:

```
outputs/posts/<YYYYMMDD>-<slug>-v1.md
```

If a previous version of the same slug already exists, increment the number (v2, v3...).

---

## Strategist core (generation discipline)

Apply on every generation in this skill: you have command of the 360Brew algorithm (2026) and write B2B authority posts. Before generating: read `authority-context.md` + `memory/`. Apply the text specs, the engagement weights (save 5x, long comment 2x), zero links in the body, zero generic hashtags. Prioritize Saves Potential. Always respect the profile's constraints and its NOT territories. Load the `360brew-algorithm`, `hooks` and `copywriting-structures` skills when you need them.
