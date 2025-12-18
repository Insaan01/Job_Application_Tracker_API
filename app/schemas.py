from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    company: str
    role: str


class ApplicationStatusCreate(BaseModel):
    status: str
    note: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
