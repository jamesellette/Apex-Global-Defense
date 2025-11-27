"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, countries, projects, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(countries.router, prefix="/countries", tags=["Countries"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Configuration"])
