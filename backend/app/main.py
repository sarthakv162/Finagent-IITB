"""FastAPI application exposing a single endpoint to run the web agent."""

from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agents.planner import Planner
from .agents.safety_interceptor import SafetyInterceptor
from .agents.web_action_agent import WebActionAgent
from .agents.web_executor import WebExecutor


class RunAgentRequest(BaseModel):
	goal: str
	start_url: str
	biller: str | None = None
	amount: float | None = None
	headless: bool = True
	auto_confirm: bool = False


app = FastAPI(title="Web Action Agent API", version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, str]:
	"""Health check endpoint."""
	return {"status": "ok", "message": "Web Action Agent API running"}


@app.post("/run-agent")
async def run_agent(req: RunAgentRequest) -> Dict[str, Any]:
    """Instantiate and run the web agent for the provided goal and URL."""

    print(
        f"[api] Received request: goal='{req.goal}', start_url='{req.start_url}', "
        f"biller='{req.biller}', amount='{req.amount}', headless={req.headless}, auto_confirm={req.auto_confirm}"
    )

    planner = Planner()
    executor = WebExecutor(headless=req.headless)
    safety = SafetyInterceptor()
    agent = WebActionAgent(
		start_url=req.start_url,
		planner=planner,
		executor=executor,
		safety=safety,
		max_steps=30,
	)

    goal_payload: Dict[str, Any] = {
        "goal": req.goal,
        "biller": req.biller,
        "amount": req.amount,
        "headless": req.headless,
        "auto_confirm": req.auto_confirm,
    }

    try:
		result = await agent.run(goal_payload)
		print(f"[api] Agent finished with status: {result.get('status')}")
		return {"status": result.get("status"), "result": result}
    except Exception as exc:  # pylint: disable=broad-except
		import traceback
		print(f"[api] Agent failed: {exc}")
		print(f"[api] Traceback: {traceback.format_exc()}")
		raise HTTPException(status_code=500, detail=str(exc)) from exc
