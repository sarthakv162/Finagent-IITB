# FinAgent — Browser Action Agent

<p align="center"><strong>A safety-gated browser automation prototype for structured web workflows.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/Browser-Playwright-2EAD33?logo=playwright" />
  <img src="https://img.shields.io/badge/Status-Prototype-orange" />
</p>

FinAgent is an experimental browser-action agent that accepts a high-level task, opens a target website with Playwright, and executes structured browser actions. The repository includes a local **dummy banking website** so the workflow can be explored without interacting with a real financial institution.

> **Safety notice:** This is a prototype and learning/research project. The included bank is a simulation; no real payment or bank transfer is performed. Do not point the agent at real banking, payment, or other sensitive websites, and do not enter real credentials or financial information.

## Features

- FastAPI HTTP interface for submitting browser tasks.
- Asynchronous browser automation using Playwright.
- Structured action model for typing, clicking, waiting, and stopping.
- Lightweight safety interceptor that can pause before sensitive-looking actions.
- DOM distillation to convert page HTML into compact state information.
- Local dummy bank website for repeatable demonstrations.

## Architecture

```text
Client
  | POST /run-agent
  v
FastAPI (backend/app/main.py)
  v
WebActionAgent
  |-- Observe: DOM distillation
  |-- Plan: Planner
  |-- Safety: SafetyInterceptor
  |-- Act: WebExecutor
  v
Playwright browser
  v
Local dummy bank website (bank_website/)
```

The current demo flow extracts a biller and amount from the request (or accepts them as explicit fields), fills the dummy bank form, and pauses before the simulated payment click unless confirmation is enabled. The general-purpose planner's LLM integration is currently a stub; this is not a production autonomous banking system.

## Project structure

| Path | Purpose |
| --- | --- |
| `backend/app/main.py` | FastAPI app and `/run-agent` endpoint |
| `backend/app/agents/` | Agent loop, planner, safety interceptor, and Playwright executor |
| `backend/app/models/schemas.py` | Typed action models |
| `backend/app/utils/dom_distiller.py` | HTML-to-state distillation |
| `backend/app/services/browser_service.py` | Reusable browser lifecycle helper |
| `backend/requirements.txt` | Python dependencies |
| `backend/.env.example` | Example local settings |
| `bank_website/` | Dummy bank UI served locally |
| `docs/ARCHITECTURE.md` | Component responsibilities and execution flow |
| `docs/API.md` | API contract and example requests |
| `scripts/` | Development launch helpers |

## Requirements

- Python 3.10 or newer
- pip
- Playwright Chromium

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/sarthakv162/Finagent-IITB.git
cd Finagent-IITB
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
playwright install chromium
```

### 2. Start the dummy bank

In a terminal at the repository root:

```bash
python bank_website/server.py
```

The demo site is served at [http://localhost:9000](http://localhost:9000).

### 3. Start the API

In a second terminal with the virtual environment active:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Example request

The example below targets only the local dummy website:

```bash
curl -X POST "http://127.0.0.1:8000/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Pay electricity bill to Demo Power for 250",
    "start_url": "http://localhost:9000/",
    "biller": "Demo Power",
    "amount": 250,
    "headless": false,
    "auto_confirm": false
  }'
```

With `auto_confirm` set to `false`, the agent returns `needs_confirmation` before clicking **Pay Now**. Setting it to `true` permits the simulated click to proceed. The dummy website displays a simulated success message; it does not move money.

See [API documentation](docs/API.md) for the request and response contract.

## Current limitations

- The general-purpose planner's LLM call is a placeholder heuristic, not a connected language model.
- The implemented payment demonstration is a deterministic script against the included dummy website.
- The safety interceptor is a lightweight keyword check, not a complete policy or authorization system.
- The dummy bank simulates payment success in client-side JavaScript; it has no banking, UPI, or payment-gateway integration.
- Authentication, persistent sessions, production observability, and comprehensive automated tests are not implemented.

## Development

Run the API and demo server in separate terminals as shown above. Contributions that improve planner reasoning, robust element grounding, safety checks, test coverage, and documentation are welcome.

## License

No license has been added yet. Until a license is provided, standard copyright restrictions apply; contact the repository owner before reusing the code.