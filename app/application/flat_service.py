from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.persistence.repositories import FlatRepository, PropertyRepository, UserRepository
from app.config import get_db
from app.domain import FlatCreate, FlatResponse, FlatBase, FlatCreateDiffOwner


class FlatService:
    def __init__(self, db: Session = Depends(get_db)): # Initializing service with db session to interact with repositories
        self.flat_repository = FlatRepository(db) 
        self.property_repository = PropertyRepository(db)
        self.user_repository = UserRepository(db)

    async def create_flat_as_real_estate(self, flat_data: FlatCreate, real_estate_id: int) -> FlatResponse:
        flat = self.flat_repository.add_flat(flat_data) # Creates a new flat
        self.property_repository.add_property(real_estate_id, flat) # Creates the relationship between owner (real estate) and flat
        return FlatResponse(id=flat.id, number=flat.number)  # Returns response with data of flat created
    
    async def create_flat_diff_owner(self, flat_data: FlatCreateDiffOwner) -> FlatResponse:
        flat = self.flat_repository.add_flat(flat_data) # Creates a new flat
        user = self.user_repository.get_by_name_and_last_name_for_flat(flat_data) # Calling repository to get owner by name and last name
        self.property_repository.add_property(user.id, flat) # Creates the relationship between owner (person) and flat
        return FlatResponse(id=flat.id, number=flat.number) # Returns response with data of flat created
    
    async def read_all_flats(self) -> List[FlatResponse]:
        flats = self.flat_repository.get_all() # Calling repository to get all flats
        return [FlatResponse.model_validate(flat.__dict__) for flat in flats] # Returns a list with details of all flats
    
    async def read_flat(self, flat_id: int) -> FlatResponse:
        flat = self.flat_repository.get_by_id(flat_id) # Calling repository to get flat by ID
        return FlatResponse.model_validate(flat.__dict__) # Returns response with flat details
    
    async def update_flat(self, flat_id: int, flat_data: FlatBase) -> FlatResponse:
        flat = self.flat_repository.get_by_id(flat_id) # Calling repository to get flat by ID
        if flat:
            # Updating flat details
            flat.number = flat_data.number
            self.flat_repository.update_flat(flat) # Updating details at repository
            return FlatResponse.model_validate(flat.__dict__) # Returns response with flat data updated
        return None
    
    async def delete_flat(self, flat_id: int) -> bool:
        flat = self.flat_repository.get_by_id(flat_id) # Calling repository to get flat by ID
        if flat:
            property = self.property_repository.get_by_flat_id(flat_id) # Calling repository to get property by flat ID
            self.property_repository.delete_property(property) # Deletes property from respository
            self.flat_repository.delete_flat(flat) # Deletes flat from respository
            return True
        return False