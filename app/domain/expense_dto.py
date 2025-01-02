from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.persistence.models import ExpenseItem


class ExpenseBase(BaseModel):
    date: datetime
    
class ExpenseCreate(ExpenseBase):
    tenant_name: str
    tenant_last_name: str
    items: List[int]

class ExpenseResponse(ExpenseBase):
    id: int
    total_cost: float
    items: List["ExpenseItem"]
    
    class Config:
        model_config ={
            'from_attributes': True
        }