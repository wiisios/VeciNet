from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories.userRepository import UserRepository
from app.config.database import getDb
from app.domain import UserCreate, UserResponse


class UserService:
    def __init__(self, db: Session = Depends(getDb)):
        self.userRepository = UserRepository(db)

    def createUser(self, userData: UserCreate) -> UserResponse:
        user = self.userRepository.addUser(userData)
        return UserResponse.model_config(user)
    
    def readUser():
        return None
    
    def updateUser():
        return None
    
    def deleteUser():
        return None