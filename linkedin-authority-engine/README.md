# LinkedIn Authority Engine

Plugin para **Claude Code** e **Claude Cowork** que transforma a expertise de um founder em autoridade no LinkedIn. Posts tunados pelo algoritmo 360Brew, com perfil de cliente vivo (`authority-context.md`) e memória local que aprende a cada sessão.

Por [LEVEL TECH](https://thelevel.com.br) · [thelevr.com](https://thelevr.com)

## Instalação

```bash
# adiciona o marketplace (caminho local ou repositório)
/plugin marketplace add /caminho/para/linkedin-authority-engine

# instala o plugin
/plugin install linkedin-authority-engine

# cria o perfil do cliente
/linkedin-authority-engine:init
```

Depois do `init`, use `/linkedin-authority-engine:linkedin` para o menu de modos.

## Comandos

| Comando | O que faz |
|---|---|
| `init` | Onboarding. Entrevista de discovery e cria `authority-context.md`, `memory/` e `outputs/posts/`. Aceita `--refresh`. |
| `linkedin` | Menu central. Roteia para o modo escolhido. |
| `guiado` | Cria um post do zero em 7 etapas (categoria → objetivo → pauta → estrutura → tipo → hook → corpo → CTA). |
| `rewrite` | Otimiza um post em duas versões (conservadora e bold), com diagnóstico 360Brew, humanizer e score. |
| `thread` | Série de 3-7 posts sobre um tema, com arquitetura planejada. |
| `score` | Avalia e humaniza um post pronto: validação técnica, humanizer e nota nas 6 dimensões. |

## Como funciona

O plugin lê o perfil de autoridade, gera o post no framework certo, remove padrões de escrita de IA, dá uma nota técnica antes de publicar e entrega o protocolo dos 90 minutos pós-publicação. Cada post bem-sucedido alimenta a memória local, e o próximo nasce mais perto da sua voz.

- **12 skills** — referência do algoritmo 360Brew, banco de 147 hooks, 8 estruturas de copywriting, 16 tipos de conteúdo, templates por categoria, CTAs, estilo e tom, humanizer, protocolo pós-publicação, brief visual, substrato de memória e roteiro de discovery.
- **2 agents** — `linkedin-strategist` (estratégia) e `humanizer-linkedin` (passe final anti-IA).
- **3 scripts** — `score_post.py`, `suggest_hooks.py`, `validate_specs.py`.
- **1 hook** — banner de `SessionStart` apontando para o `init`.

## Estrutura

```
linkedin-authority-engine/
├── .claude-plugin/   # plugin.json + marketplace.json
├── commands/         # 6 comandos
├── skills/           # 12 skills
├── agents/           # 2 agents
├── scripts/          # 3 scripts Python
└── hooks/            # hook de SessionStart
```

O panorama completo do repositório (incluindo a camada de go-to-market) está no [README da raiz](../README.md).

## Licença

Proprietary © LEVEL TECH. Contato: caner@thelevel.com.br
