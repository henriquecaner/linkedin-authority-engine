---
name: linkedin-authority-engine:autopilot
description: Core coordinator for the LinkedIn Autopilot routines. Guides the background agy cron tasks (Weekly Analytics Scraper and Weekly Content Drafts) and manages the parallel agent orchestrations.
---

# LinkedIn Autopilot Control Hub

This skill orchestrates the autonomous background tasks and parallel agent workflows that drive the **LinkedIn Authority Engine (LAE v2.0)**.

---

## 1. Background Schedules (The Autopilot Loop)

The autopilot relies on two standard cron tasks scheduled using the Antigravity `schedule` tool:

### Task A: Weekly Analytics Scraper & Memory Update
- **Schedule**: `0 9 * * 1` (Every Monday at 9:00 AM)
- **Workflow**:
  1. Spawn a `browser_subagent` and navigate to LinkedIn Creator Analytics: `https://www.linkedin.com/analytics/creator/shares/` or your post activity page `https://www.linkedin.com/in/me/recent-activity/all/`.
  2. Locate recent posts published in the last 7-14 days. Extract:
     - Post text snippet or canonical slug.
     - Impressions (Views).
     - Reactions (Likes, Applauds, etc.).
     - Comments count.
     - Reposts/Shares count.
  3. Perform a **Gate 3 write-back** into the local memory substrate:
     - Match the scraped post with any URN/slug in `memory/published-posts.md` (or identify by text match).
     - Write the final figures into `.agents/memory/topic-performance.md` in the appropriate columns.
     - If the post's engagement-to-impressions ratio is exceptionally high (> 5%), identify its hook pattern and write it into `.agents/memory/winning-hooks.md`.
  4. Post a summary notification in the user's main chat:
     ```
     📊 [AUTOPILOT] Weekly stats scraped successfully!
     - Top performing pillar: [Pillar Name] (X.X% engagement)
     - New winning hook recorded: "[Hook Snippet]" (added to memory/winning-hooks.md)
     - Profile topic DNA database updated.
     ```

### Task B: Weekly Content Draft Generation
- **Schedule**: `0 10 * * 1` (Every Monday at 10:00 AM, following the metrics update)
- **Workflow**:
  1. Spawn the parallel crew: `linkedin-strategist` + `linkedin-writer` + `linkedin-reviewer`.
  2. **Strategist**: Analyzes the freshly updated `memory/topic-performance.md` and `authority-context.md`. Proposes 3 content angles based on high-performing pillars and formats.
  3. **Writer**: Drafts the full post copy for each of the 3 proposed angles, utilizing winning hooks from `memory/winning-hooks.md` and structures from `skills/copywriting-structures/`.
  4. **Reviewer**: Executes `.agents/scripts/validate_specs.py`, applies `humanizer-linkedin` skill rules to strip AI patterns, and scores each draft using `.agents/scripts/score_post.py`.
  5. Save the ready-to-publish files as:
     `outputs/posts/<YYYYMMDD>-<slug>-v1.md`
  6. Deliver an alert notification in the user's main chat:
     ```
     ✍️ [AUTOPILOT] Weekly content drafts are ready!
     The multi-agent crew has prepared 3 high-impact posts for this week (all rated ≥9.0/10 on the 360Brew scale).
     - Post 1: "[Title/Hook]" (Score: X.X/10) -> [File link](file:///Users/henriquecaner/Documents/GitHub/linkedin-content-caner/outputs/posts/post1.md)
     - Post 2: "[Title/Hook]" (Score: X.X/10) -> [File link](file:///Users/henriquecaner/Documents/GitHub/linkedin-content-caner/outputs/posts/post2.md)
     - Post 3: "[Title/Hook]" (Score: X.X/10) -> [File link](file:///Users/henriquecaner/Documents/GitHub/linkedin-content-caner/outputs/posts/post3.md)
     
     Type "/score" to review and edit, or "/publish" to schedule them directly through the browser.
     ```

---

## 2. Managing the Autopilot via CLI

To interact with or schedule these background routines, the user or agent can run these standard commands:

- **List active schedules**: Use `manage_task` with Action: `'list'`.
- **Trigger Scraper manually**: "Run LinkedIn metrics autopilot scraper now." (Loads this skill and runs Task A immediately).
- **Trigger Generator manually**: "Run LinkedIn content generation autopilot now." (Loads this skill and runs Task B immediately).
