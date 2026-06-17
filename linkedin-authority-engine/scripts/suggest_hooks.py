#!/usr/bin/env python3
"""
LinkedIn Hook Suggester - Sugere hooks baseado em categoria e objetivo
Uso: python suggest_hooks.py --categoria <cat> --objetivo <obj> [--tema "seu tema"] [--seed N]

Os tipos e o mapeamento categoria->tipo espelham references/hooks.md.
"""

import argparse
import random
import re

# Biblioteca de hooks organizados por tipo (subset de references/hooks.md)
HOOKS = {
    "prova_trabalho": [
        "Gastei R${valor} testando {tema}. Aqui está o que descobri:",
        "Analisei {numero} {items} nos últimos {tempo}. O padrão que encontrei:",
        "Testei {numero} ferramentas de {tema}. Só {numero_menor} funcionam:",
        "Investi {tempo} em {tema}. Resultado: {resultado}",
        "Perdi R${valor} por ignorar isso sobre {tema}:",
        "De {antes} para {depois} em {tempo}. O que mudou:",
        "{numero} experimentos depois, posso afirmar sobre {tema}:",
        "Gastei {tempo} para você não precisar: {tema}",
    ],
    "prova_autoridade": [
        "O que {numero} anos em {industria} me ensinaram sobre {tema}:",
        "Como {cargo}, descobri que {tema}:",
        "Liderando {numero} pessoas, aprendi algo sobre {tema}:",
        "Depois de {numero} projetos de {tema}, posso afirmar:",
        "{numero} clientes depois, o padrão é claro sobre {tema}:",
        "O erro que vejo em 90% das empresas sobre {tema}:",
        "A verdade que {numero} anos de experiência me mostraram:",
    ],
    "transformacao": [
        "De {antes} para {depois} em {tempo}.",
        "Era {situacao_antes}. Hoje {situacao_depois}.",
        "Há {tempo}, eu {antes}. Agora {depois}.",
        "{numero}% de crescimento em {tempo}. Veja como:",
        "De zero a {resultado} em {tempo}. O caminho:",
        "Antes: {antes}. Depois: {depois}. A diferença:",
    ],
    "contrarian": [
        "Todo mundo diz que {crenca_comum}. Eu fiz diferente:",
        "Opinião impopular: {opiniao}",
        "O conselho mais comum sobre {tema} está errado.",
        "Pare de {erro_comum}. Comece {alternativa}.",
        "95% das pessoas fazem {tema} errado. Aqui está o porquê:",
        "Você NÃO deveria {conselho_comum}. Faça isso:",
        "{crenca_comum}? Mentira. A verdade:",
    ],
    "confissao": [
        "Perdi R${valor} por causa de {erro}.",
        "Meu maior erro em {tema}:",
        "Fui demitido. E foi a melhor coisa que aconteceu.",
        "Fracassei {numero} vezes em {tema}. O que aprendi:",
        "O erro que quase destruiu {resultado}:",
        "Admito: eu estava errado sobre {tema}.",
    ],
    "curiosidade": [
        "Você sabia que {estatistica}?",
        "{numero} erros que você está cometendo em {tema}:",
        "A maneira mais fácil de {objetivo}:",
        "O que ninguém te conta sobre {tema}:",
        "Por que {pratica_comum} não funciona mais:",
        "O segredo para {resultado} em {tempo}:",
    ],
    "historia": [
        "Nunca vou esquecer quando {momento}.",
        "Em {ano}, eu estava {situacao}. Hoje...",
        "Meu mentor me disse algo que mudou tudo:",
        "Uma ligação mudou minha carreira. Aqui está o que aconteceu:",
        "O dia que {evento} me ensinou sobre {tema}:",
    ],
    # Maior Saves Potential (dimensão de peso 30% no scoring). Ver hooks.md §8.
    "listas_frameworks": [
        "Meu framework de {numero} passos para {resultado}:",
        "{numero} lições de {experiencia}:",
        "Minha checklist de {numero} itens para {objetivo}:",
        "Os {numero} princípios que mudaram meu {resultado}:",
        "{numero} regras não-negociáveis em {tema}:",
        "O sistema de {numero} etapas que uso para {objetivo}:",
        "Meu template de {tema} (copiável):",
        "{numero} red flags em {tema}:",
    ],
}

# Mapeamento categoria -> tipos de hook recomendados (espelha hooks.md)
CATEGORIA_HOOKS = {
    "licao_carreira": ["historia", "prova_autoridade", "transformacao"],
    "conquista": ["prova_trabalho", "transformacao", "prova_autoridade"],
    "fracasso": ["confissao", "historia", "prova_trabalho"],
    "desmistificar": ["contrarian", "prova_autoridade", "curiosidade"],
    "dica_pratica": ["prova_trabalho", "listas_frameworks", "curiosidade"],
    "opiniao": ["contrarian", "prova_autoridade"],
    "bastidores": ["historia", "confissao", "prova_trabalho"],
    "outro": ["curiosidade", "prova_trabalho", "listas_frameworks"],
}

