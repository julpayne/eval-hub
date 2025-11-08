"""Data models for NeMo Evaluator API integration."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class EndpointType(str, Enum):
    """Endpoint types supported by NeMo Evaluator."""

    UNDEFINED = "undefined"
    CHAT = "chat"
    COMPLETIONS = "completions"
    VLM = "vlm"
    EMBEDDING = "embedding"


class NemoApiEndpoint(BaseModel):
    """API endpoint configuration for NeMo Evaluator."""

    model_config = ConfigDict(extra="allow")

    api_key: Optional[str] = Field(None, description="API key environment variable name")
    model_id: Optional[str] = Field(None, description="Model identifier")
    stream: Optional[bool] = Field(None, description="Whether to stream responses")
    type: Optional[EndpointType] = Field(None, description="Endpoint type")
    url: Optional[str] = Field(None, description="API endpoint URL")


class NemoConfigParams(BaseModel):
    """Configuration parameters for NeMo Evaluator execution."""

    model_config = ConfigDict(extra="allow")

    limit_samples: Optional[Union[int, float]] = Field(None, description="Limit evaluation samples")
    max_new_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    max_retries: Optional[int] = Field(None, description="Number of REST request retries")
    parallelism: Optional[int] = Field(None, description="Execution parallelism")
    task: Optional[str] = Field(None, description="Task name")
    temperature: Optional[float] = Field(None, description="Generation temperature")
    request_timeout: Optional[int] = Field(None, description="REST response timeout")
    top_p: Optional[float] = Field(None, description="Top-p sampling parameter")
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Framework specific parameters")


class NemoEvaluationTarget(BaseModel):
    """Target configuration for NeMo Evaluator API endpoints."""

    api_endpoint: Optional[NemoApiEndpoint] = Field(None, description="API endpoint configuration")


class NemoEvaluationConfig(BaseModel):
    """Evaluation configuration for NeMo Evaluator."""

    model_config = ConfigDict(extra="allow")

    output_dir: Optional[str] = Field(None, description="Output directory for results")
    params: Optional[NemoConfigParams] = Field(None, description="Evaluation parameters")
    supported_endpoint_types: Optional[List[str]] = Field(None, description="Supported endpoint types")
    type: Optional[str] = Field(None, description="Task type")


class NemoEvaluationRequest(BaseModel):
    """Complete evaluation request for NeMo Evaluator."""

    model_config = ConfigDict(extra="allow")

    command: str = Field(..., description="Jinja template of command to execute")
    framework_name: str = Field(..., description="Framework name")
    pkg_name: str = Field(..., description="Package name")
    config: NemoEvaluationConfig = Field(..., description="Evaluation configuration")
    target: NemoEvaluationTarget = Field(..., description="Target configuration")


# Response models for NeMo Evaluator results
class NemoScoreStats(BaseModel):
    """Statistics for a score in NeMo Evaluator results."""

    count: Optional[int] = Field(None, description="Number of values")
    sum: Optional[float] = Field(None, description="Sum of values")
    sum_squared: Optional[float] = Field(None, description="Sum of squared values")
    min: Optional[float] = Field(None, description="Minimum value")
    max: Optional[float] = Field(None, description="Maximum value")
    mean: Optional[float] = Field(None, description="Mean value")
    variance: Optional[float] = Field(None, description="Population variance")
    stddev: Optional[float] = Field(None, description="Population standard deviation")
    stderr: Optional[float] = Field(None, description="Standard error")


class NemoScore(BaseModel):
    """Score information from NeMo Evaluator."""

    value: float = Field(..., description="Score value")
    stats: NemoScoreStats = Field(..., description="Score statistics")


class NemoMetricResult(BaseModel):
    """Metric result from NeMo Evaluator."""

    scores: Dict[str, NemoScore] = Field(default_factory=dict, description="Metric scores")


class NemoTaskResult(BaseModel):
    """Task result from NeMo Evaluator."""

    metrics: Dict[str, NemoMetricResult] = Field(default_factory=dict, description="Task metrics")


class NemoGroupResult(BaseModel):
    """Group result from NeMo Evaluator."""

    groups: Optional[Dict[str, "NemoGroupResult"]] = Field(None, description="Subgroup results")
    metrics: Dict[str, NemoMetricResult] = Field(default_factory=dict, description="Group metrics")


class NemoEvaluationResult(BaseModel):
    """Complete evaluation result from NeMo Evaluator."""

    tasks: Optional[Dict[str, NemoTaskResult]] = Field(default_factory=dict, description="Task results")
    groups: Optional[Dict[str, NemoGroupResult]] = Field(default_factory=dict, description="Group results")


class NemoContainerConfig(BaseModel):
    """Configuration for NeMo Evaluator container endpoints."""

    model_config = ConfigDict(extra="allow")

    endpoint: str = Field(..., description="NeMo Evaluator container endpoint URL")
    port: int = Field(default=3825, description="NeMo Evaluator adapter port")
    timeout_seconds: int = Field(default=3600, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    health_check_endpoint: Optional[str] = Field(None, description="Health check endpoint")
    auth_token: Optional[str] = Field(None, description="Authentication token")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

    def get_full_endpoint(self) -> str:
        """Get the complete endpoint URL."""
        if "://" in self.endpoint:
            return f"{self.endpoint}:{self.port}" if not self.endpoint.endswith(str(self.port)) else self.endpoint
        else:
            return f"http://{self.endpoint}:{self.port}"

    def get_health_check_url(self) -> Optional[str]:
        """Get the health check URL if configured."""
        if self.health_check_endpoint:
            base = self.get_full_endpoint()
            return f"{base}{self.health_check_endpoint}"
        return None


# Update GroupResult to allow self-referencing
NemoGroupResult.model_rebuild()