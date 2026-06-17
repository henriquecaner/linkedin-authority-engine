# LinkedIn Authority Engine — Plugin v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a skill `virall-linkedin-content` num plugin instalável (`linkedin-authority-engine`) para Claude Code e Claude Cowork, com onboarding self-bootstrap (`/linkedin init` Caminho A), substrato de memória local-first auto-enriquecedor e motor de posts portado e aprofundado.

**Architecture:** Plugin no padrão marketplace do hormozi-gtm (`.claude-plugin/{plugin.json,marketplace.json}` + `commands/` + `skills/` + `agents/` + `hooks/` + `scripts/`). Conhecimento vive em skills granulares (portáveis Code+Cowork); commands são entry points; hooks são conveniência do Code (lógica essencial nunca depende só de hook). A pasta do cliente guarda `authority-context.md` + `memory/` + `outputs/` — o substrato de 3 portas (escrita no onboarding, leitura na geração, write-back no fim da sessão).

**Tech Stack:** Markdown (skills/commands/agents), JSON (plugin/marketplace/hooks config), Python 3 (3 scripts portados: validate_specs, score_post, suggest_hooks), pytest (testes estruturais + smoke de CLI).

## Global Constraints

- **Plugin root:** `/Users/henriquecaner/Documents/GitHub/authority-engine/linkedin-authority-engine` (referido abaixo como `<PLUGIN>`).
- **Fonte de port:** `/Users/henriquecaner/Documents/GitHub/authority-engine/Skill-old/_extracted/virall-linkedin-content` (referido como `<SRC>`). Já extraído; se faltar, rodar `unzip -o Skill-old/virall-linkedin-content.skill -d Skill-old/_extracted`.
- **Template do perfil:** `/Users/henriquecaner/Documents/GitHub/authority-engine/Skill-old/Instrucoes_Projeto_Template_v2.md`.
- **Testes:** `/Users/henriquecaner/Documents/GitHub/authority-engine/tests/` (fora do `<PLUGIN>` para não embarcar no pacote).
- **Test runner:** o ambiente tem Python externally-managed (PEP 668); pytest vive num venv de dev já criado em `.venv/`. **Todos os comandos de teste usam `.venv/bin/python -m pytest …`** (não `python3 -m pytest`). O `.venv/` não é versionado.
- **Nome do plugin:** `linkedin-authority-engine`. Comandos namespaceados: `/linkedin-authority-engine:<cmd>` (o `<cmd>` curto é o nome do arquivo).
- **Idioma de todo conteúdo voltado ao usuário:** PT-BR com acentuação correta.
- **Substituição de port obrigatória:** toda referência a "skill LinkedIn Content 3.1" / "virall-linkedin-content" / "LinkedIn Content X.X" no conteúdo portado vira "este plugin (`linkedin-authority-engine`)".
- **Git:** repo NÃO está sob git. Task 1 roda `git init` antes do primeiro commit.
- **Portabilidade:** nenhum command pode depender de um agent rodar (no Cowork pode não rodar) — sempre carregar a skill equivalente via ferramenta Skill como fallback, padrão do hormozi-gtm.
- **Fora de escopo v1:** lead magnets, cadência/calendário, automação de comentários, `/linkedin perf`, Caminho B (transcrição/HeyGen). Não criar arquivos para esses.

---

### Task 1: Esqueleto do plugin + marketplace + git

**Files:**
- Create: `<PLUGIN>/.claude-plugin/plugin.json`
- Create: `<PLUGIN>/.claude-plugin/marketplace.json`
- Create: `<PLUGIN>/README.md`
- Create: `tests/test_plugin_structure.py`
- Create: `tests/conftest.py`

**Interfaces:**
- Produces: `PLUGIN_DIR` fixture (pytest) = caminho absoluto do `<PLUGIN>`, consumido por todas as tasks de teste seguintes.
- Produces: `plugin.json` com `name: "linkedin-authority-engine"`, `version: "1.0.0"`.

- [ ] **Step 1: Escrever o teste estrutural que falha**

Create `tests/conftest.py`:
```python
import pathlib
import pytest

@pytest.fixture
def plugin_dir():
    return pathlib.Path(__file__).resolve().parent.parent / "linkedin-authority-engine"
```

