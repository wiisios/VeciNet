from fastapi import Depends
from sqlmodel import Session

from app.presistence.repositories import ExpenseItemRepository
from app.config import getDb
from app.domain import ExpenseItemResponse, ExpenseItemBase


class ExpenseItemService:
    def __init__(self, db: Session = Depends(getDb)):
        self.expenseItemRepository = ExpenseItemRepository(db)

    async def createExpenseItem(self, expenseItemData: ExpenseItemBase) -> ExpenseItemResponse:
        expenseItem = self.expenseItemRepository.addExpenseItem(expenseItemData)
        return ExpenseItemResponse.model_validate(expenseItem.__dict__)
    
    async def readExpenseItem(self, expenseItemId: int) -> ExpenseItemResponse:
        expenseItem = self.expenseItemRepository.getById(expenseItemId)
        if expenseItem:
            expenseItem_dict = {
                "id": expenseItem.id,
                "reason": expenseItem.reason,
                "description": expenseItem.description,
                "cost": expenseItem.cost,
                "invoiceImg": expenseItem.invoiceImg
            }
            return ExpenseItemResponse.model_validate(expenseItem_dict)
        return None
    
    async def updateExpenseItem(self, expenseItemId: int, expenseItemData: ExpenseItemBase) -> ExpenseItemResponse:
        expenseItem = self.expenseItemRepository.getById(expenseItemId)
        if expenseItem:
            expenseItem.reason = expenseItemData.reason
            expenseItem.description = expenseItemData.description
            expenseItem.cost = expenseItemData.cost
            expenseItem.invoiceImg = expenseItemData.invoiceImg
            self.expenseItemRepository.updateExpenseItem(expenseItem)
            return ExpenseItemResponse.model_validate(expenseItem.__dict__)
        return None
    
    async def deleteExpenseItem(self, expenseItemId: int) -> bool:
        expenseItem = self.expenseItemRepository.getById(expenseItemId)
        if expenseItem:
            self.expenseItemRepository.deleteExpenseItem(expenseItem)
            return True
        return False