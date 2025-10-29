from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from shared.dsl import Action


class ExecutionArtifact(BaseModel):
    """Metadata describing a generated artifact (screenshot, DOM snippet, etc.)."""

    model_config = ConfigDict(extra="forbid")

    kind: str
    path: str
    sha1: Optional[str] = None
    metadata: dict = Field(default_factory=dict)


class StepResult(BaseModel):
    """Outcome of executing a single DSL step."""

    model_config = ConfigDict(extra="forbid")

    index: int
    action: Action
    status: str
    retries: int = 0
    started_at: datetime
    finished_at: datetime
    artifacts: List[ExecutionArtifact] = Field(default_factory=list)
    error: Optional[str] = None


class ExecutionMetrics(BaseModel):
    """Aggregated metrics produced by the executor."""

    model_config = ConfigDict(extra="forbid")

    vision_calls: int = 0
    total_duration_ms: int = 0
    resolver_breakdown: dict = Field(default_factory=dict)


class ExecutionResult(BaseModel):
    """Complete executor output."""

    model_config = ConfigDict(extra="forbid")

    program_id: str
    status: str
    steps: List[StepResult] = Field(default_factory=list)
    metrics: ExecutionMetrics = Field(default_factory=ExecutionMetrics)

