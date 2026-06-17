import subprocess
import sys
import pathlib

FIX = pathlib.Path(__file__).resolve().parent / "fixtures" / "post_exemplo.txt"


def _run(plugin_dir, *args):
    """Run a script with the given arguments and return subprocess result."""
    script = plugin_dir / "scripts" / args[0]
    return subprocess.run(
        [sys.executable, str(script), *args[1:]],
        capture_output=True,
        text=True,
    )


def test_validate_specs_runs(plugin_dir):
    """Test that validate_specs.py runs successfully with a post file."""
    r = _run(plugin_dir, "validate_specs.py", str(FIX))
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


def test_score_post_runs(plugin_dir):
    """Test that score_post.py runs successfully with --objetivo flag."""
    r = _run(plugin_dir, "score_post.py", str(FIX), "--objetivo", "authority")
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""


def test_suggest_hooks_runs(plugin_dir):
    """Test that suggest_hooks.py runs successfully with categoria/objetivo/tema."""
    r = _run(
        plugin_dir,
        "suggest_hooks.py",
        "--categoria",
        "conquista",
        "--objetivo",
        "authority",
        "--tema",
        "vendas B2B",
    )
    assert r.returncode == 0, f"Exit code {r.returncode}: {r.stderr}"
    assert r.stdout.strip() != ""
