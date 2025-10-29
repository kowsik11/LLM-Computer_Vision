from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.runs import StepArtifact
from app.services.runs import get_run

router = APIRouter()


@router.get("/{run_id}", response_model=List[StepArtifact], summary="List run artifacts")
async def list_run_artifacts(run_id: str) -> List[StepArtifact]:
    """Return all artifacts associated with a run."""

    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    artifacts: list[StepArtifact] = []
    for step in run.steps:
        artifacts.extend(step.artifacts)
    return artifacts

