import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const SCRIPT = [
  {
    scene: "1. Apresentação Inicial",
    file: "Frontend Web",
    type: "LIVE",
    path: "Aba do Navegador (Frontend)",
    command: "Nenhum",
    step: "1. Deixe na tela do site (Frontend). 2. Respire, sorria e olhe para a câmera para começar.",
    talk: "Olá! Aqui é a Natália. Hoje vou apresentar nosso Projeto Avançado Web3! Nós criamos um sistema completo onde as pessoas podem usar moedas digitais, guardar fundos para render recompensas e participar das decisões do projeto. Para me ajudar a explicar a teoria enquanto mostro o código, vou chamar minha assistente pessoal de inteligência artificial.",
    code: ""
  },
  {
    scene: "2. Chamando a Assistente",
    file: "Aguardar Áudio",
    type: "LIVE",
    path: "Terminal da Assistente",
    command: "./INICIAR_NATY.bat",
    step: "1. Abra o Terminal da assistente. 2. Fale a frase abaixo. (A Naty vai escutar e ler o arquivo 'relatorio_final.md' que contém a Definição do Problema, Arquitetura e os Dados de Deploy).",
    talk: "[FALE EXATAMENTE ISSO]: Naty, apresente o projeto por favor.",
    code: ""
  },
  {
    scene: "3. O Relatório Final",
    file: "relatorio_final.md",
    type: "FILE",
    path: "web3_protocol/relatorio_final.md",
    command: "Nenhum",
    step: "1. Abra o arquivo 'relatorio_final.md'. 2. Mostre o diagrama na tela enquanto a Naty (IA) fala.",
    talk: "Como a Naty acabou de explicar, nosso sistema é dividido em quatro partes principais. Aqui neste relatório, nós temos todo o desenho de como essas partes conversam entre si para fazer o aplicativo funcionar.",
    code: ""
  },
  {
    scene: "4. Contrato da Moeda (Token)",
    file: "NatyToken.sol",
    type: "FILE",
    path: "contracts/NatyToken.sol",
    command: "Nenhum",
    step: "1. Abra a pasta 'contracts' e clique no arquivo 'NatyToken.sol'.",
    talk: "O primeiro pilar é o NatyToken. Ele funciona como o 'dinheiro' do nosso ecossistema. Nós usamos um padrão moderno e seguro, que permite fazer transferências mais rápidas e sem cobrar taxas desnecessárias dos usuários.",
    code: ""
  },
  {
    scene: "5. Contrato das Artes (NFT)",
    file: "NatyNFT.sol",
    type: "FILE",
    path: "contracts/NatyNFT.sol",
    command: "Nenhum",
    step: "1. Na mesma pasta, clique no arquivo 'NatyNFT.sol'.",
    talk: "Em seguida, temos o NatyNFT. Esse código é o responsável por criar artes digitais exclusivas. Pense neles como medalhas virtuais que a gente entrega para recompensar os usuários mais engajados.",
    code: ""
  },
  {
    scene: "6. Sistema de Recompensas",
    file: "NatyStaking.sol",
    type: "FILE",
    path: "contracts/NatyStaking.sol",
    command: "Nenhum",
    step: "1. Clique no arquivo 'NatyStaking.sol'. 2. Aponte para a parte do Oráculo se quiser.",
    talk: "O coração de tudo é o NatyStaking. É aqui que o usuário guarda seus tokens para render juros. O mais legal é que nós conectamos ele com informações do mundo real, pegando o preço do Ethereum na hora exata para calcular as recompensas certinhas.",
    code: ""
  },
  {
    scene: "7. Poder de Decisão (DAO)",
    file: "NatyDAO.sol",
    type: "FILE",
    path: "contracts/NatyDAO.sol",
    command: "Nenhum",
    step: "1. Clique no último contrato, o 'NatyDAO.sol'.",
    talk: "Por fim, temos o NatyDAO. Esse contrato garante que o projeto seja da comunidade. Quem tem tokens guardados no sistema ganha o direito de votar e decidir o futuro do aplicativo de forma totalmente justa e automática.",
    code: ""
  },
  {
    scene: "8. Rodando os Testes Finais",
    file: "Terminal de Testes",
    type: "LIVE",
    path: "Novo Terminal",
    command: "cd web3_protocol && npx hardhat test",
    step: "1. Abra um NOVO terminal. 2. Clique em 'COPIAR COMANDO' ao lado. 3. Cole no terminal, aperte ENTER e aguarde finalizar.",
    talk: "Para provar que toda essa engrenagem funciona sem falhas, nós criamos testes automáticos de segurança. Vou rodar eles aqui agora. Como vocês podem ver, todos os contratos passaram nos testes!",
    code: ""
  },
  {
    scene: "9. Prática no Frontend",
    file: "Frontend Web",
    type: "LIVE",
    path: "Aba do Navegador (Frontend)",
    command: "Nenhum",
    step: "1. Volte para a aba do Frontend. 2. Conecte a carteira, peça tokens, faça Stake e minte o NFT.",
    talk: "E para encerrar a nossa demonstração, vamos ver isso na prática! Vou conectar minha carteira, pegar tokens de teste e realizar um Stake. Imediatamente o sistema reconhece minha participação, liberando o meu NFT exclusivo e o meu poder de voto na DAO. Muito obrigada pela atenção e até mais!",
    code: ""
  }
];

