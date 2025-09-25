# api/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# New schema for a user
class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# Updated schema for a task
class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    user: UserSchema

    class Config:
        from_attributes = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.updated_at:
            self.updated_at = self.created_at