from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from shared.dsl import ActionProgram


class PlanRequest(BaseModel):
    """Request payload to generate a fresh DSL plan."""

    model_config = ConfigDict(extra="forbid")

    goal: str = Field(..., description="Natural language objective.")
    site_policy: List[str] = Field(..., description="Allowed base domains.")
    secrets: Dict[str, str] | None = Field(default=None, description="Available secret keys.")
    demo_trace_id: Optional[str] = Field(default=None, description="Optional trace to imitate.")


class PlanResponse(BaseModel):
    """Response carrying a new plan and schema."""

    model_config = ConfigDict(extra="forbid")

    program: ActionProgram
    schema: dict


class RepairRequest(BaseModel):
    """Planner repair payload."""

    model_config = ConfigDict(extra="forbid")

    failing_step: int = Field(..., ge=0)
    diagnostics: Dict[str, str] = Field(default_factory=dict)
    current_program: ActionProgram


class RepairResponse(BaseModel):
    """Planner repair response containing a minimal diff."""

    model_config = ConfigDict(extra="forbid")

    patch: List[dict]

