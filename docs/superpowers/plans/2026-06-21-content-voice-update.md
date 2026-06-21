# Content + Voice Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the plugin's content-type taxonomy to a funnel-job model (22 types, badges, funnel stage) and harden the voice layer with the AI-cliché checklist (humanizer + scorer).

**Architecture:** Two sequenced phases over markdown skills + a small Python scoring layer. Phase 1 rewrites `content-types/SKILL.md` (16 refined + 6 new types) and updates peripheral docs. Phase 2 adds an AI-cliché hook list to `humanizer-linkedin` (qualitative) and a new `_AI_CLICHE_HOOKS` matcher + `find_ai_cliches()` to `postlib.py`, penalized in `score_post.py`'s Hook dimension, with a one-line sync into the 360brew Metrics section.

**Tech Stack:** Markdown skills (read by Claude at runtime), Python 3.14 CLI (`postlib.py`, `score_post.py`), pytest.

## Global Constraints

- Base language of all shipped plugin artifacts is **English**. Plugin content stays EN.
- `postlib.py` is the single source of truth; matching is **union-based PT+EN**, anchored to avoid false positives. New patterns go in BOTH `_*["pt"]` and `_*["en"]` with canonical shared labels.
- Three locations must stay in sync: `postlib.SPECS`, `score_post.WEIGHTS`, the `360brew-algorithm/SKILL.md` Metrics section. **WEIGHTS and SPECS do not change in this plan** — only the Hook-dimension narrative (banda 0-3) gains the AI-cliché example.
- TDD for all Python. Frequent commits. Do NOT bump the plugin version or alter `plugin.json`/`marketplace.json` (test_plugin_structure asserts version `1.1.0`).
- Full suite must stay green: `pytest` (baseline today: 42 passed).
- AI-cliché scorer penalty = **−1.5** on the Hook dimension (user-approved). `"Here's the kicker"` is EN-only (no clean PT equivalent).

---

## PHASE 1 — Taxonomy

### Task 1: Rewrite `content-types/SKILL.md` (22 types, badges, funnel)

**Files:**
- Modify: `linkedin-authority-engine/skills/content-types/SKILL.md` (full rewrite)
- Test: `tests/test_plugin_structure.py::test_knowledge_skills_present_and_valid` (existing — must still pass)

**Interfaces:**
- Consumes: nothing (leaf content).
- Produces: the canonical catalog of 22 type names other docs reference. The 5 badged-new + Validation type names, verbatim, are: `Newsjacking`, `Spectacle / Challenge`, `Relatable / Validation`, `Objection-Handling`, `Product-Demo`, `Lead-Magnet`.

- [ ] **Step 1: Update the frontmatter description**

Replace the `description:` line so it reads (keep `name: content-types`):

```
description: Catalog of 22 LinkedIn content types with structure, funnel-stage mapping, and reach/conversion badges, plus a selection guide by objective and funnel stage. Use when deciding the post type before choosing the copywriting framework.
```

- [ ] **Step 2: Add the opening thesis (right after the `# 22 content types` title, replacing the current "## Overview")**

```markdown
## Overview

Every post does a different job. Some win reach at the top of the funnel; others convert at the bottom and barely get views — that trade-off is the point, not a bug. Pick the type by what you want the post to *do*, then choose the copywriting framework.

Badges:
- ⚡ **High reach (awareness)** — built to be seen by cold audiences.
- 💰 **High conversion (low reach, high ROI)** — few views, but they move buyers.
```

- [ ] **Step 3: Refine the 16 existing types — apply stage + badge, keep structure, improve phrasing**

For each existing type, keep its `**Structure:**` block, tighten the prose (no AI-isms — see Phase 2 banned words), and add a stage line `**Funnel stage:** <stage>` under the heading. Apply this exact mapping:

