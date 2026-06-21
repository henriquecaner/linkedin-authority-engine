# Especificação Técnica — Onboarding Caminho B (HeyGen Live Avatar & Ingestão de Transcrição)

> **Data:** 2026-06-17  
> **Status:** Rascunho de Engenharia para Revisão  
> **Módulo:** Onboarding / Módulo 5  
> **Escopo:** Integração do HeyGen Live Avatar, fluxo de gravação/transcrição e o motor de ingestão semântica (Synthesizer Engine) para preenchimento automático do `authority-context.md` com gap-flagging.

---

## 1. Visão Geral e Experiência do Usuário (UX)

O onboarding atual (Caminho A) exige que o usuário responda a um questionário extenso por escrito diretamente no chat do Claude Code/Cowork. Para fundadores de empresas (ICP alvo), a digitação longa gera fricção e queda na ativação.

O **Caminho B** resolve essa barreira de duas formas complementares:
1. **Entrevista Falada Interativa (Via Avatar HeyGen):** O cliente faz uma videochamada de 15 a 30 minutos com o avatar interativo do Henrique Caner (um clone digital). O avatar utiliza o roteiro canônico do `discovery-script` como suas *Agent Skills* para conduzir a conversa em linguagem natural, gravando e transcrevendo o áudio ao final.
2. **Ingestão Direta de Reuniões Gravadas:** Se o cliente já tiver notas de reunião estruturadas, uma transcrição de reunião do Zoom/Teams ou resumos de discovery passados, ele pode simplesmente arrastar e soltar esses arquivos na pasta do projeto e solicitar a síntese.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Founder (Cliente)
    participant LP as Web LP (thelevr.com/onboarding)
    participant HeyGen as HeyGen Live Avatar API
    participant Plugin as Claude Plugin (/init)
    participant Synth as Synthesizer Engine (LLM)
    database Context as authority-context.md

    alt Opção 1: Entrevista com Avatar Digital
        Cliente->>LP: Acessa área de onboarding falado
        LP->>HeyGen: Inicializa Sessão WebRTC (Live Avatar)
        HeyGen-->>Cliente: Henrique Digital inicia entrevista falada
        Cliente->>HeyGen: Fala sobre posicionamento, ICP e ofertas
        HeyGen->>LP: Envia Transcrição Completa ao encerrar
        LP-->>Cliente: Disponibiliza download do arquivo "transcricao.txt"
    else Opção 2: Transcrição Própria (Zoom/Teams)
        Cliente->>Cliente: Prepara arquivo de transcrição bruto
    end

    Cliente->>Plugin: Executa `/init --source transcript --path ./transcricao.txt`
    Plugin->>Synth: Envia Transcrição Bruta + Prompt de Mapeamento
    Synth->>Synth: Mapeia dados brutos nas 13 seções do Schema
    Synth->>Synth: Identifica campos obrigatórios (*) ausentes
    Synth-->>Plugin: Retorna rascunho preenchido + Lista de Gaps (Faltas)
    Plugin->>Cliente: Mostra campos preenchidos e inicia entrevista curta de follow-up para os Gaps
    Cliente->>Plugin: Responde os Gaps no chat do Claude
    Plugin->>Context: Grava o authority-context.md finalizado
```

---

## 2. Arquitetura do Sistema e Fluxo de Dados

O Caminho B divide-se em três partes:
* **Módulo A: Front-end do Onboarding Interativo (HeyGen Web SDK):** Responsável por rodar o avatar digital interativo no navegador do usuário e extrair o arquivo de transcrição.
* **Módulo B: CLI do Plugin (`/init` estendido):** Recebe o arquivo de transcrição bruto e orquestra a chamada de síntese.
* **Módulo C: Motor de Ingestão Semântica (Synthesizer Engine):** Lógica que mapeia dados desestruturados para o formato Markdown tipado de 13 seções, executando a validação de dados obrigatórios.

---

## 3. Especificação do Módulo HeyGen Live Avatar

A integração utiliza o ecossistema do **HeyGen Live Avatar** para criar um agente conversacional em tempo real que simula o fundador (Henrique Caner) entrevistando o cliente.

### 3.1. Configuração do Agente (HeyGen Console)
* **Avatar ID:** Clone digital do Henrique Caner (voz e aparência calibradas em PT-BR).
* **Agent Skills (Prompt do Sistema do Avatar):**
  * O avatar deve agir como o Henrique Caner, usando o tom *direto, irreverente e focado em arquitetura comercial*.
  * Deve injetar sistematicamente o roteiro de perguntas extraídas de `skills/discovery-script/SKILL.md`.
  * **Regra de Condução:** O avatar não precisa seguir a ordem robótica das perguntas, mas deve garantir que cobre os blocos fundamentais (Perfil, Posicionamento, ICP, Oferta e Narrativa Comercial) antes de encerrar.

### 3.2. Integração via Web SDK
O front-end na plataforma `thelevr.com/onboarding` carrega o SDK do Live Avatar via WebRTC:

```javascript
import { LiveAvatarSession } from '@heygen/liveavatar-web-sdk';

const session = new LiveAvatarSession({
  apiKey: process.env.HEYGEN_API_KEY,
  avatarId: "henrique_clone_v2",
  voiceId: "henrique_pt_br_custom",
  knowledgeBaseId: "discovery_script_v1", // Vinculado às Agent Skills
  quality: "high"
});

// Inicialização da conexão de vídeo e áudio em tempo real
await session.start({
  element: document.getElementById("avatar-container")
});

// Captura de eventos e gravação da transcrição da sessão
let fullTranscript = [];
session.on("transcription", (event) => {
  // Captura o diálogo do cliente e do avatar com carimbo de data/hora
  fullTranscript.push({
    speaker: event.speaker, // "agent" ou "user"
    text: event.text,
    timestamp: Date.now()
  });
});

