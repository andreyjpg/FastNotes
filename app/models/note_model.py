from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

class PrioritiesName(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Note(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default=datetime.now())
    end_date: Optional[datetime] = None
    priority: Optional[PrioritiesName] = None
    user_id: Optional[int] = Field(foreign_key="user.id")

