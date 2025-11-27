"""AI configuration schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class AIConfigBase(BaseModel):
    """Base AI configuration schema."""

    provider: str = "none"
    model: str | None = None
    fallback_mode: str = "prompt"  # auto, prompt, block
    allow_data_sharing: bool = False


class AIConfigCreate(AIConfigBase):
    """Schema for creating AI configuration."""

    api_key: str | None = None
    monthly_budget_usd: float | None = None
    max_input_tokens: int | None = None
    enabled_features: list[str] | None = None
    feature_settings: dict | None = None
    local_model_path: str | None = None
    local_model_config: dict | None = None


class AIConfigUpdate(BaseModel):
    """Schema for updating AI configuration."""

    provider: str | None = None
    model: str | None = None
    api_key: str | None = None
    monthly_budget_usd: float | None = None
    max_input_tokens: int | None = None
    fallback_mode: str | None = None
    allow_data_sharing: bool | None = None
    enabled_features: list[str] | None = None
    feature_settings: dict | None = None
    local_model_path: str | None = None
    local_model_config: dict | None = None


class AIConfigResponse(AIConfigBase):
    """Schema for AI configuration response."""

    id: str
    user_id: str
    monthly_budget_usd: float | None = None
    current_month_usage_usd: float = 0.0
    max_input_tokens: int | None = None
    enabled_features: list[str] | None = None
    feature_settings: dict | None = None
    local_model_path: str | None = None
    local_model_config: dict | None = None
    has_api_key: bool = False  # Don't expose actual key
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AIFeatureInfo(BaseModel):
    """Information about an AI feature."""

    feature_id: str
    name: str
    description: str
    ai_mode: str
    fallback_mode: str
    requires_api_key: bool = True


class AIProviderInfo(BaseModel):
    """Information about an AI provider."""

    provider_id: str
    name: str
    models: list[str]
    supports_streaming: bool = False
    max_tokens: int | None = None


class AIAnalysisRequest(BaseModel):
    """Request for AI analysis."""

    feature: str
    input_text: str = Field(..., min_length=1, max_length=50000)
    context: dict | None = None
    options: dict | None = None


class AIAnalysisResponse(BaseModel):
    """Response from AI analysis."""

    feature: str
    result: str | dict
    tokens_used: int = 0
    cost_usd: float = 0.0
    provider: str
    model: str | None = None
    is_fallback: bool = False