Create `tests/test_plugin_structure.py`:
```python
import json

def test_plugin_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "plugin.json"
    assert p.exists(), "plugin.json ausente"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    assert data["version"] == "1.0.0"
    for key in ("displayName", "description", "author", "license"):
        assert key in data, f"plugin.json sem chave {key}"

def test_marketplace_json_valid(plugin_dir):
    p = plugin_dir / ".claude-plugin" / "marketplace.json"
    assert p.exists(), "marketplace.json ausente"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["name"] == "linkedin-authority-engine"
    names = [pl["name"] for pl in data["plugins"]]
    assert "linkedin-authority-engine" in names
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `cd /Users/henriquecaner/Documents/GitHub/authority-engine && python3 -m pytest tests/test_plugin_structure.py -v`
Expected: FAIL (`plugin.json ausente`).

- [ ] **Step 3: Criar `plugin.json`**

Create `<PLUGIN>/.claude-plugin/plugin.json`:
```json
{
  "name": "linkedin-authority-engine",
  "displayName": "LinkedIn Authority Engine",
  "version": "1.0.0",
  "description": "Sistema que transforma a expertise do founder em autoridade no LinkedIn. Posts tunados pelo algoritmo 360Brew, com perfil de cliente vivo (authority-context.md) e auto-enriquecimento por memória local. Para Claude Code e Claude Cowork.",
  "author": { "name": "LEVEL TECH", "email": "caner@thelevel.com.br" },
  "homepage": "https://thelevr.com",
  "license": "proprietary",
  "keywords": ["linkedin", "authority", "content", "360brew", "b2b", "level"]
}
```

- [ ] **Step 4: Criar `marketplace.json`**

Create `<PLUGIN>/.claude-plugin/marketplace.json`:
```json
{
  "name": "linkedin-authority-engine",
  "owner": { "name": "LEVEL TECH", "email": "caner@thelevel.com.br" },
  "metadata": {
    "description": "Marketplace do LinkedIn Authority Engine — plugin de criação de conteúdo de autoridade no LinkedIn.",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "linkedin-authority-engine",
      "source": "./",
      "description": "Posts de LinkedIn tunados pelo algoritmo 360Brew, com perfil de cliente vivo e memória auto-enriquecedora.",
      "version": "1.0.0",
      "category": "marketing",
      "tags": ["linkedin", "authority", "content", "360brew", "b2b"]
    }
  ]
}
```

- [ ] **Step 5: Criar README mínimo**

Create `<PLUGIN>/README.md`:
```markdown
# LinkedIn Authority Engine

Plugin Claude Code / Claude Cowork para transformar a expertise do founder em autoridade no LinkedIn.

## Instalação
1. `/plugin marketplace add /caminho/para/linkedin-authority-engine`
2. `/plugin install linkedin-authority-engine`
3. Rode `/linkedin-authority-engine:init` para criar o perfil do cliente.

## Comandos
- `init` — onboarding (cria `authority-context.md`)
- `linkedin` — menu de modos
- `guiado` / `rewrite` / `thread` / `score` — criação e avaliação de posts
```

- [ ] **Step 6: Rodar os testes e confirmar que passam**

Run: `cd /Users/henriquecaner/Documents/GitHub/authority-engine && python3 -m pytest tests/test_plugin_structure.py -v`
Expected: PASS (2 passed).

- [ ] **Step 7: Verificar instalação no Claude Code (manual)**

Run: `claude` numa sessão nova e digitar `/plugin marketplace add /Users/henriquecaner/Documents/GitHub/authority-engine/linkedin-authority-engine`, depois `/plugin install linkedin-authority-engine`.
Expected: plugin aparece instalado, sem erro de manifesto.

- [ ] **Step 8: Init git + commit**

```bash
cd /Users/henriquecaner/Documents/GitHub/authority-engine
git init
printf ".venv/\ntests/__pycache__/\n.pytest_cache/\n*.pyc\n__pycache__/\n" > .gitignore
git add .gitignore linkedin-authority-engine/ tests/ docs/
git commit -m "feat(plugin): esqueleto linkedin-authority-engine + marketplace + testes estruturais"
```

---

### Task 2: Port dos 3 scripts Python + smoke tests de CLI

**Files:**
- Create: `<PLUGIN>/scripts/validate_specs.py` (cópia de `<SRC>/scripts/validate_specs.py`)
- Create: `<PLUGIN>/scripts/score_post.py` (cópia de `<SRC>/scripts/score_post.py`)
- Create: `<PLUGIN>/scripts/suggest_hooks.py` (cópia de `<SRC>/scripts/suggest_hooks.py`)
- Create: `tests/fixtures/post_exemplo.txt`
- Create: `tests/test_scripts_cli.py`

**Interfaces:**
- Consumes: `plugin_dir` fixture (Task 1).
- Produces: 3 scripts CLI estáveis com as assinaturas documentadas no SKILL original:
  - `validate_specs.py <arquivo>` → imprime relatório; exit 0.
  - `score_post.py <arquivo> --objetivo authority` → imprime score; aceita `--json` e `--compact`.
  - `suggest_hooks.py --categoria <c> --objetivo <o> --tema "<t>"` → imprime hooks; aceita `--seed`.

- [ ] **Step 1: Copiar os scripts**

```bash
cd /Users/henriquecaner/Documents/GitHub/authority-engine
mkdir -p linkedin-authority-engine/scripts
cp Skill-old/_extracted/virall-linkedin-content/scripts/validate_specs.py linkedin-authority-engine/scripts/
cp Skill-old/_extracted/virall-linkedin-content/scripts/score_post.py linkedin-authority-engine/scripts/
cp Skill-old/_extracted/virall-linkedin-content/scripts/suggest_hooks.py linkedin-authority-engine/scripts/
```

- [ ] **Step 2: Criar fixture de post**

Create `tests/fixtures/post_exemplo.txt`:
```
Demiti meu melhor vendedor ontem.

