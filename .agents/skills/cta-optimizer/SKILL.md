---
name: linkedin-authority-engine:cta-optimizer
description: Diagnose why a post's closing is weak and rewrite it to maximize the one signal that matters — saves, comments, shares, DMs, profile visits, or clicks. Use when the user has a post but the ending falls flat, defaults to "Thoughts?", or doesn't match the objective. Loads the CTA bank; returns a diagnosis plus 3-5 alternatives. Inline, no file output.
---
# CTA Optimizer

Most posts earn the read and then waste it on "Let me know what you think". This skill diagnoses the weak close and rewrites it for the goal that actually matters.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run `/linkedin-authority-engine:init` first, then stop.

## Gate 2 — Read the substrate

Load the `linkedin-authority-engine:authority-context` skill and read §3 (primary objective) and §10 (voice). Then **load the `linkedin-authority-engine:ctas` skill** — that bank is the source of truth for the formulas and the 2026 signal priority. Operate in the profile's `language`.

## When to trigger

The user says "fix my CTA", "my ending is weak", "how should I close this post", "the ending isn't earning comments/saves", or pastes a post that ends on a flat "Thoughts?". (For a whole-post problem, not just the close, use `/linkedin-authority-engine:rewrite`.)

## Inputs to ask for (only if missing)

The post (or at least its closing), and the goal: saves, comments, shares, DMs, profile visits/follows, or clicks. If the goal is unstated, default to the post's objective from §3, then to **saves** (the top 2026 signal).

## CTA patterns by goal

(Full bank + formulas in the `linkedin-authority-engine:ctas` skill. 2026 priority: Saves › Long comments › Follow › Leads.)

- **Saves** — "Save this for when you [specific situation]". Default whenever the post is a framework, checklist, or guide.
- **Comments** — a binary question or a polarizing ask that earns 3+ sentence replies. Never "Agree?".
- **Shares** — "Tag the [persona] who needs this".
- **DMs / leads** — "Comment [single trigger word] and I'll send you [resource]".
- **Profile visits / follows** — "Follow me for [specific, concrete benefit] every week".
- **Link clicks** — tease the resource, link in the first comment (never in the body — that cuts reach ~60%).

## Process

1. Read the current close. Name in one line why it is weak (no ask / wrong signal / two CTAs cancelling / disconnected from the body).
2. Pick the right goal (from input or §3).
3. Write 3 to 5 alternatives in that goal's pattern, each matched to the post's energy.
4. Recommend one, with the reason.

## Output format

```
CTA DIAGNOSIS
Current : "[paste current close]"
Why it's weak : [one line]
Target signal : [saves / comments / ...]

ALTERNATIVES
1. "[option]"  — [why it fits]
... (3 to 5)

SHIP : Option [N] — [one-line reason]
```

This skill is inline only — it returns the diagnosis and options in chat. It does not save a file.

## Rules

- One CTA per post. Two CTAs cancel each other.
- Never close on "Let me know what you think" or "Thoughts?" — punished in 2026.
- For comment CTAs, anchor to a binary or specific question, not an open one.
- Match the energy of the post. A vulnerable story does not close with "Book a call".
- If there is a link, it goes in the first comment, not the body.

## Hand-off

If the post needs more than a CTA fix, hand off to `/linkedin-authority-engine:rewrite` for a full two-version optimization, or `/linkedin-authority-engine:score` to check it against all 6 dimensions.
