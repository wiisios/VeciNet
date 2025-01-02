from pydantic import BaseModel


class FlatBase(BaseModel):
    number: str

class FlatCreate(FlatBase):
    building_id: int
    tenant_id: int

class FlatCreateDiffOwner(FlatCreate):
    owner_name: str
    owner_last_name: str

class FlatResponse(FlatBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }