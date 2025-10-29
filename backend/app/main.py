from __future__ import annotations

from fastapi import FastAPI

from app.api import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from shared.dsl import dsl_json_schema


def create_app() -> FastAPI:
    """FastAPI application factory."""

    settings = get_settings()
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get(f"{settings.api_prefix}/dsl/schema", tags=["planner"])
    async def get_dsl_schema() -> dict:
        return dsl_json_schema()

    return app


app = create_app()

