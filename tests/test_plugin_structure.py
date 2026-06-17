import json

EXPECTED_SKILLS = [
    "algoritmo-360brew", "hooks", "estruturas-copywriting", "tipos-conteudo",
    "templates-por-categoria", "ctas", "estilo-tom", "protocolo-pos-publicacao",
    "brief-visual", "humanizer-linkedin",
]

def test_knowledge_skills_present_and_valid(plugin_dir):
    for name in EXPECTED_SKILLS:
        sk = plugin_dir / "skills" / name / "SKILL.md"
        assert sk.exists(), f"skill ausente: {name}"
        text = sk.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{name}: sem frontmatter"
        assert "description:" in text.split("---")[1], f"{name}: frontmatter sem description"
        body = text.split("---", 2)[2].strip()
        assert len(body) > 200, f"{name}: corpo muito curto (port incompleto?)"

def test_no_stale_skill_references(plugin_dir):
    import re
    pat = re.compile(r"LinkedIn Content \d|virall-linkedin-content", re.I)
    for sk in (plugin_dir / "skills").rglob("SKILL.md"):
        assert not pat.search(sk.read_text(encoding="utf-8")), f"referência stale em {sk}"

def test_plugin_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "plugin.json"
    assert p.exists(), "plugin.json ausente"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    assert data["version"] == "1.0.0"
    for key in ("displayName", "description", "author", "license"):
        assert key in data, f"plugin.json sem chave {key}"

def test_marketplace_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "marketplace.json"
    assert p.exists(), "marketplace.json ausente"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    names = [pl["name"] for pl in data["plugins"]]
    assert "linkedin-authority-engine" in names
