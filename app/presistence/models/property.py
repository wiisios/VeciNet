from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .flat import Flat
    from .user import User

class Property(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ownerId: int = Field(foreign_key="user.id")
    flatId: int = Field(foreign_key="flat.id")

    owner: "User" = Relationship(back_populates="properties")
    flat: "Flat" = Relationship(back_populates="properties")