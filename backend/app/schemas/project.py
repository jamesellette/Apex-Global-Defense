"""Project schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    classification: str = "unclassified"
    region_focus: str | None = None
    tags: list[str] | None = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    settings: dict | None = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = None
    classification: str | None = None
    region_focus: str | None = None
    tags: list[str] | None = None
    settings: dict | None = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""

    id: str
    owner_id: str
    status: str
    settings: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectWithScenarios(ProjectResponse):
    """Schema for project with scenarios."""

    scenarios: list["ScenarioResponse"] = []


# Scenario Schemas
class ScenarioBase(BaseModel):
    """Base scenario schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    scenario_type: str = "conventional"


class ScenarioCreate(ScenarioBase):
    """Schema for creating a scenario."""

    project_id: str
    bounds_north: float | None = None
    bounds_south: float | None = None
    bounds_east: float | None = None
    bounds_west: float | None = None
    center_lat: float | None = None
    center_lng: float | None = None
    zoom_level: int | None = None
    participants: list[dict] | None = None
    forces: dict | None = None
    objectives: list[dict] | None = None
    simulation_config: dict | None = None


class ScenarioUpdate(BaseModel):
    """Schema for updating a scenario."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    scenario_type: str | None = None
    status: str | None = None
    bounds_north: float | None = None
    bounds_south: float | None = None
    bounds_east: float | None = None
    bounds_west: float | None = None
    center_lat: float | None = None
    center_lng: float | None = None
    zoom_level: int | None = None
    participants: list[dict] | None = None
    forces: dict | None = None
    objectives: list[dict] | None = None
    timeline: list[dict] | None = None
    map_layers: list[dict] | None = None
    annotations: list[dict] | None = None
    simulation_config: dict | None = None
    results: dict | None = None


class ScenarioResponse(ScenarioBase):
    """Schema for scenario response."""

    id: str
    project_id: str
    creator_id: str
    status: str
    bounds_north: float | None = None
    bounds_south: float | None = None
    bounds_east: float | None = None
    bounds_west: float | None = None
    center_lat: float | None = None
    center_lng: float | None = None
    zoom_level: int | None = None
    participants: list[dict] | None = None
    forces: dict | None = None
    objectives: list[dict] | None = None
    timeline: list[dict] | None = None
    map_layers: list[dict] | None = None
    annotations: list[dict] | None = None
    simulation_config: dict | None = None
    results: dict | None = None
    version: int
    parent_scenario_id: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Update forward references
ProjectWithScenarios.model_rebuild()
