---
name: linkedin
description: Mode menu and router: onboarding, guided, rewrite, thread, score. Use when the user doesn't know where to start, says 'o que vamos criar', 'me mostra as opções', 'what can you do', or pastes content with no clear instruction. Never generate here, only route. Covers all modes with an overview.
---

# Linkedin skill
## Profile check (required before any mode)

Before showing the menu or routing to a mode, silently verify whether `authority-context.md` exists in the current project.
Source of profile, in order: (1) `authority-context.md` + `memory/` on disk when present; (2) a pasted `profile-card` block; (3) otherwise run the `init` onboarding skill first, then stop.

- If it **does not exist**: show the message below and stop.

```
⚠️  No profile found.
Run the `init` onboarding skill to create your authority profile before generating posts.
```

- If it **exists**: continue with the routing below.

When the profile exists, read its `language` frontmatter field and render the menu and all prompts in that language (`pt` → Brazilian Portuguese / pt-BR, `en` → English). When no profile exists yet, the "No profile found" message stays in English — the language has not been chosen yet.

---

## Routing by argument

| Argument received | Immediate action |
|-------------------|------------------|
| `onboarding` | Start onboarding — invoke the `init` onboarding skill |
| `guided` | Start GUIDED MODE (STEP 1.0) |
| `guided [topic]` | GUIDED MODE with the topic already provided (skip STEP 1.2) |
| `rewrite` | Ask for the post and start REWRITE MODE |
| `rewrite [post]` | REWRITE MODE with the post already provided |
| `thread` | Start THREAD MODE (collect topic and number of posts) |
| `thread [topic]` | THREAD MODE with the topic already provided |
| `score [post]` | SCORE MODE directly on the pasted post |
| no argument | Show the menu below |

---

## Menu (no argument)

```
🎯 LinkedIn Authority Engine — What are we creating?

POST MODES (type the number)
0 Onboarding — create or refresh your authority profile (the `init` onboarding skill)
1 Guided   — post from scratch (full workflow)
2 Rewrite  — optimize an existing post
3 Thread   — series of posts
4 Score    — evaluate + humanize a finished post

STRATEGY (just ask — feeds your profile)
• "Define my niche"            — sharpen positioning
• "Build my audience persona"  — the one person you write for
• "Build my content pillars"   — 3-5 recurring themes + topics
• "Plan my next 4 weeks"       — 4-week content calendar

PRODUCE (just ask)
• "Turn this blog/video/tweet into a post"  — repurpose source material
• "Turn this experience into a post"        — extract a story
• "Fix my CTA"                              — diagnose + rewrite the close
• "Turn this into a carousel"               — slide-by-slide script

AUDIT (just ask)
• "Audit my LinkedIn profile"  — headline / About / Featured
• "Read my analytics"          — paste your numbers → 3 next moves

Type a number for a post mode, or just say what you want.
```

Wait for the user's choice and route to the matching skill:
- `0` or `onboarding` → invoke the `init` onboarding skill
- `1` or `guided` → invoke the `guided` skill
- `2` or `rewrite` → invoke the `rewrite` skill
- `3` or `thread` → invoke the `thread` skill
- `4` or `score` → invoke the `score` skill

The STRATEGY / PRODUCE / AUDIT items are **skills**, not numbered commands — they auto-invoke when the user asks in plain language (the trigger phrases above are examples). If the user picks one of these, just act on the request; the matching skill (`niche-definer`, `audience-persona`, `content-pillars`, `content-calendar`, `repurposer`, `story-extractor`, `cta-optimizer`, `carousel-builder`, `profile-optimizer`, `analytics-interpreter`) loads on its own. All of them honor the profile check above.
