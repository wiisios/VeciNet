from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import BuildingService
from app.domain import BuildingResponse, BuildingBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/buildings", 
    tags=["Buildings"]
    )

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate"]))], response_model=BuildingResponse)
async def create_building(building_data: BuildingBase, building_service: BuildingService = Depends()):
    try:
        return await building_service.create_building(building_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/buildings"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating building. Please try again later.",
                "instance": "/buildings"
            }
        )
    
@router.get("/all", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[BuildingResponse])
async def get_all_buildings(building_service: BuildingService = Depends()):
    try:
        return await building_service.read_all_buildings()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching buildings. Please try again later.",
                "instance": "/users"
            }
        )
    
@router.get("/{building_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate", "owner", "tenant"]))], response_model=BuildingResponse)
async def get_building_by_id(building_id: int, building_service: BuildingService = Depends()):
    try:
        building = await building_service.read_building(building_id)
        if not building:
            raise HTTPException(
                    status_code=404,
                    detail={
                        "title": "Building not found.",
                        "status": 404,
                        "detail": f"The building with ID {building_id} does not exist.",
                        "instance": f"/{building_id}"
                    }
                )
        return building
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching building. Please try again later.",
                "instance": f"/{building_id}"
            }
        )

@router.put("/{building_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate"]))], response_model=MessageResponse)
async def update_building(building_id: int, building_data: BuildingBase, building_service: BuildingService = Depends()):
    try:
        updated_building = await building_service.update_building(building_id, building_data)
        if not updated_building:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Building not found.",
                    "status": 404,
                    "detail": f"The building with ID {building_id} does not exist.",
                    "instance": f"/{building_id}"
                }
            )
        return MessageResponse(msg="Building updated successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": f"/{building_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error updating building. Please try again later.",
                "instance": f"/{building_id}"
            }
        )

@router.delete("/{building_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_building(building_id: int, building_service: BuildingService = Depends()): 
    try:
        await building_service.delete_building(building_id)
        return MessageResponse(msg="Building successfully deleted") 
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "title": "Building not found.",
                "status": 404,
                "detail": str(e),
                "instance": f"/{building_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error deleting building. Please try again later.",
                "instance": f"/{building_id}"
            }
        )