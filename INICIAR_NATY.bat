@echo off
title INICIANDO ASSISTENTE NATY
echo ==========================================
echo    INICIANDO SISTEMAS DA NATY...
echo ==========================================

:: 1. Tenta iniciar o Ollama apenas com verificacoes de existencia
C:\Windows\System32\tasklist.exe /FI "IMAGENAME eq ollama.exe" 2>NUL | C:\Windows\System32\find.exe /I "ollama.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama ja esta em execucao.
) else (
    echo [!] Verificando instalacao do Ollama...
    
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" (
        echo [!] Iniciando Ollama pelo caminho padrao...
        start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
        C:\Windows\System32\timeout.exe /t 5 >nul
    ) else (
        :: Se nao achou no caminho padrao, verifica se esta no PATH antes de tentar 'start'
        where ollama >nul 2>nul
        if "%ERRORLEVEL%"=="0" (
            echo [!] Iniciando Ollama via comando de sistema...
            start "" "ollama"
            C:\Windows\System32\timeout.exe /t 5 >nul
        ) else (
            echo [AVISO] Ollama nao encontrado. Inicie manualmente para usar a IA.
        )
    )
)

:: 2. Inicia a Assistente Naty
echo [!] Iniciando HUD e Voz...
python main.py

pause
