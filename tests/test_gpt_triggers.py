"""Trigger harness for the GPT port (Passo 1).

Each tuple asserts the expected skill's frontmatter `description:`
contains every required routing keyword (case-insensitive substring).
Proves the Passo 2 description pass actually improves ChatGPT routing.
"""
import pathlib
import re

import pytest

GPT_DIR = (
    pathlib.Path(__file__).resolve().parent.parent
    / "plugins"
    / "chatgpt"
    / "linkedin-authority-engine"
)

TRIGGERS = [
    ("tenho um rascunho, está pronto para publicar?", "score", ["publish", "ready", "evaluate"]),
    ("turn this draft into two stronger versions", "rewrite", ["two versions", "conservative", "bold"]),
    ("quero uma sequência de posts sobre liderança", "thread", ["series", "3-7", "campaign"]),
    ("create a post from scratch about pricing", "guided", ["from scratch", "7-step", "workflow"]),
    ("o que vamos criar hoje?", "linkedin", ["menu", "modes", "overview"]),
    ("criar meu perfil de autoridade", "init", ["onboarding", "authority-context", "interview"]),
    ("transforme este texto do meu blog num post", "repurposer", ["blog", "external", "repurpose"]),
    ("algo aconteceu no trabalho hoje", "story-extractor", ["lived experience", "story-arc", "vulnerability"]),
    ("planeje meu próximo mês", "content-calendar", ["4-week", "calendar", "month"]),
    ("fix my CTA", "cta-optimizer", ["CTA", "close", "ending"]),
]


def _description(skill: str) -> str:
    text = (GPT_DIR / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---"), f"{skill}: missing frontmatter"
    parts = text.split("---", 2)
    assert len(parts) == 3, f"{skill}: malformed frontmatter"
    fm = parts[1]
    m = re.search(r"description:\s*(.+)", fm, re.DOTALL)
    assert m, f"{skill}: no description: in frontmatter"
    # Take description value up to the next top-level YAML key or end.
    desc = m.group(1)
    # Cut at a newline followed by a simple key (e.g. "\nname:") if present.
    cut = re.search(r"\n[a-zA-Z_][\w-]*\s*:", desc)
    if cut:
        desc = desc[: cut.start()]
    return desc.strip()


@pytest.mark.parametrize("utterance,skill,keywords", TRIGGERS)
def test_gpt_trigger_routes(utterance, skill, keywords):
    desc = _description(skill)
    lowered = desc.lower()
    missing = [k for k in keywords if k.lower() not in lowered]
    assert not missing, (
        f"utterance {utterance!r} → skill {skill!r} missing keywords {missing} "
        f"in description: {desc[:200]!r}"
    )
