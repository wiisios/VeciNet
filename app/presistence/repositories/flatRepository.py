from typing import List
from sqlmodel import Session, select
from app.domain import FlatBase, FlatCreate
from app.presistence.models import Flat


class FlatRepository:
    def __init__(self, db: Session):
        self.db = db

    def addFlat(self, flatData: FlatCreate) -> Flat:
        flat = Flat(
            number=flatData.number, 
            buildingId=flatData.buildingId,
            tenantId=flatData.tenantId
            )
        self.db.add(flat)
        self.db.commit()
        self.db.refresh(flat)
        return flat
    
    def getAll(self) -> List[Flat]:
        statement = select(Flat)
        result = self.db.exec(statement).all()
        return result
    
    def getById(self, flatId: int) -> Flat:
        statement = select(Flat).where(Flat.id == flatId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Flat with id {flatId} not found.")
        return result
    
    def updateFlat(self, flat: FlatBase) -> None:
        self.db.commit()
        self.db.refresh(flat)

    def deleteFlat(self, flat: Flat) -> None:
        self.db.delete(flat)
        self.db.commit()