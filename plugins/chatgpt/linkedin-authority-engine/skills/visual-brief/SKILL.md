---
name: visual-brief
description: Visual brief generation for LinkedIn posts: mapping the ideal format by content type, an output template with technical specs, ready-to-use prompts for AI image generation (Midjourney/DALL-E/Canva), and rules for adapting to a client's style document. Use when finalizing a post to generate the visual brief that goes with the content.
---

# Visual brief (Step C of the finalization pipeline)

> Generated automatically after the humanized post, before the Final Score.

## Identifying the ideal format

The visual format follows from the post's content type.

| Signal in the post | Recommended format | Dimensions |
|---------------|---------------------|----------|
| List, steps, framework | PDF carousel (7-10 slides) | 1080x1350px |
| Single data point, strong statement | Static 4:5 image | 1080x1350px |
| Behind the scenes, process | Horizontal video | 1920x1080px |
| Personal story | Image with quote highlight | 1080x1350px |
| Practical how-to | PDF carousel (5-8 slides) | 1080x1350px |

**Reach multipliers (reference):**
- PDF carousel: 4.1x
- 4:5 image: +86%
- Horizontal video: +36% in B2B

## Output template

```
📐 VISUAL BRIEF

Format: [PDF carousel / 4:5 image / Video]
Dimensions: [1080x1350px (4:5) / 1920x1080px (video)]

Concept: [1 sentence describing the central image]

Slide 1 (cover): [text + main visual element]
Slides 2-N: [summary of each slide, if a carousel]

Suggested palette: [2-3 colors aligned with the niche]
Font: [Recommended style: Bold serif / Modern sans / etc.]

Image generation prompt (AI):
"[Prompt ready for Midjourney / DALL-E / Canva Magic Media]"

Visual tone: [Minimalist / Data or infographic / Human or photo / Illustration]
```

## Adaptation rules

**If the client has a style document:**
- Adapt the palette, fonts, and visual style to the brand guidelines
- Use the visual tone defined in the document (minimalist, data, human, illustration)
- Respect constraints (forbidden colors, required brand elements)

**If there's no style document:**
- Palette: 2-3 colors aligned with the topic's niche
- Font: modern sans for body text, bold serif for titles if you want contrast
- Default visual tone: minimalist

## AI prompt: template by type

**Framework or list carousel:**
> "Slide design with [primary color] background, bold sans-serif headline '[key phrase title]', minimal geometric icon on left side, [style: flat / editorial / corporate]. 4:5 ratio."

**Single data point image:**
> "Single statement card, [primary color] background, large number '[value]' centered in bold serif, small caption below in sans. Negative space dominant. 4:5 ratio."

**Personal story image:**
> "Quote card design, photo of [description] on left half, quote '[impact phrase]' on right half in serif. Muted color palette. 4:5 ratio."

## Integration with adjacent skills

If the user has an image generation or presentation skill active (e.g. Canva MCP), suggest triggering those skills to materialize the brief. Otherwise, deliver just the ready prompt.

## Video (a format, not a text type)

Video posts (a <60s take, behind-the-scenes, or a point-of-view) build trust because people hear your voice and see your face. They are a **format**, not one of the text content-types — pair them with captions and a hook in the first 2 seconds. When a post's job is trust and you can record, prefer video over a selfie.

## Related

For carousels specifically, the `carousel-builder` skill writes the slide-by-slide script and caption first, then hands off here for the slide design spec.
