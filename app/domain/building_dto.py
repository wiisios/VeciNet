from pydantic import BaseModel

class BuildingBase(BaseModel):
    name: str
    street: str
    city: str
    zip_code: int
    flat_amount: int

class BuildingResponse(BuildingBase):
    id: int
    
    class Config:
        orm_mode = True
        model_config ={
            'from_attributes': True
        }