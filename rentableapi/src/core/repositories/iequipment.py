"""Module containing equipment repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.equipment import Equipment, EquipmentIn


class IEquipmentRepository(ABC):
    """The abstract class representing protocol of equipment repository."""

    @abstractmethod
    async def get_all_equipments(self) -> Iterable[Equipment]:
        """The abstract method getting all equipments from the data storage.

        Returns:
            Iterable[Equipment]: The collection of the all equipment.
        """

    @abstractmethod
    async def get_equipment_by_id(self, equipment_id: int) -> Equipment | None:
        """The abstract method getting a equipment by provided id from the data storage.

        Args:
            equipment_id (int): The id of the equipment,

        Returns:
            Equipment | None: The equipment details.
        """

    @abstractmethod
    async def get_all_equipment_by_category_id(
        self, category_id: int
    ) -> Iterable[Equipment]:
        """The abstract method getting all equipments by provided category id from the data storage.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Equipment]: The collection of the all equipment from provided category.
        """

    @abstractmethod
    async def get_all_equipment_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Equipment]:
        """The abstract method getting all equipments by provided subcategory id from the data storage.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Equipment]: The collection of the all equipment from provided subcategory.
        """

    @abstractmethod
    async def update_equipment(
        self, equipment_id: int, data: EquipmentIn
    ) -> Equipment | None:
        """The abstract method updating equipment data in the data storage.

        Args:
            equipment_id (int): The id of the equipment.
            data (EquipmentIn): The datails of the updated equipment.

        Returns:
            Equipment | None: The updated equipment details.
        """

    @abstractmethod
    async def delete_equipment(self, equipment_id: int) -> bool:
        """The abstract method removing equipment from the data storage.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def add_equipment(self, data: EquipmentIn) -> Equipment | None:
        """The abstract method adding equipment to the data storage.

        Args:
            data (EquipmentIn): The details of the new equipment.

        Returns:
            Equipment | None: The created equipment details.
        """
