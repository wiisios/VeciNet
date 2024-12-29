from pydantic import BaseModel


class PropertyBase(BaseModel):
    flatId: int
    ownerId: int

class PropertyResponse(PropertyBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }