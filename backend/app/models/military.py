"""Military data models for Order of Battle."""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.country import Country


class BranchType(str, Enum):
    """Military branch types."""

    ARMY = "army"
    NAVY = "navy"
    AIR_FORCE = "air_force"
    MARINES = "marines"
    SPACE_FORCE = "space_force"
    COAST_GUARD = "coast_guard"
    SPECIAL_OPERATIONS = "special_operations"
    CYBER = "cyber"
    OTHER = "other"


class EquipmentCategory(str, Enum):
    """Equipment categories."""

    TANKS = "tanks"
    ARMORED_VEHICLES = "armored_vehicles"
    ARTILLERY = "artillery"
    MLRS = "mlrs"
    AIRCRAFT_FIGHTER = "aircraft_fighter"
    AIRCRAFT_ATTACK = "aircraft_attack"
    AIRCRAFT_TRANSPORT = "aircraft_transport"
    HELICOPTERS_ATTACK = "helicopters_attack"
    HELICOPTERS_TRANSPORT = "helicopters_transport"
    NAVAL_CARRIERS = "naval_carriers"
    NAVAL_DESTROYERS = "naval_destroyers"
    NAVAL_FRIGATES = "naval_frigates"
    NAVAL_SUBMARINES = "naval_submarines"
    NAVAL_PATROL = "naval_patrol"
    MISSILES_BALLISTIC = "missiles_ballistic"
    MISSILES_CRUISE = "missiles_cruise"
    DRONES = "drones"
    OTHER = "other"


class MilitaryBranch(Base):
    """Military branch model."""

    __tablename__ = "military_branches"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    country_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_type: Mapped[str] = mapped_column(String(50), nullable=False)
    personnel_active: Mapped[int | None] = mapped_column(Integer, nullable=True)
    personnel_reserve: Mapped[int | None] = mapped_column(Integer, nullable=True)
    personnel_paramilitary: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="military_branches")
    equipment: Mapped[list["MilitaryEquipment"]] = relationship(
        "MilitaryEquipment", back_populates="branch", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<MilitaryBranch {self.name}>"


class MilitaryEquipment(Base):
    """Military equipment inventory model."""

    __tablename__ = "military_equipment"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    branch_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("military_branches.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    operational_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    year_introduced: Mapped[int | None] = mapped_column(Integer, nullable=True)
    country_of_origin: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specifications: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    confidence_rating: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-1 accuracy
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    branch: Mapped["MilitaryBranch"] = relationship("MilitaryBranch", back_populates="equipment")

    def __repr__(self) -> str:
        return f"<MilitaryEquipment {self.name} x{self.quantity}>"
