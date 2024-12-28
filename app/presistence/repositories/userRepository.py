from sqlmodel import Session
from app.domain.userDto import User, UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user_data: UserCreate) -> User:
        user = User(name=user_data.name, email=user_data.email, password=user_data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user