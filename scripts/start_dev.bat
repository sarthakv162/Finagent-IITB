@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv" (
    py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
playwright install chromium

echo Starting dummy bank at http://localhost:9000
start "FinAgent Dummy Bank" cmd /k python bank_website\server.py
echo Starting API at http://127.0.0.1:8000
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000