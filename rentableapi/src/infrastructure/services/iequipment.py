"""Module containing equipment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.equipment import Equipment, EquipmentIn

class IEquipmentService(ABC):
    """An abstract class representing protocol of equipment service."""
    @abstractmethod
    async def get_equipment_by_id(self, equipment_id: int) -> Equipment | None:
        """The method getting a equipment from the repository.
        
        Args:
            equipment_id (int): The id of the equipment.
        
        Returns:
            Equipment | None: The equipment data if exists.
        """
    
    @abstractmethod
    async def get_all_equipments(self) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """

    @abstractmethod
    async def get_all_equipment_by_category_id(
        self, category_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """

    @abstractmethod
    async def get_all_equipment_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
    
    @abstractmethod
    async def add_equipment(self, data: EquipmentIn) -> Equipment | None:
        """The method adding new equipment to the repository.
        
        Args:
            data (EquipmentIn): The attributes of the equipment.

        Returns:
            Equipment | None: The newly created equipment.
        """
        
    @abstractmethod
    async def update_equipment(self, equipment_id: int, data: EquipmentIn) -> Equipment | None:
        """The method updating equipment data in the repository.
        
        Args:
            equipment_id (int): The equipment id.
            data (EquipmentIn): The attributes of the equipment.
        
        Returns:
            Equipment | None: The updated equipment.
        """

    @abstractmethod
    async def delete_equipment(self, equipment_id: int) -> bool:
        """The method deleting equipment from the repository.
        
        Args:
            equipment_id (int): The equipment id.

        Returns:
            bool: The success of the operation.
        """