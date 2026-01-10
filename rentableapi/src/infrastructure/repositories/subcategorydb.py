"""Module containing subsubcategory database repository implementation."""

from typing import Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import delete, insert, join, select, update

from src.core.domain.subcategory import Subcategory, SubcategoryIn
from src.core.repositories.isubcategory import ISubcategoryRepository
from src.db import category_table, database, subcategory_table


class SubcategoryRepository(ISubcategoryRepository):
    """A class implementing the subsubcategory repository."""

    async def get_all_subcategories(self) -> Iterable[Subcategory]:
        """The method getting all subcategories from the database.

        Returns:
            Iterable[Any]: The collection of the all subcategories.
        """
        query = (
            select(subcategory_table, category_table.c.id.label("category_id"))
            .select_from(
                join(
                    subcategory_table,
                    category_table,
                    subcategory_table.c.category_id == category_table.c.id,
                )
            )
            .order_by(subcategory_table.c.name.asc())
        )
        subcategories = await database.fetch_all(query)
        return [Subcategory(**dict(subsubcategory)) for subsubcategory in subcategories]

    async def get_subcategory_by_id(self, subcategory_id: int) -> Subcategory | None:
        """The method getting a subcategory from the database based on provided id.

        Args:
            subcategory_id (int): The id of the subcategory

        Returns:
            Any | None: The subcategory data if exists.
        """
        subcategory = await self._get_by_id(subcategory_id)
        return Subcategory(**dict(subcategory)) if subcategory else None

    async def get_all_subcategories_by_category_id(
        self, category_id: int
    ) -> Iterable[Subcategory] | None:
        """The method getting all subcategories by provided category id.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories for provided category.
        """
        query = (
            select(subcategory_table, category_table.c.id.label("category_id"))
            .select_from(
                join(
                    subcategory_table,
                    category_table,
                    subcategory_table.c.category_id == category_table.c.id,
                )
            )
            .where(subcategory_table.c.category_id == category_id)
            .order_by(subcategory_table.c.name.asc())
        )
        subcategories = await database.fetch_all(query)
        return [Subcategory(**dict(subcategory)) for subcategory in subcategories]

    async def add_subcategory(self, data: SubcategoryIn) -> Subcategory | None:
        """The method adding new subcategory to the database.

        Args:
            data (SubcategoryIn): The attributes of the subcategory.

        Returns:
            Any | None: The newly created subcategory.
        """
        query = insert(subcategory_table).values(**data.model_dump())
        new_subcategory_id = await database.execute(query)
        new_subcategory = await self._get_by_id(new_subcategory_id)
        return Subcategory(**dict(new_subcategory)) if new_subcategory else None

    async def update_subcategory(
        self, subcategory_id: int, data: SubcategoryIn
    ) -> Subcategory | None:
        """The method updating subcategory data in the database.

        Args:
            subcategory_id (int): The subcategory id.
            data (SubcategoryIn): The attributes of the subcategory.

        Returns:
            Any | None: The updated subcategory.
        """
        if self._get_by_id(subcategory_id):
            query = (
                update(subcategory_table)
                .where(subcategory_table.c.id == subcategory_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            updated_subcategory = await self._get_by_id(subcategory_id)
            return (
                Subcategory(**dict(updated_subcategory))
                if updated_subcategory
                else None
            )
        return None

    async def delete_subcategory(self, subcategory_id: int) -> bool:
        """The method removing subcategory from the database.

        Args:
            subcategory_id (int): The subcategory id.

        Returns:
            bool: Success of the operation.
        """
        if self._get_by_id(subcategory_id):
            query = delete(subcategory_table).where(
                subcategory_table.c.id == subcategory_id
            )
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, subcategory_id: int) -> Record | None:
        """A private method getting subcategory from the database based on its ID.

        Args:
            subcategory_id (int): The ID of the subcategory.

        Returns:
            Record | None: Subcategory record if exists.
        """
        query = (
            select(subcategory_table, category_table.c.id.label("category_id"))
            .select_from(
                join(
                    subcategory_table,
                    category_table,
                    subcategory_table.c.category_id == category_table.c.id,
                )
            )
            .where(subcategory_table.c.id == subcategory_id)
        )
        return await database.fetch_one(query)
