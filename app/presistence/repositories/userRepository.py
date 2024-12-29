from sqlmodel import Session, select
from app.domain.userDto import UserBase, UserCreate, UserResponse
from app.presistence.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def addUser(self, user_data: UserCreate) -> User:
        user = User(name=user_data.name, lastName=user_data.lastName, email=user_data.email, password=user_data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def getById(self, userId: int) -> User:
        statement = select(User).where(User.id == userId)
        result = self.db.exec(statement).first()
        print(result)
        if result is None:
            raise ValueError(f"User with id {userId} not found.")
        return result
    
    def updateUser(self, user: UserBase) -> None:
        self.db.commit()
        self.db.refresh(user)

    def deleteUser(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        