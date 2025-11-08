"""Provider and benchmark data models."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_serializer


class ProviderType(str, Enum):
    """Type of evaluation provider."""

    BUILTIN = "builtin"
    NEMO_EVALUATOR = "nemo-evaluator"


# BenchmarkCategory enum removed - using flexible string categories instead


class Benchmark(BaseModel):
    """Benchmark specification."""

    model_config = ConfigDict(extra="allow")

    benchmark_id: str = Field(..., description="Unique benchmark identifier")
    name: str = Field(..., description="Human-readable benchmark name")
    description: str = Field(..., description="Benchmark description")
    category: str = Field(..., description="Benchmark category")
    metrics: List[str] = Field(..., description="List of metrics provided by this benchmark")
    num_few_shot: int = Field(..., description="Number of few-shot examples")
    dataset_size: Optional[int] = Field(None, description="Size of the evaluation dataset")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


class Provider(BaseModel):
    """Evaluation provider specification."""

    model_config = ConfigDict(extra="allow")

    provider_id: str = Field(..., description="Unique provider identifier")
    provider_name: str = Field(..., description="Human-readable provider name")
    description: str = Field(..., description="Provider description")
    provider_type: ProviderType = Field(..., description="Type of provider")
    base_url: Optional[str] = Field(default=None, description="Base URL for the provider API")
    benchmarks: List[Benchmark] = Field(..., description="List of benchmarks supported by this provider")

    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that base_url is provided for nemo-evaluator providers."""
        provider_type = info.data.get('provider_type')

        if provider_type == ProviderType.NEMO_EVALUATOR and v is None:
            raise ValueError("base_url is required for nemo-evaluator providers")

        return v

    @model_serializer(mode='wrap')
    def serialize_model(self, serializer, info):
        """Custom serialization to exclude base_url for builtin providers when it's None."""
        data = serializer(self)
        if self.provider_type == ProviderType.BUILTIN and self.base_url is None:
            data.pop('base_url', None)
        return data


class BenchmarkReference(BaseModel):
    """Reference to a benchmark within a collection."""

    model_config = ConfigDict(extra="allow")

    provider_id: str = Field(..., description="Provider identifier")
    benchmark_id: str = Field(..., description="Benchmark identifier")


class Collection(BaseModel):
    """Collection of benchmarks for specific evaluation scenarios."""

    model_config = ConfigDict(extra="allow")

    collection_id: str = Field(..., description="Unique collection identifier")
    name: str = Field(..., description="Human-readable collection name")
    description: str = Field(..., description="Collection description")
    benchmarks: List[BenchmarkReference] = Field(..., description="List of benchmark references in this collection")


class ProvidersData(BaseModel):
    """Complete providers configuration data."""

    model_config = ConfigDict(extra="allow")

    providers: List[Provider] = Field(..., description="List of evaluation providers")
    collections: List[Collection] = Field(..., description="List of benchmark collections")


class ProviderSummary(BaseModel):
    """Simplified provider information without benchmark details."""

    model_config = ConfigDict(extra="allow")

    provider_id: str = Field(..., description="Unique provider identifier")
    provider_name: str = Field(..., description="Human-readable provider name")
    description: str = Field(..., description="Provider description")
    provider_type: ProviderType = Field(..., description="Type of provider")
    base_url: Optional[str] = Field(default=None, description="Base URL for the provider API")
    benchmark_count: int = Field(..., description="Number of benchmarks supported by this provider")

    @model_serializer(mode='wrap')
    def serialize_model(self, serializer, info):
        """Custom serialization to exclude base_url for builtin providers when it's None."""
        data = serializer(self)
        if self.provider_type == ProviderType.BUILTIN and self.base_url is None:
            data.pop('base_url', None)
        return data


class ListProvidersResponse(BaseModel):
    """Response for listing all providers."""

    model_config = ConfigDict(extra="allow")

    providers: List[ProviderSummary] = Field(..., description="List of available providers")
    total_providers: int = Field(..., description="Total number of providers")
    total_benchmarks: int = Field(..., description="Total number of benchmarks across all providers")


class ListBenchmarksResponse(BaseModel):
    """Response for listing all benchmarks (similar to Llama Stack format)."""

    model_config = ConfigDict(extra="allow")

    benchmarks: List[Dict[str, Any]] = Field(..., description="List of all available benchmarks")
    total_count: int = Field(..., description="Total number of benchmarks")
    providers_included: List[str] = Field(..., description="List of provider IDs included in the response")


class ListCollectionsResponse(BaseModel):
    """Response for listing all collections."""

    model_config = ConfigDict(extra="allow")

    collections: List[Collection] = Field(..., description="List of available collections")
    total_collections: int = Field(..., description="Total number of collections")


class BenchmarkDetail(BaseModel):
    """Detailed benchmark information for API responses."""

    model_config = ConfigDict(extra="allow")

    benchmark_id: str = Field(..., description="Unique benchmark identifier")
    provider_id: str = Field(..., description="Provider that owns this benchmark")
    provider_name: str = Field(..., description="Human-readable provider name")
    name: str = Field(..., description="Human-readable benchmark name")
    description: str = Field(..., description="Benchmark description")
    category: str = Field(..., description="Benchmark category")
    metrics: List[str] = Field(..., description="List of metrics provided by this benchmark")
    num_few_shot: int = Field(..., description="Number of few-shot examples")
    dataset_size: Optional[int] = Field(None, description="Size of the evaluation dataset")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    provider_type: ProviderType = Field(..., description="Type of provider (builtin/nemo-evaluator)")
    base_url: Optional[str] = Field(default=None, description="Base URL for the provider API")

    @model_serializer(mode='wrap')
    def serialize_model(self, serializer, info):
        """Custom serialization to exclude base_url for builtin providers when it's None."""
        data = serializer(self)
        if self.provider_type == ProviderType.BUILTIN and self.base_url is None:
            data.pop('base_url', None)
        return data