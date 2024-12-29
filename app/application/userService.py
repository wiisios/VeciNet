from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories.userRepository import UserRepository
from app.config.database import getDb
from app.domain import UserCreate, UserResponse, UserBase


class UserService:
    def __init__(self, db: Session = Depends(getDb)):
        self.userRepository = UserRepository(db)

    async def createUser(self, userData: UserCreate) -> UserResponse:
        user = self.userRepository.addUser(userData)
        return UserResponse.model_validate(user.__dict__)
    
    async def readUser(self, userId: int) -> UserResponse:
        user = self.userRepository.getById(userId)
        print(user)
        if user:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "lastName": user.lastName,
                "email": user.email
            }
            return UserResponse.model_validate(user_dict)
        return None
    
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