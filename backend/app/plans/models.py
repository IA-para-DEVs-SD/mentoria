from datetime import datetime, timezone
from uuid import uuid4


def utc_now():
    return datetime.now(timezone.utc)

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.auth.models import UUID
from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(), primary_key=True, default=uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="plans")
    actions = relationship("Action", back_populates="plan", cascade="all, delete-orphan")
    gaps = relationship("Gap", back_populates="plan", cascade="all, delete-orphan")


class Action(Base):
    __tablename__ = "actions"

    id = Column(UUID(), primary_key=True, default=uuid4)
    plan_id = Column(UUID(), ForeignKey("plans.id"), nullable=False)
    priority = Column(String, nullable=False)  # ALTA, MEDIA, BAIXA
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    context = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pendente")
    sequence = Column(Integer, default=0)

    plan = relationship("Plan", back_populates="actions")


class Gap(Base):
    __tablename__ = "gaps"

    id = Column(UUID(), primary_key=True, default=uuid4)
    plan_id = Column(UUID(), ForeignKey("plans.id"), nullable=False)
    description = Column(String, nullable=False)
    relevance = Column(Integer, default=0)

    plan = relationship("Plan", back_populates="gaps")


class Rejection(Base):
    __tablename__ = "rejections"

    id = Column(UUID(), primary_key=True, default=uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    action_title = Column(String, nullable=False)
    rejected_at = Column(DateTime, default=utc_now)
