from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Health check")
async def health_check() -> dict[str, str]:
    """Return a static health indicator."""

    return {"status": "ok"}

