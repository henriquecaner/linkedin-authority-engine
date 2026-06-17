# Schemas de `memory/` — substrato auto-enriquecedor

Arquivos criados na pasta do cliente. Append-only. Lidos na geração (Porta 2), escritos no fim da sessão (Porta 3).

## winning-hooks.md
| data | padrão de hook | tipo | categoria | objetivo | score | vezes usado | performance média | keep/kill |
|---|---|---|---|---|---|---|---|---|

**v1 preenche:** data, padrão de hook, tipo, categoria, objetivo, score. As colunas `vezes usado`, `performance média` e `keep/kill` ficam vazias até v1.x (perf manual via `/linkedin perf` ou Unabyss).

## topic-performance.md
| data | tema | pilar | tipo de post | score | reações méd | comentários méd | saves méd | vs baseline | veredito |
|---|---|---|---|---|---|---|---|---|---|

**v1 preenche:** data, tema, pilar, tipo de post, score. As colunas `reações méd`, `comentários méd`, `saves méd`, `vs baseline` e `veredito` ficam vazias até v1.x.

## voice-profile.md
Bullets datados: `**AAAA-MM-DD:** ajuste de voz → resultado → manter? (sim/não)`

**v1: READ-ONLY.** Este arquivo é lido na geração (Porta 2) para calibrar a voz. Escrita de ajustes de voz entra em v1.x. A ausência de write-back em v1 é intencional, não um bug.

## learnings.md
Entradas livres datadas: `**AAAA-MM-DD:** aprendizado`

v1 grava entradas livres a cada sessão (o que funcionou, ajustes, rejeições).

> Schema de referência: este arquivo é a fonte da verdade (schema of record) para os contratos de Porta 3 nos 4 comandos do plugin. Qualquer divergência entre este arquivo e os comandos deve ser resolvida aqui.
