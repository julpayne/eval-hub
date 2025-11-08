"""Health check models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Overall health status")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Health check timestamp"
    )
    components: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Health status of individual components"
    )
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    active_evaluations: int = Field(
        default=0, description="Number of active evaluations"
    )
