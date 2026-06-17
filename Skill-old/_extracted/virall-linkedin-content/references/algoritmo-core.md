# Algoritmo 360Brew - Fundamentos

> Versão 3.0 · Base: Q1 2026

## Índice

1. [O Que É o 360Brew](#o-que-é-o-360brew)
2. [Os 5 Pilares](#os-5-pilares)
3. [Fórmula do Outlier](#fórmula-do-outlier)
4. [Mudanças vs 2025](#principais-mudanças-vs-2025)

**Arquivos relacionados:**
- [algoritmo-formatos.md](algoritmo-formatos.md) → Specs de texto, visual e timing
- [algoritmo-metricas.md](algoritmo-metricas.md) → Números, benchmarks e probabilidades

---

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

**Próximo:** [Specs de Formato e Visual →](algoritmo-formatos.md)
