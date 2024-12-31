from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseService
from app.domain import ExpenseCreate, ExpenseResponse, ExpenseBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/expenses", 
    tags=["Expenses"]
)

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=ExpenseResponse)
async def createExpense(expenseData: ExpenseCreate, expenseService: ExpenseService = Depends()):
    try:
        return await expenseService.createExpense(expenseData)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/expenses", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[ExpenseResponse])
async def getAllExpenses(expenseService: ExpenseService = Depends()):
    return await expenseService.readAllExpenses()

@router.get("/{expenseId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=ExpenseResponse)
async def getExpenseById(expenseId: int, expenseService: ExpenseService = Depends()):
    expense = await expenseService.readExpense(expenseId)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=MessageResponse)
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

@router.delete("/{expenseId}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_expense(expenseId: int, expenseService: ExpenseService = Depends()):
    
    try:
        await expenseService.deleteExpense(expenseId)
        return MessageResponse(msg="Expense successfully deleted") 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting expense")