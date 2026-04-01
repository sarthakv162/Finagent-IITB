"""Abstract base web action agent interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseWebAgent(ABC):
	"""Generic web action agent that observes, decides, and acts."""

	def __init__(self, page: Any, max_steps: int = 50) -> None:
		self.page = page
		self.max_steps = max_steps

	@abstractmethod
	def observe(self, page: Any) -> Dict[str, Any]:
		"""Return a distilled representation of the current page state."""

	@abstractmethod
	def decide(self, state: Dict[str, Any], goal: Dict[str, Any]) -> Dict[str, Any]:
		"""Return the next structured action dictionary to move toward the goal."""

	@abstractmethod
	def act(self, page: Any, action: Dict[str, Any]) -> Dict[str, Any]:
		"""Execute the action on the page and return an outcome dictionary."""

	def run(self, goal: Dict[str, Any]) -> Dict[str, Any]:
		"""Main loop: observe -> decide -> act until success, failure, or max steps."""

		if self.page is None:
			raise ValueError("Page is not initialized")

		page = self.page
		state = self.observe(page)

		for step in range(self.max_steps):
			action = self.decide(state, goal)
			if not isinstance(action, dict):
				raise TypeError("decide must return a dictionary action")

			result = self.act(page, action)
			if not isinstance(result, dict):
				raise TypeError("act must return a dictionary result")

			if result.get("error"):
				return {
					"status": "error",
					"step": step,
					"state": state,
					"action": action,
					"result": result,
				}

			if result.get("done"):
				return {
					"status": "success",
					"step": step,
					"state": state,
					"action": action,
					"result": result,
				}

			state = self.observe(page)

		return {
			"status": "max_steps_exceeded",
			"steps": self.max_steps,
			"state": state,
		}
