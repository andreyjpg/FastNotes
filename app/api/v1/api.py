from fastapi import APIRouter
from app.api.v1.endpoints import notes, users

api_router = APIRouter()

api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(users.router, prefix="/users", tags=["users"])