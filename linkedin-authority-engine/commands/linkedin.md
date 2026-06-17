---
description: Menu de modos do LinkedIn Authority Engine. Exibe Guiado, Rewrite, Thread e Score e roteia para o modo escolhido. Use quando o usuário não sabe por onde começar ou quer uma visão geral dos modos disponíveis.
argument-hint: "[guiado|rewrite|thread|score]"
---

# /linkedin-authority-engine:linkedin

## Verificação de Perfil (obrigatória antes de qualquer modo)

Antes de exibir o menu ou rotear para um modo, verificar silenciosamente se `authority-context.md` existe no projeto atual.

- Se **não existir**: exibir a mensagem abaixo e parar.

```
⚠️  Nenhum perfil encontrado.
Execute /linkedin-authority-engine:init para criar seu perfil de autoridade antes de gerar posts.
```

- Se **existir**: continuar com o roteamento abaixo.

---

## Roteamento por Argumento

| Argumento recebido | Ação imediata |
|-------------------|---------------|
| `guiado` | Iniciar MODO GUIADO (STEP 1.0) |
| `guiado [tema]` | MODO GUIADO com tema já informado (pula STEP 1.2) |
| `rewrite` | Solicitar o post e iniciar MODO REWRITE |
| `rewrite [post]` | MODO REWRITE com o post já fornecido |
| `thread` | Iniciar MODO THREAD (coletar tema e nº de posts) |
| `thread [tema]` | MODO THREAD com tema já informado |
| `score [post]` | MODO SCORE direto no post colado |
| sem argumento | Exibir menu abaixo |

---

## Menu (sem argumento)

```
🎯 LinkedIn Authority Engine — O que vamos criar?
1 Guiado   — post do zero (workflow completo)
2 Rewrite  — otimizar post existente
3 Thread   — série de posts
4 Score    — avaliar + humanizar post pronto

Digite o número ou o nome do modo.
```

Aguardar escolha do usuário e rotear para o comando correspondente:
- `1` ou `guiado` → invocar `/linkedin-authority-engine:guiado`
- `2` ou `rewrite` → invocar `/linkedin-authority-engine:rewrite`
- `3` ou `thread` → invocar `/linkedin-authority-engine:thread`
- `4` ou `score` → invocar `/linkedin-authority-engine:score`
