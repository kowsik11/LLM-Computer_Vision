from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.settings import provide_settings
from app.schemas.planner import PlanRequest, PlanResponse, RepairRequest, RepairResponse
from app.services.planner import build_default_plan, build_repair_patch
from shared.dsl import dsl_json_schema

router = APIRouter()
repair_router = APIRouter()


@router.post(
    "/",
    response_model=PlanResponse,
    summary="Generate a DSL program from a natural language goal",
)
async def generate_plan(payload: PlanRequest, settings=Depends(provide_settings)) -> PlanResponse:  # type: ignore[assignment]
    """Invoke the planner service to build an action program."""

    try:
        program = build_default_plan(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return PlanResponse(program=program, schema=dsl_json_schema())


@repair_router.post(
    "/",
    response_model=RepairResponse,
    summary="Repair a failing DSL program",
)
async def repair_plan(payload: RepairRequest) -> RepairResponse:
    """Return a minimal JSON Patch based on diagnostics."""

    patch = build_repair_patch(payload)
    return RepairResponse(patch=patch)

