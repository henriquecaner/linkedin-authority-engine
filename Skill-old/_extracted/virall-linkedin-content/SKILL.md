---
name: virall-linkedin-content
description: "Virall Linkedin Content - Sistema completo para posts de alta performance no LinkedIn (algoritmo 360Brew 2026) com Humanizer integrado. Ativar quando o usuário pedir posts LinkedIn, conteúdo LinkedIn, carrosséis, hooks, rewrite de posts, séries/threads, ou digitar /linkedin, /linkedin guiado, /linkedin rewrite, /linkedin thread ou /linkedin score. Pipeline obrigatório: CTA → Humanizer (automático, detecta padrões de IA via skill humanizer) → Score nas 6 dimensões. 4 modos: Guiado (7 steps), Rewrite, Thread e Score. Integra Unabyss (MCP) para contexto do cliente e performance real dos posts. Regras críticas 2026: links no corpo = -60% alcance, hashtags penalizadas, protocolo 90 min pós-publicação. Suporta contexto de cliente com documento de estilo."
---

# Virall Linkedin Content V4.0

Sistema de criação de conteúdo LinkedIn otimizado para o algoritmo **360Brew** (Q1-Q2 2026).

> **Versão interna:** V4.0 (bugfixes nos 3 scripts, integração Unabyss, 1º comentário gerado no pipeline, hooks de Listas/Frameworks, docs reconciliados)

## Índice

