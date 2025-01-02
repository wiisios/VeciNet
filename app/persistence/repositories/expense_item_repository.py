from typing import List
from sqlmodel import Session, select
from app.domain import ExpenseItemBase
from app.persistence.models import ExpenseItem

class ExpenseItemRepository:
    def __init__(self, db: Session):
        self.db = db # This is the db session to be used for operations

    def add_expense_item(self, expense_item_data: ExpenseItemBase) -> ExpenseItem:
        expense_item = ExpenseItem(
            reason=expense_item_data.reason, 
            description=expense_item_data.description, 
            cost=expense_item_data.cost, 
            invoice_img=expense_item_data.invoice_img
            )
        self.db.add(expense_item) # Adding expense_item to Session
        self.db.commit() # Commiting transaction
        self.db.refresh(expense_item) # Refreshing to fetch updated state
        return expense_item
    
    def get_all(self) -> List[ExpenseItem]:
        statement = select(ExpenseItem)
        return self.db.exec(statement).all()
    
    def get_by_id(self, expense_item_id: int) -> ExpenseItem:
        statement = select(ExpenseItem).where(ExpenseItem.id == expense_item_id)
        result = self.db.exec(statement).first()
        if result is None:
            raise ValueError(f"Expense item with id {expense_item_id} not found.")
        return result
    
    def update_expense_item(self, expense_item: ExpenseItemBase) -> None:
        self.db.commit() # Commiting changes to db
        self.db.refresh(expense_item) # Refresing session to ensure it is updated

    def delete_expense_item(self, expense_item: ExpenseItem) -> None:
        self.db.delete(expense_item) # Marking expense_item to be deleted
        self.db.commit() # Commiting transaction