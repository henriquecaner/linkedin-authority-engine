# Backlog — LEVEL TECH / LinkedIn Authority Engine

Lightweight work backlog for the product + GTM layer. Lean items only
(objective, reference, expected outcome, acceptance criteria). Promote an item
to `docs/superpowers/specs/` when it needs a full design.

> Sibling docs: `gtm-context.md` (strategy) · `docs/superpowers/specs/` (design).

## Items

### 1. Entry quiz (quiz funnel) — start-using / buy front door

- **Status:** Backlog
- **Added:** 2026-06-19
- **Reference:** buzzfy.co/pt/quiz (quiz-funnel pattern)
- **Objective:** An interactive entry quiz that engages a visitor, qualifies
  them against the ICP/anti-ICP, and routes to one of two outcomes:
  **(a) start using** (→ onboarding `/init`) or **(b) buy** (→ InfinityPay Gold
  link).
- **Why:** Fills two named gaps in `gtm-context.md` — the missing top-of-funnel
  lead magnet for selling the product, and a low-touch flow that qualifies and
  closes without the founder in the loop (the biggest current bottleneck).
- **Acceptance criteria:**
  - 4–10 step interactive flow with branching logic.
  - Qualifies on the ICP gates (R$ 1M+/yr revenue, B2B, >10k addressable on
    LinkedIn, commits to executing 30–60 days) and filters out the anti-ICP.
  - Personalized end screen with a single primary CTA per branch
    (start → `/init` path; buy → Gold checkout).
  - Lead capture wired to the existing stack (HubSpot).
  - Copy in the brand voice (direct/irreverent; LP register, not raw-LinkedIn).
- **Open questions:** build vs. buy (an existing quiz tool like the buzzfy
  stack vs. custom on thelevr.com); PT-first or PT/EN/ES at launch.

### 2. Site benchmark — buzzfy.co/pt

- **Status:** Backlog
- **Added:** 2026-06-19
- **Objective:** Manual benchmark of buzzfy.co/pt (blocks automated fetch — do
  it in a browser) to extract reusable patterns for our quiz + LP.
- **Capture:** page structure (hero → sections → social proof → pricing → CTA);
  quiz placement in the funnel; quiz UX (steps, progress, branching, result
  screen); copy/value-prop angles; lead-capture timing; pricing presentation;
  CTA hierarchy.
- **Deliverable:** short benchmark note (bullets — what to copy / what to skip),
  linked back into item #1.
