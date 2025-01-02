from pydantic import BaseModel


class ExpenseItemBase(BaseModel):
    reason: str
    description: str
    cost: float
    invoice_img: str

class ExpenseItemResponse(ExpenseItemBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }