---
name: 360brew-algorithm
description: Complete reference for LinkedIn's 360Brew algorithm (v3.5, Q1 2026): fundamentals, format and timing specs, metrics, and scoring system. Use it when creating or evaluating posts to keep them aligned with the algorithm's rules, maximize organic reach, and estimate outlier probabilities. PT triggers: entenda seu alcance, otimize seus posts com você, preveja seus outliers.
---

## Core

# 360Brew algorithm - fundamentals

> Version 3.5 · Baseline: Q1 2026

## What 360Brew is

LinkedIn has finished its move to **360Brew**, a single unified engine that replaced several fragmented algorithms.

**The core shift:** the platform no longer prioritizes "who you know" (the Social Graph). It now prioritizes **"what you know"** and **"who needs to know it"** (the Interest Graph).

---

## The 5 pillars

### 1. AEO (Answer Engine Optimization)

The algorithm now works like an **answer engine**:

- Feed and search are treated as a **single entity**
- Posts are indexed as **answers** to queries
- Profile SEO = **authority ranking within a niche**

**What it means in practice:** write posts that answer the real questions your ICP is asking.

### 2. Profile classification (profile-content alignment)

Your profile is no longer just context. It's the **classification anchor**:

- 360Brew cross-checks the post against your headline, About section, experience, and skills
- Posts aligned with your expertise get an **instant boost**
- Off-niche posts get **severe reach suppression**
- The algorithm builds a "topic DNA" from how consistently you stay within 2-3 niches over time

**What it means in practice:** publish consistently about the same 2-3 niches. Straying is expensive.

### 3. The 90-minute test window (the new Golden Hour)

The algorithm didn't kill the critical window. It widened it and made it harder to pass:

- The first 90 minutes are a **test with 2-5% of your most active followers**
- What it measures in that window: **Saves, Dwell Time (>15 sec), and long comments**
- What no longer counts: quick likes and shallow clicks
- "Post and ghost" (publishing then disappearing) is **detected and penalizes your future distribution**
- Posts can resurface days later, but only if they pass the 90-minute test

**What it means in practice:** be available to reply to comments in the first 90 minutes after publishing.

### 4. Artificial pattern detection (Low Entropy Noise)

360Brew was trained specifically to spot AI-generated content and inauthentic behavior:

- It detects formulaic syntax, low lexical diversity, and the predictable cadence of AI writing
- AI-generated posts with no meaningful human editing are **deprioritized within milliseconds**
- Engagement pods are caught through pattern analysis of similar comments
- Generic automated comments destroy the distribution of the post they land on

**What it means in practice:** every post needs an authentic human voice, lived specificity, and natural imperfections.

### 5. Multimodal validation

360Brew uses AI models to:

- Read and validate visual content
- Check that the image supports the text
- Penalize text/image inconsistency

**What it means in practice:** the visual should reinforce the message, not just decorate it.

---

## The outlier formula

```
OUTLIER = Topic × Hook × Visual × Saves Potential
```

To break out of the median (where 66% of reach has been lost), **all four elements** have to be dialed in:

| Element | What it means |
|----------|-----------------|
| **Topic** | Aligned with your positioning + algorithm demand |
| **Hook** | Proof of work/authority that stops the scroll |
| **Visual** | Optimized format that supports the message |
| **Saves Potential** | Reference content people want to come back to (a 5x signal) |

**If one fails, the post won't become an outlier.**

---

## Key changes vs 2025

| Before (v2.0 - 2025) | Now (v3.5 - 2026) |
|---------------------|---------------------|
| Multiple algorithms | Single 360Brew engine (150B params) |
| Social Graph | **Interest Graph** |
| 60-min Golden Hour | **90-min window measuring Saves + Dwell Time** |
| Profile as context | **Profile as anchor (profile-content alignment)** |
| Feed and search separate | **Unified AEO** |
| Links in the body accepted | **Links in the body = -60% reach** (put them in the comments) |
| Hashtags useful | **Hashtags penalized** (the LLM reads semantics directly) |
| Likes = engagement | **Saves = 5x likes · Long comments = 2x likes** |
| Vertical video | **Horizontal +36%** for B2B |

