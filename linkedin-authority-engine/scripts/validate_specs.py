#!/usr/bin/env python3
"""
LinkedIn Post Validator - Valida specs do 360Brew
Uso: python validate_specs.py <arquivo_post.txt>
"""

import argparse
import re
import sys
from pathlib import Path

# Specs do 360Brew
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
}

# Padrões punidos
# Anchored para evitar falsos positivos (ex: "nem todo mundo concorda comigo")
PUNISHED_PATTERNS = [
    (r"\bo que voc[êe]s? acham?\s*\?", "O que você acha?"),
    (r"(?:^|[.!?…]\s*)concordam?\s*\?", "Concordam?"),
    (r"\bbom dia[,]?\s*linkedin", "Bom dia, LinkedIn!"),
    (r"\breflex[ãa]o do dia\b", "Reflexão do dia"),
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


def has_link_in_body(text: str) -> bool:
    """Detecta link em QUALQUER parte do corpo. A regra 360Brew não tem exceção:
    link pertence ao 1º comentário, nunca ao post (-60% alcance)."""
    return bool(re.search(r'https?://|www\.', text, re.IGNORECASE))


def count_hashtags(text: str) -> int:
    return len(re.findall(r'#\w+', text))


def get_long_paragraphs(text: str) -> list:
    """Retorna parágrafos com mais de 19 palavras"""
    paragraphs = split_paragraphs(text)
    long_paras = []
    for i, p in enumerate(paragraphs, 1):
        words = len(p.split())
        if words > SPECS["max_words_per_paragraph"]:
            long_paras.append((i, words, p[:50] + "..."))
    return long_paras


def check_punished_patterns(text: str) -> list:
    """Verifica padrões punidos pelo algoritmo"""
    found = []
    for pattern, name in PUNISHED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found


def validate_post(text: str) -> dict:
    """Valida post contra specs do 360Brew"""
    
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {},
        "suggestions": []
    }
    
    # Stats básicos
    chars = count_chars(text)
    paragraphs = count_paragraphs(text)
    avg_len = avg_word_length(text)
    
    results["stats"] = {
        "caracteres": chars,
        "paragrafos": paragraphs,
        "media_letras_palavra": round(avg_len, 1),
    }
    
    # Validar caracteres
    if chars < SPECS["chars_warning_min"]:
        results["errors"].append(f"Muito curto: {chars} chars (mínimo aceitável: {SPECS['chars_warning_min']}; recomendado: {SPECS['chars_min']}-{SPECS['chars_max']})")
        results["valid"] = False
        results["suggestions"].append("Expandir o conteúdo com mais contexto ou exemplos")
    elif chars < SPECS["chars_min"]:
        results["warnings"].append(f"Abaixo do ideal: {chars} chars (recomendado: {SPECS['chars_min']}-{SPECS['chars_max']})")
    elif chars > SPECS["chars_warning_max"]:
        results["errors"].append(f"Muito longo: {chars} chars (máximo aceitável: {SPECS['chars_warning_max']}; recomendado: {SPECS['chars_min']}-{SPECS['chars_max']})")
        results["valid"] = False
        results["suggestions"].append("Cortar partes menos essenciais")
    elif chars > SPECS["chars_max"]:
        results["warnings"].append(f"Acima do ideal: {chars} chars (recomendado: {SPECS['chars_min']}-{SPECS['chars_max']})")
    
    # Validar parágrafos
    if paragraphs < SPECS["paragraphs_warning"]:
        results["errors"].append(f"Poucos parágrafos: {paragraphs} (mínimo: {SPECS['paragraphs_min']})")
        results["valid"] = False
        results["suggestions"].append("Quebrar o texto em mais parágrafos curtos (1-3 linhas cada)")
    elif paragraphs < SPECS["paragraphs_min"]:
        results["warnings"].append(f"Parágrafos abaixo do ideal: {paragraphs} (recomendado: {SPECS['paragraphs_min']}+)")
    
    # Validar complexidade das palavras
    if avg_len > SPECS["avg_word_length_warning"]:
        results["errors"].append(f"Palavras muito complexas: média {avg_len:.1f} letras (máximo: {SPECS['avg_word_length_max']})")
        results["valid"] = False
        results["suggestions"].append("Usar palavras mais simples e curtas")
    elif avg_len > SPECS["avg_word_length_max"]:
        results["warnings"].append(f"Palavras um pouco complexas: média {avg_len:.1f} letras (ideal: ≤{SPECS['avg_word_length_max']})")
    
    # Verificar parágrafos longos
    long_paras = get_long_paragraphs(text)
    if long_paras:
        for para_num, word_count, preview in long_paras:
            results["warnings"].append(f"Parágrafo {para_num} muito longo: {word_count} palavras")
        results["suggestions"].append(f"Quebrar os {len(long_paras)} parágrafos longos em blocos menores")
    
    # Verificar padrões punidos
    punished = check_punished_patterns(text)
    if punished:
        for p in punished:
            results["errors"].append(f"Padrão punido detectado: '{p}'")
        results["valid"] = False
        results["suggestions"].append("Remover padrões de isca e usar hooks de prova de trabalho/autoridade")

    # Verificar link no corpo (-60% alcance)
    if has_link_in_body(text):
        results["errors"].append("Link no corpo do post detectado (-60% alcance)")
        results["valid"] = False
        results["suggestions"].append("Mover link para o 1º comentário")

    # Verificar hashtags
    hashtag_count = count_hashtags(text)
    results["stats"]["hashtags"] = hashtag_count
    if hashtag_count > 2:
        results["errors"].append(f"Hashtags em excesso: {hashtag_count} (default 2026: zero, máx 2 hiper-específicas)")
        results["valid"] = False
        results["suggestions"].append("Remover hashtags genéricas, manter no máximo 2 ultra-específicas")
    elif hashtag_count > 0:
        results["warnings"].append(f"{hashtag_count} hashtag(s) detectada(s) — confirmar se são hiper-específicas")

    return results