Ele batia meta todo mês. O time gostava dele.

Mas tinha um problema: ele mentia pros clientes pra fechar.

Descobri quando um cliente ligou furioso.

A venda fácil de hoje vira o churn caro de amanhã.

Integridade não é negociável, mesmo quando custa receita.

Salva esse post se você lidera um time comercial.
```

- [ ] **Step 3: Escrever smoke tests de CLI que falham**

Create `tests/test_scripts_cli.py`:
```python
import subprocess, sys, pathlib

FIX = pathlib.Path(__file__).resolve().parent / "fixtures" / "post_exemplo.txt"

def _run(plugin_dir, *args):
    script = plugin_dir / "scripts" / args[0]
    return subprocess.run(
        [sys.executable, str(script), *args[1:]],
        capture_output=True, text=True
    )

def test_validate_specs_runs(plugin_dir):
    r = _run(plugin_dir, "validate_specs.py", str(FIX))
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""

def test_score_post_runs(plugin_dir):
    r = _run(plugin_dir, "score_post.py", str(FIX), "--objetivo", "authority")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""

def test_suggest_hooks_runs(plugin_dir):
    r = _run(plugin_dir, "suggest_hooks.py", "--categoria", "conquista",
             "--objetivo", "authority", "--tema", "vendas B2B")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
```

- [ ] **Step 4: Rodar e confirmar que passam** (os scripts já existem e funcionam)

Run: `cd /Users/henriquecaner/Documents/GitHub/authority-engine && python3 -m pytest tests/test_scripts_cli.py -v`
Expected: PASS (3 passed). Se algum falhar por flag ausente, ler o `argparse` do script e ajustar o teste para a flag real (não alterar o script — ele é o asset validado).

- [ ] **Step 5: Commit**

```bash
git add linkedin-authority-engine/scripts/ tests/
git commit -m "feat(scripts): port validate_specs/score_post/suggest_hooks + smoke tests CLI"
```

---

### Task 3: Port das skills de conhecimento (360Brew + conteúdo + pipeline)

**Files (criar 1 `SKILL.md` por skill, conteúdo portado de `<SRC>/references/`):**
- Create: `<PLUGIN>/skills/algoritmo-360brew/SKILL.md` ← merge de `algoritmo-core.md` + `algoritmo-formatos.md` + `algoritmo-metricas.md`
- Create: `<PLUGIN>/skills/hooks/SKILL.md` ← `hooks.md`
- Create: `<PLUGIN>/skills/estruturas-copywriting/SKILL.md` ← `estruturas-copywriting.md`
- Create: `<PLUGIN>/skills/tipos-conteudo/SKILL.md` ← `tipos-conteudo.md`
- Create: `<PLUGIN>/skills/templates-por-categoria/SKILL.md` ← `templates-por-categoria.md`
- Create: `<PLUGIN>/skills/ctas/SKILL.md` ← `ctas.md`
- Create: `<PLUGIN>/skills/estilo-tom/SKILL.md` ← `estilo-tom.md`
- Create: `<PLUGIN>/skills/protocolo-pos-publicacao/SKILL.md` ← `protocolo-pos-publicacao.md`
- Create: `<PLUGIN>/skills/brief-visual/SKILL.md` ← `brief-visual.md`
- Create: `<PLUGIN>/skills/humanizer-linkedin/SKILL.md` ← `humanizer-pipeline.md` + regras de humanizer aplicáveis a LinkedIn
- Modify: `tests/test_plugin_structure.py` (adicionar validação de skills)

**Interfaces:**
- Consumes: `plugin_dir` fixture.
- Produces: 10 skills com frontmatter `description:` válido; nomes de diretório = nomes de skill canônicos consumidos pelos commands das Tasks 6-7.

- [ ] **Step 1: Escrever o teste de skills que falha**

Add to `tests/test_plugin_structure.py`:
```python
EXPECTED_SKILLS = [
    "algoritmo-360brew", "hooks", "estruturas-copywriting", "tipos-conteudo",
    "templates-por-categoria", "ctas", "estilo-tom", "protocolo-pos-publicacao",
    "brief-visual", "humanizer-linkedin",
]

