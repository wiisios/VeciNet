from typing import List

from app.persistence.models import ExpenseItem

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class Helpers():
    # Gets a List of ExpenseItems to calculate the total cost of the Expense itself
    def calculate_total_expense(items: List[ExpenseItem]) -> float:
        total_cost = 0
        for i in items:
            total_cost = total_cost + i.cost
        return total_cost