"""Scenario models for conflict simulations."""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project


class ScenarioType(str, Enum):
    """Types of scenarios."""

    CONVENTIONAL = "conventional"
    ASYMMETRIC = "asymmetric"
    CYBER = "cyber"
    CBRN = "cbrn"
    TERROR_RESPONSE = "terror_response"
    HYBRID = "hybrid"


class ScenarioStatus(str, Enum):
    """Scenario status options."""

    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Scenario(Base):
    """Scenario model for conflict simulations."""

    __tablename__ = "scenarios"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    creator_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scenario_type: Mapped[str] = mapped_column(String(50), default=ScenarioType.CONVENTIONAL.value)
    status: Mapped[str] = mapped_column(String(50), default=ScenarioStatus.DRAFT.value)
    
    # Geographic bounds
    bounds_north: Mapped[float | None] = mapped_column(Float, nullable=True)
    bounds_south: Mapped[float | None] = mapped_column(Float, nullable=True)
    bounds_east: Mapped[float | None] = mapped_column(Float, nullable=True)
    bounds_west: Mapped[float | None] = mapped_column(Float, nullable=True)
    center_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    center_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    zoom_level: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Scenario data
    participants: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    forces: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    objectives: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    timeline: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    map_layers: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    annotations: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    simulation_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    results: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    
    version: Mapped[int] = mapped_column(Integer, default=1)
    parent_scenario_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("scenarios.id", ondelete="SET NULL"), nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="scenarios")
    creator: Mapped["User"] = relationship("User", back_populates="scenarios")

    def __repr__(self) -> str:
        return f"<Scenario {self.name}>"