| # | Type (heading) | Funnel stage | Badge |
|---|---|---|---|
| 1 | Truth and Hope | Awareness | — |
| 2 | Old Way, New Way | Awareness | — |
| 3 | I Learned Something This Week | Trust | — |
| 4 | Statistics Post | Awareness | — |
| 5 | The Magic of X | Awareness | — |
| 6 | Before-and-After / Case-study | Conversion | 💰 |
| 7 | Round-up List | Awareness | — |
| 8 | Behind the Scenes | Trust | — |
| 9 | Tell a Story | Trust | — |
| 10 | How-to (Tutorial) | Awareness | — |
| 11 | Contrarian Opinion | Awareness | — |
| 12 | Lessons from Mentor | Trust | — |
| 13 | Mistakes and Failures | Trust | — |
| 14 | Create a Villain | Awareness | — |
| 15 | Framework/System | Awareness | — |
| 16 | Data-Driven | Awareness | — |

Only #6 gains a badge (💰) and is renamed `Before-and-After / Case-study`.

- [ ] **Step 4: Add the case-study 6-step framework to type #6**

Under type #6, after its existing Structure block, add:

```markdown
**Case-study 6-step (for conversion):**
1. Hook with the transformation ("From 5 to 100K followers in 6 months")
2. Visual proof (a message, screenshot, or before/after data)
3. A relatable problem (so the reader thinks "I have that now")
4. Specific, tangible results (more time with family? more revenue?)
5. Your role as the guide — the client is the hero, not you
6. A clear CTA with urgency ("Taking 5 new clients this month")

Tag the people in the thread — it adds credibility.
```

- [ ] **Step 5: Add the Story → Lesson → Application framework to type #9**

Under type #9 (Tell a Story), after its Structure block, add:

```markdown
**Framework — Story → Lesson → Application:**
→ Story: a real moment (yours, someone you know, or something you observed)
→ Lesson: the takeaway — what should people learn?
→ Application: what they can do to put the lesson into practice (use when it fits)
```

- [ ] **Step 6: Append the 6 new types (17–22)**

```markdown
## 17. Newsjacking  ⚡ High reach (awareness)

**When to use:** A relevant event just broke in your niche and you can ship fast — the window is short

**Funnel stage:** Awareness

**Structure:**

→ The event (what just happened)

→ Your cut: connect it to your niche

→ The specific problem it creates for your audience

→ Your take / what to do about it

**Note:** Speed is everything — posting three days late misses the window. Don't just summarize the news and add an opinion at the end; bring it back to your audience's specific problem.

---

## 18. Spectacle / Challenge  ⚡ High reach (awareness)

**When to use:** You can commit to a public, high-stakes challenge (use sparingly — once a month or quarter)

**Funnel stage:** Awareness

**Structure (5 components):**

→ High stakes — not mundane; your audience has to care

→ Relevant to your audience

→ Published BEFORE you know the result (the unknown is what makes people follow)

→ Value at every step — document the journey

→ Milestones people can check in on

---

## 19. Relatable / Validation

**When to use:** Name a frustration or reality your audience feels but can't articulate

**Funnel stage:** Awareness

**Structure:**

→ The unspoken reality/frustration

→ Why it's real (validate it)

→ Why no one says it out loud

→ What it means for them

**Note:** Distinct from Contrarian Opinion — validation agrees with a felt truth; contrarian challenges a belief.

---

## 20. Objection-Handling  💰 High conversion (low reach, high ROI)

**When to use:** Address a doubt that stops people from buying

**Funnel stage:** Conversion

**Structure:**

→ Open with the objection (ideally attributed to someone of weight: "A $100M CRO told me this yesterday")

→ Why it feels true

→ Your answer, back-and-forth

→ The reframe

**Note:** Source objections from your discovery calls.

---

## 21. Product-Demo  💰 High conversion (low reach, high ROI)

**When to use:** Show your product or service solving a real problem in action

**Funnel stage:** Conversion

**Structure:**

→ The real problem (specific, one your customers have)

→ The product solving it, step by step — not a feature list

→ The outcome

→ A CTA to a demo or trial

**Note:** Carries more weight when the founder/CEO shows it. Lead with use cases, not just new features.

---

## 22. Lead-Magnet  💰 High conversion (low reach, high ROI)

**When to use:** Move people off LinkedIn and into your email list

**Funnel stage:** Conversion

**Structure:**

→ A high-value, specific promise

→ The value preview (why it's worth it)

→ "Comment [WORD] and I'll send it"

→ After publishing: deliver via DM/link, capture the email

**Note:** Common mistake — offering something low-value, so no one comments.
```

