from typing import List
from pydantic import EmailStr
from sqlmodel import Session, select
from app.domain import UserBase, UserCreate, FlatCreateDiffOwner, ExpenseCreate, UserResponse
from app.presistence.models import User
from app import hash_password


class   UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def addUser(self, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password)
        user = User(
            name=user_data.name, 
            lastName=user_data.lastName, 
            email=user_data.email, 
            password=hashed_password
            )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def getAll(self) -> List[User]:
        statement = select(User)
        result = self.db.exec(statement).all()
        return result
    
    def getById(self, userId: int) -> User:
        statement = select(User).where(User.id == userId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with id {userId} not found.")
        return result
    
    def getByNameAndLastNameForFlat(self, user: FlatCreateDiffOwner) -> User:
        statement = select(User).where(
            (User.name == user.ownerName) &
            (User.lastName == user.ownerLastName))
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with name {user.ownerName} and {user.ownerLastName} not found")
        return result
    
    def getByEmail(self, email: EmailStr) -> User:
        statement = select(User).where(User.email == email)
        result = self.db.exec(statement).first()
        return result
    
    def getByNameAndLastNameForExpense(self, user: ExpenseCreate) -> User:
        statement = select(User).where(
            (User.name == user.tenantName) &
            (User.lastName == user.tenantLastName))
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with name {user.tenantName} and {user.tenantLastName} not found")
        return result
    
    def updateUser(self, user: UserBase) -> None:
        self.db.commit()
        self.db.refresh(user)

    def deleteUser(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        