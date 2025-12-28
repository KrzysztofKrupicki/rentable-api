"""Module containing subcategory-related domain models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubcategoryIn(BaseModel):
    """Model representing subcategory's DTO attributes."""

    name: str
    description: Optional[str]
    category_id: int


class Subcategory(SubcategoryIn):
    """Model representing subcategory's attributes in the database."""

    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
