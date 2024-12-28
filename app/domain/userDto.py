from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    lastName: str
    email: EmailStr

class UserCreate(User):
    password: str

class UserResponse(User):
    id: int
    
    class Config:
        orm_mode = True

