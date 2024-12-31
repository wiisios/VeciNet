from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseItemService
from app.domain import ExpenseItemResponse, ExpenseItemBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/expenseItems", 
    tags=["ExpenseItems"]
)

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=ExpenseItemResponse)
async def createExpenseItem(expenseItemData: ExpenseItemBase, expenseItemService: ExpenseItemService = Depends()):
    try:
        return await expenseItemService.createExpenseItem(expenseItemData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/expenseItems", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[ExpenseItemResponse])
async def getAllExpenseItems(expenseItemService: ExpenseItemService = Depends()):
    return await expenseItemService.readAllExpenseItems()

@router.get("/{expenseItemId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=ExpenseItemResponse)
async def getExpenseItemById(expenseItemId: int, expenseItemService: ExpenseItemService = Depends()):
    expenseItem = await expenseItemService.readExpenseItem(expenseItemId)
    if not expenseItem:
        raise HTTPException(status_code=404, detail="ExpenseItem not found")
    return expenseItem

@router.put("/{expenseItem_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=MessageResponse)
async def updateExpenseItem(expenseItemId: int, expenseItemData: ExpenseItemBase, expenseItemService: ExpenseItemService = Depends()):
    try:
        updated_expenseItem = await expenseItemService.updateExpenseItem(expenseItemId, expenseItemData)
        if not updated_expenseItem:
            raise HTTPException(status_code=404, detail="ExpenseItem not found")
        return MessageResponse(msg="ExpenseItem updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating expenseItem")

@router.delete("/{expenseItemId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_expenseItem(expenseItemId: int, expenseItemService: ExpenseItemService = Depends()):
    
    try:
        await expenseItemService.deleteExpenseItem(expenseItemId)
        return MessageResponse(msg="ExpenseItem successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting expenseItem")