"""Pydantic schemas for generic web actions."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
	"""Supported abstract action types for a web agent."""

	CLICK = "CLICK"          # Click a semantically described target
	TYPE = "TYPE"            # Type text into a semantically described target
	WAIT = "WAIT"            # Wait for page changes or conditions
	STOP = "STOP"            # Task complete or halt
	ASK_USER = "ASK_USER"    # Request clarification from user


class WebAction(BaseModel):
	"""Structured, selector-free web action description."""

	action_type: ActionType = Field(..., description="Type of action to perform")
	target_description: str = Field(
		..., description="Human-readable description of the target (no selectors)"
	)
	value: Optional[str] = Field(
		None, description="Optional value (e.g., text to type or wait hint)"
	)
	confidence: float = Field(
		0.0, ge=0.0, le=1.0, description="Model confidence in this action"
	)


__all__ = ["ActionType", "WebAction"]
