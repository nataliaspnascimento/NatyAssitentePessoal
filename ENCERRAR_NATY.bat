@echo off
title ENCERRANDO SISTEMAS...
echo ==========================================
echo    🛑 FORCANDO FINALIZACAO DA NATY...
echo ==========================================

:: 1. Fecha o Python e qualquer janela de terminal que esteja rodando a Naty ou Web3
echo [!] Finalizando processos Python (Assistentes)...
taskkill /F /IM python.exe /T 2>NUL
taskkill /F /FI "WINDOWTITLE eq INICIANDO NATY*" /T 2>NUL
taskkill /F /FI "WINDOWTITLE eq Naty Apresentadora Web3*" /T 2>NUL

echo [!] Finalizando processos Node (Frontend Web3)...
taskkill /F /IM node.exe /T 2>NUL
taskkill /F /FI "WINDOWTITLE eq Frontend NatyWeb3*" /T 2>NUL

:: 2. Limpa o terminal
echo [OK] Todos os sistemas e o protocolo Web3 foram encerrados.
timeout /t 2
exit
