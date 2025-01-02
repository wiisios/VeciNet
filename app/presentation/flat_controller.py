from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import FlatService
from app.domain import FlatCreate, FlatResponse, FlatBase, FlatCreateDiffOwner, MessageResponse
from app.security import JWTBearer, decode_jwt

router = APIRouter(
    prefix="/flats", 
    tags=["Flats"]
)

@router.post("/as_real_estate", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=FlatResponse)
async def create_flat(flat_data: FlatCreate, flat_service: FlatService = Depends(), payload: dict = Depends(decode_jwt)):
    real_estate_id: int = payload.get("user_id")
    try:
        return await flat_service.create_flat_as_real_estate(flat_data, real_estate_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/as_real_estate"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating flat. Please try again later.",
                "instance": "/as_real_estate"
            }
        )
    
@router.post("/for_diff_owners", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner"]))], response_model=FlatResponse)
async def create_flat_diff_owner(flat_data: FlatCreateDiffOwner, flat_service: FlatService = Depends()):
    try:
        return await flat_service.create_flat_diff_owner(flat_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/for_diff_owners"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating flat for different owners. Please try again later.",
                "instance": "/for_diff_owners"
            }
        )
    
@router.get("/all", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[FlatResponse])
async def get_all_flats(flat_service: FlatService = Depends()):
    try:
        return await flat_service.read_all_flats()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching flats. Please try again later.",
                "instance": "/users"
            }
        )

@router.get("/{flat_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=FlatResponse)
async def get_flat_by_id(flat_id: int, flat_service: FlatService = Depends()):
    try:
        flat = await flat_service.read_flat(flat_id)
        if not flat:
            raise HTTPException(
                    status_code=404,
                    detail={
                        "title": "Flat not found.",
                        "status": 404,
                        "detail": f"The flat with ID {flat_id} does not exist.",
                        "instance": f"/{flat_id}"
                    }
                )
        return flat
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching flat. Please try again later.",
                "instance": f"/{flat_id}"
            }
        )

@router.put("/{flat_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner"]))], response_model=MessageResponse)
async def update_flat(flat_id: int, flat_data: FlatBase, flat_service: FlatService = Depends()):
    try:
        updated_flat = await flat_service.update_flat(flat_id, flat_data)
        if not updated_flat:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Flat not found.",
                    "status": 404,
                    "detail": f"The flat with ID {flat_id} does not exist.",
                    "instance": f"/{flat_id}"
                }
            )
        return MessageResponse(msg="Flat updated successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": f"/{flat_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error updating flat. Please try again later.",
                "instance": f"/{flat_id}"
            }
        )

@router.delete("/{flat_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_flat(flat_id: int, flat_service: FlatService = Depends()):
    try:
        await flat_service.delete_flat(flat_id)
        return MessageResponse(msg="Flat successfully deleted") 
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "title": "Flat not found.",
                "status": 404,
                "detail": str(e),
                "instance": f"/{flat_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error deleting flat. Please try again later.",
                "instance": f"/{flat_id}"
            }
        )