"""Centralized Playwright browser lifecycle management."""

from __future__ import annotations

from typing import Optional

from playwright.async_api import Browser, BrowserContext, Page, async_playwright


class BrowserService:
	"""Owns Playwright startup/teardown and dispenses pages to agents."""

	def __init__(self, headless: bool = True, browser_type: str = "chromium", timeout_ms: int = 10000) -> None:
		self.headless = headless
		self.browser_type = browser_type
		self.timeout_ms = timeout_ms
		self._pw = None
		self.browser: Optional[Browser] = None
		self.context: Optional[BrowserContext] = None

	async def start(self) -> None:
		if self.browser:
			return
		self._pw = await async_playwright().start()
		launcher = getattr(self._pw, self.browser_type)
		self.browser = await launcher.launch(headless=self.headless)
		self.context = await self.browser.new_context()
		print(f"[browser_service] Started {self.browser_type} (headless={self.headless})")

	async def stop(self) -> None:
		if self.context:
			await self.context.close()
			self.context = None
		if self.browser:
			await self.browser.close()
			self.browser = None
		if self._pw:
			await self._pw.stop()
			self._pw = None
		print("[browser_service] Stopped")

	async def get_page(self) -> Page:
		"""Return a fresh page from the shared context (requires start first)."""
		if not self.context:
			raise RuntimeError("BrowserService not started; call start() first")
		page = await self.context.new_page()
		page.set_default_timeout(self.timeout_ms)
		return page

	async def __aenter__(self) -> "BrowserService":
		await self.start()
		return self

	async def __aexit__(self, exc_type, exc, tb) -> None:
		await self.stop()


__all__ = ["BrowserService"]
