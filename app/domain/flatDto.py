from pydantic import BaseModel


class FlatBase(BaseModel):
    number: str

class FlatCreate(FlatBase):
    buildingId: int
    tenantId: int

class FlatCreateDiffOwner(FlatCreate):
    ownerName: str
    ownerLastName: str

class FlatResponse(FlatBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }