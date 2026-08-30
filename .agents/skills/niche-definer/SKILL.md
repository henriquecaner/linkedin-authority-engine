---
name: linkedin-authority-engine:niche-definer
description: Define or sharpen the client's LinkedIn niche — audience, problem, unique angle, one-line positioning. Use when positioning feels vague ("marketing leaders"), the content reads as generic, or before building content pillars. Reads the authority profile, proposes a sharper niche, and writes it back to authority-context.md after the user confirms.
---
# Niche Definer

A niche is not a topic. It is the intersection of one audience, one problem they lose sleep over, and an angle on it that 90% of the space does not have. This skill sharpens that intersection and locks it into the profile.

## Gate 1 — Profile exists?

If there is no `authority-context.md` in the project, this skill has nothing to sharpen. Tell the user to run `/linkedin-authority-engine:init` first, then stop.

## Gate 2 — Read the substrate

Load the `linkedin-authority-engine:authority-context` skill. Read `authority-context.md` (especially §2 Positioning, §4 Audience, §8 Territories) and `memory/`. Operate in the profile's `language` field (`pt` → Brazilian Portuguese / pt-BR; `en` → English). You are refining an existing positioning, not inventing one from zero — start from what the profile already says and push it sharper.

## When to trigger

The user says "define my niche", "sharpen my positioning", "my LinkedIn feels generic", "I don't know what to be known for", "who am I writing for", or asks you to narrow a vague audience like "founders" or "marketing leaders".

## Inputs to ask for (only if missing)

Most of this is already in the profile from `/init`. Ask only for what is genuinely absent or contradictory. Lead with what §2 and §4 already contain and ask the user to confirm or correct it.

## The 7 questions

Work through these one at a time. Push back on vague answers — that is the whole job.

1. What do you actually do all day at work?
2. Who are the 3 people who pay you, hire you, or promote you?
3. What problem keeps these people up at night?
4. What do you know about this problem that 90% of your space does not?
5. What do you NOT want to be known for?
6. Who would you HATE to attract on LinkedIn?
7. If a stranger described you in one sentence after reading 5 of your posts, what would you want them to say?

## Process

1. Map the profile's current §2 (core theme, value proposition) and §4 (audience pains, transformation) against the 7 answers.
2. Name where the current positioning is too broad, on too many sides, or describes a feature instead of a point of view.
3. Draft a sharper niche: one audience, one problem, one angle.
4. Compress it into one line: **"I help [audience] [outcome] by [unique angle]."**

## Output format

```
NICHE — [client]

CURRENT (from the profile)
[one line summarizing what §2/§4 say today]

SHARPER
- Audience : [one specific person, not "everyone"]
- Problem  : [the one that keeps them up at night]
- Angle    : [the real point of view, what 90% of the space won't say]

ONE-LINE POSITIONING
"I help [audience] [outcome] by [unique angle]."

WHAT THIS CUTS
[what the client will no longer try to be known for — naming the NO is half the value]
```

## Gate 3-S — Write it back to the profile

A sharpened niche is durable client knowledge, so persist it. Follow the **Gate 3-S** protocol in the `linkedin-authority-engine:authority-context` skill exactly. Write at **field** granularity in **§2 Positioning** only: rewrite the **core authority theme** and the **value proposition** — leave the **3 content pillars** untouched (those belong to `content-pillars`). **Do not write §4** — the detailed audience/ICP belongs to `audience-persona`; hand the sharpened audience off to it (see Hand-off). Show the user a diff of old vs. new for those two fields only, wait for explicit confirmation, then rewrite only those fields (every sibling field and every other section stay byte-for-byte), bump `version`, set `last_updated`, and append a dated note to `memory/learnings.md`. Never overwrite a filled `*` field with something vaguer.

## Rules

- Push back on vague answers. "Marketing leaders" is not a niche. Drill until it is one person with one problem.
- Do not let the client be on too many sides. A niche the client can list 6 angles for is 6 niches.
- The angle must be a real point of view, not a feature. "I do it faster" is a feature; "most of this industry optimizes the wrong metric" is an angle.
- Naming the NO (questions 5 and 6) is as load-bearing as naming the YES. A niche with no edges is not a niche.

## Hand-off

Once the niche is locked, offer the next step: build the recurring themes on top of it with the `linkedin-authority-engine:content-pillars` skill, or sharpen who exactly you write for with `linkedin-authority-engine:audience-persona`.
