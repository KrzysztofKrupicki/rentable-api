"""Module containing subcategory service implementation."""

from typing import Iterable

from src.core.domain.subcategory import Subcategory, SubcategoryIn
from src.core.repositories.isubcategory import ISubcategoryRepository
from src.infrastructure.services.isubcategory import ISubcategoryService


class SubcategoryService(ISubcategoryService):
    """A class implementing the subcategory service."""

    _repository: ISubcategoryRepository

    def __init__(self, repository: ISubcategoryRepository) -> None:
        """The initializer of the subcategory service.

        Args:
            repository (ISubcategoryRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_subcategory_by_id(self, subcategory_id: int) -> Subcategory | None:
        """The method getting a subcategory from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Category | None: The category data if exists.
        """
        return await self._repository.get_subcategory_by_id(subcategory_id)

    async def get_all_subcategories(self) -> Iterable[Subcategory]:
        """The method getting all subcategory from the repository.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories.
        """
        return await self._repository.get_all_subcategories()

    async def get_all_subcategories_by_category_id(
        self, category_id: int
    ) -> Iterable[Subcategory]:
        """The method getting all subcategory by category id from the repository.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Subcategory]: The collection of the all subcategories.
        """
        return await self._repository.get_all_subcategories_by_category_id(category_id)

    async def add_subcategory(self, data: SubcategoryIn) -> Subcategory | None:
        """The method adding new subcategory to the repository.

        Args:
            data (SubcategoryIn): The attributes of the subcategory.

        Returns:
            Subcategory | None: The newly created subcategory.
        """
        return await self._repository.add_subcategory(data)

    async def update_subcategory(
        self, subcategory_id: int, data: SubcategoryIn
    ) -> Subcategory | None:
        """The method updating subcountry data in the repository.

        Args:
            subcategory_id (int): The subcategory id.
            data (SubcategoryIn): The attributes of the subcategory.

        Returns:
            Subcategory | None: The updated subcategory.
        """
        return await self._repository.update_subcategory(
            subcategory_id=subcategory_id, data=data
        )

    async def delete_subcategory(self, subcategory_id: int) -> bool:
        """The method deleting subcategory from the repository.

        Args:
            subcategory_id (int): The subcategory id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_subcategory(subcategory_id)
