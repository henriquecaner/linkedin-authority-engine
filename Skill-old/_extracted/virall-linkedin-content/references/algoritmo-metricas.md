# Algoritmo 360Brew - Métricas e Benchmarks

> Números, probabilidades e sistema de pontuação.

## Índice

1. [Estado do Alcance Orgânico](#estado-do-alcance-orgânico)
2. [Concentração de Performance](#concentração-de-performance)
3. [Sistema de Pontuação](#sistema-de-pontuação)
4. [Cálculo de Probabilidades](#cálculo-de-probabilidades)
5. [Benchmarks por Formato](#benchmarks-por-formato)
6. [Indicadores de Outlier Potencial](#indicadores-de-outlier-potencial)

**Arquivos relacionados:**
- [algoritmo-core.md](algoritmo-core.md) → Fundamentos e pilares
- [algoritmo-formatos.md](algoritmo-formatos.md) → Specs de formato e timing

---

## Estado do Alcance Orgânico

### Queda Histórica

| Período | Alcance vs 2023 |
|---------|-----------------|
| Q3 2024 | -50% |
| Q2-Q3 2025 | -65% |
| **Q1 2026** | **-66%** (estabilizado) |

**Interpretação:** A queda estabilizou, mas o alcance mediano é 66% menor que 2023.

### O Que Isso Significa

- Conteúdo mediano quase não aparece
- Outliers capturam a maior parte do alcance
- Qualidade importa mais que quantidade

---

## Concentração de Performance

### Gap Entre Tiers

| Tier | Gap de Performance | % do Alcance Total |
|------|--------------------|--------------------|
| **Top 1%** | 225x | 63% |
| **Top 5%** | 115x | 85% |
| **Top 10%** | 50x | 92% |
| **Mediano** | 1x (base) | 8% |

**Insight:** O Top 1% concentra 63% de todo o alcance. Não existe meio termo.

### Distribuição Real

```
Top 1%   ████████████████████████████████░░░░░░░ 63%
Top 5%   ██████████████████████░░░░░░░░░░░░░░░░░ 22%
Top 10%  █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  7%
Resto    ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  8%
```

---

## Sistema de Pontuação

### As 6 Dimensões (v3.5)

| Dimensão | Peso | O que avalia |
|----------|------|--------------|
| **Saves Potential** | **30%** | Probabilidade de salvamento. Sinal mais poderoso do algoritmo (5x curtida) |
| **Hook** | 20% | Poder de parar o scroll |
| **Algorithm** | 20% | Aderência às specs 360Brew (sem links no corpo, sem hashtags em excesso, sem padrões de IA, tópico alinhado ao perfil) |
| **Structure** | 15% | Framework + Length (chars) + parágrafos + escaneabilidade |
| **CTA** | 10% | Clareza, foco em 1 ação de alto valor (save ou comentário longo) |
| **Data** | 5% | Nível de prova, números concretos |

> **Por que Saves Potential lidera com 30%?** Saves geram 5x mais alcance que curtidas no 360Brew. Comentários longos (3+ frases) geram 2x. O dwell time acima de 15 segundos destrava a distribuição. O scoring precisa refletir essa hierarquia de sinais.

### Faixas de Decisão

| Score | Ação | Descrição |
|-------|------|-----------|
| **9.0-10.0** | ✅ Publicar | Candidato a outlier |
| **8.0-8.9** | ⚠️ Revisar | Muito bom, ajustes rápidos |
| **7.0-7.9** | 🔄 Retrabalhar | Gargalos claros |
| **6.0-6.9** | ❌ Refazer | Ajuste estrutural necessário |
| **< 6.0** | 🚫 Recomeçar | Voltar para objetivo + estrutura |

### Detalhamento por Dimensão

**Saves Potential (30%)**
| Score | Descrição |
|-------|-----------|
| 10 | Framework aplicável + checklist ou template + referência que pessoas consultam depois |
| 8-9 | Alta densidade de valor, claramente salvável como referência |
| 6-7 | Útil, mas não é material de consulta futura |
| 4-5 | Consumo único, nada para salvar |
| 0-3 | Conteúdo viral raso sem utilidade prática |

**Hook (20%)**
| Score | Descrição |
|-------|-----------|
| 10 | Prova de trabalho + número específico + curiosidade forte |
| 8-9 | Tem 2 de 3 elementos |
| 6-7 | Relevante, mas genérico |
| 4-5 | Clichê, sem ângulo |
| 0-3 | Punido pelo algoritmo ("O que você acha?", "Bom dia, LinkedIn") |

**Algorithm (20%)**
| Score | Descrição |
|-------|-----------|
| 10 | Sem links no corpo, zero hashtags genéricas, sem padrão de IA, tópico alinhado ao perfil |
| 8-9 | Maioria das specs, 1-2 gaps menores |
| 6-7 | Specs básicas, problema detectável (ex: hashtags demais) |
| 4-5 | Link no corpo OU hashtags em excesso OU padrão de IA detectável |
| 0-3 | Múltiplas violações ativas |

**Structure (15%)** avalia 3 sub-componentes:

| Sub-componente | Alvo | Derruba a nota se |
|----------------|------|-------------------|
| Length | 1.250-2.500 chars | <1.000 ou >3.000 chars |
| Parágrafos | 14+ curtos (máx. ~19 palavras) | <10 parágrafos ou qualquer parágrafo >150 chars |
| Framework | PAS, AIDA, BAB, HSO ou outro reconhecível | Estrutura ausente ou ordem confusa |

| Score | Descrição |
|-------|-----------|
| 10 | 3 sub-componentes perfeitos + dwell time alto (carrossel ou lista densa) |
| 8-9 | 2 de 3 sub-componentes perfeitos |
| 6-7 | Framework ok, length ou parágrafos fora do alvo |
| 4-5 | 2 sub-componentes falhando |
| 0-3 | Wall of text |

**CTA (10%)**
| Score | Descrição |
|-------|-----------|
| 10 | CTA único + específico + orientado a saves ou comentários longos |
| 8-9 | CTA alinhado ao objetivo, sem reforço de valor |
| 6-7 | CTA genérico |
| 4-5 | Múltiplos CTAs ou desconectado |
| 0-3 | CTA punido (só pede like, "O que você acha?") |

**Data (5%)**
| Score | Descrição |
|-------|-----------|
| 10 | 5+ dados específicos |
| 8-9 | 3-4 dados fortes |
| 6-7 | 1-2 dados ou exemplos |
| 4-5 | Linguagem vaga |
| 0-3 | Zero dados |

---

## Cálculo de Probabilidades

### Top 1%

```
Base = (scoreFinal / 10) × 20

Bônus:
  SavesPotential ≥ 9 → +7 pts
  Hook ≥ 9 → +4 pts
  Algorithm ≥ 9 → +4 pts

Teto: 35%
```

**Exemplo:** Score 9.2, Saves 9.5, Hook 9.0, Algorithm 9.0
- Base: (9.2/10) × 20 = 18.4
- Bônus: +7 (saves) + +4 (hook) + +4 (algorithm) = +15
- Total: 33.4% → **33% chance Top 1%**

### Top 5%

```
Base = (scoreFinal / 10) × 50

Bônus:
  SavesPotential ≥ 8 → +10 pts
  Hook ≥ 8 → +7 pts
  Algorithm ≥ 8 → +7 pts

Teto: 75%
```

**Exemplo:** Score 8.5, Saves 8.8, Hook 8.2, Algorithm 8.8
- Base: (8.5/10) × 50 = 42.5
- Bônus: +10 (saves) + +7 (hook) + +7 (algorithm) = +24
- Total: 66.5% → **66% chance Top 5%**

> Os bônus refletem a hierarquia das dimensões. Saves Potential domina porque é o sinal com maior multiplicador no algoritmo.

---

## Benchmarks por Formato

### Multiplicadores Comprovados

| Formato | Multiplicador | Confiança |
|---------|---------------|-----------|
| Carrossel PDF | **4.1x** | Alta (dwell time por slide rastreado) |
| Documento/PDF | **3.5x** | Alta |
| Imagem 4:5 | **+86%** | Alta |
| Vídeo Horizontal | **+36%** | Média-alta |
| Link no 1º comentário | Neutro/positivo | Alta |
| **Link no corpo do post** | **−60%** | Alta (evitar sempre) |

### Pesos de Engajamento (360Brew 2026)

| Ação | Peso Algoritmo | Observação |
|------|---------------|------------|
| **Save (Salvar)** | **5x curtida** | Sinal primário de utilidade |
| **Comentário longo (3+ frases)** | **2x curtida** | LLM verifica profundidade via NLP |
| **Dwell time >15 segundos** | Multiplicador de distribuição | Destrava distribuição para audiências frias |
| **Curtida/Reação** | 1x (residual) | Perdeu relevância substancial |
| **Dwell time <3 segundos** | Desclassificação | Post tratado como irrelevante |

### Por Tipo de Conteúdo

| Tipo | Performance Relativa | Save Potential |
|------|----------------------|---------------|
| Tutorial/How-to | Alta | Alto |
| Framework/Checklist | Muito alta | Muito alto |
| Lição Pessoal (com dados) | Alta | Médio-alto |
| Contrarian | Alta (risco alto) | Médio |
| Opinião Pura | Média | Baixo |
| Notícia/Comentário | Baixa | Baixo |

### Benchmarks de Engajamento

| Métrica | Top 1% | Top 5% | Mediano |
|---------|--------|--------|---------|
| Impressões | >50k | >20k | 2-5k |
| Engajamento | >5% | >3% | 1-2% |
| Salvamentos | >100 | >30 | 5-10 |
| Comentários | >50 | >20 | 5-10 |

---

## Indicadores de Outlier Potencial

Um post tem alta probabilidade de ser outlier quando:

1. **Score ≥ 9.0** no sistema de pontuação
2. **Saves Potential ≥ 9** (framework, checklist, template)
3. **Hook** com prova de trabalho ou autoridade + número
4. **Formato** otimizado (carrossel PDF ou 4:5)
5. **Tópico** alinhado ao perfil e com demanda (Profile-Content Alignment)
6. **Zero violações:** sem link no corpo, sem hashtags genéricas, sem padrão de IA
7. **Dwell time projetado alto** (estrutura que obriga leitura progressiva)

**Probabilidade de Outlier:**
- 6-7 indicadores = 70%+ chance
- 5 de 7 indicadores = 50%+ chance
- 4 de 7 indicadores = 30%+ chance
- < 4 indicadores = improvável

---

**Anterior:** [← Formatos](algoritmo-formatos.md) | **Início:** [Fundamentos](algoritmo-core.md)
