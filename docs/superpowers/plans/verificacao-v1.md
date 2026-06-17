# Verificação v1 — plugin `linkedin-authority-engine`

> Registro da Task 10. Data: 2026-06-17.

## Automatizado (controller) — ✅ verde

- **Suite completa:** `12 passed in 0.16s` (`.venv/bin/python -m pytest tests/ -v`).
  - 9 testes estruturais (plugin.json, marketplace.json, 10 skills + frontmatter, sem refs stale, authority-context 13 seções + schemas de memory, discovery-script cobre seções, frontmatter de commands com description+argument-hint, frontmatter de agents, hooks.json).
  - 3 smoke tests de CLI (validate_specs, score_post, suggest_hooks rodam e produzem saída).
- **Integridade de referências:** toda referência `linkedin-authority-engine:<skill>` em `commands/` e `agents/` resolve para uma skill existente. Nenhuma referência órfã.
- **Refs stale:** zero ocorrências de "LinkedIn Content X.X" / "virall-linkedin-content" em todo o plugin.
- **Scripts:** `validate_specs.py`, `score_post.py`, `suggest_hooks.py` presentes e executáveis.
- **Estrutura final:** `.claude-plugin/` (plugin.json + marketplace.json) · 6 commands · 12 skills · 2 agents · hooks.json · 3 scripts.

## Manual (requer sessão interativa do usuário) — pendente

Estes passos exigem instalar o plugin numa sessão real e rodar os comandos com uma persona real; não são executáveis pelo controller:

1. **Instalar no Claude Code:** `/plugin marketplace add /Users/henriquecaner/Documents/GitHub/authority-engine/linkedin-authority-engine` → `/plugin install linkedin-authority-engine`. Confirmar que os comandos aparecem como `/linkedin-authority-engine:*`.
2. **Fluxo completo numa pasta nova:** `/linkedin-authority-engine:init` (persona fictícia) → confirmar geração de `authority-context.md` (13 seções) + `memory/` + `outputs/posts/`. Depois `/linkedin-authority-engine:guiado <tema>` → confirmar que o post reflete o perfil, passa pelo pipeline (validate → humanizer → brief → score → protocolo), salva em `outputs/posts/` e grava write-back em `memory/`.
3. **Cowork:** instalar e rodar `init` + `guiado`; confirmar que commands/skills funcionam e que a ausência de hook não quebra (a skill `authority-context` cobre o carregamento de contexto).

## Conclusão

O plugin está estruturalmente completo e consistente para v1 (Fundação + Motor de Posts). Os passos manuais acima são a validação de aceitação final em ambiente real, a cargo do usuário.
