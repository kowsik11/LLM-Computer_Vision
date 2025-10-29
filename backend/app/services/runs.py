from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.schemas.runs import RunResponse, StepResult
from app.services.jobs import job_store


def create_run(job_id: str) -> RunResponse:
    """Create a run record tied to a job."""

    run_id = str(uuid.uuid4())
    run = RunResponse(
        id=run_id,
        job_id=job_id,
        started_at=datetime.now(tz=timezone.utc),
        finished_at=None,
        status="scheduled",
        metrics={},
        steps=[],
    )
    job_store.upsert_run(run)
    return run


def get_run(run_id: str) -> Optional[RunResponse]:
    return job_store.get_run(run_id)


def list_runs() -> list[RunResponse]:
    return job_store.list_runs()


def complete_run(run_id: str, steps: list[StepResult], metrics: dict) -> Optional[RunResponse]:
    run = job_store.get_run(run_id)
    if not run:
        return None
    updated = run.model_copy(
        update={
            "finished_at": datetime.now(tz=timezone.utc),
            "status": "completed",
            "steps": steps,
            "metrics": metrics,
        }
    )
    job_store.upsert_run(updated)
    return updated

