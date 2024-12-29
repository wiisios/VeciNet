from sqlmodel import Session, select
from app.domain import BuildingBase
from app.presistence.models import Building


class BuildingRepository:
    def __init__(self, db: Session):
        self.db = db

    def addBuilding(self, building_data: BuildingBase) -> Building:
        building = Building(
            name=building_data.name, 
            street=building_data.street, 
            city=building_data.city, 
            zipCode=building_data.zipCode,
            flatAmount=building_data.flatAmount
            )
        self.db.add(building)
        self.db.commit()
        self.db.refresh(building)
        return building
    
    def getById(self, buildingId: int) -> Building:
        statement = select(Building).where(Building.id == buildingId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Building with id {buildingId} not found.")
        return result
    
    def updateBuilding(self, building: BuildingBase) -> None:
        self.db.commit()
        self.db.refresh(building)

    def deleteBuilding(self, building: Building) -> None:
        self.db.delete(building)
        self.db.commit()