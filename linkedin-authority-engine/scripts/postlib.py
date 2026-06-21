#!/usr/bin/env python3
"""
Shared library for the LinkedIn 360Brew scripts.

Holds the text-metric utilities and the multilingual (PT + EN) matchers used by
score_post.py and validate_specs.py, so both scripts share a single source of
truth for patterns.

Language handling: matching is union-based. With lang="auto" (the default) a
text is matched against BOTH the PT and EN pattern sets, so the scorer works on
Portuguese and English posts without a detection step that could misroute. The
PT/EN keyword sets do not collide, and structural matches are deduped by a
canonical label. Pass lang="pt" or lang="en" to restrict to one language.
"""

import re

LANGS = ("pt", "en")

# 360Brew numeric specs — single source of truth shared by score_post and validate_specs.
SPECS = {
    "chars_min": 1250,
    "chars_max": 2500,
    "chars_warning_min": 1000,
    "chars_warning_max": 3000,
    "paragraphs_min": 14,
    "paragraphs_warning": 10,
    "avg_word_length_max": 5,
    "avg_word_length_warning": 6,
    "max_words_per_paragraph": 19,
    "dense_paragraph_chars": 150,
    "hashtags_max": 2,
}


def resolve_langs(lang: str) -> list:
    """Returns the active language list. 'auto' -> both languages."""
    if lang in LANGS:
        return [lang]
    return list(LANGS)


# -----------------------------
# Text-metric utilities
# -----------------------------

# Word letters for both PT (accented) and EN. Apostrophes are excluded so that
# contractions ("don't") aren't counted as longer than they read.
_WORD_RE = r"[a-záàâãéèêíïóôõöúüçñ]+"


def count_chars(text: str) -> int:
    return len(text.strip())


