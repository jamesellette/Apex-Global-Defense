"""Test configuration for the FastAPI application."""
import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Get authorization headers for authenticated requests."""
    # Register a test user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {}
