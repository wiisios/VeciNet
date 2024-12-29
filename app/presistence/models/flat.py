from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .building import Building
    from .property import Property

class Flat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    number: str

    buildingId: int | None = Field(default=None, foreign_key="building.id")
    building: "Building" = Relationship(back_populates="flats")

    tenantId: int | None = Field(default=None, foreign_key="user.id")
    tenant: "User" = Relationship(back_populates="flatTenant")

    properties: List["Property"] = Relationship(back_populates="flat")

