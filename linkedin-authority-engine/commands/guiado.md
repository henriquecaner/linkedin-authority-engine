---
description: Modo Guiado do LinkedIn Authority Engine — cria um post do zero com workflow completo de 7 steps (categoria, objetivo, pauta, estrutura, tipo, hook, corpo, CTA) lendo o perfil de autoridade e passando pelo pipeline de finalização. Use quando o usuário quer criar um post novo.
argument-hint: "[tema opcional]"
---

# /linkedin-authority-engine:guiado

## Porta 2 — Leitura do Substrato (obrigatória, automática)

Antes de qualquer geração:

1. Carregue a skill `linkedin-authority-engine:authority-context`.
2. Leia `authority-context.md` (perfil completo) e todos os arquivos em `memory/` (`winning-hooks.md`, `topic-performance.md`, `voice-profile.md`, `learnings.md`).
3. Aplicar: tom de voz, pilares de conteúdo, credenciais reais, restrições editoriais.
4. Priorizar padrões vencedores: hooks aprovados em `winning-hooks.md`, temas com alta performance em `topic-performance.md`.
5. Validar internamente a cada geração: "Isso soa como esse cliente falaria?"

---

## Pipeline: STEP 0 → 1.0 → 1.1 → [1.2] → 2 → 3 → 4 → 5 → 6 → Pipeline de Finalização

---

### STEP 0 — Contexto (automático, silencioso)

Já executado via Porta 2 acima. Confirmar internamente: tom, pilares e restrições carregados.

---

### STEP 1.0 — Categoria

Perguntar qual categoria de post:

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

---

### STEP 1.1 — Objetivo

Perguntar: "Qual o objetivo principal? Authority, Sales ou Engagement?"

---

### STEP 1.2 — Sugestões de Pauta

> Pular se o tema veio como argumento em `/linkedin-authority-engine:guiado [tema]`.

Gerar **4-5 pautas** (título curto estilo hook + 1 frase de ângulo). Se `topic-performance.md` tiver dados de performance real, priorizar temas comprovados e citar o dado (ex: "seu post sobre X teve 6x a sua média"). Usuário escolhe 1.

---

### STEP 2 — Estrutura

Carregue a skill `linkedin-authority-engine:estruturas-copywriting` e sugira **2-3 frameworks** adequados à categoria e objetivo.

Referência rápida:

| Estrutura | Flow | Melhor para |
|-----------|------|-------------|
| PAS | Problema → Agitação → Solução | Posts educativos |
| AIDA | Atenção → Interesse → Desejo → Ação | Conversão |
| BAB | Antes → Depois → Ponte | Transformação |
| HSO | Hook → Story → Offer | Narrativa + oferta |
| Storytelling | Setup → Conflito → Resolução → Lição | Conexão emocional |

Detalhes adicionais (FAB, Star-Story-Solution, APP): carregue a skill `linkedin-authority-engine:estruturas-copywriting`.

Usuário escolhe 1 framework.

---

### STEP 3 — Tipo de Conteúdo

Carregue a skill `linkedin-authority-engine:tipos-conteudo` e sugira **3 tipos** adequados. Mais populares: Story, How-to, Before-After, Contrarian, Mistakes. Lista completa na skill `linkedin-authority-engine:tipos-conteudo`.

Usuário escolhe 1 tipo.

---

### STEP 4 — Hooks