- [ ] **Step 7: Rewrite the selection guide with a funnel-stage column**

Replace the existing `## Selection guide` table with:

```markdown
## Selection guide

| Objective | Recommended types | Funnel stage |
| --- | --- | --- |
| Educate | How-to, Framework, Statistics, Data-Driven | Awareness |
| Inspire | Tell a Story, Before-and-After / Case-study, Lessons from Mentor | Trust → Conversion |
| Engage | Contrarian, Create a Villain, I Learned, Relatable / Validation | Awareness / Trust |
| Convert | Before-and-After / Case-study 💰, Objection-Handling 💰, Product-Demo 💰, Lead-Magnet 💰 | Conversion |
| Authority | Data-Driven, Framework, Spectacle ⚡, Newsjacking ⚡ | Awareness |
```

- [ ] **Step 8: Verify the skill is still structurally valid**

Run: `.venv/bin/python -m pytest tests/test_plugin_structure.py -q`
Expected: PASS (frontmatter present, body > 200 chars).

- [ ] **Step 9: Verify the catalog has 22 numbered types**

Run: `grep -cE '^## [0-9]+\. ' linkedin-authority-engine/skills/content-types/SKILL.md`
Expected: `22`

- [ ] **Step 10: Commit**

```bash
git add linkedin-authority-engine/skills/content-types/SKILL.md
git commit -m "feat(content-types): funnel-job taxonomy — 22 types, badges, stage column"
```

---

### Task 2: Update peripheral docs (count + Video note)

> Pre-flight correction (2026-06-21): the string `16 content types` exists **only** in `linkedin-authority-engine/README.md`. The root `README.md` and `CLAUDE.md` do not mention content types at all (verified by grep), so they are not touched.

**Files:**
- Modify: `linkedin-authority-engine/skills/visual-brief/SKILL.md` (add Video note)
- Modify: `linkedin-authority-engine/README.md` (count "16" → "22")

**Interfaces:**
- Consumes: the type count from Task 1 (22).
- Produces: nothing downstream.

- [ ] **Step 1: Add a Video note to `visual-brief/SKILL.md`**

Append this section to the end of `linkedin-authority-engine/skills/visual-brief/SKILL.md`:

```markdown
## Video (a format, not a text type)

Video posts (a <60s take, behind-the-scenes, or a point-of-view) build trust because people hear your voice and see your face. They are a **format**, not one of the text content-types — pair them with captions and a hook in the first 2 seconds. When a post's job is trust and you can record, prefer video over a selfie.
```

- [ ] **Step 2: Update the count in `linkedin-authority-engine/README.md`**

On line 37, the skills bullet reads "... 8 copywriting structures, 16 content types, templates by category ...". Change `16 content types` → `22 content types`.

Run to confirm: `grep -n "22 content types" linkedin-authority-engine/README.md`
Expected: one match.

- [ ] **Step 3: Verify no stale "16 content types" remains**

Run: `grep -rn "16 content types" README.md CLAUDE.md linkedin-authority-engine/README.md`
Expected: no output (exit 1).

- [ ] **Step 4: Commit**

```bash
git add linkedin-authority-engine/README.md linkedin-authority-engine/skills/visual-brief/SKILL.md
git commit -m "docs: reflect 22 content types; note Video as a format in visual-brief"
```

---

## PHASE 2 — Voice

### Task 3: Add the voice checklist to `humanizer-linkedin/SKILL.md`

