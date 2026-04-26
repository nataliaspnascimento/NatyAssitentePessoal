@echo off
title ENCERRANDO SISTEMAS...
echo ==========================================
echo    🛑 FORCANDO FINALIZACAO DA NATY...
echo ==========================================

:: 1. Fecha o Python e qualquer janela de terminal que esteja rodando a Naty
echo [!] Finalizando processos...
taskkill /F /IM python.exe /T 2>NUL
taskkill /F /FI "WINDOWTITLE eq INICIANDO ASSISTENTE NATY*" /T 2>NUL

:: 2. Limpa o terminal
echo [OK] Sistemas encerrados.
timeout /t 2
exit
