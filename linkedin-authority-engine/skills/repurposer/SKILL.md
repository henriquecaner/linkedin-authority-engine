---
name: repurposer
description: Convert an existing piece of content (blog post, tweet/thread, YouTube transcript, podcast, Notion doc) into a native LinkedIn post — one idea, rewritten for LinkedIn dynamics, not pasted verbatim. Use when the user pastes or links an external artifact to bring onto LinkedIn. For a raw personal experience with no external source, use story-extractor instead. Runs the full finalization pipeline and saves to outputs/posts/.
---

# Repurposer

A LinkedIn post is not a blog post in disguise, and a tweet thread pasted vertically is not a post. This skill extracts one idea from a source and rebuilds it native.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run `/linkedin-authority-engine:init` first, then stop.

## Gate 2 — Read the substrate

Load the `linkedin-authority-engine:authority-context` skill. Read `authority-context.md` (voice §10, pillars §2, constraints §9, NO territories §8) and `memory/`. The repurposed post must sound like the client and stay on-pillar — not like the source author. Operate in the profile's `language`.

## When to trigger

The user pastes or links a blog, tweet, thread, YouTube/podcast transcript, or doc and says "turn this into a LinkedIn post", "repurpose this", "make this work on LinkedIn", "I wrote this elsewhere".

## Inputs to ask for (only if missing)

The source content (paste or link), and which single angle the user cares about most if the source covers several.

## Process

1. Read the source. Identify the **single strongest takeaway**. One. If the source has five, pick one and save the rest for other posts.
2. Strip everything format-specific: blog headings, thread numbering, "uh / you know", newsletter framing, SEO scaffolding.
3. Rewrite the **hook** for LinkedIn — the first two lines must stop the scroll alone (load the `linkedin-authority-engine:hooks` skill for patterns).
4. Reformat the **body** in LinkedIn style: short lines, white space, one idea per line, a re-hook mid-post.
5. Write a **CTA** that fits LinkedIn (a question or save prompt, never "click here") — load the `linkedin-authority-engine:ctas` skill.

## Output

A single complete post (hook + body + CTA). Then run the finalization pipeline below.

## Finalization pipeline

Run the post through the full finalization pipeline exactly as defined in `/linkedin-authority-engine:guided` (Stages A-E): `validate_specs.py` → `linkedin-authority-engine:humanizer-linkedin` → `linkedin-authority-engine:visual-brief` → `score_post.py` → `linkedin-authority-engine:post-publication-protocol`. Then **Gate 3-M** write-back (append the approved hook to `memory/winning-hooks.md`, plus entries to `memory/topic-performance.md` and `memory/learnings.md`) and save to `outputs/posts/<YYYYMMDD>-<slug>-vN.md`.

## Rules

- A LinkedIn post is not a blog post in disguise. Cut hard.
- One idea per post. Resist cramming the whole source in.
- Never paste a tweet thread vertically.
- For video/podcast sources, lead with the moment, not the topic — open on the sharpest line, not "In this episode we discussed...".

## Hand-off

If the source had several strong takeaways, offer to repurpose the next one, or plan them across the month with `linkedin-authority-engine:content-calendar`.
