"""Planner that chooses the next web action from page state and goal."""

from __future__ import annotations

from typing import Any, Dict

from ..models.schemas import ActionType, WebAction


class Planner:
    """Reasoning brain: decide next action from distilled state and goal."""

    def __init__(self, risk_threshold: float = 0.8) -> None:
        self.risk_threshold = risk_threshold

    def plan(self, state: Dict[str, Any], goal: Dict[str, Any]) -> WebAction:
        """Return the next WebAction based on state and goal using an LLM stub."""

        missing_info = self._detect_missing_info(state, goal)
        if missing_info:
            return WebAction(
                action_type=ActionType.ASK_USER,
                target_description=missing_info,
                value=None,
                confidence=0.5,
            )

        # Stub risk gating: if risk > threshold, wait
        risk_score = self._estimate_risk(state, goal)
        if risk_score >= self.risk_threshold:
            return WebAction(
                action_type=ActionType.WAIT,
                target_description="High-risk action detected; waiting for safety gate",
                value=None,
                confidence=0.4,
            )

        llm_action = self._call_llm(state, goal)
        return WebAction(**llm_action)

    def _detect_missing_info(self, state: Dict[str, Any], goal: Dict[str, Any]) -> str | None:
        """Placeholder heuristic for missing info detection."""
        if not goal:
            return "Goal is missing or empty"
        return None

    def _estimate_risk(self, state: Dict[str, Any], goal: Dict[str, Any]) -> float:
        """Placeholder risk estimator for safety gating."""
        return 0.0

    def _call_llm(self, state: Dict[str, Any], goal: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder LLM planner; returns a selector-free structured action."""

        # This stub simply defaults to a CLICK on the first button if available; otherwise STOP.
        buttons = state.get("buttons", []) if isinstance(state, dict) else []
        if buttons:
            first_btn = buttons[0]
            return {
                "action_type": ActionType.CLICK,
                "target_description": first_btn.get("text") or "primary button",
                "value": None,
                "confidence": 0.6,
            }

        return {
            "action_type": ActionType.STOP,
            "target_description": "No actions available",
            "value": None,
            "confidence": 0.5,
        }


__all__ = ["Planner"]