def test_knowledge_skills_present_and_valid(plugin_dir):
    for name in EXPECTED_SKILLS:
        sk = plugin_dir / "skills" / name / "SKILL.md"
        assert sk.exists(), f"skill ausente: {name}"
        text = sk.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{name}: sem frontmatter"
        assert "description:" in text.split("---")[1], f"{name}: frontmatter sem description"
        body = text.split("---", 2)[2].strip()
        assert len(body) > 200, f"{name}: corpo muito curto (port incompleto?)"

def test_no_stale_skill_references(plugin_dir):
    import re
    pat = re.compile(r"LinkedIn Content \d|virall-linkedin-content", re.I)
    for sk in (plugin_dir / "skills").rglob("SKILL.md"):
        assert not pat.search(sk.read_text(encoding="utf-8")), f"referência stale em {sk}"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_knowledge_skills_present_and_valid -v`
Expected: FAIL (`skill ausente: algoritmo-360brew`).

- [ ] **Step 3: Portar cada skill**

Para cada arquivo da tabela acima:
1. Ler o `.md` de origem em `<SRC>/references/`.
2. Criar `<PLUGIN>/skills/<nome>/SKILL.md` com frontmatter:
```markdown
---
description: <1-2 frases dizendo quando usar a skill. Ex. para hooks: "Banco de 147 hooks de LinkedIn por tipo (prova de trabalho, autoridade, transformação, tensão, confissão). Use ao gerar headlines de post, primeiras linhas e variações de gancho.">
---

<conteúdo portado do arquivo de origem>
```
3. Aplicar a substituição obrigatória ("LinkedIn Content 3.1" → "este plugin").
4. Para `algoritmo-360brew`: concatenar os 3 arquivos `algoritmo-*.md` sob seções `## Core`, `## Formatos`, `## Métricas`.

- [ ] **Step 4: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: PASS (todos).

- [ ] **Step 5: Commit**

```bash
git add linkedin-authority-engine/skills/ tests/
git commit -m "feat(skills): port conhecimento 360Brew + conteúdo + pipeline (10 skills)"
```

---

### Task 4: Substrato — meta-skill `authority-context` + template + schemas de memória

**Files:**
- Create: `<PLUGIN>/skills/authority-context/SKILL.md`
- Create: `<PLUGIN>/skills/authority-context/references/authority-context-template.md` (port de `Instrucoes_Projeto_Template_v2.md`)
- Create: `<PLUGIN>/skills/authority-context/references/memory-schemas.md`
- Modify: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: `plugin_dir`.
- Produces: skill `authority-context` que documenta o protocolo das 3 portas; template canônico do `authority-context.md` (13 seções); schemas dos 4 arquivos de `memory/`. Consumido por `init` (Task 6) e pelos modos (Task 7).

- [ ] **Step 1: Escrever o teste que falha**

Add to `tests/test_plugin_structure.py`:
```python
def test_authority_context_assets(plugin_dir):
    base = plugin_dir / "skills" / "authority-context"
    assert (base / "SKILL.md").exists()
    tpl = (base / "references" / "authority-context-template.md").read_text(encoding="utf-8")
    # 13 seções numeradas do template
    for n in range(1, 14):
        assert f"# {n}." in tpl, f"template sem seção {n}"
    mem = (base / "references" / "memory-schemas.md").read_text(encoding="utf-8")
    for f in ("winning-hooks.md", "topic-performance.md", "voice-profile.md", "learnings.md"):
        assert f in mem, f"memory-schemas sem {f}"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_authority_context_assets -v`
Expected: FAIL.

- [ ] **Step 3: Portar o template**

Copiar `Instrucoes_Projeto_Template_v2.md` → `<PLUGIN>/skills/authority-context/references/authority-context-template.md`. Editar o cabeçalho e a seção 11: trocar toda menção a "Skill LinkedIn Content 3.1" por "este plugin (`linkedin-authority-engine`)". Manter as 13 seções e os marcadores `*` de campo crítico intactos.

- [ ] **Step 4: Criar `memory-schemas.md`**

Create `<PLUGIN>/skills/authority-context/references/memory-schemas.md`:
```markdown
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
```

- [ ] **Step 5: Criar a meta-skill**

Create `<PLUGIN>/skills/authority-context/SKILL.md`:
```markdown
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
```

