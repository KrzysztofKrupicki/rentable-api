"""Module containing equipment-related domain models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4


class EquipmentIn(BaseModel):
    """Model representing equipment's DTO attributes."""

    name: str
    description: Optional[str]
    subcategory_id: int
    price_per_day: float
    is_available: bool


class EquipmentBroker(EquipmentIn):
    """A broker class including user in the model."""

    equipment_owner_id: UUID4


class Equipment(EquipmentBroker):
    """Model representing equipment's attributes in the database."""

    id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
