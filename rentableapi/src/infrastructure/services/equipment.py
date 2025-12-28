"""Module containing subcategory service implementation."""

from typing import Iterable

from fastapi import HTTPException

from src.core.domain.equipment import Equipment, EquipmentIn
from src.core.repositories.iequipment import IEquipmentRepository
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.services.iequipment import IEquipmentService

class EquipmentService(IEquipmentService):
    """A class implementing the equipment service."""

    _repository: IEquipmentRepository
    _user_repository: IUserRepository

    def __init__(
        self, 
        repository: IEquipmentRepository,
        user_repository: IUserRepository
    ) -> None:
        """The initializer of the subcategory service.
        
        Args:
            repository (IEquipmentRepository): The reference to the repository.
            user_repository (IUserRepository): The reference to the user repository.
        """
        self._repository = repository
        self._user_repository = user_repository
    
    async def get_equipment_by_id(self, equipment_id: int) -> Equipment | None:
        """The method getting a equipment from the repository.
        
        Args:
            equipment_id (int): The id of the equipment.
        
        Returns:
            Equipment | None: The equipment data if exists.
        """
        return await self._repository.get_equipment_by_id(equipment_id)

    async def get_all_equipments(self) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        return await self._repository.get_all_equipments()

    async def get_all_equipment_by_category_id(
        self, category_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        return await self._repository.get_all_equipment_by_category_id(category_id)

    async def get_all_equipment_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the repository.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        return await self._repository.get_all_equipment_by_subcategory_id(subcategory_id)
    
    async def add_equipment(self, data: EquipmentIn) -> Equipment | None:
        """The method adding new equipment to the repository.
        
        Args:
            data (EquipmentIn): The attributes of the equipment.

        Returns:
            Equipment | None: The newly created equipment.
        """
        if not await self._user_repository.get_by_uuid(data.equipment_owner_id):
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return await self._repository.add_equipment(data)

    async def update_equipment(self, equipment_id: int, data: EquipmentIn) -> Equipment | None:
        """The method updating equipment data in the repository.
        
        Args:
            equipment_id (int): The equipment id.
            data (EquipmentIn): The attributes of the equipment.
        
        Returns:
            Equipment | None: The updated equipment.
        """
        return await self._repository.update_equipment(equipment_id, data)

    async def delete_equipment(self, equipment_id: int) -> bool:
        """The method deleting equipment from the repository.
        
        Args:
            equipment_id (int): The equipment id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_equipment(equipment_id)