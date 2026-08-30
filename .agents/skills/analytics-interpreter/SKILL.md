---
name: linkedin-authority-engine:analytics-interpreter
description: Translate raw LinkedIn analytics into a clear diagnosis — what is working, what is not, and exactly 3 actions for next month. Use when the user pastes their numbers or asks "what do my analytics mean", "why did reach drop", "what should I do differently". Reads the profile goal and past performance; writes the diagnosis back to memory/.
---
# Analytics Interpreter

Numbers are not a diagnosis. This skill finds the 2-3 patterns that matter, ties them to the client's goal, and returns three moves — not ten.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run `/linkedin-authority-engine:init` first, then stop.

## Gate 2 — Read the substrate

Load the `linkedin-authority-engine:authority-context` skill. Read `authority-context.md` (§3 primary objective + tracking metric) and `memory/topic-performance.md` (any past scores/baseline). The diagnosis is judged against **the client's goal**, not against vanity. Operate in the profile's `language`.

## When to trigger

The user pastes LinkedIn analytics or says "what do my numbers mean", "why did my reach drop", "interpret my analytics", "what's working on my LinkedIn".

## Inputs to ask for (only if missing)

The analytics (paste: impressions, engagement rate, profile visits, follower growth, top and bottom posts over a date range), and the date range. If the user only has totals, work with those and say what a per-post breakdown would add.

## Reference benchmarks

- Engagement rate: 3-5% healthy, 7%+ great.
- Profile visits per post: 5-20 emerging, 50+ established.
- Follower growth per post: 0.5-2 net new healthy.
- Best formats: carousels and personal stories tend to lead.

## Process

1. Spot the **2-3 patterns that matter** — not all 12 metrics.
2. Compare top vs. bottom posts: what do the winners share that the losers do not?
3. Tie the diagnosis to the §3 goal (authority / sales / engagement).
4. Recommend exactly **3 specific actions** for next month.

## Output format

```
ANALYTICS DIAGNOSIS — [range]

WHAT'S WORKING
[1-2 patterns, with the numbers]

WHAT'S NOT
[1-2 patterns, with the numbers]

VANITY CHECK
[flag any metric that looks good but isn't converting toward the §3 goal]

3 ACTIONS FOR NEXT MONTH
1. [specific action] 2. [specific] 3. [specific]
```

## Save + write-back

1. Save the diagnosis to `outputs/strategy/<YYYYMMDD>-analytics.md`.
2. **Gate 3-M** write-back: append a dated entry to `memory/learnings.md` (the 2-3 patterns + the 3 actions). Append-only — never overwrite. Note: the `topic-performance.md` performance columns (`avg reactions`, `avg comments`, `avg saves`, `vs baseline`, `verdict`) stay empty until v1.x per the schema of record (`references/memory-schemas.md`) — do **not** write them here; capture the performance read in the `learnings.md` note instead.

## Rules

- Vanity metric warnings:
  - Impressions without profile visits = entertaining, not converting.
  - Engagement without follower growth = same audience, no new reach.
  - Profile visits without DMs = the bio is not converting (hand off to `linkedin-authority-engine:profile-optimizer`).
- Never just praise the numbers.
- Do not panic on a drop. Look for: cadence drop, angle change, a competitor taking the niche, an algorithm shift.
- Three actions. Not ten. Three.

## Hand-off

If the diagnosis points to a profile that does not convert visits, hand off to `linkedin-authority-engine:profile-optimizer`. If a format is clearly winning, plan more of it with `linkedin-authority-engine:content-calendar`.
