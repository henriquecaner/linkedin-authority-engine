#!/usr/bin/env python3
"""
Unipile deep discovery — pull a LinkedIn member profile, recent posts and
company page through Unipile API v2, then render a raw JSON payload plus a
readable dossier for `/init` Path U.

Stdlib only. No third-party dependency.

Exit codes: 0 ok · 2 credentials / no usable account · 3 Unipile API error ·
4 unparseable LinkedIn URL.
"""

import argparse
import collections
import datetime
import json
import os
import random
import re
import socket
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import NamedTuple

try:
    import postlib
except ImportError:  # allow `import unipile_discovery` from any cwd
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import postlib

BASE_HOST = "api.unipile.com"
DEFAULT_TIMEOUT_MS = 30000
BACKOFF_SCHEDULE_S = [0.5, 2.0]
MAX_BACKOFF_S = 30.0
JITTER_S = 0.25
SPACING_BASE_S = 0.6
SPACING_RAND_S = 0.8
PRE_THROTTLE_CAP_MS = 60_000
MAX_POST_PAGES = 20
POST_PAGE_CAP = 50
ACCOUNT_PAGE_LIMIT = 100

TRANSIENT_TYPES = frozenset({
    "api/internal_error",
    "api/proxy_error",
    "api/proxy_timeout",
    "api/proxy_auth_error",
    "provider/server_error",
    "provider/timeout",
})
KEY_PROBLEM_TYPES = frozenset({
    "api/missing_authorization",
    "api/expired_authorization",
    "api/invalid_auth_format",
    "api/insufficient_permissions",
})

MEMBER_URL_RE = re.compile(r"linkedin\.com/in/([^/?#]+)", re.IGNORECASE)
COMPANY_URL_RE = re.compile(r"linkedin\.com/company/([^/?#]+)", re.IGNORECASE)
ACCOUNT_SCOPE_RE = re.compile(r"^/v2/(acc_[^/]+)/")
FIRST_PERSON_RE = re.compile(r"\b(eu|meu|minha|I|my|me)\b", re.IGNORECASE)
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]",
)

TEXT_KEYS = ("text", "commentary", "content", "body", "post.text")
DATE_KEYS = ("date", "created_at", "posted_at", "parsed_datetime")
REACTION_KEYS = ("reactions_counter", "reaction_counter", "reactions_count", "reactions")
COMMENT_KEYS = ("comments_counter", "comment_counter", "comments_count", "comments")
IMPRESSION_PATHS = ("analytics.impressions_counter", "impressions_counter",
                    "analytics.impressions", "impressions")
COMPANY_ID_PATHS = (
    "current_position.company_id",
    "current_position.company.id",
    "current_positions.0.company_id",
    "current_positions.0.company.id",
    "experience.0.company_id",
    "experience.0.company.id",
    "company.id",
    "company_id",
)

STOPWORDS = frozenset("""
a ao aos aquela aquelas aquele aqueles aquilo as ate com como da das de do dos
dos e ela elas ele eles em entre era eram essa essas esse esses esta estas este
estes foi foram ha isso isto ja lhe lhes mais mas me mesmo minha minhas meu meus
muito na nas nao nem no nos nossa nossas nosso nossos nunca o os ou para pela
pelas pelo pelos por qual quando que quem se sem ser seu seus sobre sua suas
tambem tem tenho ter teu teus tua tuas um uma uns umas voce voces vos porque
onde qual quais quanto todos toda tudo pode fazer sou sao esta estou estamos
muito pouco entre apos ate desde durante contra desde sobre sob esse essa isso
the and for with from that this have has had are was were been being will would
should could shall may might must can not but our your their his her its they
them then than when where which while with about into over after before between
through during such each other some any all both few more most what who whom
whose how why you your yours our ours them they their theirs there here when
its it’s it is are was were has have had do does did done will would can could
shall should may might must ought and the
""".split())


# -----------------------------
# Credentials
# -----------------------------

class Credentials(NamedTuple):
    host: str
    api_key: str
    account_id: str | None
    timeout_s: float


def parse_dotenv_file(path: Path) -> dict:
    """Minimal .env parser: skip blanks and `#` comments, split on the first
    `=`, strip one layer of matching quotes, ignore a leading `export`."""
    out = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return out
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        if key:
            out[key] = val
    return out