1. [Command Router](#command-router-linkedin)
2. [Contexto de Cliente](#contexto-de-cliente)
3. [Modos de Operação](#modos-de-operação)
4. [Pipeline de Finalização](#pipeline-de-finalização) ← compartilhado por todos os modos
5. [MODO GUIADO](#modo-guiado--workflow-completo)
6. [MODO REWRITE](#modo-rewrite--otimizar-post-existente)
7. [MODO THREAD/SÉRIE](#modo-threadsérie--sequência-de-posts)
8. [MODO SCORE](#modo-score--avaliação-imediata)
9. [Conceitos 360Brew (resumo)](#conceitos-360brew-resumo)
10. [Checklist Rápido](#checklist-rápido)
11. [Arquivos de Referência](#arquivos-de-referência)

---

## Command Router `/linkedin`

> **PRIORIDADE MÁXIMA:** Se a mensagem do usuário começar com `/linkedin`, executar o roteamento abaixo antes de qualquer outra coisa. Ignorar o restante do fluxo normal até o comando ser processado.

| Comando | Ação imediata |
|---------|---------------|
| `/linkedin` | Exibir menu de modos e aguardar escolha |
| `/linkedin guiado` | Iniciar MODO GUIADO (STEP 1) |
| `/linkedin guiado [tema]` | MODO GUIADO já com tema (pula STEP 1.2) |
| `/linkedin rewrite` | Solicitar o post e iniciar MODO REWRITE |
| `/linkedin rewrite [post]` | MODO REWRITE com o post já fornecido |
| `/linkedin thread` | Iniciar MODO THREAD (coletar tema e nº de posts) |
| `/linkedin thread [tema]` | MODO THREAD com tema já informado |
| `/linkedin score [post]` | MODO SCORE direto no post colado |
| `/linkedin help` | Exibir esta tabela |

**Comportamento de `/linkedin` (sem argumento):**

```
🎯 Virall Linkedin Content — O que vamos criar?

1️⃣  Guiado      — Criar post do zero (workflow completo)
2️⃣  Rewrite     — Otimizar post existente
3️⃣  Thread      — Série de posts sobre um tema
4️⃣  Score       — Avaliar + humanizar post pronto

Digite o número ou o nome do modo.
```

---

## Contexto de Cliente

> Verificar silenciosamente antes de iniciar qualquer modo (STEP 0).

1. **Unabyss (MCP)** — se disponível, consultar posicionamento, tom e performance real dos últimos posts. Queries prontas em [integracao-unabyss.md](references/integracao-unabyss.md). Fonte primária de dados reais.
2. **Instruções do Projeto** — perfil, posicionamento, pilares, objetivos, restrições
3. **Documento de Estilo** — tom de voz, vocabulário, exemplos de referência, emojis
4. **Aprendizados deste cliente** — fallback local em [aprendizados-clientes.md](references/aprendizados-clientes.md) quando o Unabyss não estiver disponível.

**Se existir contexto:** Aplicar automaticamente tom, pilares, credenciais e restrições. Validar sempre: "Isso soa como esse cliente falaria?"

**Se não existir:** Default em [estilo-tom.md](references/estilo-tom.md) — PT-BR, conversacional, direto, zero frescura.

---

## Modos de Operação

| Modo | Quando usar | Entrada |
|------|-------------|---------|
| 🆕 **Guiado** | Criar post do zero | Tema ou ideia vaga |
| ✏️ **Rewrite** | Otimizar post existente | Post pronto ou rascunho |
| 🔗 **Thread** | Criar sequência de posts | Tema central + nº de posts |
| 📊 **Score** | Avaliar post pronto | Post colado |

Todos os modos terminam executando o mesmo **Pipeline de Finalização** abaixo.

---

## Pipeline de Finalização

> Bloco compartilhado por todos os modos. Sempre executar nesta ordem, sem perguntar.

**Entrada:** post completo (hook + corpo + CTA escolhido).

### Etapa A — Validação técnica (script)

Rodar `validate_specs.py` no post para checagem mecânica:
```bash
python scripts/validate_specs.py post.txt
```

Se retornar erros (link no corpo, hashtags em excesso, palavras complexas, parágrafos densos), **corrigir antes** de seguir. Não passa pra Etapa B com erro técnico.

### Etapa B — Humanizer

Acionar a skill `humanizer` no post completo. Apresentar diff compacto (máx. 5 itens). Detalhes em [humanizer-pipeline.md](references/humanizer-pipeline.md).

### Etapa C — Brief Visual

Gerar automaticamente após o post humanizado. Template e regras em [brief-visual.md](references/brief-visual.md).

### Etapa D — Score Final (script)

Rodar `score_post.py` no post humanizado:
```bash
python scripts/score_post.py post.txt --objetivo authority
```

Apresentar o relatório nas 6 dimensões + Top 1% / Top 5%. Detalhes em [algoritmo-metricas.md](references/algoritmo-metricas.md).

Se houver dados no Unabyss, apresentar também o baseline do perfil (média real de reações/comentários) junto do score — contexto relativo > absoluto.

### Etapa E — 1º Comentário + Protocolo Pós-Publicação

1. **Gerar o 1º comentário pronto** para colar logo após publicar: link (se houver) + contexto extra que não coube no post + 1 pergunta que convide respostas de 3+ frases. O protocolo exige esse comentário — entregar pronto, não como tarefa.
2. Entregar o resumo dos 90 minutos críticos. Versão completa em [protocolo-pos-publicacao.md](references/protocolo-pos-publicacao.md).
3. **Registrar no Unabyss** (se disponível): post final + score + objetivo, conforme [integracao-unabyss.md](references/integracao-unabyss.md).

```
🎯 PROTOCOLO PÓS-PUBLICAÇÃO

1. Publique
2. 1º comentário imediato: link + pergunta substancial
3. Próximos 90 min: responda todos os comentários com 3+ frases
4. Não edite o post nos primeiros 30 min
5. Não saia da plataforma — interaja em posts de outras contas
```

---

## MODO GUIADO — Workflow Completo

**Pipeline:** STEP 0 → 1.0 → 1.1 → [1.2] → 2 → 3 → 4 → 5 → 6 → **Pipeline de Finalização**

### STEP 0 — Contexto (automático)

Verificar silenciosamente: documento de estilo, instruções de projeto, histórico do cliente em `aprendizados-clientes.md`.

### STEP 1.0 — Categoria

Perguntar qual categoria:

| Opção | O que é |
|-------|---------|
| Lição de carreira | Momento marcante + aprendizado |
| Conquista | Vitória com números |
| Fracasso | Erro + lição (vulnerabilidade) |
| Desmistificar | Quebrar mito do mercado |
| Dica prática | Algo acionável |
| Opinião | Posicionamento polêmico |
| Bastidores | Dia a dia real |
| Outro | Tema livre |

### STEP 1.1 — Objetivo

Perguntar: "Authority, Sales ou Engagement?"

### STEP 1.2 — Sugestões de Pauta

> Pular se o tema veio em `/linkedin guiado [tema]`.

Gerar **4-5 pautas** (título curto estilo hook + 1 frase de ângulo). Se o STEP 0 trouxe performance real via Unabyss, priorizar temas comprovados e citar o dado ("seu post sobre X teve 6x sua média"). Usuário escolhe 1.

### STEP 2 — Estrutura

Sugerir **2-3 frameworks**. Tabela rápida abaixo, detalhes em [estruturas-copywriting.md](references/estruturas-copywriting.md).

| Estrutura | Flow | Melhor para |
|-----------|------|-------------|
| PAS | Problema → Agitação → Solução | Posts educativos |
| AIDA | Atenção → Interesse → Desejo → Ação | Conversão |
| BAB | Antes → Depois → Ponte | Transformação |
| HSO | Hook → Story → Offer | Narrativa + oferta |
| Storytelling | Setup → Conflito → Resolução → Lição | Conexão emocional |

Outras no arquivo de referência: FAB, Star-Story-Solution, APP.

### STEP 3 — Tipo de Conteúdo

Sugerir **3 tipos**. Mais populares: Story, How-to, Before-After, Contrarian, Mistakes. Lista completa em [tipos-conteudo.md](references/tipos-conteudo.md).

### STEP 4 — Hooks (assistido por script)

Opcionalmente rodar `suggest_hooks.py` para input:
```bash
python scripts/suggest_hooks.py --categoria conquista --objetivo authority --tema "vendas B2B"
```

Apresentar **3 hooks** baseados nas escolhas, priorizando: Prova de Trabalho 🏆, Prova de Autoridade 🎖️, Transformação 🔄, Tensão/Contrarian ⚡, Confissão/Fracasso 💔.

Se houver documento de estilo: usar templates característicos do cliente, credenciais reais, estilo de hook preferido. Banco completo em [hooks.md](references/hooks.md).

### STEP 5 — Corpo

Gerar corpo seguindo specs 360Brew:
- 1.250-2.500 caracteres
- 14+ parágrafos curtos (máx. ~19 palavras cada)
- Palavras simples (média ≤5 letras)
- Números específicos
- **Re-hook no meio do post**: 1 frase de tensão ou virada entre o desenvolvimento e a conclusão, para segurar dwell time (>15 seg destrava distribuição)
- **Sem links no corpo, sem hashtags genéricas**

Estrutura-base:
```
HOOK (1-2 linhas)
↓
CONTEXTO (3-4 parágrafos)
↓
DESENVOLVIMENTO (8-10 parágrafos)
↓
CONCLUSÃO (2-3 parágrafos)
↓
CTA (1 único — STEP 6)
```

Templates por categoria em [templates-por-categoria.md](references/templates-por-categoria.md).

### STEP 6 — CTA

Gerar **3 opções** alinhadas ao objetivo. Banco em [ctas.md](references/ctas.md).

**Prioridade 2026:** Saves (5x curtidas) › Comentários longos (2x) › Follow › Leads.

| Objetivo | CTA prioritário |
|----------|-----------------|
| Saves/Referência | "Salva esse post para consultar quando precisar" |
| Authority | "Me siga para mais sobre [nicho]" |
| Sales | "Comenta [PALAVRA] que eu mando no DM" |
| Engagement | "Discorda de algum ponto? Me conta qual e por quê" |

> **Regra:** Sempre que o post contiver framework, checklist ou guia, o CTA de save é o padrão.

Usuário escolhe **1 CTA**. Post montado → executar **Pipeline de Finalização**.

---

## MODO REWRITE — Otimizar Post Existente

### REWRITE STEP 1 — Diagnóstico

Rodar `validate_specs.py` no post original e analisar contra specs 360Brew. Apresentar:

```
DIAGNÓSTICO:
Score estimado: X/10
🚨 Problemas críticos: [link no corpo, hashtags em excesso]
⚠️ Importantes: [hook fraco, CTA genérico]
✅ O que funciona: [pontos fortes]
```

### REWRITE STEP 2 — Foco

Perguntar: "Foco principal? (a) Hook, (b) Alcance/specs, (c) CTA, (d) Tudo"

### REWRITE STEP 3 — Gerar 2 Versões

- **Versão A (Conservadora):** Mantém voz e estrutura, corrige problemas técnicos
- **Versão B (Bold):** Hook mais forte, reestrutura para impacto máximo

### REWRITE STEP 4 — Pipeline em ambas + Comparativo

> **Ordem corrigida:** humanizar primeiro, depois mostrar score comparativo. Senão o usuário escolhe baseado em score que vai mudar.

1. Aplicar Humanizer + score em A e B
2. Apresentar comparativo final:

| Métrica | Original | Versão A (humanizada) | Versão B (humanizada) |
|---------|----------|------------------------|------------------------|
| Score | X/10 | X/10 | X/10 |
| Saves Potential | X/10 | X/10 | X/10 |
| Hook | X/10 | X/10 | X/10 |
| Algorithm | X/10 | X/10 | X/10 |

3. Usuário escolhe (ou pede mix). Executar **Brief Visual + Protocolo Pós-Publicação** na escolhida.

---

## MODO THREAD/SÉRIE — Sequência de Posts

### THREAD STEP 1 — Definir Série

Coletar: tema central, objetivo (Authority/Sales/Engagement), nº de posts (3-7), cadência.

### THREAD STEP 2 — Arquitetura

```
POST 1 — GANCHO DA SÉRIE (Hook/Contrarian) → Apresenta tema, cria expectativa
POST 2 — PROVA DE AUTORIDADE → Credencial + contexto
POST 3 — EDUCATIVO/HOW-TO → Valor prático
POST 4 — STORY/BASTIDORES → Conexão emocional
POST 5 — CONVERSÃO/CTA → Fechamento com oferta ou lead magnet
```

Adaptar conforme nº de posts e objetivo.

### THREAD STEP 3 — Ponto de Partida

"Todos de uma vez" ou "um por vez (workflow guiado por post)".

### THREAD STEP 4 — Geração + Pipeline por post

Para cada post: gerar → executar **Pipeline de Finalização** completo (validação, humanizer, brief visual, score). Formato:

```
━━━━━━━━━━━━━━━━━━━━━━━
📝 POST [N]/[TOTAL] — [Tipo]
━━━━━━━━━━━━━━━━━━━━━━━

[Texto humanizado]

✏️ Humanizer: [diff compacto]
📊 Score: X.X/10 | Top 1%: X% | Top 5%: X%
📐 Brief Visual: [formato + conceito + prompt IA]
━━━━━━━━━━━━━━━━━━━━━━━
```

### THREAD STEP 5 — Calendário

| Post | Tema | Tipo | Score | Data sugerida | Janela (BRT) |
|------|------|------|-------|---------------|--------------|

Timing recomendado em [protocolo-pos-publicacao.md](references/protocolo-pos-publicacao.md).

---

## MODO SCORE — Avaliação Imediata

Para `/linkedin score [post]`. Pula geração e vai direto pro pipeline parcial:

1. **Validação técnica** — `validate_specs.py`
2. **Humanizer** — diff compacto
3. **Score** — `score_post.py` no post humanizado
4. **Veredicto** — publicar / ajustar / retrabalhar

Sem Brief Visual, sem Protocolo (a menos que pedido).

---

## Conceitos 360Brew (resumo)

> Detalhes em [algoritmo-core.md](references/algoritmo-core.md), [algoritmo-formatos.md](references/algoritmo-formatos.md), [algoritmo-metricas.md](references/algoritmo-metricas.md).

### Fórmula do Outlier

```
OUTLIER = Tópico × Gancho × Visual × Saves Potential
```

### Specs de texto

| Parâmetro | Valor Ótimo |
|-----------|-------------|
| Extensão | 1.250-2.500 chars |
| Parágrafos | 14+ curtos |
| Palavras | Média ≤5 letras |
| Nível leitura | 5ª-7ª série |

### Multiplicadores de alcance

| Formato | Performance |
|---------|-------------|
| Carrossel PDF | **4.1x** |
| Imagem 4:5 | **+86%** |
| Vídeo horizontal | **+36%** B2B |
| Link no 1º comentário | Neutro/positivo |
| **Link no corpo** | **−60%** (evitar sempre) |

### Pesos de engajamento (2026)

| Ação | Peso |
|------|------|
| Save | 5x curtida |
| Comentário longo (3+ frases) | 2x curtida |
| Dwell time >15 seg | Multiplicador de distribuição |
| Curtida | 1x (residual) |

### Sistema de Scoring (6 dimensões, v3.5)

| Dimensão | Peso |
|----------|------|
| Saves Potential | **30%** |
| Hook | 20% |
| Algorithm | 20% |
| Structure (Length + Parágrafos + Framework) | 15% |
| CTA | 10% |
| Data | 5% |

**Regra:** Score ≥ 9/10 para publicar. Abaixo, indicar ajuste específico.

### Hashtags

Default em 2026: **zero hashtags**. O 360Brew lê semântica diretamente. Se usar, máximo 1-2 hiper-específicas. Mais que 2 = comportamento de manipulação detectado.

---

## Checklist Rápido

### Algoritmo (crítico)
- [ ] Nenhum link no corpo? (vai no 1º comentário)
- [ ] Zero hashtags genéricas? (default: sem hashtags)
- [ ] Tópico alinhado ao perfil? (Profile-Content Alignment)
- [ ] Post passou pelo Humanizer?

### Conteúdo
- [ ] 1.250-2.500 caracteres?
- [ ] 14+ parágrafos curtos?
- [ ] Hook de prova de trabalho/autoridade?
- [ ] Números específicos?
- [ ] Alto Saves Potential (framework, checklist, lista)?

### CTA e Visual
- [ ] 1 único CTA orientado a save ou comentário longo?
- [ ] Brief visual gerado?

### Pós-Publicação
- [ ] 1º comentário pronto (gerado na Etapa E)?
- [ ] Disponível 90 min para responder?
- [ ] Post registrado no Unabyss para o feedback loop?

### 🚨 Red Flags
❌ Link no corpo (−60%)
❌ Post and ghost
❌ Hashtags genéricas
❌ Padrões de IA não tratados
❌ Tópico fora do nicho
❌ Blocos densos (−71%)
❌ "O que você acha?" / CTA que só pede like
❌ Múltiplos CTAs

---

## Arquivos de Referência

### Pipeline
| Arquivo | Conteúdo |
|---------|----------|
| [humanizer-pipeline.md](references/humanizer-pipeline.md) | Como acionar a skill `humanizer` no post |
| [brief-visual.md](references/brief-visual.md) | Brief visual com prompt IA por tipo |
| [protocolo-pos-publicacao.md](references/protocolo-pos-publicacao.md) | 90 min críticos + timing por objetivo |
| [integracao-unabyss.md](references/integracao-unabyss.md) | Unabyss (MCP): contexto + performance real. Fonte primária do feedback loop |
| [aprendizados-clientes.md](references/aprendizados-clientes.md) | Feedback loop local (fallback do Unabyss) |

### Algoritmo 360Brew
| Arquivo | Conteúdo |
|---------|----------|
| [algoritmo-core.md](references/algoritmo-core.md) | Fundamentos, 5 pilares, Profile-Content Alignment |
| [algoritmo-formatos.md](references/algoritmo-formatos.md) | Specs de texto, visual, links, hashtags |
| [algoritmo-metricas.md](references/algoritmo-metricas.md) | Pesos, benchmarks, scoring 6 dimensões |

### Bibliotecas de Conteúdo
| Arquivo | Conteúdo |
|---------|----------|
| [hooks.md](references/hooks.md) | 147 hooks por tipo |
| [templates-por-categoria.md](references/templates-por-categoria.md) | Templates por categoria |
| [tipos-conteudo.md](references/tipos-conteudo.md) | 16 tipos detalhados |
| [estruturas-copywriting.md](references/estruturas-copywriting.md) | PAS, AIDA, BAB, HSO etc. |
| [ctas.md](references/ctas.md) | CTAs por objetivo (inclui Save) |
| [estilo-tom.md](references/estilo-tom.md) | Guia de estilo e tom default |

### Exemplos
| Arquivo | Conteúdo |
|---------|----------|
| [exemplo-execucao-completa.md](references/exemplo-execucao-completa.md) | Workflow completo do início ao fim |

### Scripts
| Script | Uso |
|--------|-----|
| `scripts/validate_specs.py post.txt` | Validar specs 360Brew (chars, parágrafos, links, hashtags). Etapa A do Pipeline |
| `scripts/score_post.py post.txt --objetivo authority` | Score nas 6 dimensões. Etapa D do Pipeline. `--compact` ou `--json` para integração |
| `scripts/suggest_hooks.py --categoria X --objetivo Y --tema "Z"` | Hooks por categoria/objetivo (inclui Listas/Frameworks). Input do STEP 4. `--seed` p/ reprodutibilidade |
