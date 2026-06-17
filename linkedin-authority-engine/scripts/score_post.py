#!/usr/bin/env python3
"""
LinkedIn Post Scorer v3.5 - Calcula score baseado nas 6 dimensões do 360Brew.

Uso: python score_post.py <arquivo_post.txt> [--objetivo authority|sales|engagement]

Saída padrão: relatório legível. Use --json para output estruturado.
Use --compact para resumo em 1 linha (útil pra integração no workflow).
"""

import argparse
import re
import sys
from pathlib import Path

# Pesos das dimensões (v3.5) — alinhados com references/algoritmo-metricas.md
WEIGHTS = {
    "saves_potential": 0.30,
    "hook": 0.20,
    "algorithm": 0.20,
    "structure": 0.15,
    "cta": 0.10,
    "data": 0.05,
}

# Hooks punidos pelo 360Brew
# Anchored para evitar falsos positivos (ex: "nem todo mundo concorda comigo")
PUNISHED_HOOKS = [
    r"\bo que voc[êe]s? acham?\s*\?",
    r"(?:^|[.!?…]\s*)concordam?\s*\?",
    r"\bbom dia[,]?\s*linkedin",
    r"\breflex[ãa]o do dia\b",
]

# Palavras de dados/números
DATA_PATTERNS = [
    r"\d+%",
    r"R\$\s*[\d.,]+",
    r"\$\s*[\d.,]+",
    r"\d+x",
    r"\d+\s*(dias|meses|anos|semanas|horas)",
    r"de\s+\d+\s+para\s+\d+",
]

# Padrões de alto potencial de salvamento
SAVES_PATTERNS = [
    (r"passo\s*\d", "Passos numerados"),
    (r"etapa\s*\d", "Etapas numeradas"),
    (r"^\s*\d+\s*[-–.]\s*\w", "Lista numerada"),
    (r"checklist", "Checklist"),
    (r"framework", "Framework nomeado"),
    (r"template", "Template"),
    (r"guia\s+(completo|definitivo|pr[áa]tico)", "Guia explícito"),
    (r"como\s+\w+\s+em\s+\d+", "How-to com número"),
    (r"\d+\s+(dicas|regras|princípios|erros|sinais)", "Lista de valor"),
]


def count_chars(text: str) -> int:
    return len(text.strip())


def split_paragraphs(text: str) -> list:
    """Parágrafos = blocos separados por linha em branco (formato LinkedIn)."""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def count_paragraphs(text: str) -> int:
    return len(split_paragraphs(text))


def avg_word_length(text: str) -> float:
    words = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]+\b', text.lower())
    if not words:
        return 0
    return sum(len(w) for w in words) / len(words)


def count_data_points(text: str) -> int:
    count = 0
    for pattern in DATA_PATTERNS:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def has_punished_hook(text: str) -> bool:
    first_lines = '\n'.join(text.split('\n')[:5]).lower()
    for pattern in PUNISHED_HOOKS:
        if re.search(pattern, first_lines, re.IGNORECASE):
            return True
    return False


def extract_hook(text: str) -> str:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines[:3])


def has_link_in_body(text: str) -> bool:
    """Detecta link em QUALQUER parte do corpo. A regra 360Brew não tem exceção:
    link pertence ao 1º comentário, nunca ao post (-60% alcance)."""
    return bool(re.search(r'https?://|www\.', text, re.IGNORECASE))


def count_hashtags(text: str) -> int:
    return len(re.findall(r'#\w+', text))


# -----------------------------
# Dimensões (6)
# -----------------------------

def score_saves_potential(text: str) -> tuple:
    """Avalia potencial de save (30%). Sinal mais poderoso do algoritmo."""
    feedback = []
    score = 4.0

    matches = []
    for pattern, label in SAVES_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            matches.append(label)

    if len(matches) >= 3:
        score = 10.0
        feedback.append(f"✓ Alto potencial de save: {', '.join(matches[:3])}")
    elif len(matches) == 2:
        score = 8.5
        feedback.append(f"✓ Bom potencial de save: {', '.join(matches)}")
    elif len(matches) == 1:
        score = 6.5
        feedback.append(f"○ Potencial moderado: {matches[0]}")
    else:
        score = 3.5
        feedback.append("❌ Sem gatilhos de save — adicionar framework, checklist ou lista numerada")

    last_lines = '\n'.join(text.split('\n')[-5:]).lower()
    if re.search(r"(salva|salve)\s+(esse|este|o)\s+post", last_lines):
        score = min(10, score + 1.0)
        feedback.append("✓ CTA de save explícito (+1)")

    return min(10, max(0, score)), feedback


