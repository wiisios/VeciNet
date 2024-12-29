from fastapi import APIRouter, Depends, HTTPException
from app.application import UserService
from app.domain import UserCreate, UserResponse, UserBase, MessageResponse

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def createUser(userData: UserCreate, userService: UserService = Depends()):
    try:
        return await userService.createUser(userData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{userId}", response_model=UserResponse)
async def getUserById(userId: int, userService: UserService = Depends()):
    user = await userService.readUser(userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=MessageResponse)
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

@router.delete("/users/{userId}", response_model=MessageResponse)
async def delete_user(userId: int, userService: UserService = Depends()):
    
    try:
        await userService.deleteUser(userId)
        return MessageResponse(msg="User successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting user")
