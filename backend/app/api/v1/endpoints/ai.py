"""AI configuration endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.ai_config import AIConfiguration, AIProvider
from app.models.user import User
from app.schemas.ai_config import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    AIConfigCreate,
    AIConfigResponse,
    AIConfigUpdate,
    AIFeatureInfo,
    AIProviderInfo,
)

router = APIRouter()


# Feature and provider information
AI_FEATURES = [
    AIFeatureInfo(
        feature_id="intelligence_analysis",
        name="Intelligence Analysis",
        description="Auto extraction and summarization of intelligence data",
        ai_mode="Auto extraction, summarization",
        fallback_mode="Manual tagging templates",
        requires_api_key=True,
    ),
    AIFeatureInfo(
        feature_id="scenario_generation",
        name="Scenario Generation",
        description="Natural language scenario builder",
        ai_mode="Natural language builder",
        fallback_mode="Wizard-based",
        requires_api_key=True,
    ),
    AIFeatureInfo(
        feature_id="threat_assessment",
        name="Threat Assessment",
        description="Pattern recognition for threat analysis",
        ai_mode="Pattern recognition",
        fallback_mode="Weighted matrix",
        requires_api_key=True,
    ),
    AIFeatureInfo(
        feature_id="report_generation",
        name="Report Generation",
        description="Automated briefing generation",
        ai_mode="Auto briefs",
        fallback_mode="Template library",
        requires_api_key=True,
    ),
    AIFeatureInfo(
        feature_id="translation",
        name="Translation",
        description="Real-time OSINT translation",
        ai_mode="Real-time OSINT translation",
        fallback_mode="API/manual",
        requires_api_key=True,
    ),
]

AI_PROVIDERS = [
    AIProviderInfo(
        provider_id="openai",
        name="OpenAI",
        models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        supports_streaming=True,
        max_tokens=128000,
    ),
    AIProviderInfo(
        provider_id="anthropic",
        name="Anthropic",
        models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        supports_streaming=True,
        max_tokens=200000,
    ),
    AIProviderInfo(
        provider_id="local",
        name="Local Model",
        models=["llama-2", "mistral", "custom"],
        supports_streaming=False,
        max_tokens=None,
    ),
    AIProviderInfo(
        provider_id="none",
        name="Disabled",
        models=[],
        supports_streaming=False,
        max_tokens=None,
    ),
]


@router.get("/providers", response_model=list[AIProviderInfo])
async def list_providers() -> list[AIProviderInfo]:
    """List available AI providers. Public endpoint."""
    return AI_PROVIDERS


@router.get("/features", response_model=list[AIFeatureInfo])
async def list_features() -> list[AIFeatureInfo]:
    """List available AI features. Public endpoint."""
    return AI_FEATURES


@router.get("/config", response_model=AIConfigResponse | None)
async def get_ai_config(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AIConfiguration | None:
    """Get current user's AI configuration."""
    result = await db.execute(
        select(AIConfiguration).where(AIConfiguration.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    
    if config:
        # Add has_api_key field
        config_dict = {
            "id": config.id,
            "user_id": config.user_id,
            "provider": config.provider,
            "model": config.model,
            "fallback_mode": config.fallback_mode,
            "allow_data_sharing": config.allow_data_sharing,
            "monthly_budget_usd": config.monthly_budget_usd,
            "current_month_usage_usd": config.current_month_usage_usd,
            "max_input_tokens": config.max_input_tokens,
            "enabled_features": config.enabled_features,
            "feature_settings": config.feature_settings,
            "local_model_path": config.local_model_path,
            "local_model_config": config.local_model_config,
            "has_api_key": config.api_key_encrypted is not None,
            "created_at": config.created_at,
            "updated_at": config.updated_at,
        }
        return AIConfigResponse(**config_dict)
    return None


@router.post("/config", response_model=AIConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_config(
    config_in: AIConfigCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AIConfiguration:
    """Create AI configuration for current user."""
    # Check if config already exists
    result = await db.execute(
        select(AIConfiguration).where(AIConfiguration.user_id == current_user.id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AI configuration already exists. Use PATCH to update.",
        )
    
    config_data = config_in.model_dump(exclude={"api_key"})
    config = AIConfiguration(
        user_id=current_user.id,
        **config_data,
    )
    
    # Store API key (should be encrypted in production)
    if config_in.api_key:
        config.api_key_encrypted = config_in.api_key  # TODO: Encrypt
    
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


@router.patch("/config", response_model=AIConfigResponse)
async def update_ai_config(
    config_in: AIConfigUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AIConfiguration:
    """Update AI configuration for current user."""
    result = await db.execute(
        select(AIConfiguration).where(AIConfiguration.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI configuration not found. Create one first.",
        )
    
    update_data = config_in.model_dump(exclude_unset=True, exclude={"api_key"})
    for field, value in update_data.items():
        setattr(config, field, value)
    
    # Handle API key update separately
    if config_in.api_key is not None:
        config.api_key_encrypted = config_in.api_key  # TODO: Encrypt
    
    await db.commit()
    await db.refresh(config)
    return config


@router.delete("/config", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_config(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Delete AI configuration for current user."""
    result = await db.execute(
        select(AIConfiguration).where(AIConfiguration.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI configuration not found",
        )
    
    await db.delete(config)
    await db.commit()


@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_with_ai(
    request: AIAnalysisRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AIAnalysisResponse:
    """Perform AI analysis on input data."""
    # Get user's AI config
    result = await db.execute(
        select(AIConfiguration).where(AIConfiguration.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    
    # Check if AI is configured and feature is enabled
    if not config or config.provider == AIProvider.NONE.value:
        # Use fallback mode
        return _get_fallback_response(request)
    
    if config.enabled_features and request.feature not in config.enabled_features:
        return _get_fallback_response(request)
    
    # In a real implementation, this would call the AI provider
    # For now, return a mock response
    return AIAnalysisResponse(
        feature=request.feature,
        result="AI analysis would be performed here with the configured provider.",
        tokens_used=0,
        cost_usd=0.0,
        provider=config.provider,
        model=config.model,
        is_fallback=False,
    )


def _get_fallback_response(request: AIAnalysisRequest) -> AIAnalysisResponse:
    """Get fallback response when AI is not available."""
    fallback_messages = {
        "intelligence_analysis": "Use manual tagging templates for intelligence analysis.",
        "scenario_generation": "Use the wizard-based scenario builder.",
        "threat_assessment": "Use the weighted matrix assessment tool.",
        "report_generation": "Use the template library for report generation.",
        "translation": "Use external translation API or manual translation.",
    }
    
    message = fallback_messages.get(
        request.feature,
        "AI features are not configured. Please enable AI in settings.",
    )
    
    return AIAnalysisResponse(
        feature=request.feature,
        result=message,
        tokens_used=0,
        cost_usd=0.0,
        provider="none",
        model=None,
        is_fallback=True,
    )
