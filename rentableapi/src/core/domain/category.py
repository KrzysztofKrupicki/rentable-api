"""Module containing category-related domain models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryIn(BaseModel):
    """Model representing category's DTO attributes."""

    name: str
    description: Optional[str]


class Category(CategoryIn):
    """Model representing category's attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
