from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.note_model import PrioritiesName
from sqlmodel import SQLModel

class NoteBase(BaseModel):
    id: int
    title: str = Field(..., min_length=4, max_length=150)
    description: str = Field(..., min_length=0, max_length=150)
    createt_at: datetime
    end_date: datetime | None
    priority: PrioritiesName | None


class NoteCreate(SQLModel):
    title: str = Field(..., min_length=4, max_length=150)
    description: str = Field(..., min_length=0, max_length=150)
    end_date: datetime | None
    priority: PrioritiesName | None

class NoteUpdate(SQLModel):
    title: str
    description: Optional[str] = None
    end_date: Optional[datetime] = None
    priority: Optional[PrioritiesName] = None

class NotePriority(SQLModel):
    id: int
    priority: PrioritiesName
