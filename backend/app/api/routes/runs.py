from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.runs import RunResponse
from app.services.runs import get_run, list_runs

router = APIRouter()


@router.get("/", response_model=List[RunResponse], summary="List runs")
async def list_runs_route() -> List[RunResponse]:
    """List all runs in the in-memory store."""

    return list_runs()


@router.get("/{run_id}", response_model=RunResponse, summary="Get run detail")
async def get_run_route(run_id: str) -> RunResponse:
    """Retrieve a specific run."""

    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return run

