from datetime import datetime, timedelta, timezone
from typing import Annotated

import os
from dotenv import load_dotenv
from fastapi import Depends
from pydantic import BaseModel
from app.api.errors import CredentialsException

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session
from app.core.database import get_session

from app.repositories.user_repo import UserRepository
from app.dto.user_dto import UserResponse

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("OATH_TOKEN"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, os.getenv("OATH_TOKEN"), algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("sub")
        if username is None:
            raise  CredentialsException()
        repo = UserRepository(db)
        user = repo.get_user_by_username(username)
        if not user:
            raise CredentialsException()
        user_dto = UserResponse.model_validate(user)
        return user_dto
    except:
        raise CredentialsException()
    