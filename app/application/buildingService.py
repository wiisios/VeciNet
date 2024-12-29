from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories import BuildingRepository
from app.config import getDb
from app.domain import BuildingResponse, BuildingBase


class BuildingService:
    def __init__(self, db: Session = Depends(getDb)):
        self.buildingRepository = BuildingRepository(db)

    async def createBuilding(self, buildingData: BuildingBase) -> BuildingResponse:
        building = self.buildingRepository.addBuilding(buildingData)
        return BuildingResponse.model_validate(building.__dict__)
    
    async def readBuilding(self, buildingId: int) -> BuildingResponse:
        building = self.buildingRepository.getById(buildingId)
        if building:
            building_dict = {
                "id": building.id,
                "name": building.name,
                "street": building.street,
                "city": building.city,
                "zipCode": building.zipCode,
                "flatAmount": building.flatAmount
            }
            return BuildingResponse.model_validate(building_dict)
        return None
    
    async def updateBuilding(self, buildingId: int, buildingData: BuildingBase) -> BuildingResponse:
        building = self.buildingRepository.getById(buildingId)
        if building:
            building.name = buildingData.name
            building.street = buildingData.street
            building.city = buildingData.city
            building.zipCode = buildingData.zipCode
            building.flatAmount = buildingData.flatAmount
            self.buildingRepository.updateBuilding(building)
            return BuildingResponse.model_validate(building.__dict__)
        return None
    
    async def deleteBuilding(self, buildingId: int) -> bool:
        building = self.buildingRepository.getById(buildingId)
        if building:
            self.buildingRepository.deleteBuilding(building)
            return True
        return False