- [ ] **Step 6: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add linkedin-authority-engine/skills/authority-context/ tests/
git commit -m "feat(substrato): meta-skill authority-context + template 13 seções + schemas de memory"
```

---

### Task 5: Skill `discovery-script` (perguntas da entrevista — Caminho A)

**Files:**
- Create: `<PLUGIN>/skills/discovery-script/SKILL.md`
- Modify: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: `plugin_dir`; template de `authority-context` (Task 4) como referência do mapa de campos.
- Produces: skill `discovery-script` com um bloco de perguntas por cada uma das 13 seções, cobrindo todos os campos críticos `*`. Consumido por `init` (Task 6).

- [ ] **Step 1: Escrever o teste que falha**

Add to `tests/test_plugin_structure.py`:
```python
def test_discovery_script_covers_sections(plugin_dir):
    sk = (plugin_dir / "skills" / "discovery-script" / "SKILL.md").read_text(encoding="utf-8")
    # uma âncora de bloco por seção do perfil
    for label in ["Perfil", "Posicionamento", "Objetivos", "Audiência", "Ofertas",
                  "Narrativa comercial", "Paisagem competitiva", "Territórios",
                  "Restrições", "Tom de voz", "Instrução de conteúdo"]:
        assert label in sk, f"discovery-script sem bloco: {label}"
    assert sk.lower().count("?") >= 25, "discovery-script com poucas perguntas"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_discovery_script_covers_sections -v`
Expected: FAIL.

- [ ] **Step 3: Criar a skill**

Create `<PLUGIN>/skills/discovery-script/SKILL.md` — reconstruir as perguntas a partir do mapa de Q do template (cada campo do template indica a Q de origem). Estrutura: frontmatter `description` + um `## <Seção>` por bloco, com perguntas em lista. Marcar `*` nas que alimentam campo crítico. Exemplo de blocos (cobrir todos os 11 blocos do teste + visual/notas opcionais):
```markdown
---
description: Roteiro de entrevista de discovery para montar o perfil do cliente (authority-context.md) no Caminho A (entrevista guiada in-session). Use dentro do command init. Perguntas agrupadas pelas 13 seções do perfil; * = alimenta campo crítico.
---

# Discovery Script — entrevista guiada

Conduzir uma pergunta por vez (ou blocos curtos). Não avançar de seção sem cobrir os campos `*`.

## Perfil do cliente
- Qual seu nome completo, cargo e empresa? *
- Há quanto tempo na posição e quantos anos de experiência na área?
- Em 30 segundos, como você se apresentaria? (vira a bio) *
- Quais marcadores de credibilidade você tem? (resultados, marcas, números) *

## Posicionamento e autoridade
- Em qual grande tema você quer ser referência? *
- Se separássemos em 3 pilares de conteúdo, quais seriam? *
- De onde você pega o cliente e para onde leva? (proposta de valor) *
- Quais histórias/cases reais você tem pra contar?
- Que crenças do seu mercado você discorda?
- Se desse UMA palestra, qual o tema?

## Objetivos
- O foco é Authority, Sales ou Engagement? *
- O que tornaria isso um sucesso em 90 dias? *

## Audiência
- Quem você quer alcançar? (cargo, setor, porte, geografia) *
- Quais as 3 maiores dores dessa audiência? *
- Qual o antes→depois que ela busca? *

## Ofertas
- Quais suas ofertas (formato e ticket)? Qual priorizar agora?

## Narrativa comercial
- Como você convence hoje? Quais as objeções mais frequentes? *

## Paisagem competitiva
- Quais 3 concorrentes diretos? Que executivos você admira no posicionamento? *

## Territórios
- Temas que você adora falar? Temas que NÃO quer tocar? Suas fontes de informação? *

## Restrições
- Palavras/expressões a NÃO usar? Algo confidencial ou sensível? *

## Tom de voz
- Seu estilo em 3 palavras? Qual benchmark de tom? Nível de vulnerabilidade (1-5)? *

## Instrução de conteúdo
- Mix desejado (autoridade % / prova de trabalho % / pessoal %)? *
- Frequência e formato preferido de post?

## Identidade visual (opcional)
- Fontes, paleta, estilo de carrossel?

## Notas
- Algo que ajude a criar conteúdo que não perguntei? Palavras-chave da marca? *
```

- [ ] **Step 4: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add linkedin-authority-engine/skills/discovery-script/ tests/
git commit -m "feat(onboarding): skill discovery-script (entrevista guiada Caminho A)"
```

---

### Task 6: Command `/linkedin init` (Caminho A)

**Files:**
- Create: `<PLUGIN>/commands/init.md`
- Modify: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: skills `discovery-script` e `authority-context` (Tasks 4-5).
- Produces: comando `init` que gera `authority-context.md` + inicializa `memory/` + `outputs/posts/` na pasta do cliente. Consumido pelo fluxo do usuário e referenciado pelo hook (Task 9).

- [ ] **Step 1: Escrever o teste de commands que falha**

Add to `tests/test_plugin_structure.py`:
```python
def test_command_frontmatter(plugin_dir):
    import os
    cmds = ["init"]  # ampliado na Task 7
    for c in cmds:
        p = plugin_dir / "commands" / f"{c}.md"
        assert p.exists(), f"command ausente: {c}"
        text = p.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{c}: sem frontmatter"
        assert "description:" in text.split("---")[1], f"{c}: sem description"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_command_frontmatter -v`
Expected: FAIL (`command ausente: init`).

- [ ] **Step 3: Criar o command**

Create `<PLUGIN>/commands/init.md`:
```markdown
---
description: Onboarding do cliente. Conduz a entrevista de discovery (Caminho A) e cria authority-context.md na pasta do projeto, mais memory/ e outputs/posts/. Auto-sugerido quando outros comandos rodam sem perfil. Suporta --refresh para atualizar perfil existente.
argument-hint: "[--refresh]"
---

