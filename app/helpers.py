from typing import List

from app.presistence.models import ExpenseItem

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class Helpers():
    def calculateTotalExpense(items: List[ExpenseItem]) -> float:
        totalCost = 0
        for i in items:
            totalCost = totalCost + i.cost
        return totalCost