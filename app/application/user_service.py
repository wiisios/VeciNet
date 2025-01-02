from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.persistence.repositories import UserRepository
from app.config import get_db
from app.domain import UserCreate, UserResponse, UserBase, UserLogin
from app import verify_password


class UserService:
    def __init__(self, db: Session = Depends(get_db)): # Initializing service with db session to interact with repositories
        self.user_repository = UserRepository(db)  

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = self.user_repository.add_user(user_data) # Calling repository to add a user
        return UserResponse.model_validate(user.__dict__) # Returns response with data of user created
    
    async def read_user(self, user_id: int) -> UserResponse:
        user = self.user_repository.get_by_id(user_id) # Calling repository to get user by ID
        return UserResponse.model_validate(user.__dict__) # Returns response with user details
    
    async def read_all_users(self) -> List[UserResponse]:
        users = self.user_repository.get_all() # Calling repository to get all users
        return [UserResponse.model_validate(user.__dict__) for user in users] # Returns a list with details of all users
    
    async def update_user(self, user_id: int, user_data: UserBase) -> UserResponse:
        user = self.user_repository.get_by_id(user_id) # Calling repository to get user by ID
        if user:
            # Updating user details
            user.name = user_data.name
            user.last_name = user_data.last_name
            user.email = user_data.email
            self.user_repository.update_user(user) # Updating details at repository
            return UserResponse.model_validate(user.__dict__) # Returns response with user data updated
        return None
    
    async def delete_user(self, user_id: int) -> bool:
        user = self.user_repository.get_by_id(user_id) # Calling repository to get user by ID
        if user:
            self.user_repository.delete_user(user) # Deletes user from respository
            return True
        return False
    
    async def check_user(self, data: UserLogin) -> UserResponse:
        user = self.user_repository.get_by_email(data.email) # Calling repository to get user by email
        if verify_password(data.password, user.password): # Checks user password
            return UserResponse.model_validate(user.__dict__) # Returns response with user details
        return None