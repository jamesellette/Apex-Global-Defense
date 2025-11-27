"""Country and military data models."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.military import MilitaryBranch


class Country(Base):
    """Country model with basic information."""

    __tablename__ = "countries"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    iso_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    iso_code_2: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=True)
    subregion: Mapped[str | None] = mapped_column(String(100), nullable=True)
    capital: Mapped[str | None] = mapped_column(String(255), nullable=True)
    population: Mapped[int | None] = mapped_column(Integer, nullable=True)
    area_sq_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    gdp_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    defense_budget_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    flag_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    extra_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    military_branches: Mapped[list["MilitaryBranch"]] = relationship(
        "MilitaryBranch", back_populates="country", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Country {self.name} ({self.iso_code})>"