def load_credentials(environ=None, extra_paths=None) -> Credentials:
    """First hit wins per key: environ, then ./​.env, then the shared home file."""
    env = dict(environ) if environ is not None else dict(os.environ)
    if extra_paths is None:
        extra_paths = [Path.cwd() / ".env",
                       Path.home() / ".linkedin-authority-engine.env"]
    file_vals: dict = {}
    for p in extra_paths:
        vals = parse_dotenv_file(Path(p))
        for k, v in vals.items():
            file_vals.setdefault(k, v)

    def get(key, default=None):
        if key in env and env[key] not in (None, ""):
            return env[key]
        return file_vals.get(key, default)

    api_key = get("UNIPILE_API_KEY")
    if not api_key:
        checked = ["environment"] + [str(p) for p in extra_paths]
        print(
            "unipile_discovery: missing UNIPILE_API_KEY (checked: "
            + ", ".join(checked) + "). Set UNIPILE_API_KEY and optionally "
            "UNIPILE_DSN / UNIPILE_LINKEDIN_ACCOUNT_ID.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    host = get("UNIPILE_DSN", BASE_HOST) or BASE_HOST
    account_id = get("UNIPILE_LINKEDIN_ACCOUNT_ID") or None
    try:
        timeout_ms = int(get("UNIPILE_TIMEOUT_MS", str(DEFAULT_TIMEOUT_MS)))
    except (TypeError, ValueError):
        timeout_ms = DEFAULT_TIMEOUT_MS
    timeout_s = timeout_ms / 1000.0 if timeout_ms > 0 else 0.0
    return Credentials(host=host, api_key=api_key,
                       account_id=account_id, timeout_s=timeout_s)


# -----------------------------
# Errors
# -----------------------------

class UnipileError(Exception):
    def __init__(self, status: int, method: str, path: str, raw: str,
                 body: dict | None = None,
                 retry_after_ms: int | None = None):
        super().__init__(f"Unipile {method} {path} failed: {status} {raw[:200]}")
        self.status = status
        self.method = method
        self.path = path
        self.raw = raw
        self.body = body or {}
        self.type = self.body.get("type")
        self.title = self.body.get("title")
        self.detail = self.body.get("detail")
        self.req_id = self.body.get("req_id")
        self.retry_after_ms = retry_after_ms

    @property
    def rate_limit_scope(self):
        if self.status != 429:
            return None
        return "api" if self.type == "api/too_many_requests" else "provider"

    @property
    def is_transient(self) -> bool:
        if self.rate_limit_scope == "api":
            return True
        if self.type is not None and self.type in TRANSIENT_TYPES:
            return True
        return self.status >= 500 and self.type is None

    @property
    def is_key_problem(self) -> bool:
        if self.type is not None and self.type in KEY_PROBLEM_TYPES:
            return True
        return self.status == 401 and self.type is None

    @property
    def is_subscription_problem(self) -> bool:
        return self.type == "api/inactive_subscription"


class IdentifierError(ValueError):
    pass


def _fail_identifier(value: str, kind: str) -> None:
    print(f"unipile_discovery: unparseable LinkedIn {kind} URL: {value!r}",
          file=sys.stderr)
    raise SystemExit(4)


# -----------------------------
# Rate-limit helpers
# -----------------------------

def normalize_reset_header(val, now_ms: float | None = None) -> int | None:
    """Normalize `x-ratelimit-reset` to epoch-ms. Accepts seconds-offset,
    ms-offset, or epoch (seconds or ms) — same three-branch heuristic as the
    sibling engine: >1e12 already epoch ms; >1e9 epoch seconds; else offset."""
    if val is None:
        return None
    try:
        n = float(str(val).strip())
    except (ValueError, TypeError):
        return None
    if not (n > 0):
        return None
    now = now_ms if now_ms is not None else time.time() * 1000.0
    if n > 1_000_000_000_000:
        return int(n)
    if n > 1_000_000_000:
        return int(n * 1000)
    return int(now + n * 1000)


def parse_retry_after_ms(val) -> int | None:
    if val is None:
        return None
    s = str(val).strip()
    try:
        n = float(s)
        if n >= 0:
            return int(n * 1000)
    except ValueError:
        pass
    try:
        ts = datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z")
        ts = ts.replace(tzinfo=datetime.timezone.utc)
        diff = ts.timestamp() * 1000 - time.time() * 1000
        return int(max(diff, 0))
    except ValueError:
        return None


def _get_header(headers, name: str):
    if headers is None:
        return None
    try:
        v = headers.get(name)
        if v is not None:
            return v
    except (AttributeError, TypeError):
        pass
    try:
        items = headers.items()
    except AttributeError:
        return None
    lname = name.lower()
    for k, v in items:
        if str(k).lower() == lname:
            return v
    return None


# -----------------------------
# HTTP client
# -----------------------------

class UnipileClient:
    def __init__(self, host: str, api_key: str, timeout_s: float = 30.0,
                 max_retries: int = 2, opener=None, sleep=None,
                 rand=None):
        self.host = host
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self._opener = opener
        self._sleep = sleep if sleep is not None else time.sleep
        self._rand = rand if rand is not None else random.random
        self._snapshots: dict = {}
        self._warned_windows: set = set()
        self._calls = 0

    def _do_open(self, req, timeout_s):
        if self._opener is not None:
            return self._opener(req, timeout_s)
        if timeout_s and timeout_s > 0:
            return urllib.request.urlopen(req, timeout=timeout_s)
        return urllib.request.urlopen(req)

    def _record_rate_limit(self, scope: str, headers) -> None:
        limit = _get_header(headers, "x-ratelimit-limit")
        remaining = _get_header(headers, "x-ratelimit-remaining")
        reset = _get_header(headers, "x-ratelimit-reset")
        try:
            limit_n = int(float(limit)) if limit is not None else None
        except (ValueError, TypeError):
            limit_n = None
        try:
            rem_n = int(float(remaining)) if remaining is not None else None
        except (ValueError, TypeError):
            rem_n = None
        reset_at = normalize_reset_header(reset)
        if limit_n is None and rem_n is None and reset_at is None:
            return
        self._snapshots[scope] = {"limit": limit_n, "remaining": rem_n,
                                  "reset_at": reset_at,
                                  "at": time.time() * 1000.0}
        if rem_n is not None and rem_n <= 2 and reset_at is not None:
            key = (scope, reset_at)
            if key not in self._warned_windows:
                self._warned_windows.add(key)
                print(
                    f"unipile_discovery: rate limit nearly exhausted for "
                    f"{scope}: remaining={rem_n}",
                    file=sys.stderr,
                )

    def _pre_throttle(self, scope: str) -> None:
        snap = self._snapshots.get(scope)
        if not snap or snap.get("remaining") != 0:
            return
        reset_at = snap.get("reset_at")
        if not reset_at:
            return
        wait_ms = min(reset_at - time.time() * 1000.0, PRE_THROTTLE_CAP_MS)
        if wait_ms > 0:
            self._sleep(wait_ms / 1000.0)

    def get(self, path: str, query: dict | None = None) -> dict:
        # 1. Build the URL, dropping None query values.
        parts = urllib.parse.urlencode(
            {k: v for k, v in (query or {}).items() if v is not None})
        url = f"https://{self.host}{path}" + (f"?{parts}" if parts else "")
        # 2. Rate-limit scope: the account in the path, else global.
        m = ACCOUNT_SCOPE_RE.match(path)
        scope = m.group(1) if m else "global"
        # Every request here is a GET, so retrying on transient errors is
        # safe. Never copy this retry policy onto a POST without an
        # idempotency story (a retried POST can duplicate a side effect).
        # 4. Jittered spacing from the second call onward: spread actions
        # with random delays, never burst (audit-doc rule). Once per get(),
        # not per retry attempt, so backoff accounting stays exact.
        if self._calls > 0:
            self._sleep(SPACING_BASE_S + self._rand() * SPACING_RAND_S)
        self._calls += 1
        for attempt in range(self.max_retries + 1):
            # 3. Pre-throttle on a drained snapshot for this scope.
            self._pre_throttle(scope)
            req = urllib.request.Request(
                url,
                headers={"X-API-KEY": self.api_key,
                         "accept": "application/json"},
                method="GET",
            )
            try:
                resp = self._do_open(req, self.timeout_s)
            except urllib.error.HTTPError as e:
                headers = getattr(e, "headers", None)
                self._record_rate_limit(scope, headers)
                try:
                    raw_bytes = e.read()
                except Exception:
                    raw_bytes = b""
                raw = (raw_bytes.decode("utf-8", "replace")
                       if isinstance(raw_bytes, bytes) else str(raw_bytes))
                try:
                    parsed = json.loads(raw) if raw else None
                    body = parsed if isinstance(parsed, dict) else None
                except (ValueError, TypeError):
                    body = None
                retry_after = parse_retry_after_ms(
                    _get_header(headers, "retry-after"))
                err = UnipileError(e.code, "GET", path, raw,
                                   body=body, retry_after_ms=retry_after)
                if (attempt < self.max_retries
                        and (err.is_transient
                             or err.rate_limit_scope == "api")):
                    backoff = (BACKOFF_SCHEDULE_S[attempt]
                               if attempt < len(BACKOFF_SCHEDULE_S)
                               else BACKOFF_SCHEDULE_S[-1])
                    base = (err.retry_after_ms / 1000.0
                            if err.retry_after_ms is not None else backoff)
                    self._sleep(min(base + self._rand() * JITTER_S,
                                    MAX_BACKOFF_S))
                    continue
                raise err
            except (urllib.error.URLError, socket.timeout,
                    TimeoutError, ConnectionError, OSError) as e:
                if attempt < self.max_retries:
                    backoff = (BACKOFF_SCHEDULE_S[attempt]
                               if attempt < len(BACKOFF_SCHEDULE_S)
                               else BACKOFF_SCHEDULE_S[-1])
                    self._sleep(min(backoff + self._rand() * JITTER_S,
                                    MAX_BACKOFF_S))
                    continue
                raise UnipileError(0, "GET", path, f"network/timeout: {e}",
                                   body={"type": "api/timeout",
                                         "title": "Network or timeout",
                                         "detail": str(e)})
            # 6. Record rate-limit headers on every response, ok or not.
            headers = getattr(resp, "headers", None)
            if headers is None and hasattr(resp, "info"):
                try:
                    headers = resp.info()
                except Exception:
                    headers = None
            self._record_rate_limit(scope, headers)
            try:
                payload = resp.read()
            except Exception:
                payload = b""
            if isinstance(payload, bytes):
                payload = payload.decode("utf-8", "replace")
            if not payload:
                return {}
            try:
                data = json.loads(payload)
            except ValueError:
                return {}
            return data if isinstance(data, dict) else {}
        raise UnipileError(0, "GET", path, "retry loop exhausted",
                           body={"type": "api/timeout"})


# -----------------------------
# Account resolution
# -----------------------------

def resolve_account_id(client: UnipileClient) -> str:
    seen: list = []
    offset = 0
    for _ in range(20):
        q = {"limit": ACCOUNT_PAGE_LIMIT}
        if offset > 0:
            q["offset"] = offset
        data = client.get("/v2/accounts", q)
        items = data.get("data") or []
        seen.extend(items)
        if not data.get("has_more") or not items:
            break
        offset += len(items)
    linked = [a for a in seen
              if str(a.get("provider", "")).lower() == "linkedin"
              and a.get("is_locked") is not True]
    if not linked:
        print(
            "unipile_discovery: no usable LinkedIn account. Connect one via "
            "Hosted Auth in the reach-sales-outreach engine "
            "(npm run connect -- linkedin BR) and put the resulting acc_... "
            "in UNIPILE_LINKEDIN_ACCOUNT_ID.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    chosen = linked[0]
    if chosen.get("status") not in (None, "running"):
        print(
            f"unipile_discovery: warning: account {chosen.get('id')} status "
            f"is {chosen.get('status')!r} (expected 'running') — a reconnect "
            f"may be needed; continuing anyway.",
            file=sys.stderr,
        )
    if len(linked) > 1:
        ids = ", ".join(str(a.get("id")) for a in linked)
        print(
            f"unipile_discovery: {len(linked)} LinkedIn accounts found "
            f"({ids}); using {chosen.get('id')}. Pin one with --account-id.",
            file=sys.stderr,
        )
    return chosen["id"]


# -----------------------------
# Identifier parsing
# -----------------------------

def parse_public_identifier(value: str) -> str:
    v = (value or "").strip()
    m = MEMBER_URL_RE.search(v)
    if m:
        return urllib.parse.unquote(m.group(1).strip().rstrip("/"))
    if v and "/" not in v:
        return urllib.parse.unquote(v)
    _fail_identifier(value, "member")
    raise SystemExit(4)  # unreachable; keeps type-checkers calm


def parse_company_identifier(value: str) -> str:
    v = (value or "").strip()
    m = COMPANY_URL_RE.search(v)
    if m:
        return urllib.parse.unquote(m.group(1).strip().rstrip("/"))
    if v and "/" not in v:
        return urllib.parse.unquote(v)
    _fail_identifier(value, "company")
    raise SystemExit(4)  # unreachable


# -----------------------------
# Defensive field access
# -----------------------------

def pick(obj, *paths, default=None):
    """Walk dotted paths over dicts (and integer-indexable lists); return the
    first non-empty value. Python form of the upstream `a ?? b` idiom."""
    for path in paths:
        cur = obj
        ok = True
        for bit in str(path).split("."):
            if isinstance(cur, dict):
                if bit not in cur:
                    ok = False
                    break
                cur = cur[bit]
            elif isinstance(cur, (list, tuple)):
                try:
                    cur = cur[int(bit)]
                except (ValueError, IndexError):
                    ok = False
                    break
            else:
                ok = False
                break
        if ok and cur not in (None, "", [], {}):
            return cur
    return default


# -----------------------------
# Fetchers
# -----------------------------

def fetch_profile(client: UnipileClient, account_id: str, identifier: str,
                  sections: list | None = None) -> dict:
    sections = sections or ["linkedin_skills"]
    path = (f"/v2/{urllib.parse.quote(account_id)}/users/"
            f"{urllib.parse.quote(identifier)}")
    query = {"with_sections": ",".join(sections)} if sections else None
    try:
        return client.get(path, query)
    except UnipileError as e:
        blob = f"{e.detail or ''}\n{e.raw or ''}".lower()
        if (e.status in (400, 404, 422) and query
                and ("section" in blob or "with_sections" in blob)):
            print(
                f"unipile_discovery: warning: server rejected "
                f"with_sections={query['with_sections']!r}; retrying with a "
                f"base profile.",
                file=sys.stderr,
            )
            return client.get(path, None)
        raise


def fetch_profile_resolved(client: UnipileClient, account_id: str,
                           identifier: str,
                           sections: list | None = None) -> tuple:
    """Profile plus the identifier to use for posts. Live quirk
    (2026-09-11): looking up your own slug 400s with
    `provider/invalid_parameters` (third-party slugs work). On that exact
    error, compare against `users/me` and fall over to `me` on match."""
    try:
        profile = fetch_profile(client, account_id, identifier, sections)
    except UnipileError as e:
        if not (e.status == 400 and e.type == "provider/invalid_parameters"):
            raise
        acc = urllib.parse.quote(account_id)
        query = ({"with_sections": ",".join(sections)}
                 if sections else None)
        try:
            me = client.get(f"/v2/{acc}/users/me", query)
        except UnipileError:
            me = client.get(f"/v2/{acc}/users/me", None)
        if (str(me.get("public_identifier") or "").lower()
                == identifier.lower()):
            print("unipile_discovery: self-lookup by slug is rejected by "
                  "the provider; using users/me for this profile.",
                  file=sys.stderr)
            return me, "me"
        raise
    # Posts reject slugs on some routes even when the profile fetch accepts
    # them (live 2026-09-11): prefer the provider id from the payload.
    return profile, profile.get("id") or identifier

def fetch_posts(client: UnipileClient, account_id: str, identifier: str,
                target: int, page_cap: int = POST_PAGE_CAP) -> list:
    """Cursor pagination: stop on empty page, missing next_cursor, total_count
    reached, or MAX_POST_PAGES. Slice to target (providers may overshoot)."""
    out: list = []
    cursor = None
    total = None
    path = (f"/v2/{urllib.parse.quote(account_id)}/users/"
            f"{urllib.parse.quote(identifier)}/posts")
    for _ in range(MAX_POST_PAGES):
        remaining = target - len(out)
        if remaining <= 0 or target <= 0:
            break
        q: dict = {"limit": min(remaining, page_cap)}
        if cursor:
            q["cursor"] = cursor
        data = client.get(path, q)
        items = data.get("data")
        if items is None:
            items = data.get("items", [])
        out.extend(items or [])
        total = data.get("total_count", total)
        cursor = data.get("next_cursor")
        if not items or not cursor:
            break
        if total is not None and len(out) >= total:
            break
    return out[:target]


def find_company_id(profile: dict) -> str | None:
    val = pick(profile, *COMPANY_ID_PATHS)
    if val is None:
        return None
    if isinstance(val, dict):
        return val.get("id") or val.get("company_id")
    return str(val)


def fetch_company(client: UnipileClient, account_id: str,
                  company_id: str) -> dict:
    path = (f"/v2/{urllib.parse.quote(account_id)}/linkedin/company/"
            f"{urllib.parse.quote(company_id)}")
    try:
        return client.get(path, None)
    except UnipileError as e:
        if e.status == 404 and not re.fullmatch(r"\d+", company_id or ""):
            print(
                f"unipile_discovery: company lookup 404 for slug-shaped id "
                f"{company_id!r} — this route may accept only numeric ids; "
                f"continuing without company data.",
                file=sys.stderr,
            )
            return {}
        raise


# -----------------------------
# Post extractors (candidate key lists — unverified upstream)
# -----------------------------

def extract_post_text(post: dict) -> tuple:
    for key in TEXT_KEYS:
        if "." in key:
            val = pick(post, key)
        else:
            val = post.get(key) if isinstance(post, dict) else None
        if isinstance(val, str) and val.strip():
            return val, key
    return "", None


def extract_post_date(post: dict) -> tuple:
    for key in DATE_KEYS:
        val = post.get(key) if isinstance(post, dict) else None
        if val not in (None, ""):
            return val, key
    return None, None


def _sum_counts(val):
    """Collapse a counter to a number. Live shape (2026-09-11): reactions
    arrive as a list of {reaction, count}; comments arrive as a scalar."""
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, list):
        return sum(x.get("count", 0) for x in val
                   if isinstance(x, dict)
                   and isinstance(x.get("count"), (int, float)))
    return pick(val, "total", "count", default=val)

def extract_engagement(post: dict) -> dict:
    """Per-post engagement. Live (2026-09-11): `analytics.impressions_counter`
    IS returned for the account owner's own posts — impressions are not
    UI-only, so a performance loop can read them here instead of scraping."""
    out = {"reactions": None, "reactions_key": None,
           "comments": None, "comments_key": None,
           "impressions": None, "impressions_key": None,
           "reposts": None}
    if not isinstance(post, dict):
        return out
    for key in REACTION_KEYS:
        val = post.get(key)
        if val not in (None, ""):
            out["reactions"] = _sum_counts(val)
            out["reactions_key"] = key
            break
    for key in COMMENT_KEYS:
        val = post.get(key)
        if val not in (None, ""):
            out["comments"] = _sum_counts(val)
            out["comments_key"] = key
            break
    for key in IMPRESSION_PATHS:
        val = pick(post, key)
        if isinstance(val, (int, float)):
            out["impressions"] = val
            out["impressions_key"] = key
            break
    reposts = post.get("reposts_counter")
    if isinstance(reposts, (int, float)):
        out["reposts"] = reposts
    return out

def post_uid(post: dict):
    """Best display id: live shape has no `social_id`; the base64 `id`
    decodes to ["activity:<n>"] and `share_url` carries activity-<n>."""
    if not isinstance(post, dict):
        return None
    if post.get("social_id"):
        return post["social_id"]
    m = re.search(r"activity-(\d+)", str(post.get("share_url") or ""))
    if m:
        return f"urn:li:activity:{m.group(1)}"
    return post.get("id")


def _hook_of(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines[:3])


def _closing_of(text: str) -> str:
    return "\n".join(text.split("\n")[-5:])


def _fold_token(tok: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", tok.lower())
                   if not unicodedata.combining(c))


# -----------------------------
# Corpus measurement (postlib primitives only)
# -----------------------------

def voice_metrics(posts: list, lang: str = "auto") -> dict:
    texts = []
    for p in posts:
        if isinstance(p, str):
            texts.append(p)
        else:
            t, _ = extract_post_text(p or {})
            texts.append(t)
    n = len(texts)
    with_text = [t for t in texts if t.strip()]
    eff_lang = lang
    if lang == "auto":
        eff_lang = postlib.detect_language("\n".join(with_text)) if with_text else "en"

    chars = [postlib.count_chars(t) for t in with_text]
    if chars:
        mean_c = sum(chars) / len(chars)
        srt = sorted(chars)
        mid = len(srt) // 2
        median_c = (srt[mid] if len(srt) % 2 == 1
                    else (srt[mid - 1] + srt[mid]) / 2)
        outside = sum(1 for c in chars
                      if c < postlib.SPECS["chars_min"]
                      or c > postlib.SPECS["chars_max"])
        chars_m = {"mean": round(mean_c, 1), "median": median_c,
                   "min": min(chars), "max": max(chars),
                   "outside_spec": outside}
    else:
        chars_m = {"mean": 0, "median": 0, "min": 0, "max": 0,
                   "outside_spec": 0}

    para_counts = [postlib.count_paragraphs(t) for t in with_text]
    all_paras: list = []
    for t in with_text:
        all_paras.extend(postlib.split_paragraphs(t))
    para_char_counts = [len(p) for p in all_paras]
    dense_share = (sum(1 for c in para_char_counts
                       if c > postlib.SPECS["dense_paragraph_chars"])
                   / len(para_char_counts)) if para_char_counts else 0.0
    paras_m = {
        "mean_count": round(sum(para_counts) / len(para_counts), 2) if para_counts else 0,
        "mean_chars_per_paragraph": (
            round(sum(para_char_counts) / len(para_char_counts), 1)
            if para_char_counts else 0),
        "share_dense": round(dense_share, 3),
    }

    awls = [postlib.avg_word_length(t) for t in with_text]
    awl_mean = round(sum(awls) / len(awls), 2) if awls else 0.0

    def share(pred):
        return round(sum(1 for t in with_text if pred(t)) / len(with_text), 3) if with_text else 0.0

    hashtags = [postlib.count_hashtags(t) for t in with_text]
    hashtag_mean = round(sum(hashtags) / len(hashtags), 2) if hashtags else 0.0

    punished, cliches = [], []
    saves: dict = {}
    pow_n = auth_n = 0
    cta_mix: dict = {}
    for i, t in enumerate(with_text):
        hook = _hook_of(t)
        fp = postlib.find_punished(t, eff_lang)
        if fp:
            punished.append({"post": i, "matches": fp})
        fa = postlib.find_ai_cliches(t, eff_lang)
        if fa:
            cliches.append({"post": i, "matches": fa})
        for label in postlib.find_saves(t, eff_lang):
            saves[label] = saves.get(label, 0) + 1
        if postlib.has_proof_of_work(hook, eff_lang):
            pow_n += 1
        if postlib.has_authority(hook, eff_lang):
            auth_n += 1
        for cta in postlib.find_ctas(_closing_of(t), eff_lang):
            cta_mix[cta] = cta_mix.get(cta, 0) + 1

    # Top terms: tokens >= 4 chars, PT+EN stopwords removed, accent-folded.
    counter: collections.Counter = collections.Counter()
    seen_form: dict = {}
    word_re = re.compile(postlib._WORD_RE if hasattr(postlib, "_WORD_RE")
                         else r"[a-záàâãéèêíïóôõöúüçñ]+")
    for t in with_text:
        for tok in word_re.findall(t.lower()):
            if len(tok) < 4 or tok in STOPWORDS:
                continue
            folded = _fold_token(tok)
            if len(folded) < 4 or folded in STOPWORDS:
                continue
            counter[folded] += 1
            seen_form.setdefault(folded, tok)
    top_terms = [{"term": seen_form[k], "count": c}
                 for k, c in sorted(counter.items(),
                                    key=lambda kv: (-kv[1], kv[0]))[:20]]

    first_lines = []
    for t in with_text:
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        first_lines.append(lines[0] if lines else "")

    dates = []
    for p in posts:
        if isinstance(p, dict):
            d, _ = extract_post_date(p)
            if d not in (None, ""):
                dates.append(str(d))
    date_range = ({"earliest": min(dates), "latest": max(dates),
                   "n_dated": len(dates)} if dates else None)

    denom = len(with_text) if with_text else 1
    return {
        "language": eff_lang,
        "n_posts": n,
        "posts_with_text": len(with_text),
        "date_range": date_range,
        "chars": chars_m,
        "paragraphs": paras_m,
        "avg_word_length_mean": awl_mean,
        "emoji_rate": share(lambda t: bool(EMOJI_RE.search(t))),
        "hashtag_mean": hashtag_mean,
        "question_rate": share(lambda t: "?" in t),
        "first_person_rate": share(lambda t: bool(FIRST_PERSON_RE.search(t))),
        "link_in_body_rate": share(postlib.has_link_in_body),
        "punished_hooks": punished,
        "ai_cliche_hooks": cliches,
        "saves_triggers": saves,
        "proof_of_work_rate": round(pow_n / denom, 3) if with_text else 0.0,
        "authority_rate": round(auth_n / denom, 3) if with_text else 0.0,
        "cta_mix": cta_mix,
        "top_terms": top_terms,
        "first_lines": first_lines,
    }


# -----------------------------
# Key inventory
# -----------------------------

def profile_skills(profile: dict) -> tuple:
    """(skills_list, path). Live (2026-09-11): `with_sections=linkedin_skills`
    nests skills under `specifics.skills` as [{name, endorsement_id, ...}];
    top-level `skills` is accepted as a fallback."""
    if not isinstance(profile, dict):
        return [], "MISSING"
    top = profile.get("skills")
    if isinstance(top, list) and top:
        return top, f"skills x{len(top)}"
    spec = profile.get("specifics")
    nested = spec.get("skills") if isinstance(spec, dict) else None
    if isinstance(nested, list) and nested:
        return nested, f"specifics.skills x{len(nested)}"
    if isinstance(top, list):
        return [], "skills (empty)"
    if isinstance(nested, list):
        return [], "specifics.skills (empty)"
    return [], "MISSING"

def key_inventory(profile: dict, posts: list, company: dict) -> dict:
    first_post = posts[0] if posts and isinstance(posts[0], dict) else {}
    _, text_key = extract_post_text(first_post) if first_post else ("", None)
    _, date_key = extract_post_date(first_post) if first_post else (None, None)
    eng = extract_engagement(first_post) if first_post else {}
    return {
        "profile_keys": sorted(profile.keys()) if isinstance(profile, dict) else [],
        "post_keys": sorted(first_post.keys()) if isinstance(first_post, dict) else [],
        "company_keys": sorted(company.keys()) if isinstance(company, dict) else [],
        "resolved": {
            "extract_post_text": text_key or "MISSING",
            "extract_post_date": date_key or "MISSING",
            "extract_engagement.reactions": eng.get("reactions_key") or "MISSING",
            "extract_engagement.comments": eng.get("comments_key") or "MISSING",
            "extract_engagement.impressions": eng.get("impressions_key") or "MISSING (UI-only for this viewer)",
            "find_company_id": "HIT" if find_company_id(profile) else "MISSING",
            "skills": profile_skills(profile)[1],
        },
    }


# -----------------------------
# Rendering
# -----------------------------

def _display_name(profile: dict) -> str:
    if not isinstance(profile, dict):
        return "Unknown"
    full = " ".join(x for x in
                    [profile.get("first_name"), profile.get("last_name")] if x)
    return profile.get("display_name") or full or profile.get("name") or "Unknown"


def render_dossier(identifier: str, role: str, profile: dict, posts: list,
                   company: dict, metrics: dict, inventory: dict) -> str:
    name = _display_name(profile)
    lines = [f"# DISCOVERY DOSSIER — {name} ({identifier})", ""]
    lines += ["## Identity", ""]
    for k in ("display_name", "first_name", "last_name", "public_identifier",
              "id", "location", "followers_count", "profile_url",
              "is_premium", "is_verified"):
        v = profile.get(k)
        if v not in (None, ""):
            lines.append(f"- {k}: {v}")
    lines += ["", "## Headline & About", ""]
    lines.append(str(profile.get("description") or profile.get("headline")
                     or "(empty)"))
    if profile.get("bio"):
        lines += ["", str(profile["bio"])]
    lines += ["", "## Experience & education", ""]
    exp = (profile.get("experience") or profile.get("positions")
           or profile.get("current_position"))
    lines.append(json.dumps(exp, ensure_ascii=False)[:3000]
                 if exp else "(not provided by the profile payload — cover in interview)")
    lines += ["", "## Skills", ""]
    skills, _ = profile_skills(profile)
    if skills:
        for s in skills[:30]:
            if isinstance(s, dict):
                n = s.get("endorsement_count")
                lines.append(f"- {s.get('name')}"
                             + (f" (endorsements: {n})" if n else ""))
            else:
                lines.append(f"- {s}")
    else:
        lines.append("(none in payload)")
    lines += ["", "## Company", ""]
    if company:
        lines.append(json.dumps(company, ensure_ascii=False)[:2000])
    else:
        lines.append("GAP: no company data — re-run with --company-id or "
                     "--company-url.")
    lines += ["", "## Post corpus", ""]
    if not posts:
        lines.append("(no posts fetched)")
    for i, p in enumerate(posts):
        text, _ = extract_post_text(p if isinstance(p, dict) else {})
        date, _ = extract_post_date(p if isinstance(p, dict) else {})
        eng = extract_engagement(p if isinstance(p, dict) else {})
        sid = post_uid(p) if isinstance(p, dict) else None
        first = next((l.strip() for l in text.split("\n") if l.strip()), "")
        lines.append(
            f"- post {i + 1} ({sid or 'no-id'}): date={date or '?'} · "
            f"chars={len(text.strip())} · "
            f"paras={postlib.count_paragraphs(text) if text else 0} · "
            f"reactions={eng.get('reactions')} · comments={eng.get('comments')} · "
            f"reposts={eng.get('reposts')} · impressions={eng.get('impressions')} · "
            f"first line: {first[:140]}")
    lines += ["", "## Voice metrics", ""]
    lines.append(f"- n_posts: {metrics['n_posts']} "
                 f"(with text: {metrics['posts_with_text']}) · "
                 f"language: {metrics['language']}")
    c = metrics["chars"]
    lines.append(f"- chars: mean {c['mean']}, median {c['median']}, "
                 f"min {c['min']}, max {c['max']}, "
                 f"outside 1250-2500 spec: {c['outside_spec']}")
    pg = metrics["paragraphs"]
    lines.append(f"- paragraphs: mean count {pg['mean_count']}, mean chars "
                 f"per paragraph {pg['mean_chars_per_paragraph']}, dense "
                 f"share {pg['share_dense']}")
    lines.append(f"- avg_word_length: {metrics['avg_word_length_mean']} · "
                 f"emoji_rate: {metrics['emoji_rate']} · "
                 f"hashtag_mean: {metrics['hashtag_mean']} · "
                 f"question_rate: {metrics['question_rate']} · "
                 f"first_person_rate: {metrics['first_person_rate']}")
    lines.append(f"- link_in_body_rate: {metrics['link_in_body_rate']} "
                 f"(360Brew: links belong in the 1st comment)")
    lines.append(f"- proof_of_work_rate: {metrics['proof_of_work_rate']} · "
                 f"authority_rate: {metrics['authority_rate']}")
    lines += ["", "## Top terms", ""]
    for t in metrics["top_terms"]:
        lines.append(f"- {t['term']} ({t['count']})")
    if not metrics["top_terms"]:
        lines.append("(none)")
    lines += ["", "## 360Brew violations found", ""]
    lines.append(f"- punished hooks live: {metrics['punished_hooks'] or 'none'}")
    lines.append(f"- AI-cliche hooks live: {metrics['ai_cliche_hooks'] or 'none'}")
    lines.append(f"- save triggers: {metrics['saves_triggers'] or 'none'} · "
                 f"cta_mix: {metrics['cta_mix'] or 'none'}")
    lines += ["", "## Gaps", ""]
    gaps = []
    if not company:
        gaps.append("company page missing")
    if metrics["posts_with_text"] < metrics["n_posts"]:
        gaps.append(f"{metrics['n_posts'] - metrics['posts_with_text']} "
                    "posts had no extractable text")
    if not (profile.get("headline") or profile.get("description")):
        gaps.append("headline missing")
    lines.append("- " + "\n- ".join(gaps) if gaps else "(none)")
    lines += ["", "## Key inventory", ""]
    lines.append(f"- profile keys: {', '.join(inventory['profile_keys']) or '(none)'}")
    lines.append(f"- post keys: {', '.join(inventory['post_keys']) or '(none)'}")
    lines.append(f"- company keys: {', '.join(inventory['company_keys']) or '(none)'}")
    for k, v in inventory["resolved"].items():
        lines.append(f"- {k} → {v}")
    lines.append("")
    return "\n".join(lines)


# -----------------------------
# CLI
# -----------------------------

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Pull a LinkedIn profile + posts + company via Unipile v2.")
    ap.add_argument("--linkedin-url", required=True)
    ap.add_argument("--role", default="self", choices=["self", "reference"])
    ap.add_argument("--posts", type=int, default=None)
    ap.add_argument("--sections", default="linkedin_skills")
    ap.add_argument("--company-url", default=None)
    ap.add_argument("--company-id", default=None)
    ap.add_argument("--no-company", action="store_true")
    ap.add_argument("--account-id", default=None)
    ap.add_argument("--out", default="outputs/discovery")
    ap.add_argument("--lang", default="auto", choices=["auto", "pt", "en"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--show-keys", action="store_true")
    return ap


def planned_lines(args, identifier: str, account_id: str | None) -> list:
    acc = account_id or "<account_id>"
    base = f"/v2/{acc}/users/{identifier}"
    q_sec = f"?with_sections={args.sections}" if args.sections else ""
    n = args.posts if args.posts is not None else (
        10 if args.role == "reference" else 30)
    no_company = (args.no_company or
                  (args.role == "reference" and not args.company_url
                   and not args.company_id))
    out = [
        f"GET /v2/accounts?limit={ACCOUNT_PAGE_LIMIT}",
        f"GET {base}{q_sec}",
        f"GET {base}/posts?limit={min(n, POST_PAGE_CAP)}",
    ]
    if not no_company:
        cid = args.company_id or "<company-from-profile>"
        if args.company_url and not args.company_id:
            try:
                cid = parse_company_identifier(args.company_url)
            except SystemExit:
                cid = "<company-from-profile>"
        out.append(f"GET /v2/{acc}/linkedin/company/{cid}")
    return out


def main(argv=None, environ=None, opener=None, sleep=None,
         rand=None, extra_paths=None) -> int:
    args = build_parser().parse_args(argv)
    creds = load_credentials(environ if environ is not None else os.environ,
                             extra_paths=extra_paths)
    identifier = parse_public_identifier(args.linkedin_url)
    target = args.posts if args.posts is not None else (
        10 if args.role == "reference" else 30)
    no_company = (args.no_company or
                  (args.role == "reference" and not args.company_url
                   and not args.company_id))
    sections = [s for s in (args.sections or "").split(",") if s.strip()]

    if args.dry_run:
        for line in planned_lines(args, identifier,
                                  args.account_id or creds.account_id):
            print(line)
        return 0

    client = UnipileClient(creds.host, creds.api_key,
                           timeout_s=creds.timeout_s,
                           opener=opener, sleep=sleep or time.sleep,
                           rand=rand or random.random)
    try:
        account_id = args.account_id or creds.account_id or resolve_account_id(client)
        profile, eff_id = fetch_profile_resolved(client, account_id,
                                                 identifier, sections)
        posts = fetch_posts(client, account_id, eff_id, target)
        company: dict = {}
        if not no_company:
            cid = args.company_id
            if not cid and args.company_url:
                cid = parse_company_identifier(args.company_url)
            if not cid:
                cid = find_company_id(profile)
            if cid:
                company = fetch_company(client, account_id, cid) or {}
            else:
                print("unipile_discovery: no company id found in profile — "
                      "recording a gap; re-run with --company-id.",
                      file=sys.stderr)
    except UnipileError as e:
        scope = e.rate_limit_scope
        print(f"unipile_discovery: Unipile API error: status={e.status} "
              f"type={e.type} detail={e.detail} req_id={e.req_id} "
              f"scope={scope} path={e.path}", file=sys.stderr)
        raise SystemExit(3)

    metrics = voice_metrics(posts, args.lang)
    inventory = key_inventory(profile, posts, company)
    payload = {
        "fetched_at": datetime.datetime.now(
            datetime.timezone.utc).isoformat(),
        "account_id": account_id,
        "identifier": identifier,
        "role": args.role,
        "profile": profile,
        "posts": posts,
        "company": company,
    }
    if args.show_keys:
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    day = datetime.date.today().strftime("%Y%m%d")
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", identifier) or "profile"
    (outdir / f"{day}-{safe}-raw.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / f"{day}-{safe}-dossier.md").write_text(
        render_dossier(identifier, args.role, profile, posts, company,
                       metrics, inventory), encoding="utf-8")
    print(f"wrote {day}-{safe}-raw.json + {day}-{safe}-dossier.md in {outdir}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
