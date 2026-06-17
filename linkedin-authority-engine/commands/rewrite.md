---
description: Modo Rewrite do LinkedIn Authority Engine — otimiza um post existente em duas versões (conservadora e bold), aplicando diagnóstico 360Brew, humanizer e score comparativo. Use quando o usuário tem um rascunho ou post pronto que precisa de melhoria.
argument-hint: "[post a otimizar]"
---

# /linkedin-authority-engine:rewrite

## Porta 2 — Leitura do Substrato (obrigatória, automática)

Antes de qualquer análise ou geração:

1. Carregue a skill `linkedin-authority-engine:authority-context`.
2. Leia `authority-context.md` (perfil completo) e todos os arquivos em `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Aplicar: tom de voz, pilares de conteúdo, credenciais reais, restrições editoriais.
4. Priorizar padrões vencedores de `winning-hooks.md` e `topic-performance.md`.
5. Validar a cada versão gerada: "Isso soa como esse cliente falaria?"

Se não houver post fornecido como argumento, solicitar: "Cole o post que deseja otimizar."

---

## REWRITE STEP 1 — Diagnóstico

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py` no post original e analisar contra as specs 360Brew (carregue `linkedin-authority-engine:algoritmo-360brew` para referência completa).

Apresentar diagnóstico:

```
DIAGNÓSTICO:
Score estimado: X/10
🚨 Problemas críticos: [ex: link no corpo, hashtags em excesso]
⚠️  Importantes: [ex: hook fraco, CTA genérico]
✅ O que funciona: [pontos fortes do post]
```

---

## REWRITE STEP 2 — Foco

Perguntar: "Foco principal do rewrite? (a) Hook, (b) Alcance/specs, (c) CTA, (d) Tudo"

Aguardar resposta antes de gerar as versões.

---

## REWRITE STEP 3 — Gerar 2 Versões

Com base no diagnóstico e no foco escolhido, gerar:

- **Versão A (Conservadora):** Mantém a voz e estrutura originais, corrige apenas os problemas técnicos identificados. Usa credenciais e tom do perfil carregado na Porta 2.
- **Versão B (Bold):** Hook mais forte (utilize a skill `linkedin-authority-engine:hooks`), reestrutura para impacto máximo (utilize `linkedin-authority-engine:estruturas-copywriting`), maximiza Saves Potential.

Para CTAs de ambas as versões, utilize a skill `linkedin-authority-engine:ctas` alinhando ao objetivo do post.

---

## REWRITE STEP 4 — Pipeline de Finalização em Ambas + Comparativo

> Ordem correta: humanizar primeiro, depois mostrar score comparativo. Senão o usuário escolhe baseado em score que vai mudar.

### Etapa A — Validação Técnica

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py` em cada versão. Corrigir erros antes de avançar.

### Etapa B — Humanizer LinkedIn

Acionar a skill `linkedin-authority-engine:humanizer-linkedin` em cada versão (A e B). Apresentar diff compacto por versão (máx. 5 itens).

### Etapa D — Score Final

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py` em cada versão humanizada:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objetivo <authority|sales|engagement>
```

Apresentar comparativo final:

| Métrica | Original | Versão A (humanizada) | Versão B (humanizada) |
|---------|----------|------------------------|------------------------|
| Score | X/10 | X/10 | X/10 |
| Saves Potential | X/10 | X/10 | X/10 |
| Hook | X/10 | X/10 | X/10 |
| Algorithm | X/10 | X/10 | X/10 |

Usuário escolhe a versão preferida (ou pede mix). Com a versão escolhida:

### Etapa C — Brief Visual

Acionar a skill `linkedin-authority-engine:brief-visual` na versão escolhida.

### Etapa E — Protocolo Pós-Publicação

Acionar a skill `linkedin-authority-engine:protocolo-pos-publicacao`.

1. Gerar o **1º comentário pronto** para colar logo após publicar: link (se houver) + contexto extra + 1 pergunta que convide respostas de 3+ frases.
2. Entregar resumo dos 90 minutos críticos.

---

## Porta 3 — Write-back ao Substrato

Após aprovação da versão final, conforme as instruções da skill `linkedin-authority-engine:authority-context`:

1. Anexar em `memory/winning-hooks.md`: o hook da versão escolhida (se houve melhoria de hook), categoria, objetivo, score final.
2. Anexar em `memory/topic-performance.md`: tema, tipo de post, score, data, objetivo.
3. Anexar em `memory/learnings.md`: o que foi alterado no rewrite, qual versão foi escolhida e por quê, restrições aplicadas.
4. Se o usuário rejeitou uma das versões, registrar o motivo em `memory/learnings.md`.

---

## Salvar o Post Final

Salvar o post final (versão escolhida, humanizada) em:

```
outputs/posts/<AAAAMMDD>-<slug>-v1.md
```

Se já existir versão anterior do mesmo slug, incrementar o número (v2, v3...).