---

## Golden rules for 2026

1. **360Brew unified everything** - feed and search are one entity (150B parameters)
2. **Profile is the anchor** - profile-content alignment decides distribution before the post circulates
3. **Outlier = Topic × Hook × Visual × Saves Potential** - all 4 have to work
4. **Saves > everything** - 5x more powerful than likes. Build posts people want to come back to
5. **Dwell time is the trigger** - under 3 seconds = disqualified. Over 15 seconds = distribution unlocked
6. **The first 90 minutes are critical** - a test window with 2-5% of your network. Be there to reply to comments
7. **Links in the body = -60% reach** - put links in the comments right after publishing
8. **Hashtags are dead** - the LLM reads semantic context. Hashtags signal manipulation
9. **Carousels 4.1x** - the safest bet (dwell time per slide is tracked)
10. **AI patterns get detected** - 360Brew was trained to spot AI Slop

---

## Formats

# 360Brew algorithm - formats and specs

> Technical specifications for text, visual, and timing.

## Text specs

### Optimal parameters

| Parameter | Optimal value | Impact |
|-----------|-------------|---------|
| **Length** | 1250-2500 chars | +31% reach |
| **Paragraphs** | 14+ short | -71% if dense |
| **Words** | Avg ≤5 letters | -39% if complex |
| **Reading level** | 5th-7th grade | Maximum scannability |

### Body structure

```
HOOK (1-2 lines)
↓
CONTEXT (3-4 paragraphs)
→ Why the topic matters
→ Connection to a pain/desire
↓
DEVELOPMENT (8-10 paragraphs)
→ Steps, story, or proof
→ Specific numbers
↓
CONCLUSION (2-3 paragraphs)
→ The big lesson or synthesis
→ One CTA
```

### Formatting rules

**Do:**
- Paragraphs of 1-3 lines
- White space between paragraphs
- Specific numbers (not "several", but "7")
- Plain, direct language

**Avoid:**
- Dense blocks of text (>3 lines)
- Complex or technical words when you don't need them
- Multiple CTAs competing
- Excessive emojis

---

## Visual formats

### Reach multipliers

| Format | Performance | When to use |
|---------|-------------|-------------|
| **PDF carousel** | **4.1x** | Frameworks, lists, tutorials |
| **4:5 image** | **+86%** | Single posts with visual impact |
| **Horizontal video** | **+36%** | B2B content, demos |
| **Document/PDF** | **+3.5x** | Guides, checklists, templates |

### Technical specs

**Image:**
- Format: 4:5 (1080x1350px)
- Colors consistent with the brand
- Visual illustrates the content (not decorative)

**Carousel:**
- 7-10 slides is ideal
- PDF performs better than images
- First cover = visual hook
- Last cover = CTA

**Video:**
- Horizontal > vertical for B2B
- Captions required
- First 3 seconds = hook

### Multimodal validation

360Brew uses AI to check:
- The image text aligns with the post
- The visual supports the message
- Consistency across formats

**Penalty:** a generic image, or one disconnected from the text.

---

## Links and hashtags

### Links

| Position | Reach impact |
|---------|-------------------|
| **In the body of the post** | **−60% reach** (direct penalty) |
| **In the 1st comment right after publishing** | Neutral or positive |
| **In the profile bio** | Neutral |

**Rule:** links always go in the comments, never in the body. Publish the post, then immediately add the link in the 1st comment.

### Hashtags

360Brew reads semantic context directly. It doesn't rely on hashtags to categorize content.

