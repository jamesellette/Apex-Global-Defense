"""Country and military schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class CountryBase(BaseModel):
    """Base country schema."""

    name: str = Field(..., min_length=1, max_length=255)
    iso_code: str = Field(..., min_length=3, max_length=3)
    iso_code_2: str = Field(..., min_length=2, max_length=2)
    region: str | None = None
    subregion: str | None = None
    capital: str | None = None
    population: int | None = None
    area_sq_km: float | None = None
    gdp_usd: float | None = None
    defense_budget_usd: float | None = None
    lat: float | None = None
    lng: float | None = None
    flag_url: str | None = None


class CountryCreate(CountryBase):
    """Schema for creating a country."""

    metadata: dict | None = None


class CountryUpdate(BaseModel):
    """Schema for updating a country."""

    name: str | None = Field(None, min_length=1, max_length=255)
    region: str | None = None
    subregion: str | None = None
    capital: str | None = None
    population: int | None = None
    area_sq_km: float | None = None
    gdp_usd: float | None = None
    defense_budget_usd: float | None = None
    lat: float | None = None
    lng: float | None = None
    flag_url: str | None = None
    metadata: dict | None = None


class CountryResponse(CountryBase):
    """Schema for country response."""

    id: str
    metadata: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CountryWithMilitary(CountryResponse):
    """Schema for country with military data."""

    military_branches: list["MilitaryBranchResponse"] = []


# Military Schemas
class MilitaryBranchBase(BaseModel):
    """Base military branch schema."""

    name: str = Field(..., min_length=1, max_length=255)
    branch_type: str
    personnel_active: int | None = None
    personnel_reserve: int | None = None
    personnel_paramilitary: int | None = None
    budget_usd: float | None = None


class MilitaryBranchCreate(MilitaryBranchBase):
    """Schema for creating a military branch."""

    country_id: str


class MilitaryBranchResponse(MilitaryBranchBase):
    """Schema for military branch response."""

    id: str
    country_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MilitaryBranchWithEquipment(MilitaryBranchResponse):
    """Schema for military branch with equipment."""

    equipment: list["MilitaryEquipmentResponse"] = []


# Equipment Schemas
class MilitaryEquipmentBase(BaseModel):
    """Base military equipment schema."""

    category: str
    name: str = Field(..., min_length=1, max_length=255)
    model: str | None = None
    quantity: int = 0
    operational_percentage: float | None = None
    year_introduced: int | None = None
    country_of_origin: str | None = None
    confidence_rating: float | None = Field(None, ge=0, le=1)
    source: str | None = None


class MilitaryEquipmentCreate(MilitaryEquipmentBase):
    """Schema for creating military equipment."""

    branch_id: str
    specifications: dict | None = None


class MilitaryEquipmentResponse(MilitaryEquipmentBase):
    """Schema for military equipment response."""

    id: str
    branch_id: str
    specifications: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Force summary schemas
class ForceSummary(BaseModel):
    """Summary of a country's military forces."""

    total_personnel: int = 0
    active_personnel: int = 0
    reserve_personnel: int = 0
    paramilitary_personnel: int = 0
    total_tanks: int = 0
    total_aircraft: int = 0
    total_naval_vessels: int = 0
    defense_budget_usd: float | None = None


class CountryForceSummary(CountryResponse):
    """Country with force summary."""

    force_summary: ForceSummary


# Update forward references
CountryWithMilitary.model_rebuild()
MilitaryBranchWithEquipment.model_rebuild()
