from typing import List
from sqlmodel import Session, select
from app.domain import ExpenseBase
from app.presistence.models import Expense, ExpenseItem
from app import Helpers

class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def addExpense(self, expense_data: ExpenseBase, items: List[ExpenseItem]) -> Expense:
        totalCost = Helpers.calculateTotalExpense(items)
        expense = Expense(
            date=expense_data.date, 
            totalCost=totalCost, 
            items=items, 
            )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense
    
    def getAll(self) -> List[Expense]:
        statement = select(Expense)
        result = self.db.exec(statement).all()
        return result
    
    def getById(self, expenseId: int) -> Expense:
        statement = select(Expense).where(Expense.id == expenseId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Expense with id {expenseId} not found.")
        return result
    
    def updateExpense(self, expense: ExpenseBase) -> None:
        self.db.commit()
        self.db.refresh(expense)

    def deleteExpense(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()