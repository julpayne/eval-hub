"""Status and task tracking models."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of a background task."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EvaluationStatus(str, Enum):
    """Detailed evaluation status."""

    PENDING = "pending"
    INITIALIZING = "initializing"
    RUNNING = "running"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskInfo(BaseModel):
    """Information about a background task."""

    task_id: str = Field(..., description="Unique task identifier")
    evaluation_id: UUID = Field(..., description="Associated evaluation ID")
    status: TaskStatus = Field(..., description="Current task status")
    progress: float = Field(default=0.0, description="Task progress percentage")
    message: str | None = Field(None, description="Current status message")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Task creation time"
    )
    started_at: datetime | None = Field(None, description="Task start time")
    completed_at: datetime | None = Field(None, description="Task completion time")
    error_message: str | None = Field(None, description="Error message if failed")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional task metadata"
    )
