---
name: humanizer-linkedin
description: Humanizing pipeline for LinkedIn posts (Step B of the Finishing Pipeline): when to run it, how to run it, the priority AI patterns in LinkedIn posts, surgery (not demolition) principles, and the output format with a compact diff. Use automatically after the CTA is chosen, before the final score, in any post-generation mode.
---

# Humanizer pipeline (LinkedIn)

> This reference describes **how** to apply the humanizer to LinkedIn posts. The full list of 24 AI patterns lives in the `humanizer` skill and **must not be duplicated here**. If the two lists diverge, the `humanizer` skill is the official guide.

## When to run it

Automatic after the CTA is chosen and integrated into the post — it is **Step B of the Finishing Pipeline**, shared by all modes (Guided, Rewrite, Thread, and Score).

Do not ask the user. It is part of the standard pipeline.

## How to run it

1. Trigger the `humanizer` skill with the full post (hook + body + CTA)
2. The skill returns the humanized text + a diff of the detected patterns
3. Present a compact diff (5 items maximum) followed by the full humanized post

## Priority patterns in LinkedIn posts

These are the patterns that show up most often in AI-generated LinkedIn posts. If the `humanizer` skill is unavailable for some reason, Claude can run a manual pass prioritizing:

| Pattern | Examples to detect |
|--------|---------------------|
| Significance inflation | "pivotal", "transformative", "vital", "impactful", "robust" |
| Promotional language | "incredible", "revolutionary", "groundbreaking", "powerful" |
| Superficial -ing | "showing that", "reflecting the", "highlighting", "contributing" |
| Excessive em dashes | Replace with a period, comma, or rewrite |
| Rule of three | "speed, quality, and results" → collapse or vary |
| Vague attributions | "experts say", "the market indicates" → specify or remove |
| Filler phrases | "In the current context", "It's important to note that", "It's worth highlighting" |
| Generic conclusions | "The future is promising", "It's just the beginning", "The moment is now" |
| Copula avoidance | "serves as", "works as", "acts as" → direct verb |

The other 15 patterns are documented in the `humanizer` skill.

## Principles

**Surgery, not demolition.** Swap the problematic word or phrase while keeping the structure, data, and the author's voice. The humanizer does not rewrite the post, it corrects patterns.

**Preserve the client's voice.** If a style document was loaded in STEP 0, do not remove vocabulary that is an intentional part of the client's voice (even if it falls into some generic pattern).

**Preserve data.** Never change numbers, values, metrics, or proper nouns in the humanizer pass.

## Pipeline output

```
Humanizer applied:
- "[original word/phrase]" → "[correction]"
- "[detected pattern]" → removed / restructured
(max 5 items — omit if there are no significant patterns)
```

Followed by the **full humanized post** (final version for scoring).
