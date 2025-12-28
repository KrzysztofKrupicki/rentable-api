"""Module containing equipment database repository implementation."""

from typing import Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import delete, insert, select, update

from src.core.domain.equipment import Equipment, EquipmentIn
from src.core.repositories.iequipment import IEquipmentRepository
from src.db import database, equipment_table


class EquipmentRepository(IEquipmentRepository):
    """A class implementing the equipment repository."""

    async def get_all_equipments(self) -> Iterable[Equipment]:
        """The method getting all equipments from the database.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        query = select(equipment_table)
        equipments = await database.fetch_all(query)
        return [Equipment(**dict(equipment)) for equipment in equipments]

    async def get_equipment_by_id(self, equipment_id: int) -> Equipment | None:
        """The method getting equipment from the database based on its ID.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Equipment | None: The equipment if exists.
        """
        equipment = await self._get_by_id(equipment_id)
        return Equipment(**dict(equipment)) if equipment else None

    async def get_all_equipment_by_category_id(
        self, category_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the database based on its category ID.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        query = select(equipment_table).where(
            equipment_table.c.category_id == category_id
        )
        equipments = await database.fetch_all(query)
        return [Equipment(**dict(equipment)) for equipment in equipments]

    async def get_all_equipment_by_subcategory_id(
        self, subcategory_id: int
    ) -> Iterable[Equipment]:
        """The method getting all equipments from the database based on its subcategory ID.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Iterable[Equipment]: The collection of the all equipments.
        """
        query = select(equipment_table).where(
            equipment_table.c.subcategory_id == subcategory_id
        )
        equipments = await database.fetch_all(query)
        return [Equipment(**dict(equipment)) for equipment in equipments]

    async def add_equipment(self, data: EquipmentIn) -> Equipment | None:
        """The method adding new equipment to the database.

        Args:
            data (EquipmentIn): The attributes of the equipment.

        Returns:
            Equipment | None: The newly created equipment if exists.
        """
        query = insert(equipment_table).values(**data.model_dump())
        new_equipment_id = await database.execute(query)
        new_equipment = await self._get_by_id(new_equipment_id)
        return Equipment(**dict(new_equipment)) if new_equipment else None

    async def update_equipment(
        self, equipment_id: int, data: EquipmentIn
    ) -> Equipment | None:
        """The method updating equipment in the database.

        Args:
            equipment_id (int): The id of the equipment.
            data (EquipmentIn): The attributes of the equipment.

        Returns:
            Equipment | None: The updated equipment if exists.
        """
        if self._get_by_id(equipment_id):
            query = (
                update(equipment_table)
                .where(equipment_table.c.id == equipment_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            updated_equipment = await self._get_by_id(equipment_id)
            return Equipment(**dict(updated_equipment)) if updated_equipment else None
        return None

    async def delete_equipment(self, equipment_id: int) -> bool:
        """The method removing equipment from the database.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            bool: Success of the operation.
        """
        if await self._get_by_id(equipment_id):
            query = delete(equipment_table).where(equipment_table.c.id == equipment_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, equipment_id: int) -> Record | None:
        """The method getting equipment from the database based on its ID.

        Args:
            equipment_id (int): The id of the equipment.

        Returns:
            Record | None: The equipment record if exists.
        """
        query = select(equipment_table).where(equipment_table.c.id == equipment_id)
        return await database.fetch_one(query)
