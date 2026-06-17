---
name: humanizer-linkedin
description: |
  Remove padrões de escrita IA (em-dash overuse, rule of three, vocabulário IA, promotional language, vague attributions) de posts de LinkedIn em PT-BR, preservando voz e specs 360Brew. Use no Pipeline de Finalização antes do score.

  <example>
  Context: Post rascunho gerado pelo strategist precisa ser humanizado antes do score final
  user: "Humaniza esse post antes de publicar: 'A liderança transformadora é revolucionária e inovadora — ela navega pelos desafios com maestria e redefine paradigmas.'"
  assistant: "Vou usar o humanizer-linkedin para limpar os padrões de IA e preservar a voz do cliente."
  <commentary>
  Etapa B do Pipeline de Finalização: remove vocabulário inflado (revolucionária, inovadora, navega), em-dash excessivo e padrões AI antes de calcular score 360Brew.
  </commentary>
  </example>

  <example>
  Context: Rascunho de post com rule of three vaga e promotional language
  user: "Revisa esse trecho: 'Entrego resultados rápidos, simples e eficazes para executivos que buscam transformação real.'"
  assistant: "Vou acionar o humanizer-linkedin para cortar o rule of three genérico e substituir por especificidade concreta."
  <commentary>
  Rule of three vago (rápidos, simples, eficazes — sinônimos disfarçados) e promotional language (transformação real) são removidos. Output: diff compacto + post refinado.
  </commentary>
  </example>
model: opus
effort: medium
---

# Humanizer LinkedIn

Carregue a skill `linkedin-authority-engine:humanizer-linkedin` e aplique as regras ao post. Saída: post refinado + diff compacto (máx 5 itens). Não quebrar specs (parágrafos curtos, sem link no corpo).
