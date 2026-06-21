# Especificação de Design — Gemini Multimodal Live Onboarding Playground

> **Data:** 2026-06-17  
> **Status:** Proposta de Arquitetura e Interface (Aprovado para Prototipagem)  
> **Modelo de Referência:** Gemini Live API (Bidirectional WebSocket) · `gemini-2.0-flash-exp` / `gemini-3.1-flash-live-preview`  
> **Módulo:** Onboarding Alternativo / Evolução do Caminho B  

---

## 1. O Veredito: Por que essa ideia é um Game Changer?

Substituir o HeyGen (que é assíncrono, possui lag de processamento de vídeo de ~2-3 segundos e tem alto custo por minuto) pela **Gemini Multimodal Live API** para o Onboarding do *LinkedIn Authority Engine* é uma **decisão de engenharia brilhante**.

### Vantagens do Gemini Live API vs. Avatares de Vídeo:
1. **Latência de Conversação Humana:** O Gemini Live opera via WebSockets transmitindo e recebendo áudio bruto (PCM) em tempo real. A latência é de **<500ms**, criando uma experiência natural de "troca de ideia" fluida, sem silêncios constrangedores.
2. **Interrupção Ativa (Barge-in):** O modelo detecta acusticamente quando o usuário começa a falar e interrompe a sua própria saída de áudio instantaneamente, simulando perfeitamente um diálogo humano.
3. **Custo Praticamente Zero:** Em vez de pagar por minuto de processamento de vídeo do HeyGen, você paga apenas os tokens de áudio de entrada/saída da API do Gemini, o que reduz o custo em **mais de 95%**.
4. **Function Calling em Tempo Real:** Conforme o cliente responde sobre seu ICP ou ofertas por voz, o Gemini pode disparar *ferramentas* (functions) para ir preenchendo as seções do `authority-context.md` em tempo real na tela, dando um feedback visual imediato de "perfil sendo construído".

---

## 2. Arquitetura da Conexão (Como funciona sob o capô)

A Gemini Live API funciona estabelecendo uma conexão WebSocket segura diretamente do navegador (ou por meio de um proxy seguro) para o endpoint do Google.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Founder (Cliente)
    participant App as Web Playground App (Browser)
    participant Mic as Web Audio API (Microfone)
    participant WS as Gemini Live API (WebSocket)
    database Context as authority-context.md

    Cliente->>App: Clica em "Iniciar Conversa (Talk)"
    App->>WS: Conecta wss://generativelanguage.googleapis.com/ws/...
    WS-->>App: Conexão Estabelecida
    App->>WS: Envia SessionInit (System Instructions + Voice Config)
    WS-->>App: Resposta de Áudio: "Fala Henrique! Tudo bem? Vamos começar..."
    App->>Mic: Ativa gravação de microfone (PCM 16-bit, 16kHz ou 24kHz)
    
    loop Conversação Bidirecional em Tempo Real
        Mic->>App: Captura blocos de áudio PCM
        App->>WS: Envia chunk base64 via WebSocket (RealtimeInput)
        Cliente->>App: Fala: "Meu ICP são CEOs de tecnologia"
        WS->>WS: Processa áudio + Reconhece interrupção se houver
        WS-->>App: Transmite chunks de áudio de saída (PCM) + Texto
        App->>Cliente: Toca áudio instantaneamente (Web Audio Context)
        
        opt Function Calling (Preenchimento em Tempo Real)
            WS->>App: ToolCall: update_profile_field(secao="4", campo="ICP", valor="CEOs de tecnologia")
            App->>Context: Atualiza rascunho do Markdown na tela do usuário
            App->>WS: ToolResponse: {"status": "success"}
        end
    end
```

---

## 3. Configuração do Agente (Prompting & Voice Initiation)

Para que o agente inicie o papo ativamente e extraia as informações corretas, configuramos o parâmetro `setup` da sessão com as diretrizes do **Henrique Caner - O Estrategista de Autoridade**:

### 3.1. System Instructions (Setup da Sessão)
```markdown
Você é o Henrique Caner, estrategista de autoridade no LinkedIn e fundador da LEVEL TECH. Seu tom é direto, irreverente, pragmático e focado em arquitetura comercial.

Sua missão é entrevistar o usuário (que é um fundador ou líder de empresa) para extrair os elementos do seu perfil de autoridade.

DIRETRIZES DA CONVERSA:
1. Inicie a conversa ativamente com uma saudação calorosa e provocativa. Exemplo: "Fala mestre! Henrique Caner aqui. Vamos parar de postar para duas curtidas e construir sua autoridade de verdade no LinkedIn? Me conta: qual é o seu principal negócio hoje e quem é o seu cliente ideal?"
2. Não faça perguntas longas ou em blocos. Faça UMA pergunta curta de cada vez. Deixe o usuário falar e responda com insights práticos ou validações rápidas.
3. Se o usuário falar algo abstrato ou genérico, confronte-o amigavelmente para buscar dados específicos (ex: faturamento, anos de experiência, resultados reais, cases).
4. Suas metas são descobrir:
   - O Tema Central e os 3 Pilares de Conteúdo do fundador.
   - O ICP ultra-específico (e quem NÃO é o ICP).
   - O principal produto ou oferta de alto valor.
   - Uma história marcante de bastidor ou "prova de trabalho".
