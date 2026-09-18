---
name: content-calendar
description: Generate a 4-week LinkedIn content calendar tuned to the client's pillars, cadence, and audience — a day-by-day plan with pillar, format, topic, hook angle, and CTA goal per post. Use after pillars are defined, or when the user wants a month planned. Saves the calendar to outputs/strategy/ and hands each slot off to the `guided` skill. PT triggers: planeje seu mês com você, organize sua rotina de posts, preencha seu calendário.
---

# Content Calendar Planner

A calendar turns intention into a backlog. This skill lays out four weeks so the client never sits down to a blank page again.

## Gate 1 — Profile exists?

Source of profile, in order: (1) `authority-context.md` + `memory/` on disk when present; (2) a pasted `profile-card` block; (3) otherwise run the `init` onboarding skill first, then stop.

## Gate 2 — Read the substrate

Source of profile, in order: (1) `authority-context.md` + `memory/` on disk when present; (2) a pasted `profile-card` block; (3) otherwise run the `init` onboarding skill first, then stop. Load the `authority-context` skill. Read `authority-context.md` (§2 the 3 pillars, §4 Audience, §11 content mix + posting frequency + preferred days) and `memory/`. If §2 has no pillars yet, run `content-pillars` first. Operate in the profile's `language`.

## When to trigger

The user says "plan my next 4 weeks", "build my content calendar", "give me a month of posts", "I want a posting schedule", or after running `content-pillars`.

## Inputs to ask for (only if missing)

Posting cadence (pull from §11; otherwise ask), preferred posting days (§11), and the current primary objective (§3) so the CTA goals lean the right way.

## Cadence guidance

- Below 3/week : you do not exist.
- 3/week : minimum momentum.
- 4 to 5/week : the growth zone.
- Daily : only with a real system AND an idea pipeline.

## Process

1. Build a 4-week grid, one post per chosen day.
2. Per post, assign: **pillar**, **format**, **topic** (from the pillar's seeds), **hook angle**, **CTA goal**.
3. Distribute the pillars evenly across the weeks. Front-load week 1 with the strongest topics. Leave one wildcard slot per week for something timely.

## Output format

```
4-WEEK CALENDAR — [client]   ([N] posts/week, [days])

WEEK 1
| Day | Pillar | Format | Topic | Hook angle | CTA goal |
|-----|--------|--------|-------|-----------|----------|
| Mon | P1 educational | ... | ... | ... | saves |
| ... |
WEEK 2 ... WEEK 3 ... WEEK 4 ...

PILLAR MIX CHECK : P1 [x posts] · P2 [x] · P3 [x]  → balanced? [yes/no]
```

## Save the calendar

Save the final calendar to `outputs/strategy/<YYYYMMDD>-calendar-4w.md`. This is a planning artifact, not a post — it does **not** go through the post finalization pipeline (humanizer / score). If a calendar with the same date exists, suffix `-v2`, `-v3`.

## Rules

- Do not stack two carousels in a row.
- Distribute pillars evenly — no week should be 4 posts of the same pillar.
- Always include at least one contrarian / opinion post per week.
- Avoid Sunday posts unless the client has a Sunday-night audience.
- Every post in the grid must have a CTA goal. A slot with no CTA is not planned.

## Hand-off

When the user picks a slot to write, hand off to the `guided` skill with that topic — it runs the full generation + finalization pipeline and saves the post to `outputs/posts/`.
