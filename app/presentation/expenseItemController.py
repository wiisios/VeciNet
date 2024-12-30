from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseItemService
from app.domain import ExpenseItemResponse, ExpenseItemBase, MessageResponse

router = APIRouter(
    prefix="/expenseItems", 
    tags=["ExpenseItems"]
)

@router.post("/", response_model=ExpenseItemResponse)
async def createExpenseItem(expenseItemData: ExpenseItemBase, expenseItemService: ExpenseItemService = Depends()):
    try:
        return await expenseItemService.createExpenseItem(expenseItemData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{expenseItemId}", response_model=ExpenseItemResponse)
async def getExpenseItemById(expenseItemId: int, expenseItemService: ExpenseItemService = Depends()):
    expenseItem = await expenseItemService.readExpenseItem(expenseItemId)
    if not expenseItem:
        raise HTTPException(status_code=404, detail="ExpenseItem not found")
    return expenseItem

@router.put("/{expenseItem_id}", response_model=MessageResponse)
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

@router.delete("/{expenseItemId}", response_model=MessageResponse)
async def delete_expenseItem(expenseItemId: int, expenseItemService: ExpenseItemService = Depends()):
    
    try:
        await expenseItemService.deleteExpenseItem(expenseItemId)
        return MessageResponse(msg="ExpenseItem successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting expenseItem")