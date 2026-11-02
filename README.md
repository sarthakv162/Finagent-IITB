# FinAgent — Browser Action Agent

<p align="center">
  <strong>Turning natural-language goals into browser actions.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Playwright-Browser%20Automation-2EAD33?logo=playwright&logoColor=white" />
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white" />
</p>

FinAgent is a browser automation system that translates high-level user goals into structured web interactions. Built with **Python, FastAPI, and Playwright**, it combines page observation, DOM distillation, action planning, and confirmation-aware execution in a modular agent architecture.

With its included banking workflow environment, FinAgent provides an end-to-end example of automating multi-step web tasks through a simple API.

## Highlights

- **Natural-language task interface** — submit browser goals through a clean REST API.
- **Browser automation** — navigate pages and interact with web elements using Playwright.
- **DOM intelligence** — distill page structure into compact, actionable state.
- **Agent architecture** — separate planning, observation, safety evaluation, and execution modules.
- **Action confirmation** — introduce a confirmation step before selected sensitive actions.
- **Banking workflow demo** — explore a complete bill-payment interaction in the included web environment.
- **Developer-ready API** — interactive Swagger documentation and straightforward local setup.

## How it works

```text
         Natural-language goal
                  |
                  v
           FastAPI endpoint
                  |
                  v
             WebActionAgent
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Observe     Planner     Safety
       |          |          |
       +----------+----------+
                  |
                  v
             WebExecutor
                  |
                  v
           Playwright Browser
                  |
                  v
          Banking Web Environment
```

## Technology stack

| Layer | Technology |
| --- | --- |
| Backend API | FastAPI, Pydantic |
| Language | Python |
| Browser automation | Playwright |
| DOM processing | BeautifulSoup |
| Testing | Pytest, FastAPI TestClient |
| CI | GitHub Actions |

## Project structure

```text
Finagent-IITB/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── base_agent.py
│   │   │   ├── planner.py
│   │   │   ├── safety_interceptor.py
│   │   │   ├── web_action_agent.py
│   │   │   └── web_executor.py
│   │   ├── models/schemas.py
│   │   ├── utils/dom_distiller.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── bank_website/
│   ├── static/
│   ├── index.html
│   └── server.py
├── docs/
│   ├── API.md
│   └── ARCHITECTURE.md
├── scripts/
│   ├── start_dev.sh
│   └── start_dev.bat
└── README.md
```

## Getting started

### Prerequisites

- Python 3.10+
- pip
- Playwright Chromium

### 1. Clone the repository

```bash
git clone https://github.com/sarthakv162/Finagent-IITB.git
cd Finagent-IITB
```

### 2. Set up the environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r backend/requirements.txt
playwright install chromium
```

### 3. Launch FinAgent

Start the local banking website:

```bash
python bank_website/server.py
```

Start the API in another terminal:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Or launch both services together:

```bash
# Linux / macOS
bash scripts/start_dev.sh

# Windows Command Prompt
scripts\start_dev.bat
```

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API health check |
| `POST` | `/run-agent` | Execute a browser task |

Interactive API documentation is available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI schema: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### Example request

```bash
curl -X POST "http://127.0.0.1:8000/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Pay electricity bill to Demo Power for 250",
    "start_url": "http://127.0.0.1:9000/",
    "biller": "Demo Power",
    "amount": 250,
    "headless": false,
    "auto_confirm": false
  }'
```

See [docs/API.md](docs/API.md) for request fields and response statuses.

## Run tests

```bash
pytest backend/tests -q
```

GitHub Actions runs the test suite automatically for pushes and pull requests to `main`.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API reference](docs/API.md)

## License

No license file is currently included.