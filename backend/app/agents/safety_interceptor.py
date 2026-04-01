"""SafetyInterceptor to flag risky actions before execution."""

from __future__ import annotations

from typing import Iterable

from ..models.schemas import ActionType, WebAction


class SafetyResult:
    SAFE = "SAFE"
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION"


class SafetyInterceptor:
    """Lightweight heuristic safety checker for planned actions."""

    def __init__(self, risky_keywords: Iterable[str] | None = None) -> None:
        self.risky_keywords = [
            "pay",
            "submit",
            "confirm",
            "transfer",
        ] if risky_keywords is None else list(risky_keywords)

    def evaluate(self, action: WebAction) -> str:
        """Return SAFE or REQUIRES_CONFIRMATION based on heuristics."""
        if action.action_type == ActionType.CLICK:
            target = (action.target_description or "").lower()
            if any(keyword in target for keyword in self.risky_keywords):
                return SafetyResult.REQUIRES_CONFIRMATION
        return SafetyResult.SAFE


__all__ = ["SafetyInterceptor", "SafetyResult"]