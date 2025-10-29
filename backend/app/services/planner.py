from __future__ import annotations

from urllib.parse import urlparse

from shared.dsl import (
    ActionProgram,
    NavigateAction,
    TargetSpec,
    TargetBy,
    WaitCondition,
    WaitConditionKind,
    WaitForAction,
)

from app.schemas.planner import PlanRequest, RepairRequest


def build_default_plan(payload: PlanRequest) -> ActionProgram:
    """Generate a deterministic starter program for a given goal."""

    if not payload.site_policy:
        msg = "site_policy must contain at least one allowed domain"
        raise ValueError(msg)

    base_url = payload.site_policy[0].rstrip("/")
    parsed = urlparse(base_url)
    path_fragment = parsed.path or "/"

    steps = [
        NavigateAction(type="navigate", url=base_url),
        WaitForAction(
            type="wait_for",
            condition=WaitCondition(
                kind=WaitConditionKind.URL_CONTAINS,
                value=path_fragment,
            ),
        ),
    ]

    # When a login goal is detected, scaffold a generic credential fill sequence.
    lowered_goal = payload.goal.lower()
    if "login" in lowered_goal or "sign in" in lowered_goal:
        steps.extend(
            [
                WaitForAction(
                    type="wait_for",
                    condition=WaitCondition(
                        kind=WaitConditionKind.SELECTOR_VISIBLE,
                        target=TargetSpec(by=TargetBy.LABEL, name="Email"),
                    ),
                ),
            ]
        )

    return ActionProgram(steps=steps)


def build_repair_patch(payload: RepairRequest) -> list[dict]:
    """Return a placeholder minimal diff for failing programs."""

    # For the bootstrap version we simply nudge the planner to add a wait step.
    patch: list[dict] = [
        {
            "op": "add",
            "path": "/steps/-",
            "value": {
                "type": "wait_for",
                "condition": {"kind": "network_idle"},
            },
        }
    ]
    return patch

