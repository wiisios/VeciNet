from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.persistence.repositories import BuildingRepository
from app.config import get_db
from app.domain import BuildingResponse, BuildingBase


class BuildingService:
    def __init__(self, db: Session = Depends(get_db)): # Initializing service with db session to interact with repositories
        self.building_repository = BuildingRepository(db)

    async def create_building(self, building_data: BuildingBase) -> BuildingResponse:
        building = self.building_repository.add_building(building_data) # Calling repository to add a building
        return BuildingResponse.model_validate(building.__dict__) # Returns response with data of building created
    
    async def read_all_buildings(self) -> List[BuildingResponse]:
        buildings = self.building_repository.get_all() # Calling repository to get all buildings
        return [BuildingResponse.model_validate(building.__dict__) for building in buildings] # Returns a list with details of all buildings
    
    async def read_building(self, building_id: int) -> BuildingResponse:
        building = self.building_repository.get_by_id(building_id) # Calling repository to get building by ID
        return BuildingResponse.model_validate(building.__dict__) # Returns response with building details
    
    async def update_building(self, building_id: int, building_data: BuildingBase) -> BuildingResponse:
        building = self.building_repository.get_by_id(building_id) # Calling repository to get building by ID
        if building:
            # Updating building details
            building.name = building_data.name
            building.street = building_data.street
            building.city = building_data.city
            building.zip_code = building_data.zip_code
            building.flat_amount = building_data.flat_amount
            self.building_repository.update_building(building) # Updating details at repository
            return BuildingResponse.model_validate(building.__dict__) # Returns response with building data updated
        return None
    
    async def delete_building(self, building_id: int) -> bool:
        building = self.building_repository.get_by_id(building_id) # Calling repository to get building by ID
        if building:
            self.building_repository.delete_building(building) # Deletes building from respository
            return True
        return False