from typing import List

from app.presistence.models import ExpenseItem

class Helpers():
    def calculateTotalExpense(items: List[ExpenseItem]) -> float:
        totalCost = 0
        for i in items:
            totalCost = totalCost + i.cost
        return totalCost