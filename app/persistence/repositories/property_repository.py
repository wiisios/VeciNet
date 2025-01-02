from typing import List
from sqlmodel import Session, select
from app.domain import PropertyBase
from app.persistence.models import Property, Flat


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_property(self, owner_id: int, flat: Flat) -> Property:
        property = Property(
            flat_id=flat.id, 
            owner_id=owner_id, 
            )
        self.db.add(property) # Adding property to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(property) # Refreshing to fetch updated state
        return property
    
    def get_all(self) -> List[Property]:
        statement = select(Property)
        return self.db.exec(statement).all()
    
    def get_by_id(self, property_id: int) -> Property:
        statement = select(Property).where(Property.id == property_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Property with id {property_id} not found.")
        return result
    
    def get_by_flat_id(self, flat_id: int) -> Property:
        statement = select(Property).where(Property.flat_id == flat_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Property with flat_id {flat_id} not found.")
        return result
    
    def update_property(self, property: PropertyBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(property) # Refresing session to ensure it is updated

    def delete_property(self, property: Property) -> None:
        self.db.delete(property) # Marking property to be deleted
        self.db.commit() # Commiting transaction