**Files:**
- Modify: `linkedin-authority-engine/skills/humanizer-linkedin/SKILL.md` (append sections)
- Test: `tests/test_plugin_structure.py::test_knowledge_skills_present_and_valid` (existing)

**Interfaces:**
- Consumes: nothing.
- Produces: the canonical 17 banned hooks + 15 banned words list (humanizer-only; the scorer in Task 4/5 mirrors only the concrete subset).

- [ ] **Step 1: Append the banned-words section**

Append to `humanizer-linkedin/SKILL.md`:

```markdown
## LinkedIn voice recovery (LinkedIn-specific layer)

> This layer is additive to the 24 patterns in the `humanizer` skill. It targets LinkedIn-native AI tells.

### Banned words — replace with what you'd say out loud

| AI word | Say instead |
|---|---|
| Surfaced | Found / Noticed |
| Fostered | Built / Helped |
| Utilized | Used |
| Paradigm | Approach / Way |
| Mitigated | Reduced / Fixed |
| Leveraged | Used |
| Moreover | Also / And |
| Holistic | Full / Complete |
| Synergy | Teamwork / Overlap |
| Streamlined | Simplified / Sped up |
| Pivoted | Changed / Shifted |
| Ecosystem | Space / World |
| Robust | Strong / Solid |
| Facilitate | Help / Run |
| Cultivate | Build / Grow |
```

