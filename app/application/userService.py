from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories import UserRepository
from app.config import getDb
from app.domain import UserCreate, UserResponse, UserBase, UserLogin
from app import verify_password


class UserService:
    def __init__(self, db: Session = Depends(getDb)):
        self.userRepository = UserRepository(db)

    async def createUser(self, userData: UserCreate) -> UserResponse:
        user = self.userRepository.addUser(userData)
        return UserResponse.model_validate(user.__dict__)
    
    async def readUser(self, userId: int) -> UserResponse:
        user = self.userRepository.getById(userId)
        return UserResponse.model_validate(user.__dict__)
    
    async def readAllUsers(self) -> List[UserResponse]:
        users = self.userRepository.getAll()
        return [UserResponse.model_validate(user.__dict__) for user in users]
    
    async def updateUser(self, userId: int, userData: UserBase) -> UserResponse:
        user = self.userRepository.getById(userId)
        if user:
            user.name = userData.name
            user.lastName = userData.lastName
            user.email = userData.email
            self.userRepository.updateUser(user)
            return UserResponse.model_validate(user.__dict__)
        return None
    
    async def deleteUser(self, userId: int) -> bool:
        user = self.userRepository.getById(userId)
        if user:
            self.userRepository.deleteUser(user)
            return True
        return False
    
    async def check_user(self, data: UserLogin) -> UserResponse:
        user = self.userRepository.getByEmail(data.email)
        if verify_password(data.password, user.password):
            return UserResponse.model_validate(user.__dict__)
        return None