from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.dto.user_dto import UserCreate, UserResponse

from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_all(db: Session = Depends(get_session), _: UserResponse = Depends(get_current_user)):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.get_users()

@router.get("/{user_id}", response_model=list[UserResponse])
async def get_by_id(user_id: int, db: Session = Depends(get_session), _: UserResponse = Depends(get_current_user)):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.get_users(user_id) 

@router.post("/register_user")
async def register_user(body: UserCreate, db: Session = Depends(get_session)):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.register_user(body)

@router.post("/token")
async def login(body: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_session)):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.login(body.username, body.password)
