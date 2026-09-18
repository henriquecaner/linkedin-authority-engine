"""Anti-drift guard for the ChatGPT port (copies, not shared source).

The `.agents/` mirror already drifted once (absolute paths, missing scripts);
this suite fails the build if `plugins/chatgpt/linkedin-authority-engine/`
drifts from the canonical `linkedin-authority-engine/` contract again.
"""
import json
import pathlib
import re

import pytest


@pytest.fixture
def gpt_dir():
    return (
        pathlib.Path(__file__).resolve().parent.parent
        / "plugins"
        / "chatgpt"
        / "linkedin-authority-engine"
    )


@pytest.fixture
def claude_version():
    p = (
        pathlib.Path(__file__).resolve().parent.parent
        / "linkedin-authority-engine"
        / ".claude-plugin"
        / "plugin.json"
    )
    return json.loads(p.read_text(encoding="utf-8"))["version"]


def _skill_files(gpt_dir):
    return sorted((gpt_dir / "skills").glob("*/SKILL.md"))


def test_plugin_json_portable(gpt_dir, claude_version):
    p = gpt_dir / "plugin.json"
    assert p.exists(), "plugin.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("$schema", "name", "version", "description"):
        assert key in data, f"plugin.json missing key {key}"
    assert data["name"] == "linkedin-authority-engine"
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["name"]), "name not kebab-case"
    assert data["description"].strip(), "description empty"
    assert data["version"] == claude_version, "GPT copy drifted from canonical version"


def test_skill_count_and_frontmatter(gpt_dir):
    files = _skill_files(gpt_dir)
    assert len(files) == 29, f"expected 29 skills, found {len(files)}"
    for sk in files:
        text = sk.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{sk.parent.name}: missing frontmatter"
        parts = text.split("---", 2)
        assert len(parts) == 3, f"{sk.parent.name}: malformed frontmatter"
        fm, body = parts[1], parts[2]
        assert "name:" in fm and "description:" in fm, (
            f"{sk.parent.name}: incomplete frontmatter"
        )
        assert len(body) > 200, f"{sk.parent.name}: body too short"


def test_no_claude_coupling(gpt_dir):
    banned = [
        "linkedin-authority-engine:",
        "CLAUDE_PLUGIN_ROOT",
        "/linkedin-authority-engine:",
        "/Users/",
    ]
    hits = []
    for f in list(gpt_dir.rglob("SKILL.md")) + list(
        gpt_dir.rglob("*.md")
    ) + [gpt_dir / "plugin.json", gpt_dir / "hooks" / "hooks.json"]:
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        for pat in banned:
            if pat in text:
                hits.append(f"{f.relative_to(gpt_dir)}: {pat!r}")
    assert not hits, f"Claude coupling leaked into GPT copy: {hits}"


def test_script_refs_use_plugin_root(gpt_dir):
    refs = []
    for sk in _skill_files(gpt_dir):
        for m in re.finditer(r"\$\{(\w+)\}/scripts/", sk.read_text(encoding="utf-8")):
            refs.append(m.group(1))
    assert refs, "no ${...}/scripts references found at all"
    assert set(refs) == {"PLUGIN_ROOT"}, f"non-portable script roots: {set(refs)}"


def test_marketplace_entry_resolves(gpt_dir):
    mp = (
        pathlib.Path(__file__).resolve().parent.parent
        / ".agents"
        / "plugins"
        / "marketplace.json"
    )
    data = json.loads(mp.read_text(encoding="utf-8"))
    paths = [
        pl["source"]["path"] for pl in data["plugins"] if pl["name"] == "linkedin-authority-engine"
    ]
    assert paths, "marketplace has no linkedin-authority-engine entry"
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for rel in paths:
        target = (repo_root / rel).resolve()
        assert (target / "plugin.json").exists(), f"marketplace path {rel} has no plugin.json"


def test_manual_fallback_present(gpt_dir):
    skills = ["guided", "rewrite", "thread", "score", "carousel-builder"]
    prefix = "Se os scripts não executarem (ChatGPT web, sem runtime local), aplique a checagem manual abaixo."
    literals = ["1250", "2500", "14", "19", "150", "30%", "≥9"]
    for name in skills:
        text = (gpt_dir / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert prefix in text, f"{name}: manual-fallback prefix missing"
        missing = [lit for lit in literals if lit not in text]
        assert not missing, f"{name}: fallback literals missing: {missing}"
