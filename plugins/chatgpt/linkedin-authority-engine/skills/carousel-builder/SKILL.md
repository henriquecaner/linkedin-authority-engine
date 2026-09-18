---
name: carousel-builder
description: Turn a topic, framework, or long-form idea into a LinkedIn carousel script — cover slide + value slides + closing CTA slide, one idea per slide, plus the post caption. Use when the user wants a carousel/document post or has a framework that earns the swipe. Humanizes the copy and hands off to the visual-brief skill for design.
---

# Carousel Builder

A carousel earns the swipe slide by slide. This skill writes the script — one idea per slide — and the caption that teases it, then hands the design to the visual brief.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run the `init` onboarding skill first, then stop.

## Gate 2 — Read the substrate

Load the `authority-context` skill. Read `authority-context.md` (§2 pillars, §10 voice, §12 visual identity if present) and `memory/`. Operate in the profile's `language`.

## When to trigger

The user says "make this a carousel", "turn this into slides", "build me a carousel", "I have a framework to turn into slides", or wants a document/PDF post.

## Inputs to ask for (only if missing)

The topic or framework, and roughly how many slides (default 6-10).

## Structure

- **Cover slide** — the hook. One promise, one bold idea. Title max 7 words.
- **Value slides** — one idea per slide. Title + 1-3 short lines + optional micro-example.
- **Closing slide** — the CTA. One action, not three.

## Process

1. Distill the topic into a single promise that fits on a cover slide.
2. Break the promise into N-2 atomic ideas (one per value slide).
3. Order the slides so each one earns the swipe to the next.
4. Write the closing slide with one clear CTA (load `ctas`).
5. Write the **caption**: do not repeat the slides — tease them. The caption is a real post and gets the hook treatment (load `hooks`).

## Output format

```
CAROUSEL — [topic]   ([N] slides)

SLIDE 1 (COVER) : [hook, max 7 words] / [sub-line]
SLIDE 2 : [title] — [1-3 lines]
... 
SLIDE N (CLOSING) : [single CTA]

CAPTION
[hook + 2-4 short lines teasing the carousel + CTA]
```

## Finalization

1. Run `humanizer-linkedin` on the slide copy and the caption (strip AI tone).
2. Optionally score the **caption** with `${PLUGIN_ROOT}/scripts/score_post.py <caption.txt> --lang <pt|en>` for **hook and CTA signal only** — do **not** apply the ≥9/10 publish gate here. A caption is a short tease, so it will score low on Structure/Data by design; that is expected, not a failure. The slides are the value payload, not the caption.

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

3. Hand off to `visual-brief` for the slide design spec (format, layout, AI image prompt, brand colors from §12).
4. Save the script + caption to `outputs/posts/<YYYYMMDD>-<slug>-vN.md`, with `carousel` in the slug (e.g. `2026-06-26-scaling-ops-carousel-v1.md`) so the standard `<slug>-vN` versioning holds. **Gate 3-M** write-back: append the approved caption hook to `memory/winning-hooks.md`, plus entries to `memory/topic-performance.md` and `memory/learnings.md`.

## Rules

- One idea per slide. Two ideas on a slide kills the swipe.
- Cover title: max 7 words.
- Closing CTA: one action, not three.
- Caption teases, never repeats the slides.

## Hand-off

For the design itself, `visual-brief` produces the prompt and specs. To plan more carousels into the month, use `content-calendar` (and remember the rule: never two carousels back to back).
