from typing import List
from pydantic import EmailStr
from sqlmodel import Session, select
from app.domain import UserBase, UserCreate, FlatCreateDiffOwner, ExpenseCreate, UserResponse
from app.persistence.models import User
from app import hash_password


class   UserRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_user(self, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password) # Hashing user's password
        user = User(
            name=user_data.name, 
            last_name=user_data.last_name, 
            email=user_data.email, 
            password=hashed_password
            )
        self.db.add(user) # Adding user to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(user) # Refreshing to fetch updated state
        return user
    
    def get_all(self) -> List[User]:
        statement = select(User)
        return self.db.exec(statement).all()
    
    def get_by_id(self, user_id: int) -> User:
        statement = select(User).where(User.id == user_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with id {user_id} not found.")
        return result
    
    def get_by_name_and_last_name_for_flat(self, user: FlatCreateDiffOwner) -> User:
        statement = select(User).where(
            (User.name == user.owner_name) &
            (User.last_name == user.owner_last_name))
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with id {user.owner_name} and {user.owner_last_name} not found.")
        return result
    
    def get_by_email(self, email: EmailStr) -> User:
        statement = select(User).where(User.email == email)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with id {email} not found.")
        return result
    
    def get_by_name_and_last_name_for_expense(self, user: ExpenseCreate) -> User:
        statement = select(User).where(
            (User.name == user.tenant_name) &
            (User.last_name == user.tenant_last_name))
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"User with id {user.tenant_name} and {user.tenant_last_name} not found.")
        return result
    
    def update_user(self, user: UserBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(user) # Refresing session to ensure it is updated

    def delete_user(self, user: User) -> None:
        self.db.delete(user) # Marking user to be deleted
        self.db.commit() # Commiting transaction
        