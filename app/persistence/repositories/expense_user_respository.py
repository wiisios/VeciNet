from typing import List
from sqlmodel import Session, select
from app.domain import ExpenseUserBase
from app.persistence.models import ExpenseUser, Expense


class ExpenseUserRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_expense_user(self, tenant_id: int, expense: Expense) -> ExpenseUser:
        expense_user = ExpenseUser(
            expenseId=expense.id,
            userId=tenant_id
            )
        self.db.add(expense_user) # Adding expense_user to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(expense_user) # Refreshing to fetch updated state
        return expense_user
    
    def get_all(self) -> List[ExpenseUser]:
        statement = select(ExpenseUser)
        return self.db.exec(statement).all()
    
    def get_by_id(self, expense_user_id: int) -> ExpenseUser:
        statement = select(ExpenseUser).where(ExpenseUser.id == expense_user_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Expense_user with id {expense_user_id} not found.")
        return result
    
    def update_expense_user(self, expense_user: ExpenseUserBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(expense_user) # Refresing session to ensure it is updated

    def delete_expense_user(self, expense_user: ExpenseUser) -> None:
        self.db.delete(expense_user) # Marking expense_user to be deleted
        self.db.commit() # Commiting transaction