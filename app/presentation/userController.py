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
async def createUser(userData: UserCreate, userService: UserService = Depends()):
    try:
        await userService.createUser(userData)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
async def login(userData: UserLogin, userService: UserService = Depends()):
    user = await userService.check_user(userData)
    if user:
        return sign_jwt(user)
    return{
        "error": "Wrong login details"
    }

@router.get("/users", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[UserResponse])
async def getAllUsers(userService: UserService = Depends()):
    return await userService.readAllUsers()

@router.get("/{userId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=UserResponse)
async def getUserById(userId: int, userService: UserService = Depends()):
    user = await userService.readUser(userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def updateUser(userId: int, userData: UserBase, userService: UserService = Depends()):
    try:
        updated_user = await userService.updateUser(userId, userData)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return MessageResponse(msg="User updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user")

@router.delete("/{userId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_user(userId: int, userService: UserService = Depends()):
    
    try:
        await userService.deleteUser(userId)
        return MessageResponse(msg="User successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting user")
