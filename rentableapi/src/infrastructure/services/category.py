"""Module containing category service implementation."""

from typing import Iterable

from src.core.domain.category import Category, CategoryIn
from src.core.repositories.icategory import ICategoryRepository
from src.infrastructure.services.icategory import ICategoryService

class CategoryService(ICategoryService):
    """A class implementing the category service."""

    _repository: ICategoryRepository

    def __init__(self, repository: ICategoryRepository) -> None:
        """The initializer of the category service.
        
        Args:
            repository (ICategoryRepository): The reference to the repository.
        """
        self._repository = repository
    
    async def get_category_by_id(self, category_id: int) -> Category | None:
        """The method getting a category from the repository.
        
        Args:
            category_id (int): The id of the category.

        Returns: 
            Category | None: The category data if exists.
        """
        return await self._repository.get_category_by_id(category_id)

    async def get_all_categories(self) -> Iterable[Category]:
        """The method getting all categories from the repository.

        Returns:
            Iterable[Category]: The collection of the all categories.
        """
        return await self._repository.get_all_categories()

    async def add_category(self, data: CategoryIn) -> Category | None:
        """The method adding new category to the repository.
        
        Args:
            data (CategoryIn): The attributes of the category.

        Returns:
            Category | None: The newly created category.
        """
        return await self._repository.add_category(data)

    async def update_category(self, category_id: int, data: CategoryIn) -> Category | None:
        """The method updating category data in the repository.
        
        Args:
            category_id (int): The category id.
            data (CategoryIn): The attributes of the category.
        
        Returns:
            Category | None: The updated category.
        """
        return await self._repository.update_category(category_id=category_id, data=data)
    
    async def delete_category(self, category_id: int) -> bool:
        """The method deleting category from the repository.
        
        Args:
            category_id (int): The category id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_category(category_id)