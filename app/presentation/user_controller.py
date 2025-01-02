from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import UserService
from app.domain import UserCreate, UserResponse, UserBase, MessageResponse, UserLogin
from app.security import sign_jwt, JWTBearer

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
    )

@router.post("/register")
async def create_user(user_data: UserCreate, user_service: UserService = Depends()):
    try:
        await user_service.create_user(user_data)
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/register"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating user. Please try again later.",
                "instance": "/register"
            }
        )
    
@router.post("/login")
async def login(user_data: UserLogin, user_service: UserService = Depends()):
    try:
        user = await user_service.check_user(user_data)
        if user:
            return sign_jwt(user)
        raise HTTPException(
                status_code=401,
                detail={
                    "title": "Invalid login details.",
                    "status": 401,
                    "detail": "Wrong username or password.",
                    "instance": "/login"
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error during login. Please try again later.",
                "instance": "/login"
            }
        )

@router.get("/all", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[UserResponse])
async def get_all_users(user_service: UserService = Depends()):
    try:
        return await user_service.read_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching users. Please try again later.",
                "instance": "/users"
            }
        )

@router.get("/{user_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=UserResponse)
async def get_user_by_id(user_id: int, user_service: UserService = Depends()):
    try:
        user = await user_service.read_user(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "User not found.",
                    "status": 404,
                    "detail": f"The user with ID {user_id} does not exist.",
                    "instance": f"/{user_id}"
                }
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching user. Please try again later.",
                "instance": f"/{user_id}"
            }
        )

@router.put("/{user_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def update_user(user_id: int, user_data: UserBase, user_service: UserService = Depends()):
    try:
        updated_user = await user_service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "User not found.",
                    "status": 404,
                    "detail": f"The user with ID {user_id} does not exist.",
                    "instance": f"/{user_id}"
                }
            )
        return MessageResponse(msg="User updated successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": f"/{user_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error updating user. Please try again later.",
                "instance": f"/{user_id}"
            }
        )
    
@router.delete("/{user_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_user(user_id: int, user_service: UserService = Depends()):
    try:
        await user_service.delete_user(user_id)
        return MessageResponse(msg="User successfully deleted")
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "title": "User not found.",
                "status": 404,
                "detail": str(e),
                "instance": f"/{user_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error deleting user. Please try again later.",
                "instance": f"/{user_id}"
            }
        )