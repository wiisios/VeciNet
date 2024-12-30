from pydantic import BaseModel


class Expense_UserBase(BaseModel):
    expenseId: int
    userId: int

class Expense_UserResponse(Expense_UserBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }