from typing import List
from sqlmodel import Session, select
from app.domain import FlatBase, FlatCreate
from app.persistence.models import Flat


class FlatRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_flat(self, flat_data: FlatCreate) -> Flat:
        flat = Flat(
            number=flat_data.number, 
            building_id=flat_data.building_id,
            tenant_id=flat_data.tenant_id
            )
        self.db.add(flat) # Adding flat to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(flat) # Refreshing to fetch updated state
        return flat
    
    def get_all(self) -> List[Flat]:
        statement = select(Flat)
        return self.db.exec(statement).all()
    
    def get_by_id(self, flat_id: int) -> Flat:
        statement = select(Flat).where(Flat.id == flat_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Flat with id {flat_id} not found.")
        return result
    
    def update_flat(self, flat: FlatBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(flat) # Refresing session to ensure it is updated

    def delete_flat(self, flat: Flat) -> None:
        self.db.delete(flat) # Marking flat to be deleted
        self.db.commit() # Commiting transaction