# /linkedin-authority-engine:init

Cria o perfil vivo do cliente — substitui a montagem manual de "projeto Claude + instruções".

## Passos

1. **Checar contexto existente.** Se `authority-context.md` já existe na raiz: sem `--refresh`, perguntar se quer revisar/atualizar; com `--refresh`, atualizar campos defasados preservando o resto.
2. **Carregar o roteiro.** Use a ferramenta Skill para carregar `linkedin-authority-engine:discovery-script`. (Caminho A — entrevista guiada in-session. Caminho B/transcrição é futuro.)
3. **Conduzir a entrevista.** Uma pergunta por vez ou blocos curtos. Não fechar uma seção sem cobrir os campos críticos (`*`).
4. **Sintetizar o perfil.** Use a ferramenta Skill para carregar `linkedin-authority-engine:authority-context` e preencher o `references/authority-context-template.md` com as respostas. Marcar lacunas em campos `*` e pedir follow-up só do que faltou.
5. **Escrever os arquivos** na raiz do projeto:
   - `authority-context.md` (perfil preenchido, com frontmatter `last_updated`, `version`)
   - `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` (cabeçalhos vazios conforme schemas)
   - `outputs/posts/.gitkeep`
6. **Confirmar** mostrando um resumo (tema central, 3 pilares, objetivo, mix) e instruir: "rode `/linkedin-authority-engine:guiado` para o primeiro post."

## Voz
Setup/interação: PT-BR direto, sem voz de assistente robótica. Sem humanizer aqui (não é copy externa).
```

- [ ] **Step 4: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 5: Verificação manual (Caminho A end-to-end)**

Numa pasta de teste `/tmp/cliente-x`, rodar `/linkedin-authority-engine:init`, responder as perguntas com uma persona fictícia.
Expected: gera `authority-context.md` com as 13 seções preenchidas + `memory/` + `outputs/posts/`.

- [ ] **Step 6: Commit**

```bash
git add linkedin-authority-engine/commands/init.md tests/
git commit -m "feat(command): /linkedin init (onboarding Caminho A)"
```

---

### Task 7: Commands do Motor de Posts (menu + 4 modos)

**Files:**
- Create: `<PLUGIN>/commands/linkedin.md` (menu router)
- Create: `<PLUGIN>/commands/guiado.md`
- Create: `<PLUGIN>/commands/rewrite.md`
- Create: `<PLUGIN>/commands/thread.md`
- Create: `<PLUGIN>/commands/score.md`
- Modify: `tests/test_plugin_structure.py` (ampliar lista `cmds`)

**Interfaces:**
- Consumes: skills de conhecimento (Task 3), `authority-context` (Task 4), scripts (Task 2).
- Produces: 5 comandos. Cada modo lê o substrato (Porta 2) no início e grava write-back (Porta 3) ao fim, e roda o Pipeline de Finalização (validate → humanizer → brief → score → protocolo).

- [ ] **Step 1: Ampliar o teste de commands (falha)**

Edit em `tests/test_plugin_structure.py` a função `test_command_frontmatter`:
```python
    cmds = ["init", "linkedin", "guiado", "rewrite", "thread", "score"]
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_command_frontmatter -v`
Expected: FAIL (`command ausente: linkedin`).

- [ ] **Step 3: Criar `linkedin.md` (menu)**

Create `<PLUGIN>/commands/linkedin.md`:
```markdown
---
description: Menu de modos do LinkedIn Authority Engine. Exibe Guiado, Rewrite, Thread e Score e roteia para o modo escolhido. Use quando o usuário não sabe por onde começar.
argument-hint: "[guiado|rewrite|thread|score]"
---

# /linkedin-authority-engine:linkedin

