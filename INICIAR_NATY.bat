@echo off
title INICIANDO NATY E PROTOCOLO WEB3

echo [1/3] Iniciando o servidor do Frontend Web3...
cd web3_protocol\frontend
start "Frontend NatyWeb3" cmd /c "npm run dev"
cd ..\..

echo [2/3] Aguardando o servidor iniciar e abrindo o navegador...
timeout /t 3 >nul
start http://localhost:5173/
start http://localhost:5173/studio

:: Passo 3 removido para usar a Assistente Principal na apresentação

echo ==================================================
echo TUDO PRONTO! Iniciando a Assistente Principal...
echo ==================================================
python main.py
pause
