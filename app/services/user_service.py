from app.core.exceptions import InternalError, UserNotFound, UserCredentialsMismatch

from app.repositories.user_repo import UserRepository
from app.dto.user_dto import UserCreate, UserResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.models.user_model import User

from app.core.auth import create_access_token

pass_hasher = PasswordHasher()

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_users(self):
        user_data = self.repo.get_all()
        return user_data
        
    def get_user_by_id(self, id: int):
        user_data = self.repo.get_by_id(id)
        if not user_data:
            raise UserNotFound("User not Found")
        return user_data
        
    def register_user(self, user_data: UserCreate) -> UserResponse:
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = pass_hasher.hash(user_data.password)
        
        new_user = User(**user_dict)
        user = self.repo.create(new_user)
        return user 

    
    def login(self, username: str, password: str):
        try:
            user = self.repo.get_user_by_username(username)
            if not user: 
                raise UserCredentialsMismatch()
            pass_hasher.verify(user.hashed_password, password)
            token = create_access_token({"sub": user.username})
            return { "access_token": token, "token_type": "bearer" }
        except VerifyMismatchError:
            raise UserCredentialsMismatch()
        except UserCredentialsMismatch:
            raise
