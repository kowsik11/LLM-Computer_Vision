from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from shared.dsl import (
    ActionProgram,
    NavigateAction,
    TargetBy,
    TargetSpec,
    WaitCondition,
    WaitConditionKind,
    WaitForAction,
)


@dataclass
class PlannerOptions:
    """Configuration for the planner client."""

    provider: str = "heuristic"
    model: Optional[str] = None


class PlannerClient:
    """Planner client capable of backing off to deterministic heuristics."""

    def __init__(self, options: PlannerOptions | None = None) -> None:
        self._options = options or PlannerOptions()

    async def plan(
        self,
        goal: str,
        site_policy: List[str],
        secrets: Dict[str, str] | None = None,
        demo_trace_id: Optional[str] = None,
    ) -> ActionProgram:
        """Return a DSL program for a given goal."""

        del secrets, demo_trace_id  # Placeholder until advanced planner wired in.
        if not site_policy:
            msg = "site_policy must include at least one domain"
            raise ValueError(msg)

        base_url = site_policy[0].rstrip("/")
        steps = [
            NavigateAction(type="navigate", url=base_url),
            WaitForAction(
                type="wait_for",
                condition=WaitCondition(kind=WaitConditionKind.URL_CONTAINS, value="/"),
            ),
        ]

        if "download" in goal.lower():
            steps.append(
                WaitForAction(
                    type="wait_for",
                    condition=WaitCondition(
                        kind=WaitConditionKind.SELECTOR_VISIBLE,
                        target=TargetSpec(by=TargetBy.TEXT, text="Download"),
                    ),
                )
            )

        return ActionProgram(steps=steps)

    async def repair(
        self,
        failing_step: int,
        diagnostics: Dict[str, str],
        current_program: ActionProgram,
    ) -> list[dict]:
        """Return a minimal diff patch."""

        del failing_step, diagnostics, current_program
        patch: list[dict] = [
            {
                "op": "add",
                "path": "/steps/-",
                "value": {"type": "wait_for", "condition": {"kind": "network_idle"}},
            }
        ]
        return patch


async def _demo() -> None:
    """Quick CLI demo for manual testing."""

    client = PlannerClient()
    program = await client.plan(
        goal="Open the dashboard",
        site_policy=["https://example.com"],
    )
    print(program.model_dump_json(indent=2))


if __name__ == "__main__":
    import asyncio

    asyncio.run(_demo())