def score_hook(text: str) -> tuple:
    feedback = []
    score = 5.0
    hook = extract_hook(text)

    if has_punished_hook(text):
        score -= 4.0
        feedback.append("❌ Hook punido pelo 360Brew detectado (-4)")

    if re.search(r'\d+', hook):
        score += 1.5
        feedback.append("✓ Números específicos no hook (+1.5)")

    if re.search(r'(gastei|investi|testei|analisei|perdi|ganhei|constru[íi]|implementei|auditei|entrevistei|revisei|documentei|rodei|escalei|faturei|gerei|fechei|triplic|dobr)', hook, re.IGNORECASE):
        score += 2.0
        feedback.append("✓ Prova de trabalho detectada (+2)")

    if re.search(r'(\d+\s*(anos?|meses?).*?(aprendi|ensinaram|descobri)|como\s+(ceo|founder|diretor|gerente))', hook, re.IGNORECASE):
        score += 1.5
        feedback.append("✓ Prova de autoridade detectada (+1.5)")

    if re.search(r'de\s+\d+.*?para\s+\d+', hook, re.IGNORECASE):
        score += 1.5
        feedback.append("✓ Transformação com números (+1.5)")

    return min(10, max(0, score)), feedback


def score_algorithm(text: str) -> tuple:
    """Avalia aderência às specs 360Brew (20%). Saves é dimensão separada agora."""
    feedback = []
    score = 5.0

    if has_link_in_body(text):
        score -= 4.0
        feedback.append("❌ Link no corpo do post detectado (-4) — mover para 1º comentário")
    else:
        score += 1.5
        feedback.append("✓ Sem links no corpo (+1.5)")

    hashtag_count = count_hashtags(text)
    if hashtag_count == 0:
        score += 1.0
        feedback.append("✓ Sem hashtags (padrão 2026) (+1)")
    elif hashtag_count <= 2:
        score += 0.5
        feedback.append(f"○ {hashtag_count} hashtag(s) — aceitável se hiper-específicas (+0.5)")
    else:
        score -= 2.0
        feedback.append(f"❌ {hashtag_count} hashtags — excesso punido (-2)")

    avg_len = avg_word_length(text)
    if avg_len <= 5:
        score += 2.0
        feedback.append(f"✓ Palavras simples: média {avg_len:.1f} letras (+2)")
    elif avg_len <= 6:
        score += 1.0
        feedback.append(f"○ Palavras OK: média {avg_len:.1f} letras (+1)")
    else:
        score -= 1.5
        feedback.append(f"❌ Palavras complexas: média {avg_len:.1f} letras (-1.5)")

    if has_punished_hook(text):
        score -= 1.5
        feedback.append("❌ Padrão de isca detectado no hook (-1.5)")
    else:
        score += 0.5
        feedback.append("✓ Sem padrões de isca (+0.5)")

    return min(10, max(0, score)), feedback


def score_structure(text: str) -> tuple:
    """Structure (15%): 3 sub-componentes — Length, Parágrafos, Framework."""
    feedback = []
    score = 5.0

    chars = count_chars(text)
    paragraphs = count_paragraphs(text)

    # Length
    if 1250 <= chars <= 2500:
        score += 2.0
        feedback.append(f"✓ Length ideal: {chars} chars (+2)")
    elif chars < 1000:
        score -= 2.5
        feedback.append(f"❌ Muito curto: {chars} chars (-2.5)")
    elif chars > 3000:
        score -= 2.0
        feedback.append(f"❌ Muito longo: {chars} chars (-2)")
    else:
        feedback.append(f"○ Length fora do ótimo: {chars} chars (0)")

    # Parágrafos
    if paragraphs >= 14:
        score += 2.0
        feedback.append(f"✓ Escaneabilidade: {paragraphs} parágrafos (+2)")
    elif paragraphs >= 10:
        score += 1.0
        feedback.append(f"○ Parágrafos OK: {paragraphs} (+1)")
    else:
        score -= 2.0
        feedback.append(f"❌ Poucos parágrafos: {paragraphs} (-2) — quebrar mais o texto")

    # Blocos densos (parágrafo >150 chars, conforme algoritmo-metricas.md)
    dense_blocks = sum(1 for para in split_paragraphs(text) if len(para) > 150)
    if dense_blocks > 2:
        score -= 1.5
        feedback.append(f"❌ {dense_blocks} blocos densos detectados (-1.5)")

    # Framework (heurística fraca)
    framework_signals = re.findall(
        r"(problema|agita[çc][ãa]o|solu[çc][ãa]o|antes|depois|ponte|setup|conflito|resolu[çc][ãa]o|feature|vantagem|benef[íi]cio)",
        text,
        re.IGNORECASE,
    )
    if len(set(s.lower() for s in framework_signals)) >= 3:
        score += 1.0
        feedback.append("✓ Framework detectável (+1)")

    return min(10, max(0, score)), feedback


