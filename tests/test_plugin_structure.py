import json

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