- [ ] **Step 2: Append the banned-hooks section (all 17 — humanizer handles the variable templates the scorer can't)**

```markdown
### Banned hooks — rewrite if you see these

Concrete phrases (also caught by the scorer): "Read that again", "Let that sink in", "What if I told you...?", "Here's the truth about...", "Nobody tells you...", "Unlock the power of...", "Game-changer", "Here's the shift...", "The real question is...", "And here's the kicker...".

Variable templates (humanizer-only — too variable to regex safely): "Stop doing X. Do Y.", "Unpopular opinion: ...", "Most people think X. They're wrong.", "I used to believe X. Then everything changed.", "Not only that, but...", "Not because X. Because Y.", "And here's the thing most people miss...".
```

- [ ] **Step 3: Append the out-loud and specificity checks**

```markdown
### Out-loud test

Read every sentence aloud. If you wouldn't say it to a friend over coffee, rewrite it the way you'd actually say it. Vary sentence length — mix short punches with longer thoughts.

### Specificity check

Vague = AI. Specific = human. Every story carries at least 2 of: a name, a number, a date, a place. Replace "the results were impressive" with "that post got 2,192 reactions in 4 days".

> On the "use AI only for feedback" rule from the source checklist: this plugin generates and rewrites, so the equivalent discipline is **surgery, not demolition** — fix the pattern, keep the author's voice and data.
```

- [ ] **Step 4: Verify the skill is still structurally valid**

Run: `.venv/bin/python -m pytest tests/test_plugin_structure.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add linkedin-authority-engine/skills/humanizer-linkedin/SKILL.md
git commit -m "feat(humanizer-linkedin): add banned words/hooks + out-loud & specificity checks"
```

---

### Task 4: Add `_AI_CLICHE_HOOKS` + `find_ai_cliches()` to `postlib.py`

**Files:**
- Modify: `linkedin-authority-engine/scripts/postlib.py`
- Test: `tests/test_postlib.py`

**Interfaces:**
- Consumes: `resolve_langs()` (existing in postlib).
- Produces: `find_ai_cliches(text: str, lang: str = "auto") -> list` returning canonical AI-cliché labels found in the first 5 lines, deduped across languages. Used by `score_post.score_hook` in Task 5.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_postlib.py`:

```python
# --- AI-cliché hooks (separate bucket from engagement-bait) ---

def test_ai_cliche_en():
    assert "Let that sink in" in postlib.find_ai_cliches("Let that sink in.\nBig news today.", "en")

def test_ai_cliche_pt():
    assert "Let that sink in" in postlib.find_ai_cliches("Deixa isso assentar.\nNovidade hoje.", "pt")

def test_ai_cliche_clean_text_no_false_positive():
    assert postlib.find_ai_cliches("I spent 40 hours testing three tools last week.", "auto") == []

def test_ai_cliche_dedup_across_languages():
    labels = postlib.find_ai_cliches("Game-changer e divisor de águas no mesmo post", "auto")
    assert labels.count("Game-changer") == 1

def test_ai_cliche_only_first_lines():
    # a cliché buried below the first 5 lines is not a hook
    text = "Clean hook line.\n\n\n\n\n\nLet that sink in."
    assert postlib.find_ai_cliches(text, "en") == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_postlib.py -k ai_cliche -v`
Expected: FAIL with `AttributeError: module 'postlib' has no attribute 'find_ai_cliches'`.

- [ ] **Step 3: Add the pattern set and matcher**

In `postlib.py`, after the `_PUNISHED` dict block (around line 124), add:

```python
# AI-cliché hooks — DISTINCT from _PUNISHED (engagement bait). Only concrete,
# regex-safe phrases live here; variable templates ("Stop doing X. Do Y.") are
# handled qualitatively by the humanizer-linkedin skill, not the scorer.
# Labels are canonical (shared across languages) so union matching counts once.
_AI_CLICHE_HOOKS = {
    "en": [
        (r"\bread that again\b", "Read that again"),
        (r"\blet that sink in\b", "Let that sink in"),
        (r"\bwhat if i told you\b", "What if I told you"),
        (r"\bhere'?s the truth about\b", "Here's the truth about"),
        (r"\bnobody tells you\b", "Nobody tells you"),
        (r"\bunlock the power of\b", "Unlock the power of"),
        (r"\bgame[ -]?changer\b", "Game-changer"),
        (r"\bhere'?s the shift\b", "Here's the shift"),
        (r"\bthe real question is\b", "The real question is"),
        (r"\bhere'?s the kicker\b", "Here's the kicker"),
    ],
    "pt": [
        (r"\bleia (?:isso )?de novo\b", "Read that again"),
        (r"\bdeixa isso (?:assentar|bater)\b", "Let that sink in"),
        (r"\be se eu te dissesse\b", "What if I told you"),
        (r"\ba verdade sobre\b", "Here's the truth about"),
        (r"\bningu[ée]m te conta\b", "Nobody tells you"),
        (r"\b(?:destrave|desbloqueie) o poder de\b", "Unlock the power of"),
        (r"\bdivisor de águas\b", "Game-changer"),
        (r"\baqui está a virada\b", "Here's the shift"),
        (r"\ba (?:verdadeira|real) pergunta é\b", "The real question is"),
    ],
}
```

Then add this matcher next to `find_punished` (in the matchers section):

```python
def find_ai_cliches(text: str, lang: str = "auto") -> list:
    """Returns canonical AI-cliché hook labels found in the first lines
    (deduped across languages). Separate from find_punished (engagement bait)."""
    first_lines = '\n'.join(text.split('\n')[:5])
    found = []
    for l in resolve_langs(lang):
        for pattern, name in _AI_CLICHE_HOOKS[l]:
            if name not in found and re.search(pattern, first_lines, re.IGNORECASE):
                found.append(name)
    return found
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_postlib.py -k ai_cliche -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the full suite**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS (47 passed — 42 baseline + 5 new).

- [ ] **Step 6: Commit**

```bash
git add linkedin-authority-engine/scripts/postlib.py tests/test_postlib.py
git commit -m "feat(postlib): add _AI_CLICHE_HOOKS bucket + find_ai_cliches (EN+PT)"
```

---

### Task 5: Penalize AI-cliché hooks in `score_post.py` + sync the 360brew Metrics

**Files:**
- Modify: `linkedin-authority-engine/scripts/score_post.py` (`score_hook`, around lines 68-93)
- Modify: `linkedin-authority-engine/skills/360brew-algorithm/SKILL.md` (Metrics → Hook breakdown, banda 0-3)
- Test: `tests/test_postlib.py`

**Interfaces:**
- Consumes: `postlib.find_ai_cliches()` from Task 4; `score_post.score_hook(text, lang) -> (float, list)`.
- Produces: nothing downstream.

- [ ] **Step 1: Write the failing test**

First add the import at the top of `tests/test_postlib.py`, right after the existing `import postlib  # noqa: E402` line:

```python
import score_post  # noqa: E402
```

Then append the test at the end of the file. The two inputs share an identical base and differ **only** by the prefixed cliché, so the delta is exactly the penalty (the base scores 5.0 — no number, no proof-verb, no authority match — so neither input clamps):

```python
def test_score_hook_penalizes_ai_cliche():
    base = "Here is what I learned about pricing.\nThree lessons below."
    s_base, _ = score_post.score_hook(base, "en")
    s_cliche, _ = score_post.score_hook("Let that sink in. " + base, "en")
    assert s_cliche == s_base - 1.5
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_postlib.py::test_score_hook_penalizes_ai_cliche -v`
Expected: FAIL (scores equal — no penalty applied yet).

- [ ] **Step 3: Add the penalty in `score_hook`**

In `score_post.py`, inside `score_hook`, immediately after the existing `find_punished` block (the one that does `score -= 4.0`), add:

```python
    if postlib.find_ai_cliches(text, lang):
        score -= 1.5
        feedback.append("[X] AI-cliché hook detected (-1.5)")
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_postlib.py::test_score_hook_penalizes_ai_cliche -v`
Expected: PASS.

> Note: `score_hook` clamps with `min(10, max(0, score))`. The shared base scores exactly 5.0 (no number, no proof-verb, no authority), so `base = 5.0` and `cliché = 3.5` — neither clamps and the −1.5 delta is exact.

- [ ] **Step 5: Sync the 360brew Metrics narrative**

In `linkedin-authority-engine/skills/360brew-algorithm/SKILL.md`, in the **Hook (20%)** breakdown table, change the score `0-3` row description from:

```
| 0-3 | Punished by the algorithm ("What do you think?", "Good morning, LinkedIn") |
```

to:

```
| 0-3 | Punished by the algorithm ("What do you think?", "Good morning, LinkedIn") or an AI-cliché hook ("Let that sink in", "Game-changer", "Unlock the power of") |
```

- [ ] **Step 6: Run the full suite**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS (48 passed — 47 + 1 new).

- [ ] **Step 7: Commit**

```bash
git add linkedin-authority-engine/scripts/score_post.py tests/test_postlib.py linkedin-authority-engine/skills/360brew-algorithm/SKILL.md
git commit -m "feat(score): penalize AI-cliché hooks (-1.5); sync 360brew Metrics"
```

---

## Self-Review

**Spec coverage:**
- Fase 1 content-types rewrite (22, badges, stage) → Task 1. ✅
- McTighe-10 mapping (Video → visual-brief) → Task 1 (types) + Task 2 (Video note). ✅
- 6 new types + 2 frameworks → Task 1 steps 4-6. ✅
- Badge by job (⚡/💰) → Task 1 steps 2, 3, 6, 7. ✅
- Counts updated → Task 2. ✅
- humanizer banned words/hooks + out-loud + specificity + Step-4 resolution → Task 3. ✅
- `_AI_CLICHE_HOOKS` + `find_ai_cliches` EN+PT + tests → Task 4. ✅
- score_hook penalty + Metrics sync → Task 5. ✅
- WEIGHTS/SPECS untouched, version untouched → Global Constraints. ✅

**Placeholder scan:** No TBD/TODO; all code and markdown shown verbatim. ✅

**Type consistency:** `find_ai_cliches(text, lang="auto") -> list` defined in Task 4, consumed identically in Task 5. Type names (`Newsjacking`, `Spectacle / Challenge`, `Relatable / Validation`, `Objection-Handling`, `Product-Demo`, `Lead-Magnet`) consistent between Task 1 interfaces and step 6. Canonical cliché labels shared EN/PT in Task 4. ✅
