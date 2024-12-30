from sqlmodel import Session, select
from app.domain import Expense_UserBase
from app.presistence.models import Expense_User, Expense


class Expense_UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def addExpense_User(self, tenantId: int, expense: Expense) -> Expense_User:
        expense_user = Expense_User(
            expenseId=expense.id,
            userId=tenantId
            )
        self.db.add(expense_user)
        self.db.commit()
        self.db.refresh(expense_user)
        return expense_user
    
    def getById(self, expense_userId: int) -> Expense_User:
        statement = select(Expense_User).where(Expense_User.id == expense_userId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Expense_User with id {expense_userId} not found.")
        return result
    
    def updateExpense_User(self, expense_user: Expense_UserBase) -> None:
        self.db.commit()
        self.db.refresh(expense_user)

    def deleteExpense_User(self, expense_user: Expense_User) -> None:
        self.db.delete(expense_user)
        self.db.commit()