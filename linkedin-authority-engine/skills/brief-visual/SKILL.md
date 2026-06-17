---
name: brief-visual
description: Geração de brief visual para posts LinkedIn: mapeamento de formato ideal por tipo de conteúdo, template de output com specs técnicas, prompts prontos para geração de imagem com IA (Midjourney/DALL-E/Canva) e regras de adaptação a documento de estilo do cliente. Use ao finalizar um post para gerar o brief visual que acompanha o conteúdo.
---

# Brief Visual (Etapa C do Pipeline de Finalização)

> Gerado automaticamente após o post humanizado, antes do Score Final.

## Identificação do formato ideal

O formato do visual decorre do tipo de conteúdo do post.

| Sinal no post | Formato recomendado | Dimensão |
|---------------|---------------------|----------|
| Lista, passos, framework | Carrossel PDF (7-10 slides) | 1080x1350px |
| Dado único, afirmação forte | Imagem estática 4:5 | 1080x1350px |
| Bastidores, processo | Vídeo horizontal | 1920x1080px |
| História pessoal | Imagem com quote highlight | 1080x1350px |
| How-to prático | Carrossel PDF (5-8 slides) | 1080x1350px |

**Multiplicadores de alcance (referência):**
- Carrossel PDF: 4.1x
- Imagem 4:5: +86%
- Vídeo horizontal: +36% em B2B

## Template de output

```
📐 BRIEF VISUAL

Formato: [Carrossel PDF / Imagem 4:5 / Vídeo]
Dimensão: [1080x1350px (4:5) / 1920x1080px (vídeo)]

Conceito: [1 frase descrevendo a imagem central]

Slide 1 (capa): [texto + elemento visual principal]
Slide 2-N: [resumo de cada slide, se carrossel]

Paleta sugerida: [2-3 cores alinhadas ao nicho]
Fonte: [Estilo recomendado: Bold serif / Sans moderna / etc.]

Prompt de geração de imagem (IA):
"[Prompt pronto para Midjourney / DALL-E / Canva Magic Media]"

Tom visual: [Minimalista / Dados ou infográfico / Humano ou foto / Ilustração]
```

## Regras de adaptação

**Se houver documento de estilo do cliente:**
- Adaptar paleta, fontes e estilo visual às diretrizes da marca
- Usar tom visual definido no documento (minimalista, dados, humano, ilustração)
- Respeitar restrições (cores proibidas, elementos de marca obrigatórios)

**Se não houver documento de estilo:**
- Paleta: 2-3 cores alinhadas ao nicho do tema
- Fonte: sans moderna para textos, bold serif para títulos se contraste for desejado
- Tom visual padrão: minimalista

## Prompt de IA: template por tipo

**Carrossel de framework ou lista:**
> "Slide design with [cor primária] background, bold sans-serif headline '[título da frase-chave]', minimal geometric icon on left side, [estilo: flat / editorial / corporate]. 4:5 ratio."

**Imagem de dado único:**
> "Single statement card, [cor primária] background, large number '[valor]' centered in bold serif, small caption below in sans. Negative space dominant. 4:5 ratio."

**Imagem de história pessoal:**
> "Quote card design, photo of [descrição] on left half, quote '[frase de impacto]' on right half in serif. Muted color palette. 4:5 ratio."

## Integração com skills adjacentes

Se o usuário tiver skill de geração de imagem ou presentation ativa (ex: Canva MCP, premium-web-architect), sugerir acionar essas skills para materializar o brief. Senão, entregar apenas o prompt pronto.
