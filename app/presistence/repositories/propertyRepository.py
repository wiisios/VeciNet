from typing import List
from sqlmodel import Session, select
from app.domain import PropertyBase
from app.presistence.models import Property, Flat


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def addProperty(self, ownerId: int, flat: Flat) -> Property:
        property = Property(
            flatId=flat.id, 
            ownerId=ownerId, 
            )
        self.db.add(property)
        self.db.commit()
        self.db.refresh(property)
        return property
    
    def getAll(self) -> List[Property]:
        statement = select(Property)
        result = self.db.exec(statement).all()
        return result
    
    def getById(self, propertyId: int) -> Property:
        statement = select(Property).where(Property.id == propertyId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Property with id {propertyId} not found.")
        return result
    
    def getByFlatId(self, flatId: int) -> Property:
        statement = select(Property).where(Property.flatId == flatId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Property with flatId {flatId} not found.")
        return result
    
    def updateProperty(self, property: PropertyBase) -> None:
        self.db.commit()
        self.db.refresh(property)

    def deleteProperty(self, property: Property) -> None:
        self.db.delete(property)
        self.db.commit()