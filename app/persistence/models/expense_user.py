from sqlmodel import Field, SQLModel

class ExpenseUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_paid: bool = Field(default=False)

    expense_id: int | None = Field(default=None, foreign_key="expense.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")