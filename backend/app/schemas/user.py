"""User schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    organization: str | None = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=100)
    role: str = "viewer"


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=255)
    organization: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: str
    role: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str
    exp: int
