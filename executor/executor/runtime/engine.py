from __future__ import annotations

import asyncio
import contextlib
import uuid
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, Optional

from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from tenacity import AsyncRetrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

from shared.dsl import (
    Action,
    ActionProgram,
    ClickAction,
    FillAction,
    NavigateAction,
    TargetBy,
    TargetSpec,
    WaitConditionKind,
    WaitForAction,
)

from executor.models import ExecutionMetrics, ExecutionResult, StepResult


Resolver = Callable[[Page, TargetSpec], Awaitable[Any]]


class ExecutorEngine:
    """High-level executor that runs DSL programs with Playwright."""

    def __init__(self, headless: bool = True, action_timeout: float = 60.0) -> None:
        self._headless = headless
        self._action_timeout = action_timeout
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._metrics = ExecutionMetrics()

    async def __aenter__(self) -> "ExecutorEngine":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.stop()

    async def start(self) -> None:
        """Launch Playwright Chromium and create a fresh page."""

        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=self._headless)
        self._browser = browser
        self._context = await browser.new_context()
        self._page = await self._context.new_page()

    async def stop(self) -> None:
        """Tear down Playwright resources."""

        with contextlib.suppress(Exception):
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()

    async def run_program(self, program: ActionProgram) -> ExecutionResult:
        """Execute a DSL program sequentially."""

        if not self._page:
            msg = "ExecutorEngine must be started before running a program"
            raise RuntimeError(msg)

        step_results: list[StepResult] = []
        for index, action in enumerate(program.steps):
            step_start = datetime.now(tz=timezone.utc)
            try:
                await self._execute_action(self._page, action)
                status = "success"
                error_message = None
            except Exception as exc:  # noqa: BLE001
                status = "failed"
                error_message = str(exc)
            step_finish = datetime.now(tz=timezone.utc)
            step_results.append(
                StepResult(
                    index=index,
                    action=action,
                    status=status,
                    retries=0,
                    started_at=step_start,
                    finished_at=step_finish,
                    artifacts=[],
                    error=error_message,
                )
            )

        overall_status = "success" if all(result.status == "success" for result in step_results) else "failed"
        total_duration = (
            sum((result.finished_at - result.started_at).total_seconds() for result in step_results) * 1000
        )
        self._metrics.total_duration_ms = int(total_duration)

        return ExecutionResult(
            program_id=str(uuid.uuid4()),
            status=overall_status,
            steps=step_results,
            metrics=self._metrics,
        )

    async def _execute_action(self, page: Page, action: Action) -> None:
        """Dispatch an action to its respective handler."""

        if isinstance(action, NavigateAction):
            await page.goto(action.url, wait_until="domcontentloaded", timeout=self._action_timeout * 1000)
            return

        if isinstance(action, ClickAction):
            locator = await self._resolve_target(page, action.target)
            await locator.click(timeout=self._action_timeout * 1000)
            return

        if isinstance(action, FillAction):
            locator = await self._resolve_target(page, action.target)
            await locator.fill(action.value, timeout=self._action_timeout * 1000)
            return

        if isinstance(action, WaitForAction):
            await self._handle_wait_for(page, action)
            return

        msg = f"Action type {action.type} not yet implemented"
        raise NotImplementedError(msg)

    async def _resolve_target(self, page: Page, target: TargetSpec):
        """Resolve a target spec into a Playwright locator."""

        if target.by == TargetBy.ROLE:
            if not target.role:
                msg = "role targeting requires 'role'"
                raise ValueError(msg)
            return page.get_by_role(target.role, name=target.name)

        if target.by == TargetBy.LABEL:
            if not target.name:
                msg = "label targeting requires 'name'"
                raise ValueError(msg)
            return page.get_by_label(target.name)

        if target.by == TargetBy.PLACEHOLDER:
            if not target.placeholder:
                msg = "placeholder targeting requires 'placeholder'"
                raise ValueError(msg)
            return page.get_by_placeholder(target.placeholder)

        if target.by == TargetBy.TEXT:
            if not target.text:
                msg = "text targeting requires 'text'"
                raise ValueError(msg)
            return page.get_by_text(target.text)

        if target.by == TargetBy.CSS:
            if not target.css:
                msg = "css targeting requires 'css'"
                raise ValueError(msg)
            return page.locator(target.css)

        if target.by == TargetBy.XPATH:
            if not target.xpath:
                msg = "xpath targeting requires 'xpath'"
                raise ValueError(msg)
            return page.locator(f"xpath={target.xpath}")

        if target.by == TargetBy.VISION:
            msg = "vision targeting is not implemented in the bootstrap executor"
            raise NotImplementedError(msg)

        msg = f"Unsupported target strategy: {target.by}"
        raise ValueError(msg)

    async def _handle_wait_for(self, page: Page, action: WaitForAction) -> None:
        """Implement wait_for semantics."""

        condition = action.condition
        timeout_ms = self._action_timeout * 1000

        if condition.kind == WaitConditionKind.URL_CONTAINS and condition.value:
            await page.wait_for_url(f"**{condition.value}**", timeout=timeout_ms)
            return

        if condition.kind == WaitConditionKind.TEXT_PRESENT and condition.value:
            await page.wait_for_selector(f"text={condition.value}", timeout=timeout_ms)
            return

        if condition.kind == WaitConditionKind.SELECTOR_VISIBLE and condition.target:
            locator = await self._resolve_target(page, condition.target)

            async def wait_visible() -> None:
                await locator.wait_for(state="visible", timeout=timeout_ms)

            await wait_visible()
            return

        if condition.kind == WaitConditionKind.NETWORK_IDLE:
            await page.wait_for_load_state("networkidle", timeout=timeout_ms)
            return

        msg = f"Unhandled wait condition: {condition.kind}"
        raise NotImplementedError(msg)
