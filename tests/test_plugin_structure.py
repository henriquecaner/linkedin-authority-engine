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

def test_discovery_script_covers_sections(plugin_dir):
    sk = (plugin_dir / "skills" / "discovery-script" / "SKILL.md").read_text(encoding="utf-8")
    # uma âncora de bloco por seção do perfil
    for label in ["Perfil", "Posicionamento", "Objetivos", "Audiência", "Ofertas",
                  "Narrativa comercial", "Paisagem competitiva", "Territórios",
                  "Restrições", "Tom de voz", "Instrução de conteúdo"]:
        assert label in sk, f"discovery-script sem bloco: {label}"
    assert sk.lower().count("?") >= 25, "discovery-script com poucas perguntas"

def test_authority_context_assets(plugin_dir):
    base = plugin_dir / "skills" / "authority-context"
    assert (base / "SKILL.md").exists()
    tpl = (base / "references" / "authority-context-template.md").read_text(encoding="utf-8")
    # 13 seções numeradas do template
    for n in range(1, 14):
        assert f"# {n}." in tpl, f"template sem seção {n}"
    mem = (base / "references" / "memory-schemas.md").read_text(encoding="utf-8")
    for f in ("winning-hooks.md", "topic-performance.md", "voice-profile.md", "learnings.md"):
        assert f in mem, f"memory-schemas sem {f}"

def test_command_frontmatter(plugin_dir):
    import os
    cmds = ["init", "linkedin", "guiado", "rewrite", "thread", "score"]
    for c in cmds:
        p = plugin_dir / "commands" / f"{c}.md"
        assert p.exists(), f"command ausente: {c}"
        text = p.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{c}: sem frontmatter"
        assert "description:" in text.split("---")[1], f"{c}: sem description"
        assert "argument-hint:" in text.split("---")[1], f"{c}: sem argument-hint"

def test_agents_frontmatter(plugin_dir):
    for a in ["linkedin-strategist", "humanizer-linkedin"]:
        p = plugin_dir / "agents" / f"{a}.md"
        assert p.exists(), f"agent ausente: {a}"
        fm = p.read_text(encoding="utf-8").split("---")[1]
        assert "name:" in fm and "description:" in fm, f"{a}: frontmatter incompleto"
