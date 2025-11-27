"""Project and scenario endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.scenario import Scenario
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ProjectWithScenarios,
    ScenarioCreate,
    ScenarioResponse,
    ScenarioUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_filter: str | None = None,
) -> list[Project]:
    """List projects for current user."""
    query = select(Project).where(Project.owner_id == current_user.id)
    
    if status_filter:
        query = query.where(Project.status == status_filter)
    
    query = query.order_by(Project.updated_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{project_id}", response_model=ProjectWithScenarios)
async def get_project(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Project:
    """Get a project by ID with scenarios."""
    query = (
        select(Project)
        .where(Project.id == project_id, Project.owner_id == current_user.id)
        .options(selectinload(Project.scenarios))
    )
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Project:
    """Create a new project."""
    project = Project(
        **project_in.model_dump(),
        owner_id=current_user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Project:
    """Update a project."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Delete a project."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    await db.delete(project)
    await db.commit()


# Scenario endpoints
@router.get("/{project_id}/scenarios", response_model=list[ScenarioResponse])
async def list_scenarios(
    project_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[Scenario]:
    """List scenarios for a project."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    query = (
        select(Scenario)
        .where(Scenario.project_id == project_id)
        .order_by(Scenario.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{project_id}/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    project_id: str,
    scenario_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Scenario:
    """Get a scenario by ID."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id, Scenario.project_id == project_id)
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    return scenario


@router.post("/{project_id}/scenarios", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    project_id: str,
    scenario_in: ScenarioCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Scenario:
    """Create a new scenario."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    scenario = Scenario(
        **scenario_in.model_dump(exclude={"project_id"}),
        project_id=project_id,
        creator_id=current_user.id,
    )
    db.add(scenario)
    await db.commit()
    await db.refresh(scenario)
    return scenario


@router.patch("/{project_id}/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    project_id: str,
    scenario_id: str,
    scenario_in: ScenarioUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Scenario:
    """Update a scenario."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id, Scenario.project_id == project_id)
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    update_data = scenario_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
    
    await db.commit()
    await db.refresh(scenario)
    return scenario


@router.delete("/{project_id}/scenarios/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(
    project_id: str,
    scenario_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Delete a scenario."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id, Scenario.project_id == project_id)
    )
    scenario = result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    await db.delete(scenario)
    await db.commit()


@router.post("/{project_id}/scenarios/{scenario_id}/branch", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def branch_scenario(
    project_id: str,
    scenario_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    new_name: str = Query(..., min_length=1, max_length=255),
) -> Scenario:
    """Create a branch (copy) of an existing scenario."""
    # Verify project access
    project_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if not project_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    result = await db.execute(
        select(Scenario).where(Scenario.id == scenario_id, Scenario.project_id == project_id)
    )
    parent_scenario = result.scalar_one_or_none()
    
    if not parent_scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )
    
    # Create new scenario based on parent
    new_scenario = Scenario(
        project_id=project_id,
        creator_id=current_user.id,
        name=new_name,
        description=parent_scenario.description,
        scenario_type=parent_scenario.scenario_type,
        bounds_north=parent_scenario.bounds_north,
        bounds_south=parent_scenario.bounds_south,
        bounds_east=parent_scenario.bounds_east,
        bounds_west=parent_scenario.bounds_west,
        center_lat=parent_scenario.center_lat,
        center_lng=parent_scenario.center_lng,
        zoom_level=parent_scenario.zoom_level,
        participants=parent_scenario.participants,
        forces=parent_scenario.forces,
        objectives=parent_scenario.objectives,
        timeline=parent_scenario.timeline,
        map_layers=parent_scenario.map_layers,
        annotations=parent_scenario.annotations,
        simulation_config=parent_scenario.simulation_config,
        parent_scenario_id=parent_scenario.id,
        version=parent_scenario.version + 1,
    )
    db.add(new_scenario)
    await db.commit()
    await db.refresh(new_scenario)
    return new_scenario
