---
name: humanizer-linkedin
description: Remove padrões de escrita IA (em-dash overuse, rule of three, vocabulário IA, promotional language, vague attributions) de posts de LinkedIn em PT-BR, preservando voz e specs 360Brew. Use no Pipeline de Finalização antes do score.
model: opus
effort: medium
---

# Humanizer LinkedIn

Carregue a skill `linkedin-authority-engine:humanizer-linkedin` e aplique as regras ao post. Saída: post refinado + diff compacto (máx 5 itens). Não quebrar specs (parágrafos curtos, sem link no corpo).
