---
description: Referência completa do algoritmo 360Brew do LinkedIn (v3.0, Q1 2026): fundamentos, specs de formato e timing, métricas e sistema de pontuação. Use ao criar ou avaliar posts para garantir aderência às regras do algoritmo, otimizar alcance orgânico e calcular probabilidades de outlier.
---

## Core

# Algoritmo 360Brew - Fundamentos

> Versão 3.0 · Base: Q1 2026

## O Que É o 360Brew

O LinkedIn concluiu a transição para o **360Brew**, um motor unificado que substituiu múltiplos algoritmos fragmentados.

**Mudança fundamental:** A plataforma não prioriza mais "quem você conhece" (Social Graph), mas sim **"o que você sabe"** e **"quem precisa saber disso"** (Interest Graph).

---

## Os 5 Pilares

### 1. AEO (Answer Engine Optimization)

O algoritmo agora funciona como um **motor de resposta**:

- Feed e busca tratados como **entidade única**
- Posts são indexados como **respostas** para queries
- SEO de perfil = **ranking de autoridade sobre nicho**

**Implicação prática:** Escreva posts que respondam perguntas reais do seu ICP.

### 2. Classificação de Perfil (Profile-Content Alignment)

Seu perfil não é mais só contexto – é a **âncora de classificação**:

- O 360Brew cruza o conteúdo do post com headline, seção Sobre, experiência e skills do perfil
- Posts alinhados com expertise = **boost imediato**
- Posts fora do nicho = **supressão severa de alcance**
- O algoritmo constrói um "DNA de tópico" baseado em consistência de 2-3 nichos ao longo do tempo

**Implicação prática:** Publique consistentemente sobre os mesmos 2-3 nichos. Desvios custam caro.

### 3. Janela de Teste de 90 Minutos (nova Golden Hour)

O algoritmo não eliminou a janela crítica – ele a expandiu e tornou mais exigente:

- Os primeiros 90 minutos são um **teste com 2-5% dos seus seguidores mais ativos**
- O que o algoritmo mede nessa janela: **Saves, Dwell Time (>15 seg) e comentários longos**
- O que NÃO conta mais: curtidas rápidas e cliques superficiais
- "Post and ghost" (publicar e desaparecer) é **detectado e penaliza a distribuição futura**
- Posts podem ressuscitar dias depois — mas apenas se passarem no teste dos 90 minutos

**Implicação prática:** Esteja disponível para responder comentários nos primeiros 90 minutos após publicar.

### 4. Detecção de Padrões Artificiais (Low Entropy Noise)

O 360Brew foi treinado explicitamente para identificar conteúdo de IA e comportamento inautêntico:

- Detecta sintaxe padronizada, falta de diversidade lexical e cadências previsíveis de IA
- Posts gerados por IA sem edição humana significativa são **despriorizados em milissegundos**
- Pods de engajamento são detectados via análise de padrões de comentários similares
- Comentários genéricos de automação destroem a distribuição do post que os recebe

**Implicação prática:** Todo conteúdo precisa de voz humana autêntica, especificidade vivida e imperfeições naturais.

### 5. Validação Multimodal

O 360Brew usa modelos de IA para:

- Ler e validar conteúdo visual
- Verificar se imagem suporta o texto
- Penalizar inconsistência texto/imagem

**Implicação prática:** Visual deve complementar e reforçar a mensagem, não ser decorativo.

---

## Fórmula do Outlier

```
OUTLIER = Tópico × Gancho × Visual × Saves Potential
```

Para sair da mediana (onde 66% do alcance foi perdido), **TODOS os quatro elementos** precisam estar otimizados:

| Elemento | O que significa |
|----------|-----------------|
| **Tópico** | Alinhado com seu posicionamento + demanda do algoritmo |
| **Gancho** | Prova de trabalho/autoridade que para o scroll |
| **Visual** | Formato otimizado que suporta a mensagem |
| **Saves Potential** | Conteúdo de referência que as pessoas querem consultar depois (sinal 5x) |

**Se um falhar, o post não vira outlier.**

---

## Principais Mudanças vs 2025

| Antes (v2.0 - 2025) | Agora (v3.0 - 2026) |
|---------------------|---------------------|
| Múltiplos algoritmos | Motor único 360Brew (150B params) |
| Social Graph | **Interest Graph** |
| Golden Hour de 60min | **Janela de 90min medindo Saves + Dwell Time** |
| Perfil como contexto | **Perfil como âncora (Profile-Content Alignment)** |
| Feed e busca separados | **AEO unificado** |
| Links no corpo aceitos | **Links no corpo = -60% alcance** (colocar nos comentários) |
| Hashtags úteis | **Hashtags penalizadas** (LLM lê semântica diretamente) |
| Curtidas = engajamento | **Saves = 5x curtidas · Comentários longos = 2x curtidas** |
| Vídeo vertical | **Horizontal +36%** B2B |

