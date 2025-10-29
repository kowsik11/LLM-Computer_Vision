from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.jobs import JobCreateRequest, JobResponse
from app.services.jobs import job_store
from app.services.runs import create_run

router = APIRouter()


@router.get("/", response_model=List[JobResponse], summary="List jobs")
async def list_jobs() -> List[JobResponse]:
    """Return all jobs in the in-memory store."""

    return job_store.list_jobs()


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED, summary="Create a job")
async def create_job(payload: JobCreateRequest) -> JobResponse:
    """Create a new job and enqueue a run placeholder."""

    job = job_store.create_job(payload)
    run = create_run(job.id)
    job_store.upsert_run(run)
    return job


@router.get("/{job_id}", response_model=JobResponse, summary="Get job")
async def get_job(job_id: str) -> JobResponse:
    """Retrieve a specific job."""

    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

