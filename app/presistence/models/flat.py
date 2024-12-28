from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User

class Flat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    number: str

    buildingId: int | None = Field(default=None, foreign_key="building.id")

    ownerId: int | None = Field(default=None, foreign_key="user.id")
    owner: "User" = Relationship(back_populates="flatOwner")

    tenant: "User" = Relationship(back_populates="flatTenant")