| Use | Impact |
|-----|---------|
| 5+ hashtags | Penalty (signals manipulative behavior) |
| 3-5 generic hashtags (#Marketing, #Business) | Penalty |
| 0-2 hyper-specific hashtags | Neutral |
| No hashtags | Neutral/positive |

**Rule:** default to zero hashtags. If you use any, cap it at 1-2 that are extremely specific to your niche.

---

## Post-publishing (the critical 90-min window)

360Brew tests the post with 2-5% of your most active followers during the first 90 minutes. Here's what it measures:

| Signal | Weight | What to do |
|-------|------|-------------|
| **Saves** | Maximum | Reference content people want to come back to |
| **Dwell Time >15 sec** | High | Structure that holds the read |
| **Long comments (3+ sentences)** | High | Reply to comments — it signals an active community |
| **Quick likes** | Low | No longer the focus |

**90-minute protocol:**
1. Publish the post
2. In the 1st comment: add the link (if you have one) + extra context
3. Reply to every comment that comes in with substantial answers (3+ sentences)
4. Don't disappear — "post and ghost" suppresses future distribution

### Times by objective

| Objective | Day | Window (BRT) |
|----------|-----|--------------|
| **Authority** | Tuesday | 08:00-10:00 |
| **Sales** | Thursday | 11:00-13:00 |
| **Engagement** | Sunday | 10:00-12:00 |

### Recommended frequency

| Frequency | Result |
|------------|-----------|
| 3-4 posts/week | Optimal (consistency without saturation) |
| 5-7 posts/week | Risk of saturation |
| 1-2 posts/week | Suboptimal (the algorithm "forgets") |

### Times to avoid

- 16:00-02:00 GMT (low activity)
- Early Monday (full inbox)
- Late Friday (disengagement)

**Note:** with the Golden Hour gone, timing matters less than it used to. Focus on consistency.

---

## High-performing topics

### By viral probability

| Topic | Probability |
|--------|---------------|
| **Career education** | **3x higher** |
| **AI and technology** | High (rising) |
| **Leadership and management** | Stable |
| **Productivity** | Medium-high |
| **B2B sales** | Medium (specific niche) |

### The alignment rule

A post performs best when:
1. The topic sits within your profile positioning
2. You have a credential or proof on the subject
3. There's real demand (not an empty niche)

**Formula:** Expertise + Demand + Consistency = Authority

---

## Quick checklist

### Text
- [ ] 1250-2500 characters?
- [ ] 14+ short paragraphs?
- [ ] Plain words (avg ≤5 letters)?
- [ ] A Proof of Work / Authority Proof hook?
- [ ] Specific numbers (not vague)?
- [ ] One clear CTA?
- [ ] No links in the body? (links go in the 1st comment)
- [ ] Zero hashtags, or at most 1-2 extremely specific ones?
- [ ] Does the post read like a human wrote it, not an AI template?

### Engagement and distribution
- [ ] Does the post have high save potential (framework, checklist, template, reference)?
- [ ] Does the structure force dwell time (carousel, dense value list, progressive story)?
- [ ] Will you be available for 90 minutes after publishing to reply to comments?
- [ ] If there's a link, does it go in the 1st comment — not the body?

### Visual
- [ ] 4:5 format or PDF carousel?
- [ ] Does the visual support the message?
- [ ] Consistent colors?

### Algorithm
- [ ] Topic aligned with the profile (profile-content alignment)?
- [ ] No punished patterns ("What do you think?")?
- [ ] Does the post avoid detectable AI patterns (varied vocabulary, specific voice, natural imperfections)?

### Red flags

❌ **CRITICAL:** Link in the body of the post (−60% reach)
❌ **CRITICAL:** Too many or generic hashtags (signals manipulation to 360Brew)
❌ **CRITICAL:** "Post and ghost" — publishing then vanishing in the first 90 minutes
❌ Dense blocks of text (−71%)
❌ "What do you think?" / "Agree?" (a detected bait)
❌ Visual disconnected from the text
❌ Multiple CTAs
❌ Posts outside the profile's niche
❌ AI writing patterns with no human editing (Low Entropy Noise)

---

## Metrics

# 360Brew algorithm - metrics and benchmarks

> Numbers, probabilities, and the scoring system.

## State of organic reach

### Historical drop

| Period | Reach vs 2023 |
|---------|-----------------|
| Q3 2024 | -50% |
| Q2-Q3 2025 | -65% |
| **Q1 2026** | **-66%** (stabilized) |

**Reading it:** the drop has stabilized, but median reach is 66% lower than 2023.

### What this means

- Median content barely shows up
- Outliers capture most of the reach
- Quality matters more than quantity

---

## Performance concentration

### Gap between tiers

| Tier | Performance gap | % of total reach |
|------|--------------------|--------------------|
| **Top 1%** | 225x | 63% |
| **Top 5%** | 115x | 85% |
| **Top 10%** | 50x | 92% |
| **Median** | 1x (baseline) | 8% |

**Insight:** the Top 1% captures 63% of all reach. There's no middle ground.

### Actual distribution

```
Top 1%   ████████████████████████████████░░░░░░░ 63%
Top 5%   ██████████████████████░░░░░░░░░░░░░░░░░ 22%
Top 10%  █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  7%
Rest     ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  8%
```

---

## Scoring system

### The 6 dimensions (v3.5)

| Dimension | Weight | What it evaluates |
|----------|------|--------------|
| **Saves Potential** | **30%** | Probability of being saved. The algorithm's most powerful signal (5x a like) |
| **Hook** | 20% | Power to stop the scroll |
| **Algorithm** | 20% | Adherence to 360Brew specs (no links in the body, no hashtag overload, no AI patterns, topic aligned with the profile) |
| **Structure** | 15% | Framework + Length (chars) + paragraphs + scannability |
| **CTA** | 10% | Clarity, focused on 1 high-value action (save or long comment) |
| **Data** | 5% | Level of proof, concrete numbers |

> **Why does Saves Potential lead at 30%?** Saves generate 5x more reach than likes on 360Brew. Long comments (3+ sentences) generate 2x. Dwell time above 15 seconds unlocks distribution. The scoring has to reflect that hierarchy of signals.

### Decision bands

| Score | Action | Description |
|-------|------|-----------|
| **9.0-10.0** | ✅ Publish | Outlier candidate |
| **8.0-8.9** | ⚠️ Review | Very good, quick tweaks |
| **7.0-7.9** | 🔄 Rework | Clear bottlenecks |
| **6.0-6.9** | ❌ Redo | Structural fix needed |
| **< 6.0** | 🚫 Start over | Back to objective + structure |

### Breakdown by dimension

**Saves Potential (30%)**
| Score | Description |
|-------|-----------|
| 10 | Applicable framework + checklist or template + a reference people return to |
| 8-9 | High value density, clearly savable as a reference |
| 6-7 | Useful, but not future-reference material |
| 4-5 | One-time read, nothing to save |
| 0-3 | Shallow viral content with no practical use |

**Hook (20%)**
| Score | Description |
|-------|-----------|
| 10 | Proof of work + specific number + strong curiosity |
| 8-9 | Has 2 of 3 elements |
| 6-7 | Relevant, but generic |
| 4-5 | Cliché, no angle |
| 0-3 | Punished by the algorithm ("What do you think?", "Good morning, LinkedIn") or an AI-cliché hook ("Let that sink in", "Game-changer", "Unlock the power of") |

**Algorithm (20%)**
| Score | Description |
|-------|-----------|
| 10 | No links in the body, zero generic hashtags, no AI pattern, topic aligned with the profile |
| 8-9 | Most specs met, 1-2 minor gaps |
| 6-7 | Basic specs, a detectable problem (e.g. too many hashtags) |
| 4-5 | Link in the body OR hashtag overload OR a detectable AI pattern |
| 0-3 | Multiple active violations |

**Structure (15%)** evaluates 3 sub-components:

| Sub-component | Target | Drops the score if |
|----------------|------|-------------------|
| Length | 1250-2500 chars | <1000 or >3000 chars |
| Paragraphs | 14+ short (max ~19 words) | <10 paragraphs or any paragraph >150 chars |
| Framework | PAS, AIDA, BAB, HSO, or another recognizable one | Structure missing or confusing order |

| Score | Description |
|-------|-----------|
| 10 | 3 perfect sub-components + high dwell time (carousel or dense list) |
| 8-9 | 2 of 3 sub-components perfect |
| 6-7 | Framework ok, length or paragraphs off target |
| 4-5 | 2 sub-components failing |
| 0-3 | Wall of text |

**CTA (10%)**
| Score | Description |
|-------|-----------|
| 10 | One CTA + specific + geared toward saves or long comments |
| 8-9 | CTA aligned with the objective, no value reinforcement |
| 6-7 | Generic CTA |
| 4-5 | Multiple CTAs or disconnected |
| 0-3 | Punished CTA (only asks for a like, "What do you think?") |

**Data (5%)**
| Score | Description |
|-------|-----------|
| 10 | 5+ specific data points |
| 8-9 | 3-4 strong data points |
| 6-7 | 1-2 data points or examples |
| 4-5 | Vague language |
| 0-3 | Zero data |

---

## Probability calculation

### Top 1%

```
Base = (finalScore / 10) × 20

Bonus:
  SavesPotential ≥ 9 → +7 pts
  Hook ≥ 9 → +4 pts
  Algorithm ≥ 9 → +4 pts

Cap: 35%
```

**Example:** Score 9.2, Saves 9.5, Hook 9.0, Algorithm 9.0
- Base: (9.2/10) × 20 = 18.4
- Bonus: +7 (saves) + +4 (hook) + +4 (algorithm) = +15
- Total: 33.4% → **33% chance of Top 1%**

### Top 5%

```
Base = (finalScore / 10) × 50

Bonus:
  SavesPotential ≥ 8 → +10 pts
  Hook ≥ 8 → +7 pts
  Algorithm ≥ 8 → +7 pts

Cap: 75%
```

**Example:** Score 8.5, Saves 8.8, Hook 8.2, Algorithm 8.8
- Base: (8.5/10) × 50 = 42.5
- Bonus: +10 (saves) + +7 (hook) + +7 (algorithm) = +24
- Total: 66.5% → **66% chance of Top 5%**

> The bonuses mirror the dimension hierarchy. Saves Potential dominates because it's the signal with the highest multiplier in the algorithm.

---

## Benchmarks by format

### Proven multipliers

| Format | Multiplier | Confidence |
|---------|---------------|-----------|
| PDF carousel | **4.1x** | High (dwell time per slide tracked) |
| Document/PDF | **3.5x** | High |
| 4:5 image | **+86%** | High |
| Horizontal video | **+36%** | Medium-high |
| Link in the 1st comment | Neutral/positive | High |
| **Link in the body of the post** | **−60%** | High (always avoid) |

### Engagement weights (360Brew 2026)

| Action | Algorithm weight | Note |
|------|---------------|------------|
| **Save** | **5x a like** | Primary signal of usefulness |
| **Long comment (3+ sentences)** | **2x a like** | LLM checks depth via NLP |
| **Dwell time >15 seconds** | Distribution multiplier | Unlocks distribution to cold audiences |
| **Like/Reaction** | 1x (residual) | Lost most of its relevance |
| **Dwell time <3 seconds** | Disqualification | Post treated as irrelevant |

### By content type

| Type | Relative performance | Save potential |
|------|----------------------|---------------|
| Tutorial/How-to | High | High |
| Framework/Checklist | Very high | Very high |
| Personal lesson (with data) | High | Medium-high |
| Contrarian | High (high risk) | Medium |
| Pure opinion | Medium | Low |
| News/Commentary | Low | Low |

### Engagement benchmarks

| Metric | Top 1% | Top 5% | Median |
|---------|--------|--------|---------|
| Impressions | >50k | >20k | 2-5k |
| Engagement | >5% | >3% | 1-2% |
| Saves | >100 | >30 | 5-10 |
| Comments | >50 | >20 | 5-10 |

---

## Indicators of outlier potential

A post has a high probability of being an outlier when:

1. **Score ≥ 9.0** in the scoring system
2. **Saves Potential ≥ 9** (framework, checklist, template)
3. **Hook** with proof of work or authority + a number
4. **Format** optimized (PDF carousel or 4:5)
5. **Topic** aligned with the profile and with demand (profile-content alignment)
6. **Zero violations:** no link in the body, no generic hashtags, no AI pattern
7. **High projected dwell time** (structure that forces a progressive read)

**Outlier probability:**
- 6-7 indicators = 70%+ chance
- 5 of 7 indicators = 50%+ chance
- 4 of 7 indicators = 30%+ chance
- < 4 indicators = unlikely
