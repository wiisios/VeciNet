from sqlmodel import Field, SQLModel

class Expense_User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    isPaid: bool = Field(default=False)

    expenseId: int | None = Field(default=None, foreign_key="expense.id")
    userId: int | None = Field(default=None, foreign_key="user.id")