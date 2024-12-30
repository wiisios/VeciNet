from pydantic import BaseModel


class ExpenseItemBase(BaseModel):
    reason: str
    description: str
    cost: float
    invoiceImg: str

class ExpenseItemResponse(ExpenseItemBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }