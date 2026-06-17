---
description: Protocolo de leitura e escrita do substrato de memória do cliente (authority-context.md + memory/). Use SEMPRE antes de gerar conteúdo (ler perfil + padrões vencedores) e ao fim de toda sessão de geração (write-back). Define as 3 portas do auto-enriquecimento.
---

# Authority Context — substrato auto-enriquecedor

A pasta do cliente é a fonte de verdade (local-first). Unabyss (MCP) é enriquecimento opcional quando presente.

## Arquivos
- `authority-context.md` — perfil vivo (13 seções). Template em `references/authority-context-template.md`.
- `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` — schemas em `references/memory-schemas.md`.
- `outputs/posts/` — posts gerados versionados (`AAAAMMDD-vN`).

## Porta 1 — Escrita (onboarding)
`init` escreve `authority-context.md`. Ver command `init`.

## Porta 2 — Leitura (geração)
Antes de gerar qualquer post: ler `authority-context.md` (tema central, 3 pilares, ICP, voz, restrições, territórios SIM/NÃO) e `memory/` (priorizar hooks/temas com veredito positivo). Se Unabyss presente, puxar performance real.

## Porta 3 — Write-back (fim da sessão)
Anexar a `memory/`: hooks/temas usados, ângulo, aprovado vs rejeitado. Performance (quando houver) atualiza `topic-performance.md`/`winning-hooks.md`. Nunca sobrescrever — append.

## Guardrails
Aplicar restrições da seção 9 do perfil (palavras proibidas, confidencial, sensibilidades) e respeitar territórios NÃO da seção 8.
