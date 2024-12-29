from pydantic import BaseModel

class BuildingBase(BaseModel):
    name: str
    street: str
    city: str
    zipCode: int
    flatAmount: int

class BuildingResponse(BuildingBase):
    id: int
    
    class Config:
        orm_mode = True
        model_config ={
            'from_attributes': True
        }