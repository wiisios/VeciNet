from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import BuildingService
from app.domain import BuildingResponse, BuildingBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/buildings", 
    tags=["Buildings"]
    )

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=BuildingResponse)
async def createBuilding(buildingData: BuildingBase, buildingService: BuildingService = Depends()):
    try:
        return await buildingService.createBuilding(buildingData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/buildings", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[BuildingResponse])
async def getAllBuildings(buildingService: BuildingService = Depends()):
    return await buildingService.readAllBuildings()

@router.get("/{buildingId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=BuildingResponse)
async def getBuildingById(buildingId: int, buildingService: BuildingService = Depends()):
    building = await buildingService.readBuilding(buildingId)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.put("/{building_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=MessageResponse)
async def updateBuilding(buildingId: int, buildingData: BuildingBase, buildingService: BuildingService = Depends()):
    try:
        updated_building = await buildingService.updateBuilding(buildingId, buildingData)
        if not updated_building:
            raise HTTPException(status_code=404, detail="Building not found")
        return MessageResponse(msg="Building updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating building")

@router.delete("/{buildingId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_building(buildingId: int, buildingService: BuildingService = Depends()): 
    try:
        await buildingService.deleteBuilding(buildingId)
        return MessageResponse(msg="Building successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting building")