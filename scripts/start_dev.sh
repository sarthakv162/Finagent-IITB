#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
playwright install chromium

echo "Starting dummy bank at http://localhost:9000"
python bank_website/server.py &
BANK_PID=$!
trap 'kill "$BANK_PID" 2>/dev/null || true' EXIT

echo "Starting API at http://127.0.0.1:8000"
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000