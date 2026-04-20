from pydantic import Field
from sqlmodel import SQLModel
from datetime import datetime

class UserCreate(SQLModel):
    username: str = Field(..., min_length=4, max_length=15)
    password: str = Field(..., min_lenght=8)

class UserResponse(SQLModel):
    id: int 
    username: str
    created_at: datetime
        

class UserLogin(SQLModel):
    email: str
    password: str