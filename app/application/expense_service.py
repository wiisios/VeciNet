from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.persistence.repositories import ExpenseRepository, ExpenseUserRepository, UserRepository, ExpenseItemRepository
from app.config import get_db
from app.domain import ExpenseCreate, ExpenseResponse, ExpenseBase


class ExpenseService:
    def __init__(self, db: Session = Depends(get_db)): # Initializing service with db session to interact with repositories
        self.expense_repository = ExpenseRepository(db)
        self.expense_user_repository = ExpenseUserRepository(db)
        self.user_repository = UserRepository(db)
        self.expense_item_repository = ExpenseItemRepository(db)

    async def create_expense(self, expense_data: ExpenseCreate) -> ExpenseResponse:
        items = []
        for i in expense_data.items:
            items.append(self.expense_item_repository.get_by_id(i)) # Creates a list of expense items obtaining every object from db
        expense = self.expense_repository.add_expense(expense_data, items) # Adds expense with related items
        user = self.user_repository.get_by_name_and_last_name_for_expense(expense_data) # Calling repository to get user related to expense
        self.expense_user_repository.add_expense_user(user.id, expense) # Creates the relationship between the user and the expense
        return ExpenseResponse(id=expense.id, date=expense.date, total_cost=expense.total_cost, items=expense.items) # Returns response with data of expense created
    
    async def read_all_expenses(self) -> List[ExpenseResponse]:
        expenses = self.expense_repository.get_all() # Calling repository to get all expenses
        return [ExpenseResponse.model_validate(expense.__dict__) for expense in expenses] # Returns a list with details of all expenses
    
    async def read_expense(self, expense_id: int) -> ExpenseResponse:
        expense = self.expense_repository.get_by_id(expense_id) # Calling repository to get expense by ID
        return ExpenseResponse(id=expense.id, date=expense.date, total_cost=expense.total_cost, items=expense.items) # Returns response with expense details
    
    async def update_expense(self, expense_id: int, expense_data: ExpenseBase) -> ExpenseResponse:
        expense = self.expense_repository.get_by_id(expense_id) # Calling repository to get expense by ID
        if expense:
            # Updating expense details
            expense.date = expense_data.date
            self.expense_repository.update_expense(expense) # Updating details at repository
            return ExpenseResponse(id=expense.id, date=expense.date, total_cost=expense.total_cost, items=expense.items) # Returns response with expense data updated
        return None
    
    async def delete_expense(self, expense_id: int) -> bool:
        expense = self.expense_repository.get_by_id(expense_id) # Calling repository to get expense by ID
        if expense:
            self.expense_repository.delete_expense(expense) # Deletes expense from respository
            return True
        return False