---
name: humanizer-linkedin
description: Pipeline de humanização para posts LinkedIn (Etapa B do Pipeline de Finalização): quando executar, como executar, padrões de IA prioritários em posts LinkedIn, princípios de cirurgia (não demolição) e formato de output com diff compacto. Use automaticamente após o CTA ser escolhido, antes do score final, em qualquer modo de geração de post.
---

# Pipeline Humanizer (LinkedIn)

> Esta referência descreve **como** aplicar humanizer em posts LinkedIn. A lista completa dos 24 padrões de IA vive na skill `humanizer` e **não deve ser duplicada aqui**. Se divergir das duas listas, o guia oficial é a skill `humanizer`.

## Quando executar

Automático após o CTA ser escolhido e integrado ao post — é a **Etapa B do Pipeline de Finalização**, compartilhada por todos os modos (Guiado, Rewrite, Thread e Score).

Não perguntar ao usuário. É parte do pipeline padrão.

## Como executar

1. Acionar a skill `humanizer` com o post completo (hook + corpo + CTA)
2. A skill retorna o texto humanizado + diff dos padrões detectados
3. Apresentar diff compacto (máximo 5 itens) seguido do post humanizado completo

## Padrões prioritários em posts LinkedIn

Estes são os padrões que aparecem com mais frequência em posts LinkedIn gerados por IA. Se a skill `humanizer` estiver indisponível por algum motivo, Claude pode executar uma passada manual priorizando:

| Padrão | Exemplos a detectar |
|--------|---------------------|
| Significance inflation | "pivotal", "transformativo", "vital", "impactante", "robusto" |
| Promotional language | "incrível", "revolucionário", "groundbreaking", "poderoso" |
| Superficial -ing | "mostrando que", "refletindo a", "destacando", "contribuindo" |
| Em dashes em excesso | Substituir por ponto, vírgula ou reescrita |
| Rule of three | "velocidade, qualidade e resultado" → colapsar ou variar |
| Vague attributions | "especialistas dizem", "o mercado indica" → especificar ou remover |
| Filler phrases | "No contexto atual", "É importante ressaltar que", "Vale destacar" |
| Generic conclusions | "O futuro é promissor", "Está apenas começando", "O momento é agora" |
| Copula avoidance | "serve como", "funciona como", "atua como" → verbo direto |

Os outros 15 padrões estão documentados na skill `humanizer`.

## Princípios

**Cirurgia, não demolição.** Trocar a palavra ou frase problemática mantendo estrutura, dados e voz do autor. O humanizer não reescreve o post, ele corrige padrões.

**Preservar voz do cliente.** Se houver documento de estilo carregado no STEP 0, não remover vocabulário que é parte intencional da voz do cliente (mesmo que caia em algum padrão genérico).

**Preservar dados.** Nunca alterar números, valores, métricas ou nomes próprios na passada do humanizer.

## Output do pipeline

```
✏️ Humanizer aplicado:
- "[palavra/frase original]" → "[correção]"
- "[padrão detectado]" → removido / reestruturado
(máx. 5 itens — omitir se não houver padrões significativos)
```

Seguido pelo **post humanizado completo** (versão final para scoring).
