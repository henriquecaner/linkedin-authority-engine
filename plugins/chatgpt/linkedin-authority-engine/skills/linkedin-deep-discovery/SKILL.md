---
name: linkedin-deep-discovery
description: Desktop only — deep discovery via Unipile API v2 (requires UNIPILE_API_KEY on a local runtime). Pull a client's LinkedIn profile, recent posts and company page into a dossier that pre-fills the init interview. Use when a LinkedIn URL is available and UNIPILE_API_KEY resolves, or on "pull my LinkedIn", "refresh my profile data", "audit competitor X". Never ask the user to paste API keys in chat.
---

# LinkedIn deep discovery (Path U)

> Desktop only: this skill needs a local runtime with scripts plus `UNIPILE_API_KEY` in the environment. It never runs on ChatGPT web. Never ask the user to paste API keys in chat — if the key is missing, fall back to the manual interview.

Second discovery path for the `init` onboarding skill. Given the client's LinkedIn URL plus up to 3
competitor and 3 reference URLs, `scripts/unipile_discovery.py` pulls profile +
post corpus + company page through Unipile, writes a raw JSON payload and a
readable dossier to `outputs/discovery/`, and measures the real post corpus.
The interview then confirms and fills gaps instead of asking blind.

- From the `init` onboarding skill when a LinkedIn URL is available and `UNIPILE_API_KEY` resolves.

- On "pull my LinkedIn", "refresh my profile data", "audit competitor X".
- The manual interview stays the default whenever no API key is present.

## Gate 0 — credentials

Run `python scripts/unipile_discovery.py --dry-run --linkedin-url <url>`.
Exit 2 means no key: say so plainly and fall back to the manual interview.
Never block onboarding on a missing key. Exit 4 means the URL did not parse;
ask the user to paste it again.

## Process

1. Run for the client with `--role self` (default 30 posts).
2. Run once per competitor and reference URL with `--role reference`
   (implies `--no-company`, 10 posts unless overridden). Cap the reference
   loop at 6 profiles; beyond that the operator re-runs the script manually.
   Run the fetches sequentially so the client's jittered spacing keeps the
   loop inside one rate-limit window.
3. Read the dossiers, not the raw JSON, unless a field is missing. The raw
   JSON exists so re-deriving a dossier never needs another API call.
   Company fetches (`--company-id`/`--company-url`, slugs accepted) are slow:
   if they time out at the default 30 s, raise `UNIPILE_TIMEOUT_MS` to 60000+.
   A company miss degrades to a recorded gap, never an abort.
4. If the dossier's Key inventory shows `extract_post_text → MISSING`, stop:
   fix the candidate list in the script from the printed key set and re-run.
   Shipping with an unresolved text extractor makes every voice metric zero.

## Mapping table — dossier evidence to template field

| Dossier evidence | `authority-context.md` target | Confidence |
|---|---|---|
| Identity, headline, location, tenure | §1 Profile | high — factual |
| Bio narrative (`bio` + `description`; the payload has no experience section) | §1 short bio, career summary | draft only — must be confirmed |
| Numbers in bio/description | §1 credibility markers | draft only |
| Skills + endorsement counts (`specifics.skills`, dozens live) | §1 credibility markers (supplement) | medium |
| Top terms + post themes | §2 core theme, §8 YES territories, §13 brand keywords | draft only |
| Recurring post structures | §11 preferred format | medium |
| Voice metrics + spectrum proxies | §10 Tone of voice | medium — user confirms the spectrum |
| Competitor/reference corpora | §7 what each communicates well + the gap | medium |
| Company page (only when `--company-id`/`--company-url` is hand-supplied; the profile payload carries no company reference) | §1 company, §5 offers (as leads to ask about) | medium |
| Post `first_lines` scoring well | seeds for `memory/winning-hooks.md` | draft only |

## What the API can never supply — always ask

§3 objectives and the 90-day win, §1 company affiliation (unless a company dossier exists — the profile never supplies it), §5 offers and pricing, §6 sales pitch and
objections, §9 forbidden words / confidential info / sensitivities, §10
vulnerability level, §11 content mix and approval process, §12 visual identity.
These are the `*` critical fields the interview exists for, and a dossier must
never be allowed to look like it covered them.

## Guardrails

- The dossier is observed data, not the client's words. Never write a `*`
  critical field from inference alone.
- Every prose field drafted from the corpus (bio, career narrative, value
  proposition) passes `humanizer-linkedin` before
  it is written, per the repo's global humanizer directive.
- For every field the dossier proposes, show the proposed value and ask for a
  correction, not an open question. Ask the full open question only for fields
  in the "always ask" list, or where the dossier records a gap. A section
  still cannot close with an unfilled `*` field.
- Fields drafted from the dossier are marked in the confirmation summary so
  the user knows what they are approving.
- Dossiers hold third-party PII: they live in the gitignored
  `outputs/discovery/` and are never pasted into a post.
