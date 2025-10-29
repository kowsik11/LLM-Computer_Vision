from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from app.schemas.jobs import JobResponse, JobCreateRequest
from app.schemas.runs import RunResponse


class InMemoryJobStore:
    """Simple in-memory job store to unblock early development."""

    def __init__(self) -> None:
        self._jobs: Dict[str, JobResponse] = {}
        self._runs: Dict[str, RunResponse] = {}

    def create_job(self, payload: JobCreateRequest) -> JobResponse:
        job_id = str(uuid.uuid4())
        job = JobResponse(
            id=job_id,
            goal=payload.goal,
            site_policy=payload.site_policy,
            created_at=datetime.now(tz=timezone.utc),
            status="pending",
            latest_run_id=None,
            program=None,
        )
        self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[JobResponse]:
        return self._jobs.get(job_id)

    def list_jobs(self) -> list[JobResponse]:
        return list(self._jobs.values())

    def upsert_run(self, run: RunResponse) -> None:
        self._runs[run.id] = run
        if run.job_id in self._jobs:
            job = self._jobs[run.job_id]
            self._jobs[run.job_id] = job.model_copy(
                update={"latest_run_id": run.id, "status": run.status}
            )

    def get_run(self, run_id: str) -> Optional[RunResponse]:
        return self._runs.get(run_id)

    def list_runs(self) -> list[RunResponse]:
        return list(self._runs.values())


job_store = InMemoryJobStore()

