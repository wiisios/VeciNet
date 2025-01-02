from typing import List
from sqlmodel import Session, select
from app.domain import ExpenseBase
from app.persistence.models import Expense, ExpenseItem
from app import Helpers

class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_expense(self, expense_data: ExpenseBase, items: List[ExpenseItem]) -> Expense:
        total_cost = Helpers.calculate_total_expense(items)
        expense = Expense(
            date=expense_data.date, 
            total_cost=total_cost, 
            items=items, 
            )
        self.db.add(expense) # Adding expense to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(expense) # Refreshing to fetch updated state
        return expense
    
    def get_all(self) -> List[Expense]:
        statement = select(Expense)
        return self.db.exec(statement).all()
    
    def get_by_id(self, expense_id: int) -> Expense:
        statement = select(Expense).where(Expense.id == expense_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Expense with id {expense_id} not found.")
        return result
    
    def update_expense(self, expense: ExpenseBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(expense) # Refresing session to ensure it is updated

    def delete_expense(self, expense: Expense) -> None:
        self.db.delete(expense) # Marking expense to be deleted
        self.db.commit() # Commiting transaction