Opcionalmente rodar `${CLAUDE_PLUGIN_ROOT}/scripts/suggest_hooks.py` com a categoria, objetivo e tema:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/suggest_hooks.py --categoria <categoria> --objetivo <objetivo> --tema "<tema>"
```

Carregue também a skill `linkedin-authority-engine:hooks` para enriquecer com padrões do banco completo.

Apresentar **3 hooks** priorizando (em ordem): Prova de Trabalho, Prova de Autoridade, Transformação, Tensão/Contrarian, Confissão/Fracasso.

Usar credenciais reais do perfil carregado na Porta 2. Se `winning-hooks.md` tiver hooks aprovados para esse perfil, priorizá-los.

Usuário escolhe 1 hook.

---

### STEP 5 — Corpo

Gerar o corpo seguindo specs 360Brew (carregue `linkedin-authority-engine:algoritmo-360brew` para detalhes):

- 1.250-2.500 caracteres
- 14+ parágrafos curtos (máx. ~19 palavras cada)
- Palavras simples (média ≤5 letras)
- Números específicos
- **Re-hook no meio do post**: 1 frase de tensão ou virada entre o desenvolvimento e a conclusão, para segurar dwell time (>15 seg destrava distribuição)
- **Sem links no corpo, sem hashtags genéricas**

Estrutura base:

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

Templates por categoria: carregue `linkedin-authority-engine:templates-por-categoria`.

---

### STEP 6 — CTA

Carregue a skill `linkedin-authority-engine:ctas` e gere **3 opções** alinhadas ao objetivo escolhido.

**Prioridade 2026:** Saves (5x curtidas) › Comentários longos (2x) › Follow › Leads.

| Objetivo | CTA prioritário |
|----------|-----------------|
| Saves/Referência | "Salva esse post para consultar quando precisar" |
| Authority | "Me siga para mais sobre [nicho]" |
| Sales | "Comenta [PALAVRA] que eu mando no DM" |
| Engagement | "Discorda de algum ponto? Me conta qual e por quê" |

> Regra: sempre que o post tiver framework, checklist ou guia, o CTA de save é o padrão.

Usuário escolhe **1 CTA**. Post montado (hook + corpo + CTA) → executar **Pipeline de Finalização** abaixo.

---

## Pipeline de Finalização

> Executar nesta ordem exata, sem pular etapas.

**Entrada:** post completo (hook + corpo + CTA).

### Etapa A — Validação Técnica

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py` no post:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_specs.py post.txt
```

Se retornar erros (link no corpo, hashtags em excesso, palavras complexas, parágrafos densos): **corrigir antes de seguir**. Não avançar para Etapa B com erro técnico.

### Etapa B — Humanizer LinkedIn

Acionar a skill `linkedin-authority-engine:humanizer-linkedin` no post completo. Apresentar diff compacto (máx. 5 itens alterados).

### Etapa C — Brief Visual

Acionar a skill `linkedin-authority-engine:brief-visual` no post humanizado. Gerar automaticamente o brief com formato recomendado, conceito visual e prompt de IA.

### Etapa D — Score Final

Rodar `${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py` no post humanizado:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py post.txt --objetivo <authority|sales|engagement>
```

Apresentar relatório nas 6 dimensões (Saves Potential 30%, Hook 20%, Algorithm 20%, Structure 15%, CTA 10%, Data 5%) + classificação Top 1% / Top 5%.

Se `topic-performance.md` tiver baseline real do perfil, apresentar também a comparação (contexto relativo > absoluto).

Regra: Score ≥ 9/10 para publicar. Abaixo, indicar ajuste específico.

### Etapa E — Protocolo Pós-Publicação

Acionar a skill `linkedin-authority-engine:protocolo-pos-publicacao`.

1. Gerar o **1º comentário pronto** para colar logo após publicar: link (se houver) + contexto extra + 1 pergunta que convide respostas de 3+ frases.
2. Entregar resumo dos 90 minutos críticos.

---

## Porta 3 — Write-back ao Substrato

Após aprovação final do post, conforme as instruções da skill `linkedin-authority-engine:authority-context`:

1. Anexar em `memory/winning-hooks.md`: data, padrão de hook (se aprovado), tipo, categoria, objetivo, score obtido. (Colunas `vezes usado`, `performance média`, `keep/kill` ficam vazias até v1.x.)
2. Anexar em `memory/topic-performance.md`: data, tema, pilar, tipo de post, score. (Colunas de performance ficam vazias até v1.x.)
3. Anexar em `memory/learnings.md`: o que funcionou, o que foi ajustado, restrições aplicadas.
4. Se o usuário rejeitou alguma versão, registrar em `memory/learnings.md` o motivo da rejeição.

---

## Salvar o Post Final

Salvar o post final (versão humanizada + CTA escolhido) em:

```
outputs/posts/<AAAAMMDD>-<slug>-v1.md
```

Se já existir versão anterior do mesmo slug, incrementar o número (v2, v3...).