Se vier argumento, rotear direto para o modo. Sem argumento, exibir:
```
🎯 LinkedIn Authority Engine — O que vamos criar?
1 Guiado   — post do zero (workflow completo)
2 Rewrite  — otimizar post existente
3 Thread   — série de posts
4 Score    — avaliar + humanizar post pronto
```
Antes de qualquer modo: se não houver `authority-context.md`, sugerir `/linkedin-authority-engine:init`.
```

- [ ] **Step 4: Criar `guiado.md`, `rewrite.md`, `thread.md`, `score.md`**

Portar os 4 modos do `<SRC>/SKILL.md` (seções MODO GUIADO, MODO REWRITE, MODO THREAD, MODO SCORE) e o Pipeline de Finalização. Cada arquivo:
1. Frontmatter `description` + `argument-hint`.
2. **Início (Porta 2):** "Carregue a skill `linkedin-authority-engine:authority-context` e leia `authority-context.md` + `memory/`. Aplicar tom, pilares, credenciais, restrições e priorizar padrões vencedores."
3. Corpo do modo (steps portados, com as tabelas de framework/CTA/specs referenciando as skills da Task 3 via ferramenta Skill).
4. **Pipeline de Finalização:** validate_specs.py → skill `humanizer-linkedin` → skill `brief-visual` → score_post.py → skill `protocolo-pos-publicacao`.
5. **Fim (Porta 3):** "Anexar a `memory/` os hooks/temas usados e o que foi aprovado/rejeitado, conforme a skill `authority-context`."
6. **Salvar** o post final em `outputs/posts/<AAAAMMDD>-<slug>-vN.md`.

Aplicar a substituição obrigatória de referências stale em todo o conteúdo portado.

- [ ] **Step 5: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/ -v`
Expected: PASS (todos).

- [ ] **Step 6: Verificação manual (geração contextual)**

Na pasta `/tmp/cliente-x` (com perfil da Task 6), rodar `/linkedin-authority-engine:guiado vendas B2B`.
Expected: post gerado usa credenciais/pilares do perfil; passa pelo pipeline; salva em `outputs/posts/`; anexa entrada em `memory/`.

- [ ] **Step 7: Commit**

```bash
git add linkedin-authority-engine/commands/ tests/
git commit -m "feat(posts): menu + modos guiado/rewrite/thread/score com leitura/write-back do substrato"
```

---

### Task 8: Agents — `linkedin-strategist` + `humanizer-linkedin`

**Files:**
- Create: `<PLUGIN>/agents/linkedin-strategist.md`
- Create: `<PLUGIN>/agents/humanizer-linkedin.md`
- Modify: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: skills de conhecimento + `authority-context`.
- Produces: 2 agents com frontmatter `name`/`description`. Opcionais à execução (commands funcionam sem eles via skills) — padrão de portabilidade Cowork.

- [ ] **Step 1: Escrever o teste que falha**

Add to `tests/test_plugin_structure.py`:
```python
def test_agents_frontmatter(plugin_dir):
    for a in ["linkedin-strategist", "humanizer-linkedin"]:
        p = plugin_dir / "agents" / f"{a}.md"
        assert p.exists(), f"agent ausente: {a}"
        fm = p.read_text(encoding="utf-8").split("---")[1]
        assert "name:" in fm and "description:" in fm, f"{a}: frontmatter incompleto"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_agents_frontmatter -v`
Expected: FAIL.

- [ ] **Step 3: Criar `linkedin-strategist.md`**

Create `<PLUGIN>/agents/linkedin-strategist.md`:
```markdown
---
name: linkedin-strategist
description: Estrategista de conteúdo LinkedIn com domínio do algoritmo 360Brew. Lê o authority-context.md do cliente e gera/critica posts alinhados a tema central, pilares, voz e padrões vencedores. Use para geração pesada nos modos guiado/thread.
model: opus
effort: high
---

# LinkedIn Strategist

Você domina o algoritmo 360Brew (2026) e escreve posts de autoridade B2B. Antes de gerar: leia `authority-context.md` + `memory/`. Aplique specs de texto, pesos de engajamento (save 5x, comentário longo 2x), zero link no corpo, zero hashtag genérica. Priorize Saves Potential. Sempre respeite restrições e territórios NÃO do perfil. Carregue as skills `algoritmo-360brew`, `hooks`, `estruturas-copywriting` via ferramenta Skill quando precisar.
```

- [ ] **Step 4: Criar `humanizer-linkedin.md`**

Create `<PLUGIN>/agents/humanizer-linkedin.md`:
```markdown
---
name: humanizer-linkedin
description: Remove padrões de escrita IA (em-dash overuse, rule of three, vocabulário IA, promotional language, vague attributions) de posts de LinkedIn em PT-BR, preservando voz e specs 360Brew. Use no Pipeline de Finalização antes do score.
model: opus
effort: medium
---

# Humanizer LinkedIn

Carregue a skill `linkedin-authority-engine:humanizer-linkedin` e aplique as regras ao post. Saída: post refinado + diff compacto (máx 5 itens). Não quebrar specs (parágrafos curtos, sem link no corpo).
```