def print_report(results: dict):
    """Imprime relatório de validação"""
    
    print("\n" + "="*60)
    print("✅ VALIDAÇÃO DE SPECS - LinkedIn 360Brew")
    print("="*60)
    
    # Status geral
    if results["valid"]:
        print("\n🟢 POST VÁLIDO - Specs do 360Brew atendidas")
    else:
        print("\n🔴 POST INVÁLIDO - Corrigir erros abaixo")
    
    # Stats
    print("\n📊 ESTATÍSTICAS:")
    for stat, value in results["stats"].items():
        print(f"   • {stat}: {value}")
    
    # Erros
    if results["errors"]:
        print("\n❌ ERROS (bloqueia publicação):")
        for err in results["errors"]:
            print(f"   • {err}")
    
    # Warnings
    if results["warnings"]:
        print("\n⚠️  AVISOS (recomendado corrigir):")
        for warn in results["warnings"]:
            print(f"   • {warn}")
    
    # Sugestões
    if results["suggestions"]:
        print("\n💡 SUGESTÕES:")
        for sug in results["suggestions"]:
            print(f"   • {sug}")
    
    # Specs de referência
    print("\n" + "-"*60)
    print("📋 SPECS 360BREW DE REFERÊNCIA:")
    print(f"   • Caracteres: {SPECS['chars_min']}-{SPECS['chars_max']}")
    print(f"   • Parágrafos: {SPECS['paragraphs_min']}+ curtos")
    print(f"   • Palavras: média ≤{SPECS['avg_word_length_max']} letras")
    print(f"   • Parágrafos: máx {SPECS['max_words_per_paragraph']} palavras cada")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Validar specs de post LinkedIn")
    parser.add_argument("arquivo", help="Arquivo com o texto do post")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    parser.add_argument("--quiet", "-q", action="store_true", help="Apenas status (exit code)")
    
    args = parser.parse_args()
    
    # Ler arquivo
    try:
        text = Path(args.arquivo).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: arquivo '{args.arquivo}' não encontrado")
        sys.exit(1)
    
    # Validar
    results = validate_post(text)
    
    # Output
    if args.quiet:
        sys.exit(0 if results["valid"] else 1)
    elif args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_report(results)
    
    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
