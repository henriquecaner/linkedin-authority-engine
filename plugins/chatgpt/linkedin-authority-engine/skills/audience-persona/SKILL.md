---
name: audience-persona
description: Build a sharp, post-ready persona of the one person the client writes for on LinkedIn — title, pains, jobs-to-be-done, the words they use, what makes them save or DM. Use after the niche is defined, when content talks to "everyone", or before planning pillars/calendar. Reads the profile and writes the persona back to authority-context.md §4 after the user confirms.
---

# Audience Persona Builder

You do not write for an audience. You write for one person. This skill builds that person in enough detail that every future post can be tested against them.

## Gate 1 — Profile exists?

If there is no `authority-context.md`, run the `init` onboarding skill first, then stop.

## Gate 2 — Read the substrate

Load the `authority-context` skill. Read `authority-context.md` (especially §4 Audience and §6 Commercial narrative — objections are persona gold) and `memory/`. Operate in the profile's `language`. Start from the §4 the profile already has; you are sharpening it into one named person, not starting blank.

## When to trigger

The user says "who am I writing for", "build my audience persona", "my posts talk to everyone", "define my ICP", or after running the `niche-definer` skill.

## Inputs to ask for (only if missing)

Use the client's actual customers as the raw material — real people they have worked with, not a demographic. Pull what §4 and §6 already contain first, then fill gaps from the 12 questions.

## The 12 questions

1. Title and seniority.
2. Company stage and size.
3. Who they report to.
4. Top 3 KPIs.
5. Top 3 jobs to be done.
6. Top 3 pains.
7. What they buy or consider buying.
8. Where they consume content.
9. Who they listen to.
10. What words they use (their exact vocabulary).
11. What objections they raise.
12. What success looks like for them in 12 months.

## Process

1. Anchor on one real customer archetype. Never blend two into an average.
2. Answer the 12 questions in that person's words, not corporate paraphrase.
3. Build the persona card.
4. Generate 10 post topics that hit this person directly.

## Output format

```
PERSONA — [name the persona, e.g. "Scaling-CEO Carla"]

SNAPSHOT
- Title / seniority : [...]
- Company stage/size : [...]
- Reports to : [...]
- Top 3 KPIs : [...]
- Top 3 jobs-to-be-done : [...]
- Top 3 pains : [...]

IN THEIR WORDS
- Vocabulary they use : [...]
- Who they listen to : [...]
- Objections they raise : [...]
- Success in 12 months : [...]

10 POSTS THAT HIT THEM
1. [topic] ... 10. [topic]
```

## Gate 3-S — Write it back to the profile

Persist the persona into **§4 Audience (ICP)** of `authority-context.md` following the **Gate 3-S** protocol in the `authority-context` skill. Write at **field/subsection** granularity, not whole-section: rewrite the **`## Profile 1`** persona fields (role, pains, transformation, values), and **preserve any `## Profile 2`** subsection the user set up byte-for-byte — append or refine a second persona, never delete it. Show a diff of old vs. new for the Profile 1 fields only, confirm, rewrite only those fields, bump `version`, **set `last_updated`**, and append a dated note to `memory/learnings.md`. Never overwrite a filled `*` critical field (e.g. *Main pains*, *The big transformation they want*) with something vaguer.

## Rules

- One persona at a time. Never blend. An averaged persona speaks to no one.
- Vocabulary matters. Writing in their exact words doubles resonance — capture question 10 verbatim.
- Reject "everyone". "Everyone" is a target-practice silhouette, not a persona.
- The writing test, applied to every future post: would this persona **save it, share it, or DM me about it**? If no, rewrite or skip.

## Hand-off

With the persona locked, build the recurring themes that serve it with `content-pillars`, then turn pillars into a schedule with `content-calendar`.
