---
name: content-pillars
description: Define the 3 (up to 5) recurring themes the client returns to relentlessly, each with 5-10 ready post topics. Use when content feels random, the user asks "what should I post about", or after the niche is defined. Reads the profile, grounds pillars in what already performs (memory/), and writes them back to authority-context.md §2/§11 after the user confirms.
---

# Content Pillars Builder

Pillars are the 3 to 5 themes a creator returns to until the feed recognizes them on sight. They turn "what do I post today" into "which pillar is today".

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run the `init` onboarding skill first, then stop.

## Gate 2 — Read the substrate

Load the `authority-context` skill. Read `authority-context.md` (§2 Positioning, §4 Audience, §8 Territories, §11 Content instruction) and `memory/`. **Ground the pillars in data**: if `memory/topic-performance.md` has real scores, map the top performers to themes — pillars should lean on what already works for this account, not be invented from scratch. Operate in the profile's `language`.

## When to trigger

The user says "what should I post about", "I need a content system", "build my content pillars", "my LinkedIn feels random", "give me a content framework", or after running `niche-definer`.

## Inputs to ask for (only if missing)

Niche statement (§2 — if absent, run `niche-definer` first), the client's 3-5 areas of deep expertise, the audience's main pains (§4), and the desired ratio (default: 60% educational, 20% personal, 20% opinion).

## The 4 pillar types

Most LinkedIn creators win with a mix of these:

1. **Educational** — how-to, frameworks, breakdowns. Builds authority.
2. **Stories and personal** — experiences, behind-the-scenes, journey. Builds connection.
3. **Opinion and contrarian** — hot takes, critique, predictions. Builds reach.
4. **Showcase** — results, case studies, client wins. Builds trust and inbound.

## Process

1. From §2 expertise + §4 pains, propose 3 to 5 pillar candidates. Mark each as data-backed (already performs in `topic-performance.md`) or a new bet.
2. For each pillar: **theme** (one phrase), **promise to the audience**, **post types** (the mix from the 4 above), **frequency** (% of the calendar).
3. For each pillar, generate 5 to 10 concrete topic seeds so the user can ship tomorrow.

## Output format

```
CONTENT PILLARS — [client]

PILLAR 1 — [Theme]          [data-backed | new bet]
Promise : [what the audience gets]
Why it works : [link to niche / audience pain]
Post types : [educational / story / opinion / showcase mix]
Frequency : [X% of total content]
Topic seeds : 1. ... (5 to 10)

PILLAR 2 ... PILLAR 3 ... [PILLAR 4-5 optional]

WEEKLY MIX (example for 5 posts/week)
- Mon : Pillar 1 (educational)   - Tue : Pillar 3 (opinion)   ...
```

## Gate 3-S — Write it back to the profile

Persist the pillars following the **Gate 3-S** protocol in the `authority-context` skill, at **field** granularity. In **§2**, rewrite only the **3 content pillars** field — leave the core theme and value proposition untouched (those belong to `niche-definer`). If you defined 4-5 pillars, the extras and their topic seeds seed the **Priority themes** list in **§11** — **leave the `Content mix` table in §11 byte-for-byte** (it is a `*` critical field owned by objective calibration, not pillars). Show one diff covering every touched region (the §2 pillars field, and the §11 Priority themes list if touched), confirm, rewrite only those fields, bump `version`, set `last_updated`, append a dated note to `memory/learnings.md`. Never overwrite a filled `*` critical field with something vaguer.

## Rules

- 3 minimum, 5 maximum. More than 5 = no positioning. The profile's §2 carries exactly 3 — the load-bearing ones.
- Every pillar must serve the niche. A pillar that exists "because the user finds it interesting" but misses the audience gets cut.
- Pillars must not overlap. If two feel similar, merge them.
- The personal-stories pillar is essential, not optional. It is what makes the client not read like an LLM.
- Avoid the "thought leadership" pillar. That is a tone, not a topic.

## Hand-off

Pillars locked → turn them into a 4-week schedule with `content-calendar`, or draft the strongest topic seed now with the `guided` skill.
