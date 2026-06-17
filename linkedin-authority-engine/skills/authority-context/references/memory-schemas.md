# Schemas de `memory/` — substrato auto-enriquecedor

Arquivos criados na pasta do cliente. Append-only. Lidos na geração (Porta 2), escritos no fim da sessão (Porta 3).

## winning-hooks.md
| padrão de hook | tipo | vezes usado | performance média | keep/kill |
|---|---|---|---|---|

## topic-performance.md
| tema | pilar | nº posts | reações méd | comentários méd | saves méd | vs baseline | veredito |
|---|---|---|---|---|---|---|---|

## voice-profile.md
Bullets datados: `**AAAA-MM-DD:** ajuste de voz → resultado → manter? (sim/não)`

## learnings.md
Entradas livres datadas: `**AAAA-MM-DD:** aprendizado`

> Coluna de performance fica vazia até existir dado (entrada manual futura via `/linkedin perf` ou Unabyss). Em v1, o write-back grava apenas hooks/temas usados e aprovado/rejeitado.
