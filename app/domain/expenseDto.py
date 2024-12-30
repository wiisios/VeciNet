from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.presistence.models import ExpenseItem


class ExpenseBase(BaseModel):
    date: datetime
    
class ExpenseCreate(ExpenseBase):
    tenantName: str
    tenantLastName: str
    items: List[int]

class ExpenseResponse(ExpenseBase):
    id: int
    totalCost: float
    items: List["ExpenseItem"]
    
    class Config:
        model_config ={
            'from_attributes': True
        }