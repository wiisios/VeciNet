from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseService
from app.domain import ExpenseCreate, ExpenseResponse, ExpenseBase, MessageResponse

router = APIRouter(
    prefix="/expenses", 
    tags=["Expenses"]
)

@router.post("/", response_model=ExpenseResponse)
async def createExpense(expenseData: ExpenseCreate, expenseService: ExpenseService = Depends()):
    try:
        return await expenseService.createExpense(expenseData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{expenseId}", response_model=ExpenseResponse)
async def getExpenseById(expenseId: int, expenseService: ExpenseService = Depends()):
    expense = await expenseService.readExpense(expenseId)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=MessageResponse)
async def updateExpense(expenseId: int, expenseData: ExpenseBase, expenseService: ExpenseService = Depends()):
    try:
        updated_expense = await expenseService.updateExpense(expenseId, expenseData)
        if not updated_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return MessageResponse(msg="Expense updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating expense")

@router.delete("/{expenseId}", response_model=MessageResponse)
async def delete_expense(expenseId: int, expenseService: ExpenseService = Depends()):
    
    try:
        await expenseService.deleteExpense(expenseId)
        return MessageResponse(msg="Expense successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting expense")