---
description: Modo Score do LinkedIn Authority Engine — avalia e humaniza um post pronto, rodando validação técnica, humanizer e score nas 6 dimensões com veredicto final (publicar / ajustar / retrabalhar). Use quando o usuário tem um post pronto e quer saber se está pronto para publicar.
argument-hint: "[post a avaliar]"
---

# /linkedin-authority-engine:score

## Porta 2 — Leitura do Substrato (obrigatória, automática)

Antes de avaliar:

1. Carregue a skill `linkedin-authority-engine:authority-context`.
2. Leia `authority-context.md` (perfil completo) e todos os arquivos em `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Aplicar: tom de voz, pilares de conteúdo, credenciais reais, restrições editoriais como critérios adicionais na avaliação.
4. Se `topic-performance.md` tiver baseline real do perfil, usar para comparação relativa no score.

Se não houver post fornecido como argumento, solicitar: "Cole o post que deseja avaliar."

---

## Pipeline Parcial (MODO SCORE)

> Pula geração e Brief Visual, vai direto para avaliação. Sem Protocolo Pós-Publicação (a menos que solicitado explicitamente).

### Etapa A — Validação Técnica

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py` no post:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt
```

Apresentar resultado:

```
VALIDAÇÃO TÉCNICA:
🚨 Erros críticos: [link no corpo, hashtags em excesso, ...]
⚠️  Avisos: [parágrafos densos, palavras complexas, ...]
✅ Specs OK: [o que está dentro dos parâmetros]
```

Se houver erros críticos, perguntar se o usuário quer corrigir antes de humanizar. Se sim, corrigir; se não, continuar e registrar os erros no score final.

### Etapa B — Humanizer LinkedIn

Acionar a skill `linkedin-authority-engine:humanizer-linkedin` no post. Apresentar diff compacto (máx. 5 itens alterados) com as substituições realizadas.

### Etapa D — Score Final

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py` no post humanizado:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objetivo <authority|sales|engagement>
```

Se o objetivo não foi informado, inferir pelo conteúdo do post ou perguntar.

Apresentar relatório nas 6 dimensões:

| Dimensão | Peso | Nota | Observação |
|----------|------|------|------------|
| Saves Potential | 30% | X/10 | ... |
| Hook | 20% | X/10 | ... |
| Algorithm | 20% | X/10 | ... |
| Structure | 15% | X/10 | ... |
| CTA | 10% | X/10 | ... |
| Data | 5% | X/10 | ... |
| **Total** | 100% | **X.X/10** | |

Se `topic-performance.md` tiver baseline real, apresentar comparação: "Média deste perfil: X.X/10 — este post está X% acima/abaixo."

### Veredicto Final

Com base no score:

- **Score ≥ 9/10:** "Publicar. Post pronto."
- **Score 7-8.9/10:** "Ajustar. [Indicar 1-2 melhorias específicas com maior impacto no score.]"
- **Score < 7/10:** "Retrabalhar. [Indicar os problemas críticos e sugerir usar o modo Rewrite (`/linkedin-authority-engine:rewrite`).]"

---

## Porta 3 — Write-back ao Substrato

Após a avaliação, conforme as instruções da skill `linkedin-authority-engine:authority-context`:

1. Anexar em `memory/topic-performance.md`: tema, tipo de post, score, data da avaliação, objetivo.
2. Anexar em `memory/learnings.md`: principais achados da avaliação, erros encontrados, padrões que prejudicaram o score.
3. Se o hook for forte (nota ≥ 8/10 na dimensão Hook), anexar em `memory/winning-hooks.md`.

---

## Salvar o Post Avaliado

Salvar o post na versão humanizada (pós-Etapa B) em:

```
outputs/posts/<AAAAMMDD>-<slug>-v1.md
```

Se já existir versão anterior do mesmo slug, incrementar o número (v2, v3...).
