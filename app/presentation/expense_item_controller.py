from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.application import ExpenseItemService
from app.domain import ExpenseItemResponse, ExpenseItemBase, MessageResponse
from app.security import JWTBearer

router = APIRouter(
    prefix="/expense_items", 
    tags=["Expense_items"]
)

@router.post("/", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=ExpenseItemResponse)
async def create_expense_item(expense_item_data: ExpenseItemBase, expense_item_service: ExpenseItemService = Depends()):
    try:
        return await expense_item_service.create_expense_item(expense_item_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": "/expense-items"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error creating expense item. Please try again later.",
                "instance": "/expense-items"
            }
        )
    
@router.get("/all", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=List[ExpenseItemResponse])
async def get_all_expense_items(expense_item_service: ExpenseItemService = Depends()):
    try:
        return await expense_item_service.read_all_expense_items()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching expense items. Please try again later.",
                "instance": "/users"
            }
        )
    
@router.get("/{expense_item_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate", "owner", "tenant"]))], response_model=ExpenseItemResponse)
async def get_expense_item_by_id(expense_item_id: int, expense_item_service: ExpenseItemService = Depends()):
    try:
        expense_item = await expense_item_service.read_expense_item(expense_item_id)
        if not expense_item:
            raise HTTPException(
                    status_code=404,
                    detail={
                        "title": "Expense item not found.",
                        "status": 404,
                        "detail": f"The expense item with ID {expense_item_id} does not exist.",
                        "instance": f"/{expense_item_id}"
                    }
                )
        return expense_item
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error fetching expense item. Please try again later.",
                "instance": f"/{expense_item_id}"
            }
        )

@router.put("/{expense_item_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin", "realestate"]))], response_model=MessageResponse)
async def update_expense_item(expense_item_id: int, expense_item_data: ExpenseItemBase, expense_item_service: ExpenseItemService = Depends()):
    try:
        updated_expense_item = await expense_item_service.update_expense_item(expense_item_id, expense_item_data)
        if not updated_expense_item:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Expense item not found.",
                    "status": 404,
                    "detail": f"The expense item with ID {expense_item_id} does not exist.",
                    "instance": f"/{expense_item_id}"
                }
            )
        return MessageResponse(msg="Expense item updated successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Invalid input provided.",
                "status": 400,
                "detail": str(e),
                "instance": f"/{expense_item_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error updating expense item. Please try again later.",
                "instance": f"/{expense_item_id}"
            }
        )

@router.delete("/{expense_item_id}", dependencies=[Depends(JWTBearer(allowed_roles=["admin"]))], response_model=MessageResponse)
async def delete_expense_item(expense_item_id: int, expense_item_service: ExpenseItemService = Depends()):
    
    try:
        await expense_item_service.delete_expense_item(expense_item_id)
        return MessageResponse(msg="Expense item successfully deleted") 
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "title": "Expense item not found.",
                "status": 404,
                "detail": str(e),
                "instance": f"/{expense_item_id}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "title": "An unexpected error occurred.",
                "status": 500,
                "detail": "Error deleting expense item. Please try again later.",
                "instance": f"/{expense_item_id}"
            }
        )