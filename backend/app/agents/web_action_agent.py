"""WebActionAgent: orchestrates observe/plan/safety/execute loop."""

from __future__ import annotations

from typing import Any, Dict

import re

from ..models.schemas import ActionType, WebAction
from ..utils.dom_distiller import distill_dom
from .base_agent import BaseWebAgent
from .planner import Planner
from .safety_interceptor import SafetyInterceptor, SafetyResult
from .web_executor import WebExecutor


class WebActionAgent(BaseWebAgent):
    """Generic agent that plans and executes abstract actions on the web."""

    def __init__(
        self,
        start_url: str,
        planner: Planner,
        executor: WebExecutor,
        safety: SafetyInterceptor,
        max_steps: int = 50,
    ) -> None:
        super().__init__(page=None, max_steps=max_steps)
        self.start_url = start_url
        self.planner = planner
        self.executor = executor
        self.safety = safety

    async def observe(self, page: Any) -> Dict[str, Any]:
        html = await page.content()
        return distill_dom(html)

    def decide(self, state: Dict[str, Any], goal: Dict[str, Any]) -> WebAction:
        return self.planner.plan(state, goal)

    async def act(self, page: Any, action: WebAction) -> Dict[str, Any]:
        return await self.executor.execute(action)

    async def run(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Async observe → (safety-gated) act loop with a conscious pause."""

        # Allow callers to override headless mode per request
        if isinstance(goal, dict) and "headless" in goal:
            self.executor.headless = bool(goal.get("headless"))

        await self.executor.start()
        self.page = self.executor.page
        await self.executor.goto(self.start_url)

        state = await self.observe(self.page)

        biller_value = goal.get("biller") or goal.get("biller_name")
        amount_value = goal.get("amount")

        if (biller_value is None or amount_value in (None, "")) and isinstance(goal.get("goal"), str):
            parsed = self._parse_intent(goal["goal"])
            biller_value = biller_value or parsed.get("biller")
            amount_value = amount_value if amount_value not in (None, "") else parsed.get("amount")
        missing: list[str] = []
        if not biller_value:
            missing.append("biller")
        if amount_value in (None, ""):
            missing.append("amount")
        if missing:
            await self.executor.stop()
            return {
                "status": "needs_input",
                "missing": missing,
                "state": state,
            }

        # Build a deterministic script for the dummy bank page
        script = [
            WebAction(action_type=ActionType.TYPE, target_description="Biller Name", value=str(biller_value), confidence=0.9),
            WebAction(action_type=ActionType.TYPE, target_description="Amount", value=str(amount_value), confidence=0.9),
            WebAction(action_type=ActionType.CLICK, target_description="Pay Now", value=None, confidence=0.9),
        ]

        auto_confirm = bool(goal.get("auto_confirm", False))

        try:
            for step, action in enumerate(script):
                safety_status = self.safety.evaluate(action)
                if safety_status == SafetyResult.REQUIRES_CONFIRMATION and not auto_confirm:
                    return {
                        "status": "needs_confirmation",
                        "pending_action": action.model_dump(),
                        "state": state,
                        "step": step,
                    }

                result = await self.act(self.page, action)
                state = await self.observe(self.page)

                error_message = self._extract_error(state)
                if error_message:
                    return {
                        "status": "needs_correction",
                        "error": error_message,
                        "state": state,
                        "step": step,
                    }

                if self._is_success(state):
                    return {
                        "status": "success",
                        "steps": step + 1,
                        "state": state,
                        "result": result,
                    }

            return {
                "status": "executed_script",
                "steps": len(script),
                "state": state,
            }
        finally:
            await self.executor.stop()

    @staticmethod
    def _extract_error(state: Dict[str, Any]) -> str | None:
        messages = state.get("messages", []) if isinstance(state, dict) else []
        for msg in messages:
            if msg.get("kind") == "error" or "error" in (msg.get("text", "").lower()):
                return msg.get("text") or "Unknown error"
        return None

    @staticmethod
    def _is_success(state: Dict[str, Any]) -> bool:
        messages = state.get("messages", []) if isinstance(state, dict) else []
        return any(
            msg.get("kind") == "success" or "success" in (msg.get("text", "").lower())
            for msg in messages
        )

    @staticmethod
    def _parse_intent(text: str) -> Dict[str, Any]:
        """Heuristic parser to pull biller name and amount from NL command."""
        result: Dict[str, Any] = {}

        amount_match = re.search(r"(?:₹|rs\.?|inr)?\s*([0-9]+(?:\.[0-9]+)?)", text, flags=re.IGNORECASE)
        if amount_match:
            try:
                result["amount"] = float(amount_match.group(1))
            except ValueError:
                pass

        # naive biller extraction: take text after "to" or "for" up to amount/verb
        lowered = text.lower()
        tokens = re.split(r"\s+", text)
        biller = None

        to_idx = lowered.find(" to ")
        if to_idx != -1:
            segment = text[to_idx + 4 :]
            biller = segment
        elif "pay" in lowered:
            pay_idx = lowered.find("pay")
            biller = text[pay_idx + 3 :]

        if biller:
            # strip trailing amount substring if present
            if amount_match:
                biller = biller.replace(amount_match.group(0), "")
            biller = biller.replace("bill", "").strip(" ,.-")
            if biller:
                result["biller"] = biller

        return result


__all__ = ["WebActionAgent"]