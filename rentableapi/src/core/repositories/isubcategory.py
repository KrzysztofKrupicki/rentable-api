"""Module containing subcategory repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.subcategory import Subcategory, SubcategoryIn


class ISubcategoryRepository(ABC):
    """The abstract class representing protocol of subcategory repository."""

    @abstractmethod
    async def get_all_subcategories(self) -> Iterable[Subcategory]:
        """The abstract method getting all subcategories from the data storage.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories in the data storage.
        """

    @abstractmethod
    async def get_subcategory_by_id(self, subcategory_id: int) -> Subcategory | None:
        """The abstract method getting subcategory by provided id from the data storage.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            Subcategory | None: The subcategory details.
        """

    @abstractmethod
    async def get_subcategories_by_category_id(
        self, category_id: int
    ) -> Iterable[Subcategory] | None:
        """The abstract method getting all subcategories by provided category id.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories for provided category.
        """

    @abstractmethod
    async def add_subcategory(self, data: SubcategoryIn) -> Subcategory | None:
        """The abstract method adding new subcategory to the data storage.

        Args:
            data (SubcategoryIn): The details of the new subcategory.
        """

    @abstractmethod
    async def update_subcategory(
        self, subcategory_id: int, data: SubcategoryIn
    ) -> Subcategory | None:
        """The abstract method updating subcategory data in the data storage.

        Args:
            subcategory_id (int): The id of the subcategory.
            data (SubcategoryIn): The details of the updated subcategory.

        Returns:
            Subcategory | None: The updated subcategory details.
        """

    @abstractmethod
    async def delete_subcategory(self, subcategory_id: int) -> bool:
        """The abstract method remmoving subcategory from the data storage.

        Args:
            subcategory_id (int): The id of the subcategory.

        Returns:
            bool: Success of the operation.
        """
