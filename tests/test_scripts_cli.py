import json
import subprocess
import sys
import pathlib

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"
FIX_EN = FIXTURES / "post_example.txt"
FIX_PT = FIXTURES / "post_example_pt.txt"


def _run(plugin_dir, *args):
    """Run a script with the given arguments and return the subprocess result."""
    script = plugin_dir / "scripts" / args[0]
    return subprocess.run(
        [sys.executable, str(script), *args[1:]],
        capture_output=True,
        text=True,
    )


def _json(plugin_dir, *args):
    r = _run(plugin_dir, *args)
    return r, json.loads(r.stdout)


# --- smoke tests: scripts run on valid EN and PT posts ---

def test_validate_specs_runs_en(plugin_dir):
    r = _run(plugin_dir, "validate_specs.py", str(FIX_EN))
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


def test_validate_specs_runs_pt(plugin_dir):
    r = _run(plugin_dir, "validate_specs.py", str(FIX_PT))
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


def test_score_post_runs(plugin_dir):
    r = _run(plugin_dir, "score_post.py", str(FIX_EN), "--objective", "authority")
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


def test_suggest_hooks_runs(plugin_dir):
    r = _run(
        plugin_dir, "suggest_hooks.py",
        "--category", "achievement", "--objective", "authority", "--topic", "B2B sales",
    )
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


# --- behavior tests: the matchers must actually FIRE per language ---

def test_language_autodetect(plugin_dir):
    _, en = _json(plugin_dir, "score_post.py", str(FIX_EN), "--json")
    _, pt = _json(plugin_dir, "score_post.py", str(FIX_PT), "--json")
    assert en["language"] == "en"
    assert pt["language"] == "pt"


def test_pt_proof_of_work_fires(plugin_dir):
    """The PT fixture hook ('Perdi R$40 mil... testando') must trigger proof-of-work."""
    _, pt = _json(plugin_dir, "score_post.py", str(FIX_PT), "--json")
    hook_fb = " ".join(pt["dimensions"]["hook"]["feedback"])
    assert "Proof of work detected" in hook_fb


def test_en_proof_of_work_fires(plugin_dir):
    _, en = _json(plugin_dir, "score_post.py", str(FIX_EN), "--json")
    hook_fb = " ".join(en["dimensions"]["hook"]["feedback"])
    assert "Proof of work detected" in hook_fb


def test_pt_save_triggers_fire(plugin_dir):
    """The PT fixture has a numbered list + '5 passos' + save CTA → high saves potential."""
    _, pt = _json(plugin_dir, "score_post.py", str(FIX_PT), "--json")
    assert pt["dimensions"]["saves_potential"]["score"] >= 8.0


def test_saves_parity_pt_en(plugin_dir):
    """The PT and EN fixtures are translations of each other → same saves score (structural matching is language-parallel)."""
    _, pt = _json(plugin_dir, "score_post.py", str(FIX_PT), "--json")
    _, en = _json(plugin_dir, "score_post.py", str(FIX_EN), "--json")
    assert pt["dimensions"]["saves_potential"]["score"] == en["dimensions"]["saves_potential"]["score"]


def test_pt_punished_hook_flagged(plugin_dir, tmp_path):
    post = tmp_path / "pt_punished.txt"
    post.write_text("Bom dia, LinkedIn!\n\nReflexão do dia para vocês.\n", encoding="utf-8")
    r, data = _json(plugin_dir, "validate_specs.py", str(post), "--json")
    errs = " ".join(data["errors"])
    assert "Punished pattern detected" in errs
    assert data["valid"] is False


def test_en_punished_hook_flagged(plugin_dir, tmp_path):
    post = tmp_path / "en_punished.txt"
    post.write_text("Good morning, LinkedIn!\n\nThought of the day for you.\n", encoding="utf-8")
    r, data = _json(plugin_dir, "validate_specs.py", str(post), "--json")
    errs = " ".join(data["errors"])
    assert "Punished pattern detected" in errs
    assert data["valid"] is False


def test_lang_override_restricts(plugin_dir):
    """Scoring the PT fixture with --lang en must NOT detect the PT proof verbs."""
    _, pt_as_en = _json(plugin_dir, "score_post.py", str(FIX_PT), "--lang", "en", "--json")
    hook_fb = " ".join(pt_as_en["dimensions"]["hook"]["feedback"])
    assert "Proof of work detected" not in hook_fb


def test_suggest_hooks_seed_reproducible(plugin_dir):
    """--seed must make the suggestions deterministic."""
    _, a = _json(plugin_dir, "suggest_hooks.py", "--category", "failure",
                 "--objective", "engagement", "--seed", "7", "--json")
    _, b = _json(plugin_dir, "suggest_hooks.py", "--category", "failure",
                 "--objective", "engagement", "--seed", "7", "--json")
    assert a == b
    assert all("type" in s and "template" in s and "example" in s for s in a)
