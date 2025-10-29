"""API router registration."""

from fastapi import APIRouter

from app.api.routes import artifacts, health, jobs, planner, runs

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(planner.router, prefix="/plan", tags=["planner"])
api_router.include_router(planner.repair_router, prefix="/repair", tags=["planner"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])