def score_cta(text: str, objetivo: str) -> tuple:
    feedback = []
    score = 5.0
    last_lines = '\n'.join(text.split('\n')[-5:]).lower()

    # "save" alinhado com os CTAs oficiais de ctas.md ("Salva esse post", "Guarda aqui", "Salva —", "Salva e manda")
    cta_patterns = {
        "save": r'\b(salva|salve|guarda|guarde)\b',
        "follow": r'(me siga|siga[- ]me|ative o)',
        "comment_dm": r'comenta\s+\w+',
        "dm": r'(manda?\s+(dm|mensagem)|dm aberta)',
        "click": r'clica\s+(no\s+)?link',
        "bio": r'link\s+(na|no)\s+(bio|perfil|primeiro coment)',
    }

    detected = [k for k, p in cta_patterns.items() if re.search(p, last_lines)]
    # Dedupe: variações do mesmo CTA não contam como múltiplos CTAs
    if "comment_dm" in detected and "dm" in detected:
        detected.remove("dm")
    if "click" in detected and "bio" in detected:
        detected.remove("click")

    if not detected:
        score = 3.5
        feedback.append("❌ CTA não detectado ou muito fraco")
    else:
        score = 7.0
        feedback.append(f"✓ CTA presente ({detected[0]})")

    if "save" in detected:
        score = min(10, score + 2.0)
        feedback.append("✓ CTA de save (prioridade 2026) (+2)")

    if objetivo == "authority" and "follow" in detected:
        score = min(10, score + 1.0)
        feedback.append("✓ CTA alinhado com Authority (+1)")
    elif objetivo == "sales" and ("comment_dm" in detected or "dm" in detected):
        score = min(10, score + 1.0)
        feedback.append("✓ CTA alinhado com Sales (+1)")
    elif objetivo == "engagement" and detected and re.search(r'(me conta|conta (a[íi]|pra mim)|comenta|qual (foi|seria|desses))', last_lines):
        score = min(10, score + 1.0)
        feedback.append("✓ CTA alinhado com Engagement (+1)")

    if len(detected) > 1:
        score -= 1.5
        feedback.append(f"⚠ Múltiplos CTAs detectados ({len(detected)}) — usar só 1 (-1.5)")

    return min(10, max(0, score)), feedback


def score_data(text: str) -> tuple:
    feedback = []
    data_count = count_data_points(text)

    if data_count >= 5:
        score = 10.0
        feedback.append(f"✓ Excelente: {data_count} pontos de dados")
    elif data_count >= 3:
        score = 8.0
        feedback.append(f"✓ Bom: {data_count} pontos de dados")
    elif data_count >= 1:
        score = 6.0
        feedback.append(f"○ Básico: {data_count} pontos de dados — adicionar mais números")
    else:
        score = 3.0
        feedback.append("❌ Sem dados concretos — adicionar números, %, valores")

    return score, feedback


# -----------------------------
# Agregação
# -----------------------------

def calculate_probabilities(final_score, saves_score, hook_score, algo_score):
    top1_base = (final_score / 10) * 20
    top1_bonus = 0
    if saves_score >= 9:
        top1_bonus += 7
    if hook_score >= 9:
        top1_bonus += 4
    if algo_score >= 9:
        top1_bonus += 4
    top1 = min(35, top1_base + top1_bonus)

    top5_base = (final_score / 10) * 50
    top5_bonus = 0
    if saves_score >= 8:
        top5_bonus += 10
    if hook_score >= 8:
        top5_bonus += 7
    if algo_score >= 8:
        top5_bonus += 7
    top5 = min(75, top5_base + top5_bonus)

    return {"top1": top1, "top5": top5}