export default function Teleprompter() {
  const [currentScene, setCurrentScene] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [timer, setTimer] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [studioStatus, setStudioStatus] = useState("CONNECTED");
  
  const videoRef = useRef(null);
  const timerInterval = useRef(null);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  useEffect(() => {
    async function startWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) { console.error("Erro webcam:", err); }
    }
    startWebcam();
    
    return () => {
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(t => t.stop());
      }
    };
  }, []);

  const startRecordingRef = useRef(null);
  const togglePauseRef = useRef(null);

  useEffect(() => {
    startRecordingRef.current = startRecording;
    togglePauseRef.current = togglePause;
  });

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      
      if (e.code === 'Space') {
        e.preventDefault();
        const mr = mediaRecorder.current;
        if (!mr || mr.state === 'inactive') {
          if (startRecordingRef.current) startRecordingRef.current();
        } else if (mr.state === 'recording' || mr.state === 'paused') {
          if (togglePauseRef.current) togglePauseRef.current();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const startTimer = () => {
    if (timerInterval.current) clearInterval(timerInterval.current);
    timerInterval.current = setInterval(() => {
      setTimer(prev => prev + 1);
    }, 1000);
  };

  const stopTimer = () => {
    clearInterval(timerInterval.current);
    timerInterval.current = null;
  };

  const startRecording = async () => {
    try {
      let screenStream;
      try {
        // Tenta capturar tela + áudio do sistema
        screenStream = await navigator.mediaDevices.getDisplayMedia({ video: { frameRate: 30 }, audio: true });
      } catch (err) {
        console.warn("Aviso: Falha ao capturar tela com áudio (Possível erro de driver no Windows). Tentando apenas vídeo...", err);
        // Fallback: Tenta capturar apenas a tela (o áudio será pego só pelo microfone)
        screenStream = await navigator.mediaDevices.getDisplayMedia({ video: { frameRate: 30 } });
      }

      const webcamStream = videoRef.current?.srcObject;
      
      if (!webcamStream) {
        alert("Ligue a webcam (e dê permissão) antes de iniciar a gravação!");
        return;
      }

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const screenVideo = document.createElement('video');
      screenVideo.muted = true;
      screenVideo.srcObject = screenStream;
      screenVideo.play().catch(e => console.error("Screen video erro:", e));

      const webcamVideo = document.createElement('video');
      webcamVideo.muted = true;
      webcamVideo.srcObject = webcamStream;
      webcamVideo.play().catch(e => console.error("Webcam video erro:", e));

      const track = screenStream.getVideoTracks()[0];
      const settings = track.getSettings();
      canvas.width = settings.width || 1920;
      canvas.height = settings.height || 1080;

      const drawFrame = () => {
        if (!isRecording && mediaRecorder.current?.state === 'inactive') return;
        
        if (ctx) {
          ctx.drawImage(screenVideo, 0, 0, canvas.width, canvas.height);
          
          const camSize = canvas.width * 0.15;
          const margin = 30;
          const x = canvas.width - camSize - margin;
          const y = canvas.height - camSize - margin;

          ctx.save();
          ctx.beginPath();
          ctx.arc(x + camSize/2, y + camSize/2, camSize/2, 0, Math.PI * 2);
          ctx.closePath();
          ctx.clip();
          ctx.drawImage(webcamVideo, x, y, camSize, camSize);
          ctx.restore();
          
          ctx.strokeStyle = '#10b981';
          ctx.lineWidth = 5;
          ctx.beginPath();
          ctx.arc(x + camSize/2, y + camSize/2, camSize/2, 0, Math.PI * 2);
          ctx.stroke();
        }
        requestAnimationFrame(drawFrame);
      };

      const combinedStream = canvas.captureStream(30);
      
      const audioCtx = new window.AudioContext();
      const dest = audioCtx.createMediaStreamDestination();
      let hasAudio = false;

      if (screenStream.getAudioTracks().length > 0) {
        const systemSource = audioCtx.createMediaStreamSource(new MediaStream([screenStream.getAudioTracks()[0]]));
        systemSource.connect(dest);
        hasAudio = true;
      }

      try {
        const micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (micStream.getAudioTracks().length > 0) {
          const micSource = audioCtx.createMediaStreamSource(micStream);
          micSource.connect(dest);
          hasAudio = true;
        }
      } catch (audioErr) {
        console.warn("Sem áudio do microfone:", audioErr);
      }

      if (hasAudio) {
        combinedStream.addTrack(dest.stream.getAudioTracks()[0]);
      }

      const options = { mimeType: 'video/webm' };
      if (MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')) {
         options.mimeType = 'video/webm;codecs=vp8,opus';
      }

      try {
        mediaRecorder.current = new MediaRecorder(combinedStream, options);
      } catch (mrErr) {
        console.warn("Fallback do MediaRecorder:", mrErr);
        mediaRecorder.current = new MediaRecorder(combinedStream);
      }
      
      mediaRecorder.current.ondataavailable = (e) => chunks.current.push(e.data);
      mediaRecorder.current.onstop = () => {
        const blob = new Blob(chunks.current, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `naty_presentation_${new Date().getTime()}.webm`;
        a.click();
        chunks.current = [];
        screenStream.getTracks().forEach(t => t.stop());
        if (audioStream) audioStream.getTracks().forEach(t => t.stop());
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      setIsPaused(false);
      startTimer();
      drawFrame();
    } catch (err) { 
      console.error(err); 
      alert("Erro ao iniciar gravação: " + err.message); 
    }
  };

  const stopRecordingAndSave = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      setIsRecording(false);
      setIsPaused(false);
      stopTimer();
      setTimer(0);
    }
  };

  const togglePause = () => {
    if (!isRecording || !mediaRecorder.current) return;
    if (isPaused) {
      mediaRecorder.current.resume();
      startTimer();
    } else {
      mediaRecorder.current.pause();
      stopTimer();
    }
    setIsPaused(!isPaused);
  };

  const copyToClipboard = (text) => {
    if (!text || text === "Nenhum") {
      alert("Esta cena não possui comandos automáticos.");
      return;
    }
    navigator.clipboard.writeText(text)
      .then(() => {
        alert(`Comando [${text}] copiado com sucesso!`);
      })
      .catch(err => {
        console.error("Erro ao copiar:", err);
      });
  };

  const changeScene = (idx) => {
    setCurrentScene(idx);
  };

  const formatTime = (s) => {
    const min = Math.floor(s / 60);
    const sec = s % 60;
    return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
  };

  const togglePiP = async () => {
    if (videoRef.current && document.pictureInPictureEnabled) {
      try {
        if (document.pictureInPictureElement) await document.exitPictureInPicture();
        else await videoRef.current.requestPictureInPicture();
      } catch (err) { console.error(err); }
    }
  };

  return (
    <div style={{ background: '#0f172a', minHeight: '100vh', color: 'white', padding: '1.5rem', fontFamily: 'Inter, sans-serif', width: '100vw', margin: '-8px' }}>
      
      <div 
        onClick={togglePiP}
        title="Clique para destacar (PiP)"
        style={{ 
          position: 'fixed', bottom: '2rem', left: '2rem', width: '180px', height: '180px', 
          borderRadius: '50%', overflow: 'hidden', border: '4px solid #10b981', zIndex: 1000, background: '#000',
          boxShadow: '0 10px 40px rgba(0,0,0,0.5)', cursor: 'pointer'
        }}
      >
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', background: 'rgba(16, 185, 129, 0.8)', color: 'white', padding: '2px 8px', borderRadius: '4px', fontSize: '0.5rem', fontWeight: 'bold', zIndex: 10, pointerEvents: 'none' }}>RETORNO</div>
        <video ref={videoRef} autoPlay muted playsInline style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>

      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid #334155', paddingBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <h1 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#38bdf8' }}>NATY PRODUCTION STUDIO</h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'rgba(0,0,0,0.3)', padding: '0.3rem 0.8rem', borderRadius: '20px', border: `1px solid ${studioStatus === 'CONNECTED' ? '#10b981' : '#f43f5e'}` }}>
            <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: studioStatus === 'CONNECTED' ? '#10b981' : '#f43f5e' }}></div>
            <span style={{ fontSize: '0.6rem', fontWeight: 'bold' }}>SISTEMA: {studioStatus}</span>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          
          <div style={{ background: '#1e293b', padding: '0.5rem 1.5rem', borderRadius: '12px', border: '1px solid #334155', fontSize: '1.8rem', fontWeight: 'bold', color: '#10b981', minWidth: '120px', textAlign: 'center' }}>
            {formatTime(timer)}
          </div>
          
          {!isRecording ? (
            <button id="btn-start" onClick={startRecording} className="btn" style={{ width: 'auto', background: '#10b981', padding: '0.8rem 1.5rem', border: 'none', color: '#fff', fontWeight: 'bold', cursor: 'pointer', borderRadius: '8px' }}>⏺ INICIAR GRAVAÇÃO</button>
          ) : (
            <button id="btn-stop" onClick={stopRecordingAndSave} className="btn" style={{ width: 'auto', background: '#ef4444', padding: '0.8rem 1.5rem', border: 'none', color: '#fff', fontWeight: 'bold', cursor: 'pointer', borderRadius: '8px', boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)' }}>
              ⏹ PARAR E SALVAR
            </button>
          )}

          <button 
            id="btn-pause"
            onClick={togglePause} 
            disabled={!isRecording}
            className="btn" 
            style={{ 
              width: 'auto', 
              background: !isRecording ? '#334155' : (isPaused ? '#f59e0b' : '#3b82f6'), 
              padding: '0.8rem 1.5rem', 
              border: 'none', 
              color: !isRecording ? '#94a3b8' : '#fff', 
              fontWeight: 'bold', 
              cursor: !isRecording ? 'not-allowed' : 'pointer', 
              borderRadius: '8px' 
            }}>
            {isPaused ? "▶ RETOMAR" : "⏸ PAUSAR"}
          </button>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '1.5rem' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ maxHeight: '60vh', overflowY: 'auto', paddingRight: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {SCRIPT.map((s, idx) => (
              <div 
                key={idx} onClick={() => changeScene(idx)}
                style={{ 
                  padding: '0.8rem', background: currentScene === idx ? 'linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%)' : '#1e293b', 
                  borderRadius: '8px', cursor: 'pointer', transition: '0.2s', border: currentScene === idx ? '1px solid #7dd3fc' : '1px solid #334155'
                }}
              >
                <h3 style={{ fontSize: '0.8rem', fontWeight: 'bold', margin: '0 0 4px 0' }}>{s.scene}</h3>
                <p style={{ fontSize: '0.6rem', opacity: 0.6, margin: 0 }}>📂 {s.file}</p>
              </div>
            ))}
          </div>

        </div>

        <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '30px', border: '1px solid #334155', boxShadow: '0 20px 50px rgba(0,0,0,0.3)' }}>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
            <div 
              style={{ background: 'rgba(56, 189, 248, 0.1)', padding: '1rem', borderRadius: '15px', border: '2px solid #38bdf8', textAlign: 'left' }}
            >
              <h2 style={{ color: '#38bdf8', fontSize: '0.8rem', textTransform: 'uppercase', margin: '0 0 0.4rem 0' }}>📁 MOSTRAR ARQUIVO:</h2>
              <p style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#fff', margin: 0 }}>{SCRIPT[currentScene].path}</p>
            </div>
            
            <button 
              onClick={() => copyToClipboard(SCRIPT[currentScene].command)}
              style={{ 
                background: SCRIPT[currentScene].command === "Nenhum" ? 'rgba(148, 163, 184, 0.1)' : 'rgba(16, 185, 129, 0.1)', 
                padding: '1rem', borderRadius: '15px', 
                border: SCRIPT[currentScene].command === "Nenhum" ? '2px solid #475569' : '2px solid #10b981', 
                cursor: SCRIPT[currentScene].command === "Nenhum" ? 'not-allowed' : 'pointer', 
                textAlign: 'left', transition: '0.2s', width: '100%', margin: 0
              }}
            >
              <h2 style={{ color: SCRIPT[currentScene].command === "Nenhum" ? '#94a3b8' : '#10b981', fontSize: '0.8rem', textTransform: 'uppercase', margin: '0 0 0.4rem 0' }}>💻 COPIAR COMANDO:</h2>
              <p style={{ fontSize: '1.1rem', fontWeight: 'bold', color: SCRIPT[currentScene].command === "Nenhum" ? '#94a3b8' : '#fff', margin: 0 }}>{SCRIPT[currentScene].command}</p>
            </button>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <h2 style={{ color: '#38bdf8', fontSize: '0.9rem', letterSpacing: '2px', marginBottom: '0.5rem', textTransform: 'uppercase', marginTop: 0 }}>🛠️ PASSO A PASSO TÉCNICO:</h2>
            <p style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#e2e8f0', background: 'rgba(56, 189, 248, 0.1)', padding: '1rem', borderRadius: '12px', borderLeft: '8px solid #38bdf8', margin: 0 }}>
              {SCRIPT[currentScene].step}
            </p>
          </div>

          <div>
            <h2 style={{ color: '#10b981', fontSize: '1rem', letterSpacing: '2px', marginBottom: '0.8rem', textTransform: 'uppercase' }}>🎙️ O QUE FALAR:</h2>
            <p style={{ fontSize: '2.5rem', lineHeight: '1.2', color: '#f8fafc', fontWeight: '600', background: 'rgba(16, 185, 129, 0.05)', padding: '1.5rem', borderRadius: '20px', textShadow: '0 4px 8px rgba(0,0,0,0.5)', textAlign: 'center', margin: 0 }}>
              "{SCRIPT[currentScene].talk}"
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
