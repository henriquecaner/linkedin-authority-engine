---
description: Onboarding do cliente. Conduz a entrevista de discovery (Caminho A) e cria authority-context.md na pasta do projeto, mais memory/ e outputs/posts/. Auto-sugerido quando outros comandos rodam sem perfil. Suporta --refresh para atualizar perfil existente.
argument-hint: "[--refresh]"
---

# /linkedin-authority-engine:init

Cria o perfil vivo do cliente — substitui a montagem manual de "projeto Claude + instruções".

## Passos

1. **Checar contexto existente.** Se `authority-context.md` já existe na raiz: sem `--refresh`, perguntar se quer revisar/atualizar; com `--refresh`, atualizar campos defasados preservando o resto.
2. **Carregar o roteiro.** Use a ferramenta Skill para carregar `linkedin-authority-engine:discovery-script`. (Caminho A — entrevista guiada in-session. Caminho B/transcrição é futuro.)
3. **Conduzir a entrevista.** Uma pergunta por vez ou blocos curtos. Não fechar uma seção sem cobrir os campos críticos (`*`).
4. **Sintetizar o perfil.** Use a ferramenta Skill para carregar `linkedin-authority-engine:authority-context` e preencher o `references/authority-context-template.md` com as respostas. Marcar lacunas em campos `*` e pedir follow-up só do que faltou.
5. **Escrever os arquivos** na raiz do projeto:
   - `authority-context.md` (perfil preenchido, com frontmatter `last_updated`, `version`)
   - `memory/winning-hooks.md`, `memory/topic-performance.md`, `memory/voice-profile.md`, `memory/learnings.md` (cabeçalhos vazios conforme schemas)
   - `outputs/posts/.gitkeep`
6. **Confirmar** mostrando um resumo (tema central, 3 pilares, objetivo, mix) e instruir: "rode `/linkedin-authority-engine:guiado` para o primeiro post."

## Voz

Setup/interação: PT-BR direto, sem voz de assistente robótica. Sem humanizer aqui (não é copy externa).
