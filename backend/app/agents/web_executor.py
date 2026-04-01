"""Generic WebExecutor that executes abstract actions via Playwright."""

from __future__ import annotations

from typing import Any, Dict, Optional

from playwright.async_api import Browser, BrowserContext, Locator, Page, async_playwright

from ..models.schemas import ActionType, WebAction


class WebExecutor:
    """Launch browser, navigate, and execute abstract actions with heuristics."""

    def __init__(self, headless: bool = True, timeout_ms: int = 10000, browser_type: str = "chromium") -> None:
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.browser_type = browser_type
        self._pw = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def start(self) -> None:
        self._pw = await async_playwright().start()
        launcher = getattr(self._pw, self.browser_type)
        self.browser = await launcher.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        self.page.set_default_timeout(self.timeout_ms)
        print(f"[executor] Browser started ({self.browser_type}, headless={self.headless})")

    async def stop(self) -> None:
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._pw:
            await self._pw.stop()
        print("[executor] Browser stopped")

    async def goto(self, url: str) -> None:
        page = self._ensure_page()
        print(f"[executor] Navigating to {url}")
        await page.goto(url, wait_until="domcontentloaded")

    async def execute(self, action: WebAction) -> Dict[str, Any]:
        page = self._ensure_page()
        print(f"[executor] Executing action: {action.action_type} -> {action.target_description}")

        if action.action_type == ActionType.CLICK:
            locator = await self._find_click_target(page, action.target_description)
            await locator.click()
            return {"status": "ok", "action": action}

        if action.action_type == ActionType.TYPE:
            if action.value is None:
                raise ValueError("TYPE action requires a value to type")
            locator = await self._find_input_target(page, action.target_description)
            await locator.fill(str(action.value))
            return {"status": "ok", "action": action}

        if action.action_type == ActionType.WAIT:
            delay_ms = int(float(action.value)) if action.value is not None else 1000
            print(f"[executor] Waiting {delay_ms} ms")
            await page.wait_for_timeout(delay_ms)
            return {"status": "ok", "action": action}

        if action.action_type in {ActionType.STOP, ActionType.ASK_USER}:
            print("[executor] No-op action; returning control to planner")
            return {"status": "noop", "action": action}

        raise ValueError(f"Unsupported action type: {action.action_type}")

    async def _find_click_target(self, page: Page, description: str) -> Locator:
        # Heuristic: role-based match first, then text match on button-like elements
        role_locator = page.get_by_role("button", name=description, exact=False)
        if await role_locator.count() > 0:
            return role_locator.first

        text_locator = page.locator("button", has_text=description)
        if await text_locator.count() > 0:
            return text_locator.first

        submit_locator = page.locator("input[type='submit']", has_text=description)
        if await submit_locator.count() > 0:
            return submit_locator.first

        # Try links with the description text
        link_locator = page.get_by_role("link", name=description, exact=False)
        if await link_locator.count() > 0:
            return link_locator.first

        # Fallback: any element with matching text
        any_locator = page.locator(f":has-text('{description}')")
        if await any_locator.count() > 0:
            return any_locator.first

        raise RuntimeError(f"Could not find clickable element for description: {description}")

    async def _find_input_target(self, page: Page, description: str) -> Locator:
        # Prefer labels, then placeholders, then role-based textboxes
        label_locator = page.get_by_label(description, exact=False)
        if await label_locator.count() > 0:
            return label_locator.first

        placeholder_locator = page.get_by_placeholder(description, exact=False)
        if await placeholder_locator.count() > 0:
            return placeholder_locator.first

        textbox_locator = page.get_by_role("textbox", name=description, exact=False)
        if await textbox_locator.count() > 0:
            return textbox_locator.first

        # Fallback: input elements containing the description in placeholder
        css_locator = page.locator(f"input[placeholder*='{description}']")
        if await css_locator.count() > 0:
            return css_locator.first

        raise RuntimeError(f"Could not find input element for description: {description}")

    def _ensure_page(self) -> Page:
        if not self.page:
            raise RuntimeError("Executor not started; call start() first")
        return self.page


__all__ = ["WebExecutor"]