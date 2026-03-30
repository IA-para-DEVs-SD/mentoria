from datetime import UTC, datetime
from uuid import uuid4


def utc_now():
    return datetime.now(UTC)

import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import String as SAString
from sqlalchemy.types import TypeDecorator

from src.database import Base


class UUID(TypeDecorator):
    """UUID type compatible with both PostgreSQL and SQLite."""

    impl = SAString(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return str(value)
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(str(value))


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, default=uuid4)
    google_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="user")
