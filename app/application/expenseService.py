from typing import List
from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories import ExpenseRepository, Expense_UserRepository, UserRepository, ExpenseItemRepository
from app.config import getDb
from app.domain import ExpenseCreate, ExpenseResponse, ExpenseBase


class ExpenseService:
    def __init__(self, db: Session = Depends(getDb)):
        self.expenseRepository = ExpenseRepository(db)
        self.expense_userRepository = Expense_UserRepository(db)
        self.userRepository = UserRepository(db)
        self.expenseItemRepository = ExpenseItemRepository(db)

    async def createExpense(self, expenseData: ExpenseCreate) -> ExpenseResponse:
        items = []
        for i in expenseData.items:
            items.append(self.expenseItemRepository.getById(i))
        expense = self.expenseRepository.addExpense(expenseData, items)
        user = self.userRepository.getByNameAndLastNameForExpense(expenseData)
        self.expense_userRepository.addExpense_User(user.id, expense)
        return ExpenseResponse.model_validate(expense.__dict__)
    
    async def readAllExpenses(self) -> List[ExpenseResponse]:
        expenses = self.expenseRepository.getAll()
        return [ExpenseResponse.model_validate(expense.__dict__) for expense in expenses]
    
    async def readExpense(self, expenseId: int) -> ExpenseResponse:
        expense = self.expenseRepository.getById(expenseId)
        return ExpenseResponse.model_validate(expense.__dict__)
    
    async def updateExpense(self, expenseId: int, expenseData: ExpenseBase) -> ExpenseResponse:
        expense = self.expenseRepository.getById(expenseId)
        if expense:
            expense.date = expenseData.date
            self.expenseRepository.updateExpense(expense)
            return ExpenseResponse.model_validate(expense.__dict__)
        return None
    
    async def deleteExpense(self, expenseId: int) -> bool:
        expense = self.expenseRepository.getById(expenseId)
        if expense:
            self.expenseRepository.deleteExpense(expense)
            return True
        return False