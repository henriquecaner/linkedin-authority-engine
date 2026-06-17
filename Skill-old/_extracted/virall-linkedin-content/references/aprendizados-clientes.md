# Aprendizados de Clientes (Feedback Loop — fallback local)

> Registro de padrões observados em posts reais publicados. Input do STEP 0 quando houver cliente conhecido.
>
> **Nota v4.0:** a fonte primária de performance real agora é o **Unabyss** ([integracao-unabyss.md](integracao-unabyss.md)). Este arquivo é o fallback quando o MCP não estiver disponível, e o local para padrões consolidados que merecem virar regra da skill.

Este arquivo existe para fechar o loop entre o que o skill prevê (score estimado) e o que o algoritmo entrega na prática. Toda vez que um post gerado por este skill for publicado e tiver performance relevante (outlier positivo ou negativo), registrar aqui.

## Formato de entrada

```
## [Data publicação] — [Cliente] — [Objetivo]

**Post:** [título ou primeira frase]

**Scoring previsto:** X.X/10 (Hook: X, Saves: X, Algo: X)

**Performance real (90 min):**
- Impressões: X
- Reações: X
- Comentários: X
- Saves: X
- Shares: X

**Performance real (7 dias):**
- Impressões: X
- Dwell time médio: X seg

**Delta vs baseline do perfil:** +X% / -X% de alcance

**Hipótese do que funcionou / não funcionou:**
[Observação do cliente ou do Claude após revisão]

**Ajuste sugerido no skill:**
[Nenhum / Revisar peso X / Adicionar padrão Y ao humanizer / etc.]
```

## Padrões emergentes

Esta seção é atualizada periodicamente com os aprendizados recorrentes.

### 2026-Q2

*(Nenhum registro ainda. Começar a popular a partir dos primeiros posts publicados usando este skill.)*

## Como usar no STEP 0

Quando Claude iniciar um modo com contexto de cliente carregado, checar silenciosamente:
1. Existem registros deste cliente neste arquivo?
2. Se sim, ler os últimos 3-5 registros do cliente antes de gerar conteúdo
3. Aplicar os aprendizados: "Post com hook de prova de trabalho + número específico teve 3x mais saves para este cliente" → priorizar esse padrão no STEP 4

## Como usar na Etapa D do Pipeline (Score Final)

Após o score ser calculado, se houver histórico do cliente, apresentar:

```
📊 BASELINE DESTE CLIENTE
- Score médio dos últimos 5 posts: X.X/10
- Outlier benchmark: [descrição do melhor post do cliente]
- Gap vs baseline: +X.X / -X.X
```

Isso dá contexto relativo, não só absoluto.
