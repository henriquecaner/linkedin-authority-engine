---
description: Modo Thread do LinkedIn Authority Engine — cria uma série de 3-7 posts sobre um tema central, com arquitetura planejada (gancho, autoridade, educativo, story, conversão) e pipeline de finalização por post. Use quando o usuário quer uma campanha de conteúdo sequencial.
argument-hint: "[tema central]"
---

# /linkedin-authority-engine:thread

## Porta 2 — Leitura do Substrato (obrigatória, automática)

Antes de qualquer geração:

1. Carregue a skill `linkedin-authority-engine:authority-context`.
2. Leia `authority-context.md` (perfil completo) e todos os arquivos em `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Aplicar: tom de voz, pilares de conteúdo, credenciais reais, restrições editoriais em todos os posts da série.
4. Priorizar padrões vencedores: hooks aprovados em `winning-hooks.md`, temas com alta performance em `topic-performance.md`.
5. Garantir coerência de voz e progressão narrativa entre os posts.

---

## THREAD STEP 1 — Definir a Série

Se não foram fornecidos via argumento, coletar:
- Tema central da série
- Objetivo (Authority / Sales / Engagement)
- Número de posts desejado (3-7)
- Cadência pretendida (ex: diário, em dias alternados, semanal)

---

## THREAD STEP 2 — Arquitetura da Série

Gerar a arquitetura de posts adaptada ao número escolhido:

```
POST 1 — GANCHO DA SÉRIE (Hook/Contrarian)
  → Apresenta o tema, cria expectativa, promete valor

POST 2 — PROVA DE AUTORIDADE
  → Credencial real + contexto que justifica o tema

POST 3 — EDUCATIVO/HOW-TO
  → Valor prático acionável, alto Saves Potential

POST 4 — STORY/BASTIDORES
  → Conexão emocional, bastidores reais

POST 5 — CONVERSÃO/CTA
  → Fechamento com oferta, lead magnet ou próximo passo
```

Adaptar conforme o número de posts (ex: para 3 posts, condensar em Gancho + Educativo + Conversão).

Usar credenciais reais do perfil para ancorar cada post ao posicionamento da pessoa.

Apresentar a arquitetura e aguardar aprovação antes de gerar.

---

## THREAD STEP 3 — Ponto de Partida

Perguntar: "Prefere gerar todos os posts de uma vez ou um por vez (workflow guiado)?"

- "Todos de uma vez": gerar toda a série sequencialmente.
- "Um por vez": gerar o primeiro, aguardar aprovação, então o próximo.

---

## THREAD STEP 4 — Geração + Pipeline por Post

Para **cada post** da série:

1. Gerar o post seguindo as specs 360Brew (carregue `linkedin-authority-engine:algoritmo-360brew`):
   - 1.250-2.500 caracteres
   - 14+ parágrafos curtos (máx. ~19 palavras cada)
   - Sem links no corpo, sem hashtags genéricas
   - Re-hook no meio do post
   - Usar hook adequado ao tipo de post (skill `linkedin-authority-engine:hooks`)
   - CTA alinhado ao objetivo (skill `linkedin-authority-engine:ctas`)

2. Executar o **Pipeline de Finalização** completo:

   **Etapa A — Validação Técnica**

   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt
   ```

   Corrigir erros antes de avançar.

   **Etapa B — Humanizer LinkedIn**

   Acionar a skill `linkedin-authority-engine:humanizer-linkedin`. Apresentar diff compacto (máx. 5 itens).

   **Etapa C — Brief Visual**

   Acionar a skill `linkedin-authority-engine:brief-visual`.

   **Etapa D — Score Final**

   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objetivo <authority|sales|engagement>
   ```

   **Etapa E — Protocolo Pós-Publicação**

   Acionar a skill `linkedin-authority-engine:protocolo-pos-publicacao`. Gerar o 1º comentário pronto para cada post.

3. Apresentar o post no formato:

```
━━━━━━━━━━━━━━━━━━━━━━━
POST [N]/[TOTAL] — [Tipo]
━━━━━━━━━━━━━━━━━━━━━━━

[Texto humanizado]

Humanizer: [diff compacto]
Score: X.X/10 | Top 1%: X% | Top 5%: X%
Brief Visual: [formato + conceito + prompt IA]
━━━━━━━━━━━━━━━━━━━━━━━
```

---

## THREAD STEP 5 — Calendário de Publicação

Após gerar todos os posts, apresentar o calendário sugerido:

| Post | Tema | Tipo | Score | Data sugerida | Janela (BRT) |
|------|------|------|-------|---------------|--------------|

Para timing recomendado por objetivo e dia da semana, consulte a skill `linkedin-authority-engine:protocolo-pos-publicacao`.

---

## Porta 3 — Write-back ao Substrato

Após aprovação da série, conforme as instruções da skill `linkedin-authority-engine:authority-context`:

1. Anexar em `memory/winning-hooks.md`: por hook aprovado da série — data, padrão de hook, tipo, categoria, objetivo, score. (Colunas `vezes usado`, `performance média`, `keep/kill` ficam vazias até v1.x.)
2. Anexar em `memory/topic-performance.md`: por post da série — data, tema, pilar, tipo de post, score. (Colunas de performance ficam vazias até v1.x.)
3. Anexar em `memory/learnings.md`: o que funcionou na arquitetura, o que foi ajustado, padrões identificados.
4. Se algum post foi rejeitado ou reescrito, registrar o motivo em `memory/learnings.md`.

---

## Salvar os Posts Finais

Salvar cada post aprovado em:

```
outputs/posts/<AAAAMMDD>-<slug-do-post>-v1.md
```

Se já existir versão anterior do mesmo slug, incrementar o número (v2, v3...).
