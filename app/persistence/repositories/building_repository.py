from typing import List
from sqlmodel import Session, select
from app.domain import BuildingBase
from app.persistence.models import Building


class BuildingRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_building(self, building_data: BuildingBase) -> Building:
        building = Building(
            name=building_data.name, 
            street=building_data.street, 
            city=building_data.city, 
            zip_code=building_data.zip_code,
            flat_amount=building_data.flat_amount
            )
        self.db.add(building) # Adding building to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(building) # Refreshing to fetch updated state
        return building
    
    def get_all(self) -> List[Building]:
        statement = select(Building)
        return self.db.exec(statement).all()
    
    def get_by_id(self, building_id: int) -> Building:
        statement = select(Building).where(Building.id == building_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Building with id {building_id} not found.")
        return result
    
    def update_building(self, building: BuildingBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(building) # Refresing session to ensure it is updated

    def delete_building(self, building: Building) -> None:
        self.db.delete(building) # Marking building to be deleted
        self.db.commit() # Commiting transaction