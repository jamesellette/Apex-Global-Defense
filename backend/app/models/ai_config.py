"""AI configuration models."""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class AIProvider(str, Enum):
    """Supported AI providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    NONE = "none"


class AIFeature(str, Enum):
    """AI feature types."""

    INTELLIGENCE_ANALYSIS = "intelligence_analysis"
    SCENARIO_GENERATION = "scenario_generation"
    THREAT_ASSESSMENT = "threat_assessment"
    REPORT_GENERATION = "report_generation"
    TRANSLATION = "translation"


class AIConfiguration(Base):
    """AI configuration settings per user."""

    __tablename__ = "ai_configurations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    
    # Provider settings
    provider: Mapped[str] = mapped_column(String(50), default=AIProvider.NONE.value)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    api_key_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Budget control
    monthly_budget_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_month_usage_usd: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Data restrictions
    allow_data_sharing: Mapped[bool] = mapped_column(Boolean, default=False)
    max_input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Fallback behavior
    fallback_mode: Mapped[str] = mapped_column(String(50), default="prompt")  # auto, prompt, block
    
    # Feature toggles
    enabled_features: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    feature_settings: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    
    # Local model settings
    local_model_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    local_model_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<AIConfiguration user={self.user_id} provider={self.provider}>"
