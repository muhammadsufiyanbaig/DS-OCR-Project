from sqlmodel import Field, SQLModel
from typing import Optional


class Item(SQLModel, table=True):
    """Item model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


# Add more models here as needed