- [ ] **Step 5: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/ -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add linkedin-authority-engine/agents/ tests/
git commit -m "feat(agents): linkedin-strategist + humanizer-linkedin"
```

---

### Task 9: Hook `SessionStart`

**Files:**
- Create: `<PLUGIN>/hooks/hooks.json`
- Modify: `tests/test_plugin_structure.py`

**Interfaces:**
- Consumes: nada (config standalone).
- Produces: banner de boas-vindas que aponta para `init`. Conveniência do Code; no Cowork o carregamento de contexto é coberto pela skill `authority-context`.

- [ ] **Step 1: Escrever o teste que falha**

Add to `tests/test_plugin_structure.py`:
```python
def test_hooks_json_valid(plugin_dir):
    import json
    p = plugin_dir / "hooks" / "hooks.json"
    assert p.exists(), "hooks.json ausente"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "SessionStart" in data["hooks"]
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tests/test_plugin_structure.py::test_hooks_json_valid -v`
Expected: FAIL.

- [ ] **Step 3: Criar `hooks.json`**

Create `<PLUGIN>/hooks/hooks.json`:
```json
{
  "description": "linkedin-authority-engine: banner de SessionStart apontando para o onboarding.",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'LinkedIn Authority Engine ativo. Se ainda não há authority-context.md neste projeto, rode /linkedin-authority-engine:init. Depois use /linkedin-authority-engine:linkedin para criar posts.'"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 4: Rodar e confirmar que passam**

Run: `python3 -m pytest tests/ -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add linkedin-authority-engine/hooks/ tests/
git commit -m "feat(hook): banner SessionStart apontando para init"
```

---

### Task 10: Verificação end-to-end (Code + Cowork) + tag v1.0.0

**Files:**
- Create: `docs/superpowers/plans/verificacao-v1.md` (registro do teste manual)

**Interfaces:**
- Consumes: tudo.
- Produces: confirmação de que o produto vendável funciona nos dois ambientes.

- [ ] **Step 1: Reinstalar do zero no Claude Code**

Remover e reinstalar: `/plugin marketplace remove linkedin-authority-engine` então `/plugin marketplace add <PLUGIN>` + `/plugin install linkedin-authority-engine`.
Expected: instala limpo, comandos aparecem com `/linkedin-authority-engine:`.

- [ ] **Step 2: Fluxo completo numa pasta nova**

Em `/tmp/cliente-e2e`: `init` (persona fictícia) → `guiado` → verificar que o post reflete o perfil, passou pelo pipeline, salvou em `outputs/posts/` e gravou em `memory/`.
Expected: todos os artefatos presentes e coerentes.

- [ ] **Step 3: Verificar no Claude Cowork**

Instalar o plugin no Cowork. Rodar `init` e `guiado`.
Expected: commands e skills funcionam; ausência de hook não quebra (skill `authority-context` cobre o carregamento de contexto).

- [ ] **Step 4: Rodar a suíte completa**

Run: `cd /Users/henriquecaner/Documents/GitHub/authority-engine && python3 -m pytest tests/ -v`
Expected: PASS (todos).

- [ ] **Step 5: Registrar resultado + tag**

Escrever `docs/superpowers/plans/verificacao-v1.md` com o que foi testado e qualquer ressalva. Depois:
```bash
git add docs/ && git commit -m "docs: registro de verificação v1 (Code + Cowork)"
git tag v1.0.0
```

---

## Self-Review (preenchido)

**Cobertura do spec:**
- Esqueleto/plugin.json/marketplace → Task 1 ✓
- Substrato 3 portas + contratos → Task 4 (schemas) + Tasks 6/7 (escrita/leitura/write-back) ✓
- `authority-context.md` schema (13 seções) → Task 4 ✓
- `/linkedin init` Caminho A + discovery-script → Tasks 5-6 ✓
- Motor de Posts (commands + skills + agents + scripts + pipeline) → Tasks 2,3,7,8 ✓
- Hook SessionStart + cobertura Cowork por skill → Task 9 + Task 10 step 3 ✓
- Portabilidade Code/Cowork → Global Constraints + Tasks 7/8 (skill como fallback) + Task 10 ✓
- Deferidos (perf, lead magnets, comentários, Caminho B/HeyGen) → explicitamente fora de escopo ✓

**Placeholder scan:** ports especificam arquivo-origem + transformação exata (não "portar apropriadamente"). Sem TBD/TODO.

**Type/nome consistency:** nomes de skill (`authority-context`, `discovery-script`, `humanizer-linkedin`, `algoritmo-360brew`, etc.) e de command (`init`, `linkedin`, `guiado`, `rewrite`, `thread`, `score`) usados de forma idêntica entre tasks e nos testes.
