@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === PECONHA+ ===
if not exist .venv (
  echo Criando ambiente virtual...
  python -m venv .venv || (echo Python nao encontrado. Instale em python.org e marque "Add to PATH". & pause & exit /b 1)
)
call .venv\Scripts\activate.bat
echo Instalando dependencias...
pip install -q -r requirements.txt
echo.
echo Abrindo http://localhost:5000  (Ctrl+C para parar)
start "" http://localhost:5000
python run.py
pause