---

## Regras de Ouro 2026

1. **360Brew unificou tudo** – Feed e busca são uma entidade (150B parâmetros)
2. **Perfil é âncora** – Profile-Content Alignment determina distribuição antes do post circular
3. **Outlier = Tópico × Hook × Visual × Saves Potential** – Os 4 precisam funcionar
4. **Saves > Tudo** – 5x mais poderoso que curtidas. Construa posts que pessoas queiram consultar depois
5. **Dwell time é gatilho** – Menos de 3 segundos = desclassificado. Mais de 15 segundos = distribuição destravada
6. **90 minutos críticos** – Janela de teste com 2-5% da rede. Esteja presente para responder comentários
7. **Links no corpo = -60% alcance** – Coloque links nos comentários logo após publicar
8. **Hashtags estão mortas** – O LLM lê contexto semântico. Hashtags sinalizam manipulação
9. **Carrosséis 4.1x** – Aposta mais segura (dwell time por slide é rastreado)
10. **Padrões de IA são detectados** – O 360Brew foi treinado para identificar AI Slop

---

## Formatos

# Algoritmo 360Brew - Formatos e Specs

> Especificações técnicas para texto, visual e timing.

## Specs de Texto

### Parâmetros Ótimos

| Parâmetro | Valor Ótimo | Impacto |
|-----------|-------------|---------|
| **Extensão** | 1.250-2.500 chars | +31% alcance |
| **Parágrafos** | 14+ curtos | -71% se denso |
| **Palavras** | Média ≤5 letras | -39% se complexo |
| **Nível leitura** | 5ª-7ª série | Máxima escaneabilidade |

### Estrutura do Corpo

```
HOOK (1-2 linhas)
↓
CONTEXTO (3-4 parágrafos)
→ Por que o tema importa
→ Conexão com dor/desejo
↓
DESENVOLVIMENTO (8-10 parágrafos)
→ Passos, história ou provas
→ Números específicos
↓
CONCLUSÃO (2-3 parágrafos)
→ Grande lição ou síntese
→ CTA único
```

### Regras de Formatação

**Fazer:**
- Parágrafos de 1-3 linhas
- Espaço entre parágrafos
- Números específicos (não "vários", mas "7")
- Linguagem simples e direta

**Evitar:**
- Blocos de texto densos (>3 linhas)
- Palavras complexas/técnicas sem necessidade
- Múltiplos CTAs competindo
- Emojis excessivos

---

## Formatos Visuais

### Multiplicadores de Alcance

| Formato | Performance | Quando usar |
|---------|-------------|-------------|
| **Carrossel PDF** | **4.1x** | Frameworks, listas, tutoriais |
| **Imagem 4:5** | **+86%** | Posts únicos com impacto visual |
| **Vídeo Horizontal** | **+36%** | Conteúdo B2B, demonstrações |
| **Documento/PDF** | **+3.5x** | Guias, checklists, templates |

### Especificações Técnicas

**Imagem:**
- Formato: 4:5 (1080x1350px)
- Cores consistentes com marca
- Visual ilustra o conteúdo (não decorativo)

**Carrossel:**
- 7-10 slides ideal
- PDF performa melhor que imagens
- Primeira capa = hook visual
- Última capa = CTA

**Vídeo:**
- Horizontal > Vertical para B2B
- Legendas obrigatórias
- Primeiros 3 segundos = hook

### Validação Multimodal

O 360Brew usa IA para verificar:
- Texto da imagem alinhado com post
- Visual suporta a mensagem
- Consistência entre formatos

**Penalização:** Imagem genérica ou desconectada do texto.

---

## Links e Hashtags

### Links

| Posição | Impacto no Alcance |
|---------|-------------------|
| **No corpo do post** | **−60% alcance** (penalização direta) |
| **No 1º comentário logo após publicar** | Neutro ou positivo |
| **Na bio do perfil** | Neutro |

**Regra:** Links sempre nos comentários, nunca no corpo. Publique o post, depois adicione imediatamente o link no 1º comentário.

### Hashtags

O 360Brew lê contexto semântico diretamente — não depende de hashtags para categorizar conteúdo.

