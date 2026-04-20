from sqlmodel import Session, select
from app.models.user_model import User
from app.dto.user_dto import UserResponse, UserLogin

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(User)
        return self.session.exec(statement).all()
    
    def get_by_id(self, user_id: int):
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()
    
    def create(self, db_user: User):
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
    
    def get_user_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()
        
