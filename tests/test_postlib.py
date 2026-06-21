"""Direct unit tests for the shared multilingual matcher library (postlib.py)."""
import sys
import pathlib

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "linkedin-authority-engine" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import postlib  # noqa: E402
import score_post  # noqa: E402


# --- language detection ---

def test_detect_language_pt():
    assert postlib.detect_language("Não sei o que você acha disso, mas funciona.") == "pt"

def test_detect_language_en():
    assert postlib.detect_language("I don't know what you think, but it works.") == "en"


# --- data points: R$ must not be double-counted ---

def test_data_points_brl_not_double_counted():
    assert postlib.count_data_points("Faturei R$ 500 esse mês", "pt") == 1

def test_data_points_mixed_currency_and_percent():
    assert postlib.count_data_points("$100 and R$200 and 50%", "auto") == 3


# --- proof-of-work verbs are word-anchored ---

@pytest.mark.parametrize("text", ["our brand strategy", "a grand vision", "disclosed terms"])
def test_proof_of_work_no_substring_false_positive_en(text):
    assert postlib.has_proof_of_work(text, "en") is False

def test_proof_of_work_true_en():
    assert postlib.has_proof_of_work("I ran 50 tests and tripled output", "en") is True

@pytest.mark.parametrize("text", ["uma oportunidade perdida", "fomos ao rodeio"])
def test_proof_of_work_no_substring_false_positive_pt(text):
    assert postlib.has_proof_of_work(text, "pt") is False

def test_proof_of_work_pt_stem():
    assert postlib.has_proof_of_work("triplicamos o pipeline", "pt") is True


# --- CTA detection ---

def test_comment_cta_ignores_generic_comment():
    assert "comment_dm" not in postlib.find_ctas("comment below with your thoughts", "en")

def test_comment_cta_detects_keyword():
    assert "comment_dm" in postlib.find_ctas("Comment FRAMEWORK and I'll send it", "en")

def test_cta_union_pt_and_en():
    assert "save" in postlib.find_ctas("Salva esse post", "auto")
    assert "save" in postlib.find_ctas("Save this post", "auto")


# --- saves triggers, with number-first phrasing ---

def test_saves_number_first_steps():
    labels = postlib.find_saves("my 5-step system for growth", "en")
    assert "Numbered steps" in labels

def test_saves_dedup_across_languages():
    # 'checklist' exists in both PT and EN sets but must count once under union.
    labels = postlib.find_saves("here is a checklist", "auto")
    assert labels.count("Checklist") == 1


# --- punished hooks per language ---

def test_punished_pt():
    assert "Bom dia, LinkedIn" in postlib.find_punished("Bom dia, LinkedIn!\n", "pt")

def test_punished_en():
    assert "Good morning, LinkedIn" in postlib.find_punished("Good morning, LinkedIn!\n", "en")


# --- lang restriction ---

def test_lang_restriction_excludes_other_language():
    # A PT proof verb must not fire when matching is restricted to EN.
    assert postlib.has_proof_of_work("Gastei R$40k testando", "en") is False
    assert postlib.has_proof_of_work("Gastei R$40k testando", "pt") is True


# --- shared specs ---

def test_specs_present():
    for key in ("chars_min", "chars_max", "paragraphs_min", "avg_word_length_max"):
        assert key in postlib.SPECS


# --- AI-cliché hooks (separate bucket from engagement-bait) ---

def test_ai_cliche_en():
    assert "Let that sink in" in postlib.find_ai_cliches("Let that sink in.\nBig news today.", "en")

def test_ai_cliche_pt():
    assert "Let that sink in" in postlib.find_ai_cliches("Deixa isso assentar.\nNovidade hoje.", "pt")

def test_ai_cliche_clean_text_no_false_positive():
    assert postlib.find_ai_cliches("I spent 40 hours testing three tools last week.", "auto") == []

def test_ai_cliche_dedup_across_languages():
    labels = postlib.find_ai_cliches("Game-changer e divisor de águas no mesmo post", "auto")
    assert labels.count("Game-changer") == 1

def test_ai_cliche_only_first_lines():
    # a cliché buried below the first 5 lines is not a hook
    text = "Clean hook line.\n\n\n\n\n\nLet that sink in."
    assert postlib.find_ai_cliches(text, "en") == []

def test_ai_cliche_pt_verdade_sobre_needs_frame():
    # bare "a verdade sobre" is ordinary PT — must NOT fire
    assert postlib.find_ai_cliches("Compartilho a verdade sobre nossa jornada.", "pt") == []
    # the framed hook DOES fire
    assert "Here's the truth about" in postlib.find_ai_cliches("Aqui está a verdade sobre pricing.", "pt")

def test_ai_cliche_curly_apostrophe():
    assert "Here's the shift" in postlib.find_ai_cliches("Here’s the shift in B2B.", "en")


def test_score_hook_penalizes_ai_cliche():
    base = "Here is what I learned about pricing.\nThree lessons below."
    s_base, _ = score_post.score_hook(base, "en")
    s_cliche, _ = score_post.score_hook("Let that sink in. " + base, "en")
    assert s_cliche == s_base - 1.5