session.on("ended", () => {
  // Salva a transcrição consolidada em um arquivo texto para o usuário
  saveTranscriptToFile(fullTranscript);
});
```

---

## 4. O Motor de Ingestão Semântica (Synthesizer Engine)

Quando o usuário executa o comando informando o arquivo de transcrição, o plugin processa o conteúdo por meio de um pipeline de LLM estruturado.

### 4.1. Prompt do Synthesizer (Ingestão)
O prompt abaixo instrui o modelo a extrair as informações da transcrição bruta, ordenando-as no formato do template canônico de 13 seções do `authority-context-template.md`:

```markdown
Você é o Synthesizer Engine do LinkedIn Authority Engine. 
Sua tarefa é ler uma transcrição bruta de entrevista de discovery (ou notas de reunião) e mapear as informações de forma estruturada para preencher o Perfil de Autoridade do cliente.

# Entrada
Transcrição Bruta:
<TRANSCRICAO_BRUTA>

# Diretrizes de Mapeamento
1. Mapeie rigorosamente as falas do cliente nas 13 seções do template oficial.
2. Não invente dados. Se uma seção ou campo não for mencionado na transcrição, marque o campo como "[PENDENTE]" ou deixe em branco.
3. Preserve citações diretas de jargões, números, cases de sucesso e metáforas ricas usadas pelo cliente. Isso preserva a voz autêntica.
4. Identifique todos os campos críticos (marcados com "*" no template). Se algum desses campos críticos não puder ser preenchido com segurança a partir da transcrição, você DEVE gerar uma pergunta de follow-up ultra-focada para esse gap.

# Saída Esperada (Formato JSON para o CLI processar)
{
  "context_draft_md": "conteúdo markdown completo preenchido...",
  "gaps": [
    {
      "secao": "2. Posicionamento e autoridade",
      "campo_critico": "3 pilares",
      "motivo": "O cliente mencionou o tema central, mas não detalhou os 3 pilares de conteúdo de suporte.",
      "pergunta_follow_up": "Henrique, na transcrição você mencionou que seu tema principal é arquitetura de vendas, mas quais seriam os 3 subtemas ou pilares práticos que você quer bater toda semana no LinkedIn?"
    }
  ]
}
```

---

## 5. Modificações no CLI e Comandos do Plugin

O comando `/linkedin-authority-engine:init` será atualizado para receber e tratar a nova fonte de entrada.

### 5.1. Assinatura do Comando Modificada
`init.md` passará a aceitar novos argumentos para dar suporte ao processamento da transcrição:

```markdown
---
description: Onboarding do cliente. Conduz a entrevista no chat ou processa transcrições de áudio/video de discovery para criar o authority-context.md.
argument-hint: "[--refresh] [--source chat|transcript] [--path <caminho_arquivo>]"
---
```

### 5.2. Fluxo do Script de Inicialização (Lógica Interna)

```python
def run_init(args):
    # Verificar se o perfil já existe
    if has_existing_context() and not args.refresh:
        prompt_user("Perfil já existente. Deseja atualizar usando --refresh?")
        return

    if args.source == "transcript":
        if not args.path:
            print("Erro: Informe o caminho do arquivo de transcrição utilizando --path <caminho>")
            sys.exit(1)
            
        print(f"🔄 Processando transcrição em {args.path}...")
        transcript_content = read_file(args.path)
        
        # Executa chamada ao LLM Synthesizer
        result = call_synthesizer_llm(transcript_content)
        
        draft_md = result["context_draft_md"]
        gaps = result["gaps"]
        
        if gaps:
            print(f"⚠️ Encontramos {len(gaps)} campos críticos pendentes no seu perfil.")
            print("Vamos resolvê-los agora para garantir o melhor ajuste do algoritmo.\n")
            
            # Entrevista interativa focada nos GAPs (Apenas campos obrigatórios ausentes)
            for gap in gaps:
                print(f"Seção: {gap['secao']} | Campo: {gap['campo_critico']}")
                answer = input_from_user(gap['pergunta_follow_up'] + "\n>> ")
                # Injeta a resposta diretamente no rascunho Markdown
                draft_md = update_markdown_field(draft_md, gap['secao'], gap['campo_critico'], answer)
        
        # Gravação final dos arquivos de substrato de memória
        write_file("authority-context.md", draft_md)
        initialize_empty_memory_files()
        
        print("\n✅ Perfil vivo 'authority-context.md' gerado com sucesso via Caminho B!")
        print("Sugerimos rodar /linkedin-authority-engine:guided para criar seu primeiro post.")
        
    else:
        # Padrão: Roda o Caminho A (Entrevista guiada inteira no chat)
        run_chat_interview()
```

---

## 6. Plano de Testes & Mocks (Pytest)

Para garantir a confiabilidade do motor de ingestão semântica sem depender de conexões externas de rede, implementaremos testes automatizados na suíte de testes existente:

* **Mocks de LLM:** Criar fixtures que simulam o retorno do `Synthesizer Engine` (retornando JSONs com drafts de markdown e listas de GAPs variados).
* **Casos de Teste Essenciais (`tests/test_onboarding_caminho_b.py`):**
  * `test_synthesizer_extraction_success`: Verifica se o motor consegue ler uma transcrição simulada simples e mapear campos básicos perfeitamente.
  * `test_gap_flagging_triggers`: Passar uma transcrição em que faltem propositalmente dados críticos (como ICP ou Oferta) e validar se o parser identifica os gaps corretos e formula as perguntas de follow-up.
  * `test_init_cli_with_transcript_param`: Testar o CLI de inicialização passando `--source transcript` e verificar se a orquestração do arquivo de rascunho e a gravação de arquivos finais acontecem corretamente.
