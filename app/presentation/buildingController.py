from fastapi import APIRouter, Depends, HTTPException
from app.application import BuildingService
from app.domain import BuildingResponse, BuildingBase, MessageResponse

router = APIRouter()

@router.post("/buildings/", response_model=BuildingResponse)
async def createBuilding(buildingData: BuildingBase, buildingService: BuildingService = Depends()):
    try:
        return await buildingService.createBuilding(buildingData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/buildings/{buildingId}", response_model=BuildingResponse)
async def getBuildingById(buildingId: int, buildingService: BuildingService = Depends()):
    building = await buildingService.readBuilding(buildingId)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.put("/buildings/{building_id}", response_model=MessageResponse)
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

@router.delete("/buildings/{buildingId}", response_model=MessageResponse)
async def delete_building(buildingId: int, buildingService: BuildingService = Depends()):
    
    try:
        await buildingService.deleteBuilding(buildingId)
        return MessageResponse(msg="Building successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting building")