# Mapeamento objetivo -> ajustes (listas_frameworks puxa saves em qualquer objetivo)
OBJETIVO_BONUS = {
    "authority": ["prova_autoridade", "prova_trabalho", "listas_frameworks"],
    "sales": ["transformacao", "prova_trabalho", "listas_frameworks"],
    "engagement": ["contrarian", "curiosidade", "confissao"],
}


def get_recommended_types(categoria: str, objetivo: str) -> list:
    """Retorna tipos de hook recomendados para categoria + objetivo"""
    base_types = CATEGORIA_HOOKS.get(categoria, CATEGORIA_HOOKS["outro"])
    bonus_types = OBJETIVO_BONUS.get(objetivo, [])

    all_types = []
    for t in base_types:
        if t in bonus_types:
            all_types.insert(0, t)  # Prioridade: aparece em ambos
        else:
            all_types.append(t)

    for t in bonus_types:
        if t not in all_types:
            all_types.append(t)

    return all_types[:4]  # Top 4


def fill_placeholders(hook: str, tema: str) -> str:
    """Preenche {tema} com o tema real e demais placeholders com [marcadores]."""
    hook = hook.replace("{tema}", tema)
    hook = hook.replace("{numero}", "X").replace("{numero_menor}", "X")
    return re.sub(r"\{(\w+)\}", lambda m: "[" + m.group(1).replace("_", " ") + "]", hook)


def suggest_hooks(categoria: str, objetivo: str, tema: str = "[seu tema]", count: int = 5) -> list:
    """Gera sugestões de hooks"""
    recommended_types = get_recommended_types(categoria, objetivo)
    suggestions = []

    for hook_type in recommended_types:
        hooks = HOOKS.get(hook_type, [])
        selected = random.sample(hooks, min(2, len(hooks)))
        for hook in selected:
            suggestions.append({
                "tipo": hook_type.replace("_", " ").title(),
                "template": hook,
                "exemplo": fill_placeholders(hook, tema),
            })

    return suggestions[:count]


def print_suggestions(suggestions: list, categoria: str, objetivo: str, tema: str):
    """Imprime sugestões formatadas"""
    print("\n" + "=" * 60)
    print("🎣 SUGESTÕES DE HOOKS - LinkedIn 360Brew")
    print("=" * 60)

    print(f"\n📋 Configuração:")
    print(f"   • Categoria: {categoria.replace('_', ' ').title()}")
    print(f"   • Objetivo: {objetivo.title()}")
    print(f"   • Tema: {tema}")

    print("\n" + "-" * 60)
    print("💡 HOOKS RECOMENDADOS:")
    print("-" * 60)

    for i, sug in enumerate(suggestions, 1):
        print(f"\n{i}. [{sug['tipo']}]")
        print(f"   Template: {sug['template']}")
        print(f"   Exemplo:  {sug['exemplo']}")

    print("\n" + "-" * 60)
    print("⚠️  HOOKS A EVITAR (punidos pelo 360Brew):")
    print("   ❌ 'O que você acha?'")
    print("   ❌ 'Concordam?'")
    print("   ❌ 'Bom dia, LinkedIn!'")
    print("   ❌ Clickbaits genéricos sem prova")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Sugerir hooks para posts LinkedIn")
    parser.add_argument("--categoria", "-c", required=True,
                        choices=["licao_carreira", "conquista", "fracasso",
                                 "desmistificar", "dica_pratica", "opiniao",
                                 "bastidores", "outro"],
                        help="Categoria do post")
    parser.add_argument("--objetivo", "-o", required=True,
                        choices=["authority", "sales", "engagement"],
                        help="Objetivo do post")
    parser.add_argument("--tema", "-t", default="[seu tema]",
                        help="Tema específico do post")
    parser.add_argument("--count", "-n", type=int, default=5,
                        help="Número de sugestões (default: 5; apresentar 3 ao usuário)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed para output reprodutível")
    parser.add_argument("--json", action="store_true", help="Output em JSON")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    suggestions = suggest_hooks(args.categoria, args.objetivo, args.tema, args.count)

    if args.json:
        import json
        print(json.dumps(suggestions, ensure_ascii=False, indent=2))
    else:
        print_suggestions(suggestions, args.categoria, args.objetivo, args.tema)


if __name__ == "__main__":
    main()
