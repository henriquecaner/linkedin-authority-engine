import json

EXPECTED_SKILLS = [
    "360brew-algorithm", "hooks", "copywriting-structures", "content-types",
    "templates-by-category", "ctas", "style-and-tone", "post-publication-protocol",
    "visual-brief", "humanizer-linkedin",
]

def test_knowledge_skills_present_and_valid(plugin_dir):
    for name in EXPECTED_SKILLS:
        sk = plugin_dir / "skills" / name / "SKILL.md"
        assert sk.exists(), f"missing skill: {name}"
        text = sk.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{name}: no frontmatter"
        assert "description:" in text.split("---")[1], f"{name}: frontmatter without description"
        body = text.split("---", 2)[2].strip()
        assert len(body) > 200, f"{name}: body too short (incomplete port?)"

def test_no_stale_skill_references(plugin_dir):
    import re
    pat = re.compile(r"LinkedIn Content \d|virall-linkedin-content", re.I)
    for sk in (plugin_dir / "skills").rglob("SKILL.md"):
        assert not pat.search(sk.read_text(encoding="utf-8")), f"stale reference in {sk}"

def test_plugin_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "plugin.json"
    assert p.exists(), "plugin.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    assert data["version"] == "1.1.0"
    for key in ("displayName", "description", "author", "license"):
        assert key in data, f"plugin.json missing key {key}"

def test_marketplace_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "marketplace.json"
    assert p.exists(), "marketplace.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    names = [pl["name"] for pl in data["plugins"]]
    assert "linkedin-authority-engine" in names

def test_discovery_script_covers_sections(plugin_dir):
    sk = (plugin_dir / "skills" / "discovery-script" / "SKILL.md").read_text(encoding="utf-8").lower()
    # one block anchor per profile section (canonical EN labels)
    for label in ["profile", "positioning", "goals", "audience", "offers",
                  "commercial narrative", "competitive landscape", "territories",
                  "constraints", "tone of voice", "content instruction"]:
        assert label in sk, f"discovery-script missing block: {label}"
    assert sk.count("?") >= 25, "discovery-script has too few questions"

def test_authority_context_assets(plugin_dir):
    base = plugin_dir / "skills" / "authority-context"
    assert (base / "SKILL.md").exists()
    tpl = (base / "references" / "authority-context-template.md").read_text(encoding="utf-8")
    # 13 numbered sections of the template
    for n in range(1, 14):
        assert f"# {n}." in tpl, f"template missing section {n}"
    mem = (base / "references" / "memory-schemas.md").read_text(encoding="utf-8")
    for f in ("winning-hooks.md", "topic-performance.md", "voice-profile.md", "learnings.md"):
        assert f in mem, f"memory-schemas missing {f}"

def test_command_frontmatter(plugin_dir):
    cmds = ["init", "linkedin", "guided", "rewrite", "thread", "score"]
    for c in cmds:
        p = plugin_dir / "commands" / f"{c}.md"
        assert p.exists(), f"missing command: {c}"
        text = p.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{c}: no frontmatter"
        assert "description:" in text.split("---")[1], f"{c}: no description"
        assert "argument-hint:" in text.split("---")[1], f"{c}: no argument-hint"

def test_agents_frontmatter(plugin_dir):
    for a in ["linkedin-strategist", "humanizer-linkedin"]:
        p = plugin_dir / "agents" / f"{a}.md"
        assert p.exists(), f"missing agent: {a}"
        fm = p.read_text(encoding="utf-8").split("---")[1]
        assert "name:" in fm and "description:" in fm, f"{a}: incomplete frontmatter"

def test_hooks_json_valid(plugin_dir):
    import json
    p = plugin_dir / "hooks" / "hooks.json"
    assert p.exists(), "hooks.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "SessionStart" in data["hooks"]
