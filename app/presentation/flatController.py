from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import FlatService
from app.domain import FlatCreate, FlatResponse, FlatBase, FlatCreateDiffOwner, MessageResponse
from app.security import JWTBearer, decode_jwt

router = APIRouter(
    prefix="/flats", 
    tags=["Flats"]
)

@router.post("/asRealEstate", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=FlatResponse)
async def createFlat(flatData: FlatCreate, flatService: FlatService = Depends(), payload: dict = Depends(decode_jwt)):
    realEstateId: int = payload.get("id")
    try:
        return await flatService.createFlatasRealEstate(flatData, realEstateId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/forDiffOwners", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner"]))], response_model=FlatResponse)
async def createFlatDiffOwner(flatData: FlatCreateDiffOwner, flatService: FlatService = Depends()):
    try:
        return await flatService.createFlatDiffOwner(flatData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/flats", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[FlatResponse])
async def getAllFlats(flatService: FlatService = Depends()):
    return await flatService.readAllFlats()

@router.get("/{flatId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=FlatResponse)
async def getFlatById(flatId: int, flatService: FlatService = Depends()):
    flat = await flatService.readFlat(flatId)
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")
    return flat

@router.put("/{flat_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner"]))], response_model=MessageResponse)
async def updateFlat(flatId: int, flatData: FlatBase, flatService: FlatService = Depends()):
    try:
        updated_flat = await flatService.updateFlat(flatId, flatData)
        if not updated_flat:
            raise HTTPException(status_code=404, detail="Flat not found")
        return MessageResponse(msg="Flat updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating flat")

@router.delete("/{flatId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_flat(flatId: int, flatService: FlatService = Depends()):
    
    try:
        await flatService.deleteFlat(flatId)
        return MessageResponse(msg="Flat successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting flat")