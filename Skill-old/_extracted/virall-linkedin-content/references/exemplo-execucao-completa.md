# Exemplo de Execução Completa (v4.0)

> Demonstração do MODO GUIADO do início ao fim, incluindo o Pipeline de Finalização. Todos os números de score abaixo são **output real** de `validate_specs.py` e `score_post.py` — se os scripts mudarem, regenerar este exemplo.

---

## Contexto do Exemplo

**Usuário:** Founder de SaaS B2B de automação de vendas
**Experiência:** 8 anos em vendas, 3 anos como founder
**Objetivo:** Construir autoridade no nicho

---

## STEP 0 — Contexto (silencioso)

- Unabyss disponível → query de posicionamento + últimos posts. Retorno: nicho "vendas B2B/growth", posts sobre processo comercial têm 3x mais comentários que posts de opinião.
- Sem documento de estilo → default [estilo-tom.md](estilo-tom.md).

## STEP 1.0 — Categoria

Usuário escolhe: **Conquista** (vitória com números).

## STEP 1.1 — Objetivo

Usuário escolhe: **Authority**.

## STEP 1.2 — Sugestões de Pauta

Pautas priorizadas pelo dado do Unabyss (posts de processo > posts de opinião):

1. **"Como triplicamos o pipeline sem aumentar o time"** ← escolhida
2. "O framework que reduziu churn em 40%"
3. "3 métricas que salvaram meu SaaS"
4. "De R$10k MRR para R$150k em 18 meses"

## STEP 2 — Estrutura

Sugeridas: **BAB** ⭐ (transformação com números), FAB, PAS. Usuário escolhe **BAB**.

## STEP 3 — Tipo de Conteúdo

Sugeridos: **Before-After** ⭐, How-to, Data-Driven. Usuário escolhe **Before-After**.

## STEP 4 — Hooks

`suggest_hooks.py -c conquista -o authority -t "pipeline B2B"` como input + 3 opções geradas. Escolhido (Prova de Trabalho + Transformação):

```
Triplicamos o pipeline em 6 meses. De R$80k para R$250k.

Sem contratar. Sem anúncios. Sem cold call.
```

## STEP 5 — Corpo + STEP 6 — CTA

CTA escolhido: **Save** ("Salva esse post para aplicar o framework no seu funil") — regra: post com framework → CTA de save é o padrão.

**Post completo montado:**

```
Triplicamos o pipeline em 6 meses. De R$80k para R$250k.

Sem contratar. Sem anúncios. Sem cold call.

Esse é o framework que usamos. Salva — você vai precisar dele.

ANTES:

Nosso time de 4 SDRs fazia 200 ligações por dia.

Taxa de conversão: 2%.

Pipeline mensal: R$80k.

Todo mundo esgotado. Resultado parado.

DEPOIS:

Pipeline mensal: R$250k.

Mesmo time. Mesmas 4 pessoas.

Taxa de conversão: 8%.

Zero ligações frias.

A PONTE — o framework de 3 passos:

1. Troque cold call por conteúdo que ensina

Criamos 3 posts por semana com dúvidas reais do ICP.

Cada post nasce de uma objeção ouvida em call.

Leads chegam já aquecidos. Metade do ciclo de venda.

2. Automatize a triagem inicial

Um form simples de 4 perguntas filtra 70% dos curiosos.

SDR só fala com quem tem fit real.

O tempo do time vai para quem pode fechar.

3. Nutra antes da call

5 emails em 14 dias. Conteúdo útil, não pitch.

O lead chega na call sabendo o que quer.

Os números em 6 meses:

• Pipeline: R$80k → R$250k

• Conversão: 2% → 8%

• Ciclo de venda: caiu 40%

• Custo por lead: caiu 35%

Aqui está a parte que ninguém fala:

Volume de atividade não é resultado.

Atividade certa, na hora certa, vira pipeline previsível.

Salva esse post para aplicar o framework no seu funil.
```

---

## Pipeline de Finalização

### Etapa A — Validação técnica

`validate_specs.py` → **🟢 POST VÁLIDO**

| Stat | Valor |
|------|-------|
| Caracteres | 1.265 ✓ (1.250-2.500) |
| Parágrafos | 34 ✓ (14+) |
| Média letras/palavra | 4.5 ✓ (≤5) |
| Hashtags | 0 ✓ |
| Links no corpo | nenhum ✓ |

### Etapa B — Humanizer

Diff compacto (exemplo):

```
✏️ Humanizer aplicado:
- "resultados incríveis" → "R$250k/mês"
- "Em suma," → removido
(2 padrões — post já tinha voz humana)
```

### Etapa C — Brief Visual

```
📐 BRIEF VISUAL
Formato: Carrossel PDF (8 slides) — post tem framework numerado
Dimensão: 1080x1350px (4:5)
Conceito: capa com "R$80k → R$250k" em destaque; 1 slide por passo
Slide 1 (capa): hook visual com o contraste de números
Slides 2-7: antes/depois + os 3 passos do framework
Slide 8: CTA de save
Paleta: 2 cores sóbrias do nicho B2B
Prompt IA: "Slide design with deep blue background, bold sans-serif
headline 'R$80k → R$250k', minimal geometric icon, flat editorial. 4:5"
Tom visual: Dados/infográfico
```

### Etapa D — Score Final (output real do script)

`score_post.py ex.txt --objetivo authority`:

| Dimensão | Peso | Score |
|----------|------|-------|
| Saves Potential | 30% | 9.5 |
| Hook | 20% | 8.5 |
| Algorithm | 20% | 10.0 |
| Structure | 15% | 10.0 |
| CTA | 10% | 9.0 |
| Data | 5% | 10.0 |

**Score Final: 9.5/10** → ✅ PUBLICAR — candidato a outlier

**Probabilidades:** Top 1%: 30% · Top 5%: 71%
(Top 1% = base 18.9 + bônus Saves≥9 (+7) + Algorithm≥9 (+4) = 29.9 ≈ 30)

**Baseline via Unabyss:** média do perfil 12 reações/post; melhor post recente: processo comercial (40 reações). Este post ataca o mesmo padrão ✓

### Etapa E — 1º Comentário + Protocolo

**1º comentário pronto:**

```
O form de 4 perguntas que uso na triagem tá aqui: [link]

E me conta: qual dos 3 passos é o gargalo no seu funil hoje?
Respondo todo mundo.
```

**Protocolo:** publicar terça 08:00-10:00 BRT (Authority), responder tudo com 3+ frases por 90 min, não editar nos primeiros 30 min.

**Registro no Unabyss:** post + score + objetivo gravados ("Status: aguardando publicação").

---

## Checklist Final

- [x] 1.265 chars (1.250-2.500)
- [x] 34 parágrafos (14+)
- [x] Hook com prova de trabalho + números
- [x] Framework numerado (Saves Potential 9.5)
- [x] CTA único de save
- [x] Zero links no corpo, zero hashtags
- [x] Humanizer aplicado
- [x] Brief visual + 1º comentário prontos
- [x] Score 9.5 ≥ 9.0
- [x] Registrado no Unabyss

**Status:** ✅ Pronto para publicar
