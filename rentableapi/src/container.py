"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.categorydb import CategoryRepository
from src.infrastructure.repositories.equipment_reviewdb import EquipmentReviewRepository
from src.infrastructure.repositories.equipmentdb import EquipmentRepository
from src.infrastructure.repositories.reservationdb import ReservationRepository
from src.infrastructure.repositories.subcategorydb import SubcategoryRepository
from src.infrastructure.repositories.user_reviewdb import UserReviewRepository
from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.services.category import CategoryService
from src.infrastructure.services.equipment import EquipmentService
from src.infrastructure.services.equipment_review import EquipmentReviewService
from src.infrastructure.services.reservation import ReservationService
from src.infrastructure.services.subcategory import SubcategoryService
from src.infrastructure.services.user_review import UserReviewService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injection purposes."""

    category_repository = Singleton(CategoryRepository)
    subcategory_repository = Singleton(SubcategoryRepository)
    equipment_repository = Singleton(EquipmentRepository)
    equipment_review_repository = Singleton(EquipmentReviewRepository)
    user_review_repository = Singleton(UserReviewRepository)
    reservation_repository = Singleton(ReservationRepository)

    user_repository = Singleton(UserRepository)

    category_service = Factory(CategoryService, repository=category_repository)
    subcategory_service = Factory(SubcategoryService, repository=subcategory_repository)
    equipment_service = Factory(
        EquipmentService,
        repository=equipment_repository,
        user_repository=user_repository,
    )
    equipment_review_service = Factory(
        EquipmentReviewService, repository=equipment_review_repository
    )
    user_review_service = Factory(UserReviewService, repository=user_review_repository)
    reservation_service = Factory(ReservationService, repository=reservation_repository)
    user_service = Factory(UserService, repository=user_repository)
