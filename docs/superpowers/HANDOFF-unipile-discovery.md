# Handoff — Unipile deep discovery (1.4.0) → agente da main

Fonte: branch `henriquecaner/unipile-integration` (este commit).
Destino: checkout `/Users/henriquecaner/GitHub/authority-engine` (working tree suja).

## Ordem (obrigatória)

`HEAD..main` está vazio: merge desta branch na main é fast-forward. A working tree da main tem um `-gtm/` uncommitted em `.gitignore`. Git recusa o FF com "local changes would be overwritten".

1. **Você** commit/stash do `-gtm/` **antes** de puxar esta branch.
2. Fast-forward. Não resolva `-gtm/` como artefato de merge: o `AGENTS.md` novo ainda lista `gtm/` como gitignored. Des-ignorar commita teardowns de concorrente e pricing — decisão explícita sua, não herdada.
3. Depois do FF, aplique o patch de counts abaixo.

## O que vale

O Unipile desta branch. Plugin `1.4.0` = deep discovery. O draft Composio em `docs/superpowers/specs/2026-07-10-connect-publish-loop-design.md` **não** fica 1.4.0 — recua para 1.5.0 (Wave 6 do spec).

Não reimplemente fetch, HTTP client, paginação, extractors, voice metrics, nem dossier. Importe `linkedin-authority-engine/scripts/unipile_discovery.py`.

## O que aproveitar: receber dados + rodar o report

Contrato estável (stdlib, opener/sleep/rand injetáveis, 85 testes offline):

```python
from unipile_discovery import (
    load_credentials, UnipileClient, fetch_profile_resolved, fetch_posts,
    fetch_company, voice_metrics, extract_engagement, extract_post_text,
    extract_post_date, post_uid, key_inventory, render_dossier, main,
)
```

- **Ingest:** `main([...])` ou as funções acima. CLI: `--linkedin-url` + `--role self|reference` + `--posts N` + `--out DIR` + `--json` + `--dry-run`.
- **Report:** `outputs/discovery/<YYYYMMDD>-<id>-raw.json` (payload cru, re-derive sem nova chamada) e `-dossier.md`.
- **Performance loop (substitui a premissa do Wave 5):** posts próprios trazem `analytics.impressions_counter` (1058/786/210 no corpus live de 2026-09-11), `reactions_counter` (lista somada), `comments_counter`, `reposts_counter`. `extract_engagement(post)` devolve os quatro. **Não precisa scrapar a UI de analytics para impressões de posts próprios.** Saves continuam ausentes no payload — o browser ainda serve só isso (e alcance de perfil, se existir só na UI).
- Write-back: o formato de `memory/topic-performance.md` (schema em `skills/authority-context/references/memory-schemas.md`) aceita `avg reactions / comments / saves`. Impressões cabem como extensão; não invente um segundo collector.

Wave 5 (`performance-collector` via browser) degrada para: Unipile no dono da conta; paste/browser só para saves e o que a API não der.

A premissa do spec linha 11 ("impressões e alcance de perfil pessoal só existem na UI") está **falsificada para impressões de post do dono**. Alcance de perfil e saves: não vistos no payload.

## Quirks live (não re-derivar)

- Posts recusam slug (`400 provider/invalid_parameters`). Sempre use o `id` do perfil (`ACo…`) em `/users/{id}/posts`. `fetch_profile_resolved` já faz isso; self-slug 400 cai em `users/me`.
- Skills vivem em `specifics.skills`, não top-level. Headline/about = `description`/`bio`. Sem experience/company no perfil (self e third-party). Company page aceita slug; rota lenta — timeout 30s + retry costuma bastar; `UNIPILE_TIMEOUT_MS=60000` se falhar.
- Sem `social_id`; `post_uid` deriva `urn:li:activity:<n>` de `share_url`.

## Patch de counts no AGENTS.md / CLAUDE.md (pós-FF)

Os números que o rewrite da main cravou ficam falsos no merge:

| Campo | Era (rewrite main) | Passa a ser |
|---|---|---|
| skills | 22 | 23 (+ `linkedin-deep-discovery`) |
| CLI files | 3 scripts + postlib, ou "4 files" | 4 CLIs + postlib (`unipile_discovery.py`) |
| pytest | 53 | 85 |
| version nos manifests | 1.3.0 | 1.4.0 |
| `voice-profile.md` | read-only em v1 | Gate 1 seeding permitido; Gate 3-M ainda proibido |

Tabela de layout: uma linha para `unipile_discovery.py`; `.env` / `.env.example` (nunca commitar `.env`).

## Não pegar

`/init` Path U, tags `[D]` do discovery-script, seeding de `voice-profile.md`, skill `linkedin-deep-discovery` como workflow de onboarding — isso é plugin, não Composio. Hosted Auth continua no `reach-sales-outreach` (`npm run connect -- linkedin BR`).
