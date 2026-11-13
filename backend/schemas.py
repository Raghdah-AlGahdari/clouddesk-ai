from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: Literal["user", "agent"]
    created_at: datetime


class TicketCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str
    priority: Literal["low", "medium", "high"] = "medium"


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "closed"]
    user_id: int
    created_at: datetime
