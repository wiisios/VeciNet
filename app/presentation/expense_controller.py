from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseService
from app.domain import ExpenseCreate, ExpenseResponse, ExpenseBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/expenses", 
    tags=["Expenses"]
)

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate"]))], response_model=ExpenseResponse)
async def create_expense(expense_data: ExpenseCreate, expense_service: ExpenseService = Depends()):
    try:
        return await expense_service.create_expense(expense_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/expenses"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating expense. Please try again later.",
                "instance": "/expenses"
            }
        )
    
@router.get("/all", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[ExpenseResponse])
async def get_all_expenses(expense_service: ExpenseService = Depends()):
    try:
        return await expense_service.read_all_expenses()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching expenses. Please try again later.",
                "instance": "/users"
            }
        )
    
@router.get("/{expense_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate", "owner", "tenant"]))], response_model=ExpenseResponse)
async def get_expense_by_id(expense_id: int, expense_service: ExpenseService = Depends()):
    try:
        expense = await expense_service.read_expense(expense_id)
        if not expense:
            raise HTTPException(
                    status_code=404,
                    detail={
                        "title": "Expense not found.",
                        "status": 404,
                        "detail": f"The expense with ID {expense_id} does not exist.",
                        "instance": f"/{expense_id}"
                    }
                )
        return expense
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": f"Error fetching expense. Please try again later. Details: {e}",
                "instance": f"/{expense_id}"
            }
        )

@router.put("/{expense_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "real_estate"]))], response_model=MessageResponse)
async def update_expense(expense_id: int, expense_data: ExpenseBase, expense_service: ExpenseService = Depends()):
    try:
        updated_expense = await expense_service.update_expense(expense_id, expense_data)
        if not updated_expense:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Expense not found.",
                    "status": 404,
                    "detail": f"The expense with ID {expense_id} does not exist.",
                    "instance": f"/{expense_id}"
                }
            )
        return MessageResponse(msg="Expense updated successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": f"/{expense_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error updating expense. Please try again later.",
                "instance": f"/{expense_id}"
            }
        )

@router.delete("/{expense_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_expense(expense_id: int, expense_service: ExpenseService = Depends()):
    try:
        await expense_service.delete_expense(expense_id)
        return MessageResponse(msg="Expense successfully deleted") 
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "title": "Expense not found.",
                "status": 404,
                "detail": str(e),
                "instance": f"/{expense_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error deleting expense. Please try again later.",
                "instance": f"/{expense_id}"
            }
        )