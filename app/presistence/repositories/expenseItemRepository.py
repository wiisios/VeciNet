from typing import List
from sqlmodel import Session, select
from app.domain import ExpenseItemBase
from app.presistence.models import ExpenseItem

class ExpenseItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def addExpenseItem(self, expenseItem_data: ExpenseItemBase) -> ExpenseItem:
        expenseItem = ExpenseItem(
            reason=expenseItem_data.reason, 
            description=expenseItem_data.description, 
            cost=expenseItem_data.cost, 
            invoiceImg=expenseItem_data.invoiceImg
            )
        self.db.add(expenseItem)
        self.db.commit()
        self.db.refresh(expenseItem)
        return expenseItem
    
    def getAll(self) -> List[ExpenseItem]:
        statement = select(ExpenseItem)
        result = self.db.exec(statement).all()
        return result
    
    def getById(self, expenseItemId: int) -> ExpenseItem:
        statement = select(ExpenseItem).where(ExpenseItem.id == expenseItemId)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"ExpenseItem with id {expenseItemId} not found.")
        return result
    
    def updateExpenseItem(self, expenseItem: ExpenseItemBase) -> None:
        self.db.commit()
        self.db.refresh(expenseItem)

    def deleteExpenseItem(self, expenseItem: ExpenseItem) -> None:
        self.db.delete(expenseItem)
        self.db.commit()