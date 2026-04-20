from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default=datetime.now())
    