def split_paragraphs(text: str) -> list:
    """Paragraphs = blocks separated by a blank line (LinkedIn format)."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def count_paragraphs(text: str) -> int:
    return len(split_paragraphs(text))


def avg_word_length(text: str) -> float:
    words = re.findall(_WORD_RE, text.lower())
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def has_link_in_body(text: str) -> bool:
    """Detects a link ANYWHERE in the body. The 360Brew rule has no exception:
    links belong in the 1st comment, never in the post (-60% reach)."""
    return bool(re.search(r'https?://|www\.', text, re.IGNORECASE))


def count_hashtags(text: str) -> int:
    return len(re.findall(r'#\w+', text))


def detect_language(text: str) -> str:
    """Best-effort language guess ('pt' or 'en'), used for reporting only —
    matching is union-based and does not depend on this."""
    low = text.lower()
    diacritics = len(re.findall(r"[ãõáéíóúâêôàçü]", low))
    pt = len(re.findall(r"\b(de|que|n[ãa]o|com|para|voc[êe]|uma|por|mais|como|isso|est[áa]|s[ãa]o|tem|dos|das)\b", low))
    en = len(re.findall(r"\b(the|and|you|for|with|that|this|are|have|from|your|not|how|was|its)\b", low))
    return "pt" if (pt + diacritics * 2) >= en else "en"


# -----------------------------
# Multilingual pattern sets
# -----------------------------

# Language-neutral data signals (currency, percentage, multiplier).
# A single currency pattern covers both "$" and "R$" so a BRL value isn't counted twice.
_DATA_NEUTRAL = [r"\d+%", r"R?\$\s*[\d.,]+", r"\d+x\b"]

# Per-language time-span and transformation-range data signals.
_DATA_TIME = {
    "en": r"\d+\s*(?:days|weeks|months|years|hours)",
    "pt": r"\d+\s*(?:dias|semanas|meses|anos|horas)",
}
_TRANSFORMATION_RANGE = {
    "en": r"from\s+\d+.*?to\s+\d+",
    "pt": r"de\s+\d+.*?para\s+\d+",
}

# Hooks punished by 360Brew. Anchored to avoid false positives.
_PUNISHED = {
    "en": [
        (r"\bwhat do you think\s*\?", "What do you think?"),
        (r"(?:^|[.!?…]\s*)(?:agree|right)\s*\?", "Agree?"),
        (r"\bgood morning[,]?\s*linkedin", "Good morning, LinkedIn"),
        (r"\bthought of the day\b", "Thought of the day"),
    ],
    "pt": [
        (r"\bo que voc[êe]s? acham?\s*\?", "O que você acha?"),
        (r"(?:^|[.!?…]\s*)concordam?\s*\?", "Concordam?"),
        (r"\bbom dia[,]?\s*linkedin", "Bom dia, LinkedIn"),
        (r"\breflex[ãa]o do dia\b", "Reflexão do dia"),
    ],
}

# AI-cliché hooks — DISTINCT from _PUNISHED (engagement bait). Only concrete,
# regex-safe phrases live here; variable templates ("Stop doing X. Do Y.") are
# handled qualitatively by the humanizer-linkedin skill, not the scorer.
# Labels are canonical (shared across languages) so union matching counts once.
_AI_CLICHE_HOOKS = {
    "en": [
        (r"\bread that again\b", "Read that again"),
        (r"\blet that sink in\b", "Let that sink in"),
        (r"\bwhat if i told you\b", "What if I told you"),
        (r"\bhere'?s the truth about\b", "Here's the truth about"),
        (r"\bnobody tells you\b", "Nobody tells you"),
        (r"\bunlock the power of\b", "Unlock the power of"),
        (r"\bgame[ -]?changer\b", "Game-changer"),
        (r"\bhere'?s the shift\b", "Here's the shift"),
        (r"\bthe real question is\b", "The real question is"),
        (r"\bhere'?s the kicker\b", "Here's the kicker"),
    ],
    "pt": [
        (r"\bleia (?:isso )?de novo\b", "Read that again"),
        (r"\bdeixa isso (?:assentar|bater)\b", "Let that sink in"),
        (r"\be se eu te dissesse\b", "What if I told you"),
        (r"\ba verdade sobre\b", "Here's the truth about"),
        (r"\bningu[ée]m te conta\b", "Nobody tells you"),
        (r"\b(?:destrave|desbloqueie) o poder de\b", "Unlock the power of"),
        (r"\bdivisor de águas\b", "Game-changer"),
        (r"\baqui está a virada\b", "Here's the shift"),
        (r"\ba (?:verdadeira|real) pergunta é\b", "The real question is"),
    ],
}

# High save-potential patterns. Labels are canonical (shared across languages)
# so a structural match is counted once even under union matching.
_SAVES = {
    "en": [
        (r"(?:step\s*\d|\d+[\s-]+steps?)", "Numbered steps"),
        (r"(?:phase\s*\d|\d+[\s-]+phases?)", "Numbered phases"),
        (r"^\s*\d+\s*[-–.]\s*\w", "Numbered list"),
        (r"checklist", "Checklist"),
        (r"framework", "Named framework"),
        (r"template", "Template"),
        (r"(?:complete|definitive|practical)\s+guide", "Explicit guide"),
        (r"how\s+to\s+.+?\s+in\s+\d+", "How-to with a number"),
        (r"\d+\s+(?:tips|rules|principles|mistakes|signs)", "Value list"),
    ],
    "pt": [
        (r"(?:passo\s*\d|\d+[\s-]+passos?)", "Numbered steps"),
        (r"(?:etapa\s*\d|\d+[\s-]+etapas?)", "Numbered phases"),
        (r"^\s*\d+\s*[-–.]\s*\w", "Numbered list"),
        (r"checklist", "Checklist"),
        (r"framework", "Named framework"),
        (r"template", "Template"),
        (r"guia\s+(?:completo|definitivo|pr[áa]tico)", "Explicit guide"),
        (r"como\s+.+?\s+em\s+\d+", "How-to with a number"),
        (r"\d+\s+(?:dicas|regras|princ[íi]pios|erros|sinais)", "Value list"),
    ],
}

# Proof-of-work verbs in the hook. Word-anchored to avoid substring false
# positives ("ran" in "brand", "perdi" in "perdida"). The PT stems triplic*/dobr*
# stay prefix-matched (triplicamos, dobrou) but still require a leading boundary.
_PROOF_VERBS = {
    "en": r"\b(spent|invested|tested|analyzed|lost|earned|built|implemented|audited|interviewed|reviewed|documented|ran|scaled|generated|closed|tripled|doubled)\b",
    "pt": r"\b(gastei|investi|testei|analisei|perdi|ganhei|constru[íi]|implementei|auditei|entrevistei|revisei|documentei|rodei|escalei|faturei|gerei|fechei)\b|\b(?:triplic|dobr)\w*",
}

# Authority proof in the hook.
_AUTHORITY = {
    "en": r"(\d+\s*(years?|months?).*?(learned|taught|discovered)|as\s+(a\s+)?(ceo|founder|director|manager|head|vp))",
    "pt": r"(\d+\s*(anos?|meses?).*?(aprendi|ensinaram|descobri)|como\s+(ceo|founder|diretor|gerente))",
}

# Framework signals in the body.
_FRAMEWORK_SIGNALS = {
    "en": r"(problem|agitation|solution|before|after|bridge|setup|conflict|resolution|feature|advantage|benefit)",
    "pt": r"(problema|agita[çc][ãa]o|solu[çc][ãa]o|antes|depois|ponte|setup|conflito|resolu[çc][ãa]o|feature|vantagem|benef[íi]cio)",
}

# CTA patterns, keyed by canonical CTA type (shared across languages).
_CTA = {
    "en": {
        "save": r'\b(save|bookmark)\b',
        "follow": r'(follow me|follow back|hit follow|turn on)',
        # Requires an UPPERCASE keyword ("Comment FRAMEWORK") so generic
        # "comment below" isn't misread as a lead-magnet/DM CTA.
        "comment_dm": r'comment\s+(?-i:[A-Z]{2,})\b',
        "dm": r'(dm me|send\s+(a\s+)?(dm|message)|open dms?)',
        "click": r'click\s+(the\s+)?link',
        "bio": r'link\s+in\s+(the\s+)?(bio|profile|first comment)',
    },
    "pt": {
        "save": r'\b(salva|salve|guarda|guarde)\b',
        "follow": r'(me siga|siga[- ]me|ative o)',
        "comment_dm": r'comenta\s+(?-i:[A-Z]{2,})\b',
        "dm": r'(manda?\s+(dm|mensagem)|dm aberta)',
        "click": r'clica\s+(no\s+)?link',
        "bio": r'link\s+(na|no)\s+(bio|perfil|primeiro coment)',
    },
}

# Explicit "save this post" CTA in the closing lines.
_SAVE_CTA = {
    "en": r"(save|bookmark)\s+(this|the)\s+post|\bbookmark this\b",
    "pt": r"(salva|salve)\s+(esse|este|o)\s+post",
}

# Engagement cue in the closing lines.
_ENGAGEMENT_CUE = {
    "en": r"(tell me|let me know|comment|which (one|of these))",
    "pt": r"(me conta|conta (a[íi]|pra mim)|comenta|qual (foi|seria|desses))",
}


# -----------------------------
# Matchers (union over active languages)
# -----------------------------

def find_punished(text: str, lang: str = "auto") -> list:
    """Returns the display names of punished hooks found in the first lines."""
    first_lines = '\n'.join(text.split('\n')[:5])
    found = []
    for l in resolve_langs(lang):
        for pattern, name in _PUNISHED[l]:
            if re.search(pattern, first_lines, re.IGNORECASE) and name not in found:
                found.append(name)
    return found


def find_ai_cliches(text: str, lang: str = "auto") -> list:
    """Returns canonical AI-cliché hook labels found in the first lines
    (deduped across languages). Separate from find_punished (engagement bait)."""
    first_lines = '\n'.join(text.split('\n')[:5])
    found = []
    for l in resolve_langs(lang):
        for pattern, name in _AI_CLICHE_HOOKS[l]:
            if name not in found and re.search(pattern, first_lines, re.IGNORECASE):
                found.append(name)
    return found


def count_data_points(text: str, lang: str = "auto") -> int:
    count = 0
    for pattern in _DATA_NEUTRAL:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    for l in resolve_langs(lang):
        count += len(re.findall(_DATA_TIME[l], text, re.IGNORECASE))
        count += len(re.findall(_TRANSFORMATION_RANGE[l], text, re.IGNORECASE))
    return count


def find_saves(text: str, lang: str = "auto") -> list:
    """Returns canonical save-trigger labels (deduped across languages)."""
    labels = []
    for l in resolve_langs(lang):
        for pattern, label in _SAVES[l]:
            if label not in labels and re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                labels.append(label)
    return labels


def has_proof_of_work(hook: str, lang: str = "auto") -> bool:
    return any(re.search(_PROOF_VERBS[l], hook, re.IGNORECASE) for l in resolve_langs(lang))


def has_authority(hook: str, lang: str = "auto") -> bool:
    return any(re.search(_AUTHORITY[l], hook, re.IGNORECASE) for l in resolve_langs(lang))


def has_transformation_range(text: str, lang: str = "auto") -> bool:
    return any(re.search(_TRANSFORMATION_RANGE[l], text, re.IGNORECASE) for l in resolve_langs(lang))


def framework_signal_count(text: str, lang: str = "auto") -> int:
    signals = set()
    for l in resolve_langs(lang):
        # _FRAMEWORK_SIGNALS has a single capture group, so findall yields strings.
        for m in re.findall(_FRAMEWORK_SIGNALS[l], text, re.IGNORECASE):
            signals.add(m.lower())
    return len(signals)


def find_ctas(closing_lines: str, lang: str = "auto") -> list:
    """Returns canonical CTA keys detected in the closing lines (first-seen order)."""
    detected = []
    for l in resolve_langs(lang):
        for key, pattern in _CTA[l].items():
            if key not in detected and re.search(pattern, closing_lines, re.IGNORECASE):
                detected.append(key)
    return detected


def has_save_cta(closing_lines: str, lang: str = "auto") -> bool:
    return any(re.search(_SAVE_CTA[l], closing_lines, re.IGNORECASE) for l in resolve_langs(lang))


def has_engagement_cue(closing_lines: str, lang: str = "auto") -> bool:
    return any(re.search(_ENGAGEMENT_CUE[l], closing_lines, re.IGNORECASE) for l in resolve_langs(lang))
