# Integração Unabyss — Dados Reais de Performance

> O Unabyss é a camada de memória persistente do usuário (MCP). Ele é a **fonte primária** de contexto de cliente e de performance real dos posts. O arquivo [aprendizados-clientes.md](aprendizados-clientes.md) é o fallback quando o MCP não estiver disponível.

## Por que isso importa

O sistema de scoring estima performance com benchmarks genéricos do 360Brew. O Unabyss fecha o loop com dados do perfil real: quais temas, hooks e CTAs performaram **para este usuário**. Pauta guiada por dado real > pauta guiada por benchmark.

## Como detectar se o Unabyss está disponível

Procurar tools MCP com nomes `query`, `store`, `agentic_query` (o prefixo do servidor varia por sessão). Se não existirem, usar o fallback em arquivo sem perguntar nada ao usuário.

## Quando CONSULTAR (`query`)

| Momento | Query sugerida |
|---------|----------------|
| **STEP 0 — Contexto** | "Qual o posicionamento, nicho e tom de voz de [usuário/cliente] no LinkedIn?" |
| **STEP 0 — Histórico** | "Quais foram os últimos posts de LinkedIn publicados e suas métricas (impressões, reações, comentários, saves)?" |
| **STEP 1.2 — Pautas** | "Quais temas e formatos de post LinkedIn tiveram melhor engajamento nos últimos meses?" |
| **Etapa D — Baseline** | "Qual a média de reações e comentários dos últimos 5 posts de LinkedIn?" |

**Uso no STEP 1.2:** se houver dados, priorizar pautas em temas comprovados e mencionar o porquê ("seu post sobre X teve 40 reações — 6x sua média"). Se não houver, seguir o fluxo normal.

**Uso na Etapa D (Score):** se houver baseline, apresentar junto com o score:

```
📊 BASELINE DESTE PERFIL (via Unabyss)
- Média dos últimos posts: X reações, Y comentários
- Melhor post recente: [tema] (X reações)
- Este post ataca o mesmo padrão? [sim/não + ajuste]
```

## Quando GRAVAR (`store`)

1. **Ao entregar o post final** (fim do Pipeline):

```
LinkedIn post finalizado em [data] — [cliente/usuário]
Tema: [tema] | Categoria: [categoria] | Objetivo: [objetivo]
Hook: "[primeira linha]"
Score Virall: X.X/10 (Saves X, Hook X, Algo X)
CTA: [tipo de CTA]
Status: aguardando publicação
```

2. **Quando o usuário trouxer métricas reais** (90 min ou 7 dias depois):

```
Performance LinkedIn — post de [data] ("[hook resumido]")
Impressões: X | Reações: X | Comentários: X | Saves: X
Delta vs baseline: +X% / -X%
Aprendizado: [o que funcionou ou não — 1 frase]
```

Gravar de forma proativa, sem pedir permissão — é parte do pipeline. Avisar em 1 linha: "Registrei no Unabyss para calibrar os próximos posts."

## Regras

- **Nunca bloquear o fluxo** esperando o Unabyss. Timeout ou erro → fallback silencioso para [aprendizados-clientes.md](aprendizados-clientes.md).
- **Não inventar métricas.** Se o Unabyss não tiver impressões/saves, dizer que faltam e pedir o export do Analytics se o usuário quiser o loop completo.
- **Prefixar memórias** com "LinkedIn post" / "Performance LinkedIn" para facilitar retrieval futuro.
