from pydantic import BaseModel


class PropertyBase(BaseModel):
    flat_id: int
    owner_id: int

class PropertyResponse(PropertyBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }