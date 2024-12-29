from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    lastName: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
        model_config ={
            'from_attributes': True
        }



