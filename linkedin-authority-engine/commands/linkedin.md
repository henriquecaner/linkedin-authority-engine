---
description: Mode menu for the LinkedIn Authority Engine. Shows Onboarding, Guided, Rewrite, Thread and Score and routes to the chosen mode. Use when the user doesn't know where to start or wants an overview of the available modes.
argument-hint: "[onboarding|guided|rewrite|thread|score]"
---

# /linkedin-authority-engine:linkedin

## Profile check (required before any mode)

Before showing the menu or routing to a mode, silently verify whether `authority-context.md` exists in the current project.

- If it **does not exist**: show the message below and stop.

```
⚠️  No profile found.
Run /linkedin-authority-engine:init to create your authority profile before generating posts.
```

- If it **exists**: continue with the routing below.

When the profile exists, read its `language` frontmatter field and render the menu and all prompts in that language (`pt` → Brazilian Portuguese / pt-BR, `en` → English). When no profile exists yet, the "No profile found" message stays in English — the language has not been chosen yet.

---

## Routing by argument

| Argument received | Immediate action |
|-------------------|------------------|
| `onboarding` | Start onboarding — invoke `/linkedin-authority-engine:init` |
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
0 Onboarding — create or refresh your authority profile (/init)
1 Guided   — post from scratch (full workflow)
2 Rewrite  — optimize an existing post
3 Thread   — series of posts
4 Score    — evaluate + humanize a finished post

Type the number or the mode name.
```

Wait for the user's choice and route to the matching command:
- `0` or `onboarding` → invoke `/linkedin-authority-engine:init`
- `1` or `guided` → invoke `/linkedin-authority-engine:guided`
- `2` or `rewrite` → invoke `/linkedin-authority-engine:rewrite`
- `3` or `thread` → invoke `/linkedin-authority-engine:thread`
- `4` or `score` → invoke `/linkedin-authority-engine:score`
