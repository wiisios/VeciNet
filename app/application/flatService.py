from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories import FlatRepository, PropertyRepository, UserRepository
from app.config import getDb
from app.domain import FlatCreate, FlatResponse, FlatBase, FlatCreateDiffOwner


class FlatService:
    def __init__(self, db: Session = Depends(getDb)):
        self.flatRepository = FlatRepository(db)
        self.propertyRepository = PropertyRepository(db)
        self.userRepository = UserRepository(db)

    async def createFlatasRealEstate(self, flatData: FlatCreate, realEstateId: int) -> FlatResponse:
        flat = self.flatRepository.addFlat(flatData, realEstateId)
        self.propertyRepository.addProperty(realEstateId, flat)
        return FlatResponse.model_validate(flat.__dict__)
    
    async def createFlatDiffOwner(self, flatData: FlatCreateDiffOwner) -> FlatResponse:
        flat = self.flatRepository.addFlat(flatData)
        user = self.userRepository.getByNameAndLastNameForFlat(flatData)
        self.propertyRepository.addProperty(user.id, flat)
        return FlatResponse.model_validate(flat.__dict__)
    
    async def readAllFlats(self) -> List[FlatResponse]:
        flats = self.flatRepository.getAll()
        return [FlatResponse.model_validate(flat.__dict__) for flat in flats]
    
    async def readFlat(self, flatId: int) -> FlatResponse:
        flat = self.flatRepository.getById(flatId)
        return FlatResponse.model_validate(flat.__dict__)
    
    async def updateFlat(self, flatId: int, flatData: FlatBase) -> FlatResponse:
        flat = self.flatRepository.getById(flatId)
        if flat:
            flat.number = flatData.number
            self.flatRepository.updateFlat(flat)
            return FlatResponse.model_validate(flat.__dict__)
        return None
    
    async def deleteFlat(self, flatId: int) -> bool:
        flat = self.flatRepository.getById(flatId)
        if flat:
            property = self.propertyRepository.getByFlatId(flatId)
            self.propertyRepository.deleteProperty(property)
            self.flatRepository.deleteFlat(flat)
            return True
        return False