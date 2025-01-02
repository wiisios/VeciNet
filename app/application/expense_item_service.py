from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.persistence.repositories import ExpenseItemRepository
from app.config import get_db
from app.domain import ExpenseItemResponse, ExpenseItemBase


class ExpenseItemService:
    def __init__(self, db: Session = Depends(get_db)): # Initializing service with db session to interact with repositories
        self.expense_item_repository = ExpenseItemRepository(db)

    async def create_expense_item(self, expense_item_data: ExpenseItemBase) -> ExpenseItemResponse:
        expense_item = self.expense_item_repository.add_expense_item(expense_item_data) # Calling repository to add an expense item
        return ExpenseItemResponse.model_validate(expense_item.__dict__) # Returns response with data of expense item created
    
    async def read_all_expense_items(self) -> List[ExpenseItemResponse]:
        expense_items = self.expense_item_repository.get_all() # Calling repository to get all expense items
        return [ExpenseItemResponse.model_validate(expense_item.__dict__) for expense_item in expense_items] # Returns a list with details of all expense items
    
    async def read_expense_item(self, expense_item_id: int) -> ExpenseItemResponse:
        expense_item = self.expense_item_repository.get_by_id(expense_item_id) # Calling repository to get expense item by ID
        return ExpenseItemResponse.model_validate(expense_item.__dict__) # Returns response with expense item details
    
    async def update_expense_item(self, expense_item_id: int, expense_item_data: ExpenseItemBase) -> ExpenseItemResponse:
        expense_item = self.expense_item_repository.get_by_id(expense_item_id) # Calling repository to get expense item by ID
        if expense_item:
            # Updating expense item details
            expense_item.reason = expense_item_data.reason
            expense_item.description = expense_item_data.description
            expense_item.cost = expense_item_data.cost
            expense_item.invoice_img = expense_item_data.invoice_img
            self.expense_item_repository.update_expense_item(expense_item) # Updating details at repository
            return ExpenseItemResponse.model_validate(expense_item.__dict__) # Returns response with expense item data updated
        return None
    
    async def delete_expense_item(self, expense_item_id: int) -> bool:
        expense_item = self.expense_item_repository.get_by_id(expense_item_id) # Calling repository to get expense item by ID
        if expense_item:
            self.expense_item_repository.delete_expense_item(expense_item) # Deletes expense item from respository
            return True
        return False