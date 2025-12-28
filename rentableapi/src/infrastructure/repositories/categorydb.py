"""Module containing category database repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import delete, insert, select, update

from src.core.domain.category import Category, CategoryIn
from src.core.repositories.icategory import ICategoryRepository
from src.db import category_table, database


class CategoryRepository(ICategoryRepository):
    """A class implementing the category repository."""

    async def get_all_categories(self) -> Iterable[Category]:
        """The method getting all categories from the database.

        Returns:
            Iterable[Any]: The collection of the all categories.
        """
        query = select(category_table).order_by(category_table.c.name.asc())
        categories = await database.fetch_all(query)
        return [Category(**dict(category)) for category in categories]

    async def get_category_by_id(self, category_id: int) -> Category | None:
        """The method getting a category from the database based on provided id.

        Args:
            category_id (int): The id of the category

        Returns:
            Any | None: The category data if exists.
        """
        category = await self._get_by_id(category_id)
        return Category(**dict(category)) if category else None

    async def add_category(self, data: CategoryIn) -> Category | None:
        """The method adding new category to the database.

        Args:
            data (CategoryIn): The attributes of the category.

        Returns:
            Any | None: The newly created category.
        """
        query = insert(category_table).values(**data.model_dump())
        new_category_id = await database.execute(query)
        new_category = await self._get_by_id(new_category_id)
        return Category(**dict(new_category)) if new_category else None

    async def update_category(self, category_id: int, data: CategoryIn) -> Category | None:
        """The method updating category data in the database.

        Args:
            category_id (int): The category id.
            data (CategoryIn): The attributes of the category.

        Returns:
            Any | None: The updated category.
        """
        if self._get_by_id(category_id):
            query = (
                update(category_table)
                .where(category_table.c.id == category_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            updated_category = await self._get_by_id(category_id)
            return Category(**dict(updated_category)) if updated_category else None
        return None

    async def delete_category(self, category_id: int) -> bool:
        """The method removing category from the database.

        Args:
            category_id (int): The category id.

        Returns:
            bool: Success of the operation.
        """
        if self._get_by_id(category_id):
            query = delete(category_table).where(category_table.c.id == category_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, category_id: int) -> Record | None:
        """A private method getting category from the database based on its ID.

        Args:
            category_id (int): The ID of the category.

        Returns:
            Record | None: Category record if exists.
        """
        query = (
            select(category_table)
            .where(category_table.c.id == category_id)
            .order_by(category_table.c.name.asc())
        )
        return await database.fetch_one(query)
