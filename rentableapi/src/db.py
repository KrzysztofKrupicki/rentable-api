"""A module providing database access."""

import asyncio

from asyncpg.exceptions import (  # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import config

metadata = sqlalchemy.MetaData()

category_table = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
)

subcategory_table = sqlalchemy.Table(
    "subcategories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
)

equipment_table = sqlalchemy.Table(
    "equipment",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "subcategory_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("subcategories.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "equipment_owner_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column("price_per_day", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("is_available", sqlalchemy.Boolean, nullable=False),
)

reservation_table = sqlalchemy.Table(
    "reservations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "equipment_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("equipment.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column("start_date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("end_date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Enum(
            "pending",
            "waiting_for_payment",
            "confirmed",
            "canceled",
            "finished",
            name="reservation_status",
        ),
        nullable=False,
        server_default="pending",
    ),
    sqlalchemy.Column("total_price", sqlalchemy.Float, nullable=False),
)

equipment_review_table = sqlalchemy.Table(
    "equipment_reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "reviewer_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "equipment_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("equipment.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "rating",
        sqlalchemy.Integer,
        sqlalchemy.CheckConstraint("rating >= 0 AND rating <= 10"),
        nullable=False,
    ),
    sqlalchemy.Column("comment", sqlalchemy.String, nullable=True),
)

user_review_table = sqlalchemy.Table(
    "user_reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "reviewer_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "reviewed_user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "rating",
        sqlalchemy.Integer,
        sqlalchemy.CheckConstraint("rating >= 0 AND rating <= 10"),
        nullable=False,
    ),
    sqlalchemy.Column("comment", sqlalchemy.String, nullable=True),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
