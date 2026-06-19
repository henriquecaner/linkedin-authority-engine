---
plugin: hormozi-gtm
plugin_version: 1.0.1
command: pricing
version: 2
status: draft
created: 2026-06-18
client: level-tech
product: linkedin-authority-engine
frameworks:
  - pricing-playbook
  - value-equation
  - ltv-cac
  - money-models
humanizer_pass: false
humanizer_mode: n/a
voz: raw
audit_ref: outputs/audit/audit-level-tech-20260618-v2.md
parent_version: outputs/pricing/pricing-level-tech-20260617-v1.md
---

# Pricing Review v2 — LinkedIn Authority Engine

## TL;DR

Modelo travado em 2026-06-18. Mudou tudo desde o v1: produto agora é **plugin + guia/wiki/SDK + suporte por chat (CS) + 12 meses de updates**; escada de **add-ons que empilham** (não tiers alternativos); pricing **estático com gross-up** sobre taxa InfinityPay+Nitro + imposto Simples Anexo III; **sem mensalidade — recorrência é renovação anual.**

- **Gold (base): R$ 3.997** → ~R$ 3.000 limpos.
- **Gold + Platinum (add-on, 12h de Henrique @ R$ 500/h): R$ 11.997** → ~R$ 9.000 limpos. Exatamente 3x o Gold.
- **+ Extensão (12→24 meses): +R$ 1.197** → ~R$ 897 limpos.
- **Sem free tier.** Taxa absorvida, preço estático, até 10x sem juros, cupom PIX ≤20%.

**Maior alavanca:** não é o número do Gold — é a **take-rate da extensão + taxa de renovação anual**. Sem mensalidade, é isso que tira você da esteira no ano 2.
**Maior risco:** sem MRR, o ano 1 é 100% front-end → ~11-15 vendas/mês TODO mês pro piso de R$ 25-40k de lucro. Você assumiu a esteira de propósito e gerencia o caixa com a antecipação do Nitro.
**Único ponto ainda no escuro:** Fator R (Anexo III vs V) — confirmar com contador.

---

## 📊 A escada de produtos

| Passo | Composição | Sticker | Líquido limpo | Alavanca "/mês" (10x) |
|---|---|---|---|---|
| **Gold** (base, sozinho) | plugin + guia/wiki/SDK + chat CS + 12m updates | **R$ 3.997** | ~R$ 3.000 | R$ 399/mês |
| **+ Platinum** (só com Gold) | + 12h de Henrique (1h/sem × 12 sem) | **R$ 11.997** | ~R$ 9.000 | R$ 1.200/mês |
| **+ Extensão** (Gold ou bundle) | + updates/suporte 12→24 meses | +**R$ 1.197** | +~R$ 897 | — |

Caminhos válidos: Gold · Gold+Extensão · Gold+Platinum · Gold+Platinum+Extensão. **Platinum nunca vive sozinho.**

---

## 🧮 Por que o sticker é esse: gross-up estático

Preço estático, taxa absorvida (não repassada). O sticker tem que proteger o líquido no **pior caminho de pagamento**: cupom 20% no PIX **ou** 10x absorvido (17,39%). Imposto Simples Anexo III por cima (6% hoje / ~10% na escala).

```
Preço estático = Líquido desejado ÷ fator do pior caminho
Pior fator (cupom 20% PIX, imposto 6%): 0,80 × 0,94 = 0,752
Gold: 3.000 ÷ 0,752 = 3.989 → R$ 3.997
```

**Comportamento do Gold R$ 3.997 (imposto 6%):**

| Caminho | Você recebe limpo |
|---|---|
| PIX cheio | ~R$ 3.757 |
| PIX −10% | ~R$ 3.381 |
| PIX −20% | ~R$ 3.006 |
| Cartão 1x (5,99%) | ~R$ 3.520 |
| 10x sem juros (absorve 17,39%) | ~R$ 3.062 |

Em qualquer caminho, ≥ R$ 3.000. O cupom PIX é desconto **e** ferramenta de margem: empurra pro PIX, onde a taxa é ~0.

**Tabela de taxas (InfinityPay + Nitro):** PIX ≈ 0% · 1x 5,99% · 3x 12,49% · 10x 17,39% · 12x 18,79%. (Validado: R$ 1.000 em 12x → R$ 812,10.)

---

## ⚖️ As 5 leis — re-score vs v1

| Lei | v1 | v2 | Por quê |
|---|---|---|---|
| 1. Valor, não preço | 🟡 | 🟢 | Ancora em agência/ghostwriter (R$ 2-6k/mês), não em SaaS. Bundle 3x ancora o Gold. |
| 2. Cobra o que vale | 🔴 | 🟢 | Saiu do cost-plus. Líquido-alvo definido pelo valor, gross-up só blinda taxa/imposto. |
| 3. Preço sinaliza qualidade | 🔴 | 🟢 | R$ 3.997 (não mais R$ 2.397) confirma a promessa pro ICP de R$ 1M+. |
| 4. Tiering captura mercado | 🔴 | 🟢 | Escada de add-ons: base + ajuda (3x) + extensão. Captura quem quer DIY e quem quer mão na massa. |
| 5. Runway maior, ask maior | 🟡 | 🟡 | 12 meses de updates inclusos + extensão paga. Mas sem mensalidade, o runway longo só vira caixa na renovação (ano 2), não compondo no ano 1. |

