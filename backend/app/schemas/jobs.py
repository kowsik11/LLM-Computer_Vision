from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from shared.dsl import ActionProgram


class JobCreateRequest(BaseModel):
    """Create-and-run job request."""

    model_config = ConfigDict(extra="forbid")

    goal: str
    site_policy: List[str]
    secrets: Dict[str, str] | None = None
    demo_trace_id: Optional[str] = None


class JobResponse(BaseModel):
    """Job resource representation."""

    model_config = ConfigDict(extra="forbid")

    id: str
    goal: str
    site_policy: List[str]
    created_at: datetime
    status: str
    latest_run_id: Optional[str] = None
    program: Optional[ActionProgram] = None

