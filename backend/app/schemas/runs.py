from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from shared.dsl import Action


class StepArtifact(BaseModel):
    """Artifact metadata associated with a run step."""

    model_config = ConfigDict(extra="forbid")

    id: str
    kind: str
    path: str
    sha1: str
    meta: dict = Field(default_factory=dict)


class StepResult(BaseModel):
    """Run step execution result."""

    model_config = ConfigDict(extra="forbid")

    id: str
    index: int
    action: Action
    status: str
    retries: int
    duration_ms: int
    artifacts: List[StepArtifact] = Field(default_factory=list)


class RunResponse(BaseModel):
    """Run resource representation."""

    model_config = ConfigDict(extra="forbid")

    id: str
    job_id: str
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    metrics: dict = Field(default_factory=dict)
    steps: List[StepResult] = Field(default_factory=list)

