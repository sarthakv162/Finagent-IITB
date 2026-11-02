"""FastAPI application exposing the browser-agent API."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .agents.planner import Planner
from .agents.safety_interceptor import SafetyInterceptor
from .agents.web_action_agent import WebActionAgent
from .agents.web_executor import WebExecutor

logger = logging.getLogger(__name__)


class RunAgentRequest(BaseModel):
    """Input contract for a single browser-agent run."""

    goal: str = Field(min_length=1, description="Task to perform on the target page")
    start_url: str = Field(min_length=1, description="URL of the page to open")
    biller: str | None = None
    amount: float | None = Field(default=None, gt=0)
    headless: bool = True
    auto_confirm: bool = False


app = FastAPI(
    title="FinAgent Browser Action API",
    description="Prototype API for safety-gated browser automation against test websites.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000", "http://127.0.0.1:9000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Return a simple API health check."""
    return {"status": "ok", "message": "FinAgent API is running"}


@app.post("/run-agent")
async def run_agent(req: RunAgentRequest) -> dict[str, Any]:
    """Run the browser agent against the supplied test page."""
    logger.info("Received browser task for URL: %s", req.start_url)

    try:
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
        goal_payload = {
            "goal": req.goal,
            "biller": req.biller,
            "amount": req.amount,
            "headless": req.headless,
            "auto_confirm": req.auto_confirm,
        }
        result = await agent.run(goal_payload)
        logger.info("Agent completed with status: %s", result.get("status"))
        return {"status": result.get("status"), "result": result}
    except Exception as exc:
        logger.exception("Browser-agent execution failed")
        raise HTTPException(status_code=500, detail="Agent execution failed") from exc