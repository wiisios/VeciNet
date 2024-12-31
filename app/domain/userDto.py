from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    lastName: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):   
    id: int
    role: str
    
    class Config:
        model_config ={
            'from_attributes': True
        }



