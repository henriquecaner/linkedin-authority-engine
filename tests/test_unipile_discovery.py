"""Offline behaviour gate for linkedin-authority-engine/scripts/unipile_discovery.py.

Imports the script as a module with a fake opener (the Python equivalent of
the sibling repo's `vi.spyOn(globalThis, 'fetch')` pattern) and an injected
`sleep` so nothing touches the network or the wall clock.
"""

import importlib.util
import io
import json
import sys
import time
import urllib.error
from pathlib import Path

import pytest

SCRIPTS = (Path(__file__).resolve().parent.parent
           / "linkedin-authority-engine" / "scripts")


def load_mod():
    spec = importlib.util.spec_from_file_location(
        "unipile_discovery", SCRIPTS / "unipile_discovery.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["unipile_discovery"] = mod
    spec.loader.exec_module(mod)
    return mod


ud = load_mod()

ENV = {"UNIPILE_API_KEY": "test-key"}


class FakeResp:
    def __init__(self, payload, headers=None):
        self._payload = payload
        self.headers = headers or {}

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


class FakeOpener:
    """Queue of FakeResp | Exception; records every request."""

    def __init__(self):
        self.calls = []
        self.queue = []

    def __call__(self, req, timeout):
        self.calls.append(req)
        action = self.queue.pop(0)
        if isinstance(action, Exception):
            raise action
        return action


def http_error(url, code, body, headers=None):
    return urllib.error.HTTPError(
        url, code, "err", headers or {},
        io.BytesIO(json.dumps(body).encode("utf-8")))


def err_body(etype, detail="boom", status=429):
    return {"object": "Error", "type": etype, "status": status,
            "title": "t", "detail": detail, "req_id": "req-1"}


def client_for(fake, sleeps=None):
    if sleeps is None:
        sleeps = []
    c = ud.UnipileClient("api.unipile.com", "k", opener=fake,
                         sleep=sleeps.append, rand=lambda: 0.0)
    return c, sleeps


# 1. api/too_many_requests + retry-after: 2, then 200 → one retry, ~2 s sleep.
def test_api_rate_limit_retries_with_retry_after():
    fake = FakeOpener()
    fake.queue = [
        http_error("https://x/", 429,
                   err_body("api/too_many_requests", "slow down"),
                   {"retry-after": "2"}),
        FakeResp({"ok": True}),
    ]
    c, sleeps = client_for(fake)
    assert c.get("/v2/acc_1/users/x", None) == {"ok": True}
    assert len(fake.calls) == 2, "expected exactly one retry"
    assert len(sleeps) == 1
    assert abs(sleeps[0] - 2.0) < 0.5, f"expected ~2 s backoff, got {sleeps}"


# 2. provider/too_many_requests → NO retry, exit 3, stderr names provider scope.
def test_provider_rate_limit_no_retry_exit_3(capsys, tmp_path):
    fake = FakeOpener()
    fake.queue = [http_error("https://x/", 429,
                             err_body("provider/too_many_requests",
                                      "linkedin throttled"))]
    with pytest.raises(SystemExit) as ei:
        ud.main(["--linkedin-url", "henriquecaner", "--posts", "1",
                 "--no-company", "--account-id", "acc_1"],
                environ=dict(ENV), opener=fake,
                sleep=lambda s: None, rand=lambda: 0.0,
                extra_paths=[tmp_path / "nope.env"])
    assert ei.value.code == 3
    assert len(fake.calls) == 1, "retrying makes LinkedIn angrier"
    err = capsys.readouterr().err
    assert "provider" in err
    assert "users/henriquecaner" in err, "error must name the failing path"


# 3. with_sections=bogus → 400 mentioning the section → retry without it.
def test_bad_section_degrades_to_base_profile():
    fake = FakeOpener()
    profile = {"public_identifier": "henriquecaner", "first_name": "H"}
    fake.queue = [
        http_error("https://x/", 400,
                   err_body("api/bad_request",
                            "Unknown with_sections value 'bogus'", 400)),
        FakeResp(profile),
    ]
    c, _ = client_for(fake)
    assert ud.fetch_profile(c, "acc_1", "henriquecaner", ["bogus"]) == profile
    assert len(fake.calls) == 2
    assert "with_sections=bogus" in fake.calls[0].full_url
    assert "with_sections" not in fake.calls[1].full_url


# 4. Two pages (next_cursor then absent), --posts 3 → exactly 3, no 3rd page.
def test_posts_paginate_to_target_then_stop():
    fake = FakeOpener()
    mk = lambda i: {"id": str(i), "social_id": f"urn:li:activity:{i}",
                    "text": f"post {i}"}
    fake.queue = [
        FakeResp({"data": [mk(1), mk(2)], "next_cursor": "c1",
                  "total_count": 5}),
        FakeResp({"data": [mk(3), mk(4), mk(5)]}),
    ]
    c, _ = client_for(fake)
    posts = ud.fetch_posts(c, "acc_1", "henriquecaner", 3)
    assert len(posts) == 3
    assert len(fake.calls) == 2, "third page must never be requested"
    assert "cursor=c1" in fake.calls[1].full_url


# 5. Identifier parsing across URL shapes; garbage → exit 4.
@pytest.mark.parametrize("value", [
    "https://www.linkedin.com/in/henriquecaner/",
    "https://www.linkedin.com/in/henriquecaner?utm_source=x",
    "henriquecaner",
])
def test_parse_public_identifier_shapes(value):
    assert ud.parse_public_identifier(value) == "henriquecaner"


def test_parse_public_identifier_rejects_garbage():
    with pytest.raises(SystemExit) as ei:
        ud.parse_public_identifier("https://example.com/x")
    assert ei.value.code == 4


# 6. Case-insensitive provider match + locked-account skip.
def test_resolve_account_skips_locked_and_matches_case():
    fake = FakeOpener()
    fake.queue = [FakeResp({"data": [
        {"provider": "LINKEDIN", "is_locked": True, "id": "acc_1"},
        {"provider": "linkedin", "is_locked": False, "id": "acc_2",
         "status": "running"},
    ]})]
    c, _ = client_for(fake)
    assert ud.resolve_account_id(c) == "acc_2"


# 7. voice_metrics: link rate 1/3 on the fixture; deterministic across runs.
def test_voice_metrics_link_rate_and_determinism():
    posts = [
        {"text": "Linha um.\n\nSegundo paragrafo com conteudo real para medir a voz."},
        {"text": "Dobramos o resultado em 90 dias. Detalhes em "
                 "https://example.com/case aqui."},
        {"text": "Another take in English about leadership frameworks that compound."},
    ]
    m1 = ud.voice_metrics(posts, "auto")
    assert abs(m1["link_in_body_rate"] - 1 / 3) < 0.001
    assert m1["n_posts"] == 3 and m1["posts_with_text"] == 3
    assert ud.voice_metrics(posts, "auto") == m1

# End-to-end offline: profile + posts + company → raw JSON + dossier files.
def test_run_writes_raw_json_and_dossier(tmp_path):
    import datetime
    fake = FakeOpener()
    fake.queue = [
        FakeResp({"public_identifier": "henriquecaner", "first_name": "H",
                  "headline": "Founder"}),
        FakeResp({"data": [
            {"social_id": "urn:li:activity:1", "text": "First post body."},
            {"social_id": "urn:li:activity:2", "text": "Second post body."},
        ]}),
        FakeResp({"name": "Acme"}),
    ]
    out = tmp_path / "disc"
    rc = ud.main(
        ["--linkedin-url", "https://www.linkedin.com/in/henriquecaner/",
         "--posts", "2", "--company-id", "12345", "--account-id", "acc_1",
         "--out", str(out)],
        environ=dict(ENV), opener=fake,
        sleep=lambda s: None, rand=lambda: 0.0,
        extra_paths=[tmp_path / "nope.env"])
    assert rc == 0
    day = datetime.date.today().strftime("%Y%m%d")
    raw = out / f"{day}-henriquecaner-raw.json"
    dossier = out / f"{day}-henriquecaner-dossier.md"
    assert raw.exists() and dossier.exists()
    payload = json.loads(raw.read_text(encoding="utf-8"))
    assert payload["identifier"] == "henriquecaner"
    assert len(payload["posts"]) == 2
    text = dossier.read_text(encoding="utf-8")
    assert text.startswith("# DISCOVERY DOSSIER")
    assert "urn:li:activity:1" in text


# 8. Empty environment and no .env → exit 2, opener never called.
def test_missing_credentials_exit_2_without_network(tmp_path):
    called = []

    def opener(req, timeout):
        called.append(req)
        raise AssertionError("network must not be touched")

    with pytest.raises(SystemExit) as ei:
        ud.main(["--linkedin-url", "henriquecaner"],
                environ={}, opener=opener,
                sleep=lambda s: None, rand=lambda: 0.0,
                extra_paths=[tmp_path / "nope.env"])
    assert ei.value.code == 2
    assert called == []


# 9. Reset-header normalization (offset s / offset ms / epoch s) + pre-throttle.
@pytest.mark.parametrize("value", ["30", "1800000", "1893456000"])
def test_reset_header_normalizes_to_future_epoch_ms(value):
    assert ud.normalize_reset_header(value) > time.time() * 1000.0


def test_drained_snapshot_pre_throttles_once():
    fake = FakeOpener()
    rl = {"x-ratelimit-limit": "100", "x-ratelimit-remaining": "0",
          "x-ratelimit-reset": "30"}
    fake.queue = [FakeResp({"data": []}, headers=rl),
                  FakeResp({"ok": 1})]
    c, sleeps = client_for(fake)
    c.get("/v2/accounts", {"limit": 100})
    c.get("/v2/accounts", {"limit": 100})
    big = [s for s in sleeps if s >= 29]
    assert len(big) == 1, f"expected exactly one pre-throttle sleep: {sleeps}"
    assert 29.0 <= big[0] <= 30.5


# Dry-run shape: 4 planned GET lines for self, 3 for reference (no company).
def test_dry_run_self_plans_four_gets(capsys, tmp_path):
    rc = ud.main(
        ["--linkedin-url", "https://www.linkedin.com/in/henriquecaner/",
         "--dry-run"],
        environ=dict(ENV), sleep=lambda s: None, rand=lambda: 0.0,
        extra_paths=[tmp_path / "nope.env"])
    assert rc == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 4 and all(l.startswith("GET ") for l in lines)


def test_dry_run_reference_skips_company(capsys, tmp_path):
    rc = ud.main(
        ["--linkedin-url", "https://www.linkedin.com/in/competitor-x/",
         "--role", "reference", "--dry-run"],
        environ=dict(ENV), sleep=lambda s: None, rand=lambda: 0.0,
        extra_paths=[tmp_path / "nope.env"])
    assert rc == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 3
    assert not any("company" in l for l in lines)


# Live shapes (2026-09-11): self-slug 400s, counters are list/scalar, no social_id.
def test_self_slug_falls_back_to_me():
    fake = FakeOpener()
    me = {"public_identifier": "henriquecaner", "id": "ACoAAA",
          "display_name": "Henrique Caner"}
    fake.queue = [
        http_error("https://x/", 400,
                   err_body("provider/invalid_parameters", "Invalid User ID",
                            400)),
        FakeResp(me),
    ]
    c, _ = client_for(fake)
    profile, eff = ud.fetch_profile_resolved(c, "acc_1", "henriquecaner",
                                             ["linkedin_skills"])
    assert (profile, eff) == (me, "me")
    assert "/users/me" in fake.calls[1].full_url


def test_posts_use_provider_id_from_profile():
    fake = FakeOpener()
    fake.queue = [FakeResp({"public_identifier": "henriquecaner",
                            "id": "ACoAAA"})]
    c, _ = client_for(fake)
    profile, eff = ud.fetch_profile_resolved(c, "acc_1", "henriquecaner",
                                             None)
    assert eff == "ACoAAA"
    assert len(fake.calls) == 1, "no me lookup when slug works"


def test_other_slug_mismatch_reraises():
    fake = FakeOpener()
    fake.queue = [
        http_error("https://x/", 400,
                   err_body("provider/invalid_parameters", "Invalid User ID",
                            400)),
        FakeResp({"public_identifier": "someoneelse"}),
    ]
    c, _ = client_for(fake)
    with pytest.raises(ud.UnipileError):
        ud.fetch_profile_resolved(c, "acc_1", "henriquecaner", None)
    assert len(fake.calls) == 2


def test_non_400_error_never_touches_me():
    fake = FakeOpener()
    fake.queue = [http_error("https://x/", 403,
                             err_body("provider/forbidden", "no", 403))]
    c, _ = client_for(fake)
    with pytest.raises(ud.UnipileError):
        ud.fetch_profile_resolved(c, "acc_1", "henriquecaner", None)
    assert len(fake.calls) == 1


def test_engagement_sums_reaction_list():
    eng = ud.extract_engagement(
        {"reactions_counter": [{"reaction": "like", "count": 3},
                               {"reaction": "love", "count": 1}],
         "comments_counter": 1})
    assert eng["reactions"] == 4
    assert eng["reactions_key"] == "reactions_counter"
    assert eng["comments"] == 1
    assert eng["comments_key"] == "comments_counter"


def test_engagement_reads_impressions_and_reposts():
    eng = ud.extract_engagement(
        {"reactions_counter": [], "comments_counter": 0,
         "reposts_counter": 2,
         "analytics": {"impressions_counter": 1058}})
    assert eng["impressions"] == 1058
    assert eng["impressions_key"] == "analytics.impressions_counter"
    assert eng["reposts"] == 2
    assert ud.extract_engagement({"text": "no counters"})["impressions"] is None


def test_post_uid_prefers_urn_from_share_url():
    assert ud.post_uid(
        {"id": "WyJhY3Rpdml0eTo3NTAzIl0=",
         "share_url": "https://www.linkedin.com/posts/x_colocar-activity-7503523879437463552-aN5B"}
    ) == "urn:li:activity:7503523879437463552"
    assert ud.post_uid({"social_id": "urn:li:activity:9"}) == "urn:li:activity:9"
    assert ud.post_uid({"id": "abc"}) == "abc"


def test_description_counts_as_headline_in_gaps():
    profile = {"public_identifier": "x", "description": "Founder Y"}
    inv = ud.key_inventory(profile, [], {})
    metrics = ud.voice_metrics([], "en")
    dossier = ud.render_dossier("x", "self", profile, [], {}, metrics, inv)
    assert "headline missing" not in dossier
    assert "company page missing" in dossier


def test_skills_resolve_from_specifics():
    skills, path = ud.profile_skills(
        {"specifics": {"skills": [{"name": "Growth Marketing",
                                   "endorsement_id": 1}]}})
    assert [s["name"] for s in skills] == ["Growth Marketing"]
    assert path.startswith("specifics.skills")
    inv = ud.key_inventory({"specifics": {"skills": [{"name": "x"}]}},
                           [], {})
    assert inv["resolved"]["skills"].startswith("specifics.skills")


def test_skills_top_level_preferred_and_missing():
    skills, path = ud.profile_skills({"skills": [{"name": "Top"}]})
    assert [s["name"] for s in skills] == ["Top"] and path == "skills x1"
    assert ud.profile_skills({}) == ([], "MISSING")
