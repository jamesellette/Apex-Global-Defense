"""Country and military data endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.endpoints.auth import get_current_user, get_current_user_optional
from app.db.session import get_db
from app.models.country import Country
from app.models.military import MilitaryBranch, MilitaryEquipment
from app.models.user import User
from app.schemas.country import (
    CountryCreate,
    CountryResponse,
    CountryUpdate,
    CountryWithMilitary,
    ForceSummary,
    MilitaryBranchCreate,
    MilitaryBranchResponse,
    MilitaryBranchWithEquipment,
    MilitaryEquipmentCreate,
    MilitaryEquipmentResponse,
)

router = APIRouter()


@router.get("/", response_model=list[CountryResponse])
async def list_countries(
    db: Annotated[AsyncSession, Depends(get_db)],
    _current_user: Annotated[User | None, Depends(get_current_user_optional)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    region: str | None = None,
    search: str | None = None,
) -> list[Country]:
    """List all countries with optional filtering. Public endpoint."""
    query = select(Country)
    
    if region:
        query = query.where(Country.region == region)
    if search:
        query = query.where(
            Country.name.ilike(f"%{search}%") | Country.iso_code.ilike(f"%{search}%")
        )
    
    query = query.order_by(Country.name).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{country_id}", response_model=CountryWithMilitary)
async def get_country(
    country_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Country:
    """Get a country by ID with military data."""
    query = (
        select(Country)
        .where(Country.id == country_id)
        .options(
            selectinload(Country.military_branches).selectinload(MilitaryBranch.equipment)
        )
    )
    result = await db.execute(query)
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    return country


@router.get("/iso/{iso_code}", response_model=CountryWithMilitary)
async def get_country_by_iso(
    iso_code: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Country:
    """Get a country by ISO code with military data."""
    query = (
        select(Country)
        .where(Country.iso_code == iso_code.upper())
        .options(
            selectinload(Country.military_branches).selectinload(MilitaryBranch.equipment)
        )
    )
    result = await db.execute(query)
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    return country


@router.post("/", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(
    country_in: CountryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Country:
    """Create a new country."""
    # Check if country already exists
    result = await db.execute(
        select(Country).where(Country.iso_code == country_in.iso_code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Country with this ISO code already exists",
        )
    
    country = Country(**country_in.model_dump())
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


@router.patch("/{country_id}", response_model=CountryResponse)
async def update_country(
    country_id: str,
    country_in: CountryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Country:
    """Update a country."""
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    
    update_data = country_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(country, field, value)
    
    await db.commit()
    await db.refresh(country)
    return country


@router.get("/{country_id}/summary", response_model=ForceSummary)
async def get_country_force_summary(
    country_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ForceSummary:
    """Get force summary for a country."""
    # Get country
    result = await db.execute(select(Country).where(Country.id == country_id))
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    
    # Get personnel counts
    branch_result = await db.execute(
        select(
            func.coalesce(func.sum(MilitaryBranch.personnel_active), 0),
            func.coalesce(func.sum(MilitaryBranch.personnel_reserve), 0),
            func.coalesce(func.sum(MilitaryBranch.personnel_paramilitary), 0),
        ).where(MilitaryBranch.country_id == country_id)
    )
    active, reserve, paramilitary = branch_result.one()
    
    # Get equipment counts by category
    equipment_result = await db.execute(
        select(MilitaryEquipment.category, func.sum(MilitaryEquipment.quantity))
        .join(MilitaryBranch)
        .where(MilitaryBranch.country_id == country_id)
        .group_by(MilitaryEquipment.category)
    )
    equipment_counts = dict(equipment_result.all())
    
    tanks = equipment_counts.get("tanks", 0) or 0
    aircraft = sum(
        equipment_counts.get(cat, 0) or 0
        for cat in ["aircraft_fighter", "aircraft_attack", "aircraft_transport"]
    )
    naval = sum(
        equipment_counts.get(cat, 0) or 0
        for cat in ["naval_carriers", "naval_destroyers", "naval_frigates", "naval_submarines", "naval_patrol"]
    )
    
    return ForceSummary(
        total_personnel=int(active + reserve + paramilitary),
        active_personnel=int(active),
        reserve_personnel=int(reserve),
        paramilitary_personnel=int(paramilitary),
        total_tanks=int(tanks),
        total_aircraft=int(aircraft),
        total_naval_vessels=int(naval),
        defense_budget_usd=country.defense_budget_usd,
    )


# Military Branch endpoints
@router.post("/{country_id}/branches", response_model=MilitaryBranchResponse, status_code=status.HTTP_201_CREATED)
async def create_military_branch(
    country_id: str,
    branch_in: MilitaryBranchCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MilitaryBranch:
    """Create a military branch for a country."""
    # Verify country exists
    result = await db.execute(select(Country).where(Country.id == country_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    
    branch = MilitaryBranch(**branch_in.model_dump())
    branch.country_id = country_id
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch


@router.get("/{country_id}/branches", response_model=list[MilitaryBranchWithEquipment])
async def list_military_branches(
    country_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[MilitaryBranch]:
    """List military branches for a country."""
    query = (
        select(MilitaryBranch)
        .where(MilitaryBranch.country_id == country_id)
        .options(selectinload(MilitaryBranch.equipment))
        .order_by(MilitaryBranch.name)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


# Equipment endpoints
@router.post("/branches/{branch_id}/equipment", response_model=MilitaryEquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    branch_id: str,
    equipment_in: MilitaryEquipmentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MilitaryEquipment:
    """Add equipment to a military branch."""
    # Verify branch exists
    result = await db.execute(select(MilitaryBranch).where(MilitaryBranch.id == branch_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Military branch not found",
        )
    
    equipment = MilitaryEquipment(**equipment_in.model_dump())
    equipment.branch_id = branch_id
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment
