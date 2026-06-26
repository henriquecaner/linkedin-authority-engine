---
name: story-extractor
description: Extract a publishable LinkedIn story from a raw lived experience — structure it into a story-arc post (situation, tension, turning point, outcome, lesson) that starts at the punch. Use when the user dumps a first-person experience with no external source, says "something happened", or wants to turn a moment into a post. To repurpose an existing blog/video/tweet, use repurposer instead. Respects the profile's vulnerability level; runs the full finalization pipeline.
---

# Story Extractor

The client lived something. This skill turns the raw dump into a story with tension, told the way stories land on LinkedIn — starting at the punch, not the chronology.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run `/linkedin-authority-engine:init` first, then stop.

## Gate 2 — Read the substrate

Load the `linkedin-authority-engine:authority-context` skill. Read `authority-context.md` — especially §2 (stories available, untold stories), §10 **vulnerability level (1-5)**, §9 constraints, §8 NO territories — and `memory/`. **Never push the story past the client's stated vulnerability level.** Operate in the profile's `language`.

## When to trigger

The user says "something happened at work", "let me tell you about", "turn this experience into a post", "I have a story", or dumps a messy first-person account.

## Inputs to ask for (only if missing)

The raw experience, and the lesson the user wants the reader to walk away with (if they have one — otherwise you propose it).

## The story arc

1. **Situation** — 2 lines max.
2. **Tension** — what made it hard, risky, or weird. No tension, no story.
3. **Turning point** — the decision, the moment, the realization.
4. **Outcome** — what happened.
5. **Lesson** — what the reader takes away.

## Process

1. Find the tension. If the dump has none, push the user for the friction — what nearly went wrong, what was at stake.
2. Cut the chronology. Start at the punch (mid-tension or at the turning point), then back-fill the setup.
3. Build the arc with real names, real numbers, real dates — within §9/§8 constraints.
4. End on a sharp, earned lesson. Let the reader extract it; do not moralize.

## Output

A single complete post (hook + story body + CTA). Then run the finalization pipeline.

## Finalization pipeline

Run the post through the full finalization pipeline exactly as defined in `/linkedin-authority-engine:guided` (Stages A-E): `validate_specs.py` → `linkedin-authority-engine:humanizer-linkedin` → `linkedin-authority-engine:visual-brief` → `score_post.py` → `linkedin-authority-engine:post-publication-protocol`. Then **Gate 3-M** write-back (append the approved hook to `memory/winning-hooks.md`, plus entries to `memory/topic-performance.md` and `memory/learnings.md`) and save to `outputs/posts/<YYYYMMDD>-<slug>-vN.md`. For ready-made section scaffolds, load `linkedin-authority-engine:templates-by-category` (career lesson, failure).

## Rules

- No story without tension. Push for friction.
- Real names, real numbers, real dates — never generic "a client", "some growth".
- Never moralize. The reader extracts the lesson; you do not spell out "and that's why you should never give up".
- Cut the chronology. Stories on LinkedIn jump: start at the punch, then back-fill.
- Reject "be yourself" / "never give up" lessons. Find the sharper, specific one only this experience earns.
- Honor §10. If the vulnerability level is 1-2, keep it professional; do not manufacture confessional drama the client did not authorize.

## Hand-off

If the client has more untold stories in §2, offer to extract the next one, or schedule them with `linkedin-authority-engine:content-calendar`.
