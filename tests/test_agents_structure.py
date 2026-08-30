import os
import re
import pytest
import pathlib

AGENTS_SKILLS = [
    "360brew-algorithm", "hooks", "copywriting-structures", "content-types",
    "templates-by-category", "ctas", "style-and-tone", "post-publication-protocol",
    "visual-brief", "humanizer-linkedin", "niche-definer", "audience-persona", 
    "content-pillars", "content-calendar", "repurposer", "story-extractor", 
    "cta-optimizer", "carousel-builder", "profile-optimizer", "analytics-interpreter",
    "init", "linkedin", "guided", "rewrite", "thread", "score", "linkedin-autopilot"
]

@pytest.fixture
def agents_dir():
    return pathlib.Path(__file__).resolve().parent.parent / ".agents"

def test_agents_folder_exists(agents_dir):
    assert agents_dir.exists()
    assert (agents_dir / "skills").exists()
    assert (agents_dir / "agents").exists()
    assert (agents_dir / "scripts").exists()
    assert (agents_dir / "AGENTS.md").exists()

def test_agents_skills_prefixed_and_valid(agents_dir):
    for name in AGENTS_SKILLS:
        skill_path = agents_dir / "skills" / name / "SKILL.md"
        assert skill_path.exists(), f"missing skill: {name}"
        text = skill_path.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{name}: no frontmatter"
        
        # Check that frontmatter name is correctly prefixed with linkedin-authority-engine:
        fm = text.split("---")[1]
        assert "name: linkedin-authority-engine:" in fm, f"{name} does not have standard namespace name in frontmatter"
        assert "description:" in fm, f"{name} is missing a description in frontmatter"
        
        # Check body length
        body = text.split("---", 2)[2].strip()
        assert len(body) > 200, f"{name} body too short (incomplete migration)"

def test_agents_agents_present_and_valid(agents_dir):
    expected_agents = ["linkedin-strategist", "linkedin-writer", "linkedin-reviewer", "humanizer-linkedin"]
    for a in expected_agents:
        p = agents_dir / "agents" / f"{a}.md"
        assert p.exists(), f"missing agent configuration file: {a}.md"
        text = p.read_text(encoding="utf-8")
        assert text.startswith("---"), f"agent {a} missing frontmatter"
        fm = text.split("---")[1]
        assert "name:" in fm, f"agent {a} missing 'name' in frontmatter"
        assert "description:" in fm, f"agent {a} missing 'description' in frontmatter"

def test_no_absolute_paths_in_reviewer_and_autopilot(agents_dir):
    # Verify we are using relative portable paths instead of hardcoded home directories for python script runs
    reviewer_content = (agents_dir / "agents" / "linkedin-reviewer.md").read_text(encoding="utf-8")
    assert "python3 /Users/" not in reviewer_content, "absolute script execution path found in reviewer agent"
    
    autopilot_content = (agents_dir / "skills" / "linkedin-autopilot" / "SKILL.md").read_text(encoding="utf-8")
    assert "python3 /Users/" not in autopilot_content, "absolute script execution path found in autopilot skill"
