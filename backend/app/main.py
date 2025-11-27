"""Apex Global Defense - Main Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Apex Global Defense (AGD) is an enterprise-level defense simulation 
    and strategic planning platform designed for military strategists, 
    defense analysts, intelligence professionals, and security planners.
    
    ## Features
    
    - **Global Map Integration**: Multi-layer map overlays with real-time visualization
    - **Order of Battle Database**: Comprehensive military force data for top nations
    - **Scenario Planning**: Create and simulate conflict scenarios
    - **AI-Assisted Analysis**: Optional AI features with fallback modes
    - **Project Management**: Organize analyses with projects and scenarios
    
    ## Warfare Domains
    
    - Conventional (Land, Air, Sea)
    - CBRN (Nuclear, Biological, Chemical)
    - Cyber Operations
    - Insurgent/Asymmetric Warfare
    - Terror Attack Response Planning
    """,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
    }


@app.get("/")
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": "/health",
    }
