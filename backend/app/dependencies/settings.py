from fastapi import Depends

from app.core.config import Settings, get_settings


def provide_settings(settings: Settings = Depends(get_settings)) -> Settings:
    """Expose application settings to request handlers."""

    return settings

