from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .flat import Flat

class Building(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    street: str
    city: str
    zipCode: int
    flatAmount: int

    flats: List["Flat"] = Relationship(back_populates="building")