5. Quando tiver informações seguras sobre esses pontos, use a ferramenta `update_profile_field` para preencher as seções correspondentes na tela.
```

### 3.2. Configuração de Voz
A sessão WebSocket é iniciada especificando a modalidade de resposta de áudio e a voz desejada (Laomedeia ou Aoede são excelentes para vozes executivas/estratégicas claras):

```json
{
  "setup": {
    "model": "models/gemini-2.0-flash-exp",
    "generationConfig": {
      "responseModalities": ["AUDIO"],
      "speechConfig": {
        "voiceConfig": {
          "prebuiltVoiceConfig": {
            "voiceName": "Aoede" // Voz natural masculina/feminina de baixa latência
          }
        }
      }
    },
    "systemInstruction": {
      "parts": [
        {
          "text": "<INSTRUCOES_DO_SISTEMA_AQUI>"
        }
      ]
    },
    "tools": [
      {
        "functionDeclarations": [
          {
            "name": "update_profile_field",
            "description": "Atualiza uma seção do perfil de autoridade do cliente em tempo real na tela.",
            "parameters": {
              "type": "OBJECT",
              "properties": {
                "section": {
                  "type": "STRING",
                  "description": "O número da seção (de 1 a 13) ou nome da seção a ser atualizada."
                },
                "field": {
                  "type": "STRING",
                  "description": "O nome do campo ou variável específica."
                },
                "value": {
                  "type": "STRING",
                  "description": "O valor ou texto extraído das falas do cliente para preencher o campo."
                }
              },
              "required": ["section", "field", "value"]
            }
          }
        ]
      }
    ]
  }
}
```

---

## 4. UI Design do Playground (Estética Premium & Alinhamento Visual)

Seguindo as diretrizes de design de alta fidelidade e estética premium da LEVEL TECH, o Playground será desenvolvido com um visual **Dark Mode Minimalista e Tecnológico (estilo Cyberpunk/Sci-Fi refinado)**.

### Elementos Visuais do Painel:
* **Background:** Preto profundo com gradiente sutil radial em azul neon/roxo escuro (`background: radial-gradient(circle, #0c0d14 0%, #050508 100%)`).
* **Micro-animação de Onda de Voz (The Wave):** No centro da tela, em vez de um avatar estático, teremos uma animação fluida em canvas ou CSS ondulando de acordo com as frequências do microfone do usuário (quando ele fala) e da resposta do Gemini (quando o robô fala).
* **Painel Lateral de Configurações (Glassmorphism):** Um menu lateral direito translúcido (`backdrop-filter: blur(12px)`) onde o usuário pode selecionar o modelo de IA, ajustar a sensibilidade de ruído, escolher a voz do entrevistador e monitorar o tamanho de contexto da sessão.
* **Console de Saída em Tempo Real (Live Builder):** No lado esquerdo, um editor Markdown interativo que exibe o arquivo `authority-context.md` sendo escrito e atualizado dinamicamente à medida que as funções (`update_profile_field`) são disparadas pelo Gemini.

---

## 5. Arquétipo de Implementação Web (HTML/JS)

Abaixo está a estrutura limpa de como implementar o loop de captura de áudio do microfone do usuário em chunks PCM de 16-bit / 16kHz e transmiti-los via WebSocket:

```javascript
// Configuração do contexto de áudio
let audioContext;
let ws;
let processor;
let inputSource;

async function startLiveSession() {
  audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
  
  // Conectar com a Gemini Live API via WebSocket
  ws = new WebSocket("wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=" + API_KEY);
  
  ws.onopen = () => {
    // 1. Enviar mensagem de inicialização (Setup)
    sendSetupMessage();
    
    // 2. Iniciar captura de áudio do microfone
    startMicrophoneCapture();
  };
  
  ws.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    
    // Tratar áudio de saída enviado pelo Gemini
    if (data.serverContent?.modelTurn?.parts) {
      for (const part of data.serverContent.modelTurn.parts) {
        if (part.inlineData && part.inlineData.mimeType.startsWith("audio/pcm")) {
          playAudioChunk(part.inlineData.data); // Executa play base64 PCM
        }
      }
    }
    
    // Tratar Function Calling (Preenchimento na tela)
    if (data.toolCall) {
      handleToolCall(data.toolCall);
    }
  };
}

async function startMicrophoneCapture() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  inputSource = audioContext.createMediaStreamSource(stream);
  
  // Criar processador de áudio para chunks de PCM
  processor = audioContext.createScriptProcessor(2048, 1, 1);
  inputSource.connect(processor);
  processor.connect(audioContext.destination);
  
  processor.onaudioprocess = (e) => {
    const inputBuffer = e.inputBuffer.getChannelData(0);
    const pcm16Data = convertFloat32ToPCM16(inputBuffer);
    
    // Envia o chunk base64 para o WebSocket do Gemini
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        realtimeInput: {
          mediaChunks: [{
            mimeType: "audio/pcm",
            data: arrayBufferToBase64(pcm16Data)
          }]
        }
      }));
    }
  };
}

function convertFloat32ToPCM16(buffer) {
  let l = buffer.length;
  let buf = new Int16Array(l);
  while (l--) {
    let s = Math.max(-1, Math.min(1, buffer[l]));
    buf[l] = s < 0 ? s * 0x8000 : s * 0x7FFF;
  }
  return buf.buffer;
}
```

---

## 6. Próximos Passos & Integração com o Projeto

Caso queira avançar com esse playground, podemos:
1. **Adicionar uma rota web ou página dedicada `/playground`** ao site `thelevr.com` integrando esse script de WebSocket nativo para capturar o onboarding de forma inovadora.
2. **Substituir o backend de IA tradicional:** O arquivo gerado ao final da chamada é um Markdown pronto compatível com o `authority-context.md` do plugin, permitindo que o usuário baixe-o ou envie diretamente para o repositório local do Claude Code via API.
