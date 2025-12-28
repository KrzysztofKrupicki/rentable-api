"""Module containing category repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.category import Category, CategoryIn


class ICategoryRepository(ABC):
    """The abstract class representing protocol of category repository."""

    @abstractmethod
    async def get_all_categories(self) -> Iterable[Category]:
        """The abstract method getting all categories from the data storage.

        Returns:
            Iterable[Category]: The collection of the all categories in the data storage.
        """

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Category | None:
        """The abstract method getting category by provided id from the data storage.

        Args:
            category_id (int): The id of the category.

        Returns:
            Category | None: The category details.
        """

    @abstractmethod
    async def add_category(self, data: CategoryIn) -> Category | None:
        """The abstract method adding new category to the data storage.

        Args:
            data (CategoryIn): The details of the new category.
        """

    @abstractmethod
    async def update_category(
        self, category_id: int, data: CategoryIn
    ) -> Category | None:
        """The abstract method updating category data in the data storage.

        Args:
            category_id (int): The id of the category.
            data (CategoryIn): The details of the updated category.

        Returns:
            Category | None: The updated category details.
        """

    @abstractmethod
    async def delete_category(self, category_id: int) -> bool:
        """The abstract method remmoving category from the data storage.

        Args:
            category_id (int): The id of the category.

        Returns:
            bool: Success of the operation.
        """