**Placar: 4 🟢 / 1 🟡 / 0 🔴.** v1 era 0/2/3. O modelo agora sustenta o preço.

---

## 🔁 O money model: renovação anual (sem mensalidade) — decisão consciente

Você descartou a mensalidade R$ 297. Recorrência = **renovação anual + extensão**. Funciona (modelo "licença + manutenção"), mas com 2 consequências que você assumiu de olhos abertos:

1. **Ano 1 = 100% front-end.** Sem MRR compondo. Pra bater R$ 25-40k de lucro/mês, precisa de **~11-15 vendas/mês, todo mês**, sem colchão de recorrente num mês fraco. É a esteira que o v1 alertou — agora é escolha sua.
2. **Você sai da esteira no ano 2**, quando renovações compõem por cima das vendas novas. Por isso a **métrica-religião vira taxa de renovação anual**, não MRR.

**A favor:** com Nitro, mesmo a venda 10x "sem juros" te antecipa o valor cheio (−17,39%) **na hora**. Você recebe ~R$ 3.062 do Gold hoje, não pingado. É a sua ferramenta de gestão de caixa — casa com o "eu gerencio meu fluxo".

**A extensão R$ 1.197 no carrinho é seu principal puxador de caixa pra frente** — adianta receita do ano 2. Maximiza a take-rate dela.

### Matemática do piso (R$ 30k lucro/mês), ano 1

- Gold limpo ~R$ 3.000. Custos fixos ~R$ 2.000/mês (ferramentas) + CS (quando contratar).
- Só Gold: **~11-12 vendas/mês** pro piso (antes do custo de CS).
- 1 bundle Gold+Platinum (~R$ 9.000 limpos) = 3 Golds em caixa — mas custa 12h suas. Use pra acelerar, não como volume.
- Cada extensão soma ~R$ 897 e ainda adianta o ano 2.

---

## 🧪 Teste de validação (2 semanas)

Próximos 10-15 leads, começando pela **audiência warm que já espera o produto**, recebem o pricing novo.

**Critérios:**
- Fechar **≥4 dos primeiros 15** no Gold R$ 3.997 → preço validado, escala.
- Trava E todo "não" cita preço → testa cupom maior no PIX antes de mexer no sticker (não baixa o sticker; protege o sinal de qualidade).
- "Não" cita falta de prova/case self-serve → é percepção, não preço: reforça cases na LP, não baixa preço.
- **Take-rate da extensão** e **% que sobe pro bundle Platinum** = sinais de profundidade de ascensão.

---

## ⚠️ Riscos

1. **Esteira no ano 1 (sem MRR).** Mitigação: lança warm primeiro (alta conversão, ciclo curto), usa a antecipação do Nitro pro caixa, e trata renovação como métrica-mãe desde a 1ª venda.
2. **🔴 Fator R — o número que mais mexe na tabela.** Se cair no Anexo V (~15,5% vs 6%), o Gold precisa ir pra ~R$ 3.550 pra manter R$ 3.000 limpos. **Confirmar com contador antes de fixar o checkout.** É o único item ainda no chute.
3. **Imposto sobe com a faixa.** A ~R$ 540k/ano de receita (3ª faixa, ~10% efetivo), reprecifica o Gold pra ~R$ 3.333 pra manter o líquido. Revisita ao virar de faixa.
4. **Platinum come 12h suas a R$ 500/h.** É desconto consciente sobre sua tarifa de R$ 700-1500. Se o bundle vender em volume, monitore: a 3 bundles/mês são 36h/mês a meia-tarifa. Se virar gargalo, sobe a hora ou corta toques.
5. **Bundle R$ 11.997 ancora mais fraco que um R$ 19.997.** Você priorizou acessibilidade (3x limpo). Aceitável — só não é o anchor máximo possível.

---

## 🔄 Próximos passos

1. ✅ Escada e pricing travados no `gtm-context`.
2. **Confirmar Fator R** com contador (único item aberto).
3. **`/hormozi-gtm:lp`** — LP de vendas com a oferta 8.0 + esse pricing. PT-BR v1 essa semana, EN v2 depois.
4. Após 10-15 vendas, `/hormozi-gtm:pricing` v3 pra calibrar com dado real (renewal rate, take-rate da extensão, % bundle).

---

*Pricing review v2 gerado pelo plugin hormozi-gtm. Persona Alex Hormozi. Voz raw, sem humanizer (output interno/diagnóstico). Parent: pricing-level-tech-20260617-v1.md.*
