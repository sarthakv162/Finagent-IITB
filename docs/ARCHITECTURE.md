# FinAgent Architecture

FinAgent follows a modular agent architecture that separates API orchestration, page observation, action planning, safety evaluation, and browser execution.

## System overview

```text
Client
  |
  | POST /run-agent
  v
FastAPI application
  |
  v
WebActionAgent
  |
  +---- DOM Observer / Distiller
  |
  +---- Planner
  |
  +---- Safety Interceptor
  |
  v
WebExecutor
  |
  v
Playwright
  |
  v
Target website
```

## Core modules

| Module | Responsibility |
| --- | --- |
| `app/main.py` | Exposes the FastAPI endpoints and coordinates agent requests. |
| `agents/base_agent.py` | Defines shared agent structure and behavior. |
| `agents/web_action_agent.py` | Coordinates page observation, task flow, and browser actions. |
| `agents/planner.py` | Handles task planning and action selection. |
| `agents/safety_interceptor.py` | Evaluates actions and applies confirmation requirements. |
| `agents/web_executor.py` | Performs browser navigation and interactions through Playwright. |
| `models/schemas.py` | Defines typed action and execution data models. |
| `utils/dom_distiller.py` | Converts raw HTML into a compact representation of page controls and messages. |

## Request lifecycle

1. A client submits a goal and target URL to `POST /run-agent`.
2. FastAPI validates the request and initializes the agent components.
3. The agent opens the target page through Playwright.
4. The DOM distiller extracts relevant page controls, labels, links, and status messages.
5. The agent determines the next browser actions for the requested workflow.
6. The safety interceptor evaluates actions and identifies actions requiring confirmation.
7. The executor carries out approved browser interactions.
8. The API returns the final execution status and result.

## Included workflow environment

The `bank_website/` directory contains the browser interface used by the included bill-payment workflow. It can be launched locally and used as the target page when testing the API.

## Extending the agent

The modular structure makes it straightforward to add new task planners, page-understanding strategies, action types, confirmation policies, and website workflows.