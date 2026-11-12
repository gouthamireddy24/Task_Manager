from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True