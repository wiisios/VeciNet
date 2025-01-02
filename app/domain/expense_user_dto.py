from pydantic import BaseModel


class ExpenseUserBase(BaseModel):
    expense_id: int
    user_id: int

class ExpenseUserResponse(ExpenseUserBase):
    id: int

    class Config:
        model_config ={
            'from_attributes': True
        }