def score_post(text, objetivo="authority"):
    saves_score, saves_fb = score_saves_potential(text)
    hook_score, hook_fb = score_hook(text)
    algo_score, algo_fb = score_algorithm(text)
    structure_score, structure_fb = score_structure(text)
    cta_score, cta_fb = score_cta(text, objetivo)
    data_score, data_fb = score_data(text)

    final_score = (
        saves_score * WEIGHTS["saves_potential"] +
        hook_score * WEIGHTS["hook"] +
        algo_score * WEIGHTS["algorithm"] +
        structure_score * WEIGHTS["structure"] +
        cta_score * WEIGHTS["cta"] +
        data_score * WEIGHTS["data"]
    )

    probs = calculate_probabilities(final_score, saves_score, hook_score, algo_score)

    dimensions = [
        ("Saves Potential", saves_score),
        ("Hook", hook_score),
        ("Algorithm", algo_score),
        ("Structure", structure_score),
        ("CTA", cta_score),
        ("Data", data_score),
    ]
    dimensions_sorted = sorted(dimensions, key=lambda x: x[1], reverse=True)

    return {
        "final_score": round(final_score, 1),
        "dimensions": {
            "saves_potential": {"score": saves_score, "feedback": saves_fb},
            "hook": {"score": hook_score, "feedback": hook_fb},
            "algorithm": {"score": algo_score, "feedback": algo_fb},
            "structure": {"score": structure_score, "feedback": structure_fb},
            "cta": {"score": cta_score, "feedback": cta_fb},
            "data": {"score": data_score, "feedback": data_fb},
        },
        "strongest": [d[0] for d in dimensions_sorted[:2]],
        "weakest": [d[0] for d in dimensions_sorted[-2:]],
        "probabilities": probs,
        "recommendation": get_recommendation(final_score),
    }


def get_recommendation(score):
    if score >= 9.0:
        return "✅ PUBLICAR — candidato a outlier"
    elif score >= 8.0:
        return "⚠️ REVISAR — ajustes rápidos e publicar"
    elif score >= 7.0:
        return "🔄 RETRABALHAR — gargalos claros"
    elif score >= 6.0:
        return "❌ REFAZER — ajuste estrutural"
    else:
        return "🚫 RECOMEÇAR — voltar para objetivo + estrutura"


def print_report(result):
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE SCORE — LinkedIn 360Brew (v3.5)")
    print("=" * 60)

    print(f"\n🎯 SCORE FINAL: {result['final_score']}/10")
    print(f"   {result['recommendation']}")

    print(f"\n📈 Probabilidades:")
    print(f"   Top 1%: {result['probabilities']['top1']:.0f}%")
    print(f"   Top 5%: {result['probabilities']['top5']:.0f}%")

    print(f"\n💪 Dimensões mais fortes: {', '.join(result['strongest'])}")
    print(f"⚠️  Dimensões mais fracas: {', '.join(result['weakest'])}")

    print("\n" + "-" * 60)
    print("📋 DETALHAMENTO POR DIMENSÃO:")
    print("-" * 60)

    labels = {
        "saves_potential": "SAVES POTENTIAL",
        "hook": "HOOK",
        "algorithm": "ALGORITHM",
        "structure": "STRUCTURE",
        "cta": "CTA",
        "data": "DATA",
    }

    for dim_key, dim_data in result['dimensions'].items():
        weight = WEIGHTS[dim_key] * 100
        print(f"\n{labels[dim_key]} ({weight:.0f}%): {dim_data['score']}/10")
        for fb in dim_data['feedback']:
            print(f"   {fb}")

    print("\n" + "=" * 60)


def print_compact(result):
    d = result["dimensions"]
    print(
        f"Score {result['final_score']}/10 | "
        f"Top1: {result['probabilities']['top1']:.0f}% | "
        f"Top5: {result['probabilities']['top5']:.0f}% | "
        f"Saves {d['saves_potential']['score']:.1f} Hook {d['hook']['score']:.1f} "
        f"Algo {d['algorithm']['score']:.1f} Struct {d['structure']['score']:.1f} "
        f"CTA {d['cta']['score']:.1f} Data {d['data']['score']:.1f} | "
        f"{result['recommendation']}"
    )


def main():
    parser = argparse.ArgumentParser(description="Score de post LinkedIn v3.5 baseado no 360Brew")
    parser.add_argument("arquivo", help="Arquivo com o texto do post")
    parser.add_argument("--objetivo", "-o", choices=["authority", "sales", "engagement"],
                        default="authority", help="Objetivo do post (default: authority)")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    parser.add_argument("--compact", action="store_true", help="Output em 1 linha para pipeline")

    args = parser.parse_args()

    try:
        text = Path(args.arquivo).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: arquivo '{args.arquivo}' não encontrado")
        sys.exit(1)

    result = score_post(text, args.objetivo)

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.compact:
        print_compact(result)
    else:
        print_report(result)


if __name__ == "__main__":
    main()
