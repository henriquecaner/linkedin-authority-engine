---
name: profile-optimizer
description: Audit a LinkedIn profile (headline, banner, photo, About, Featured, Experience) and return prioritized fixes with rewritten copy, scored by impact. Use when the user pastes their profile or asks "audit my LinkedIn", "fix my headline", "is my profile converting". Grounds rewrites in the client's positioning; saves the audit to outputs/strategy/. PT triggers: otimize seu perfil com você, reescreva seu headline, converta suas visitas.
---

# Profile Optimizer

The profile is where the post sends people. A great post into a weak profile leaks every visitor. This skill audits the profile in impact order and rewrites the load-bearing copy.

## Gate 1 — Profile exists?

Source of profile, in order: (1) `authority-context.md` + `memory/` on disk when present; (2) a pasted `profile-card` block; (3) otherwise run the `init` onboarding skill first, then stop. (This grounds the rewrites in the client's real positioning instead of generic advice.)

## Gate 2 — Read the substrate

Source of profile, in order: (1) `authority-context.md` + `memory/` on disk when present; (2) a pasted `profile-card` block; (3) otherwise run the `init` onboarding skill first, then stop. Load the `authority-context` skill. Read `authority-context.md` (§2 Positioning, §4 Audience, §5 Offers, §1 credibility markers) and `memory/`. The rewrites must match this positioning and speak to this ICP. Operate in the profile's `language`.

## When to trigger

The user says "audit my LinkedIn profile", "fix my headline", "rewrite my About", "is my profile converting", or pastes their current profile copy.

## Inputs to ask for (only if missing)

The current profile copy — headline, About, Featured items, current-role description. If the user only has some of it, audit what they paste and flag what is missing.

## Audit order (by impact)

1. **Headline** — highest leverage. 220 chars to answer "who do you help with what".
2. **Banner** — reinforce positioning, no random art.
3. **Profile photo** — clear face, eye contact.
4. **About** — hook above the "see more" cut, then story, then CTA.
5. **Featured** — 3 to 5 items max, every one serves the CTA.
6. **Experience** — current role matches the headline promise.

## Process

1. Score each element 1-5 against the positioning in §2/§4.
2. List the **top 3 fixes by impact** (not all six).
3. Rewrite the copy for the weakest high-impact elements — at minimum the headline.

## Output format

```
PROFILE AUDIT — [client]

SCORES
- Headline : X/5 — [one-liner]
- Banner : X/5   - Photo : X/5   - About : X/5   - Featured : X/5   - Experience : X/5

TOP 3 FIXES (by impact)
1. [element] — what's wrong / what to do
2. ...
3. ...

REWRITES
Headline : "[new headline]"
About (first 2 lines, above the fold) : "[...]"
[other rewritten elements as needed]
```

## Save the audit

Save to `outputs/strategy/<YYYYMMDD>-profile-audit.md`. This is an audit artifact, not a post — it does **not** go through the post finalization pipeline. The rewritten **copy** should still pass `humanizer-linkedin` before the user pastes it live.

## Rules

- The headline is load-bearing. Fix it first, every time.
- Headline formula: "[role] | I help [audience] [outcome] without [pain]".
- No emoji in the headline.
- Featured section: if you cannot describe each item's purpose in one line, replace it.
- Ground every rewrite in §2/§4. A headline that does not name this client's audience and outcome is generic.

## Hand-off

If the audit reveals the positioning itself is fuzzy (not just the copy), hand off to `niche-definer` to sharpen it before rewriting the profile around it.
