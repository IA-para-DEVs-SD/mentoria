from datetime import datetime, timezone
from uuid import uuid4


def utc_now():
    return datetime.now(timezone.utc)

from sqlalchemy import Column, Date, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import relationship

from app.auth.models import UUID
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(), primary_key=True, default=uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), unique=True, nullable=False)
    career_goal = Column(String, nullable=True)
    skills = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(UUID(), primary_key=True, default=uuid4)
    profile_id = Column(UUID(), ForeignKey("profiles.id"), nullable=False)
    role = Column(String, nullable=False)
    seniority = Column(String, nullable=False)
    company = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    profile = relationship("Profile", back_populates="experiences")


class Education(Base):
    __tablename__ = "educations"

    id = Column(UUID(), primary_key=True, default=uuid4)
    profile_id = Column(UUID(), ForeignKey("profiles.id"), nullable=False)
    institution = Column(String, nullable=False)
    level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    study_area = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    profile = relationship("Profile", back_populates="educations")