| Uso | Impacto |
|-----|---------|
| 5+ hashtags | Penalização (sinaliza comportamento manipulador) |
| 3-5 hashtags genéricas (#Marketing, #Negócios) | Penalização |
| 0-2 hashtags hiper-específicas | Neutro |
| Nenhuma hashtag | Neutro/positivo |

**Regra:** Default é zero hashtags. Se usar, máximo 1-2 extremamente específicas ao nicho.

---

## Pós-Publicação (janela crítica de 90 min)

O 360Brew testa o post com 2-5% dos seus seguidores mais ativos durante os primeiros 90 minutos. O que é medido:

| Sinal | Peso | O que fazer |
|-------|------|-------------|
| **Saves (Salvamentos)** | Máximo | Conteúdo de referência que as pessoas queiram consultar depois |
| **Dwell Time >15 seg** | Alto | Estrutura que prende a leitura |
| **Comentários longos (3+ frases)** | Alto | Responda os comentários — isso sinaliza comunidade ativa |
| **Curtidas rápidas** | Baixo | Não é mais o foco |

**Protocolo de 90 minutos:**
1. Publique o post
2. No 1º comentário: adicione o link (se tiver) + contexto extra
3. Responda todos os comentários que chegarem com respostas substanciais (3+ frases)
4. Não desapareça — "post and ghost" suprime distribuição futura

### Horários por Objetivo

| Objetivo | Dia | Janela (BRT) |
|----------|-----|--------------|
| **Authority** | Terça | 08:00-10:00 |
| **Sales** | Quinta | 11:00-13:00 |
| **Engagement** | Domingo | 10:00-12:00 |

### Frequência Recomendada

| Frequência | Resultado |
|------------|-----------|
| 3-4 posts/semana | Ótimo (consistência sem saturação) |
| 5-7 posts/semana | Risco de saturação |
| 1-2 posts/semana | Subótimo (algoritmo "esquece") |

### Horários a Evitar

- 16h-02h GMT (baixa atividade)
- Segunda-feira cedo (inbox cheio)
- Sexta-feira tarde (desengajamento)

**Nota:** Com o fim da Golden Hour, timing importa menos que antes. Foque em consistência.

---

## Tópicos de Alta Performance

### Por Probabilidade Viral

| Tópico | Probabilidade |
|--------|---------------|
| **Educação de Carreira** | **3x maior** |
| **IA e Tecnologia** | Alta (em ascensão) |
| **Liderança e Gestão** | Estável |
| **Produtividade** | Média-alta |
| **Vendas B2B** | Média (nicho específico) |

### Regra do Alinhamento

Post performa melhor quando:
1. Tópico está no seu posicionamento de perfil
2. Você tem credencial/prova no tema
3. Existe demanda real (não é nicho vazio)

**Fórmula:** Expertise + Demanda + Consistência = Autoridade

---

## Checklist Rápido

### Texto
- [ ] 1.250-2.500 caracteres?
- [ ] 14+ parágrafos curtos?
- [ ] Palavras simples (média ≤5 letras)?
- [ ] Hook de prova de trabalho/autoridade?
- [ ] Números específicos (não vagos)?
- [ ] CTA único e claro?
- [ ] Nenhum link no corpo do post? (links vão no 1º comentário)
- [ ] Zero hashtags ou máximo 1-2 extremamente específicas?
- [ ] Post soa como humano, não como template de IA?

### Engajamento e Distribuição
- [ ] Post tem alto potencial de salvamento (framework, checklist, template, referência)?
- [ ] Estrutura obriga dwell time (carrossel, lista densa de valor, história progressiva)?
- [ ] Estará disponível por 90 minutos após publicar para responder comentários?
- [ ] Se tiver link, vai no 1º comentário — não no corpo?

### Visual
- [ ] Formato 4:5 ou carrossel PDF?
- [ ] Visual suporta a mensagem?
- [ ] Cores consistentes?

### Algoritmo
- [ ] Tópico alinhado ao perfil (Profile-Content Alignment)?
- [ ] Sem padrões punidos ("O que você acha?")?
- [ ] Post evita padrões detectáveis de IA (vocabulário variado, voz específica, imperfeições naturais)?

### Red Flags

❌ **CRÍTICO:** Link no corpo do post (−60% alcance)
❌ **CRÍTICO:** Hashtags em excesso ou genéricas (sinaliza manipulação ao 360Brew)
❌ **CRÍTICO:** "Post and ghost" — publicar e sumir nos primeiros 90 minutos
❌ Blocos de texto densos (−71%)
❌ "O que você acha?" / "Concordam?" (isca detectada)
❌ Visual desconectado do texto
❌ Múltiplos CTAs
❌ Posts fora do nicho do perfil
❌ Padrões de escrita de IA sem edição humana (Low Entropy Noise)

---

## Métricas

# Algoritmo 360Brew - Métricas e Benchmarks

> Números, probabilidades e sistema de pontuação.

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
