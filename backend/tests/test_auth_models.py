"""
Testes unitários para o módulo auth/models.py
"""
import uuid
from datetime import datetime

import pytest

from app.auth.models import User, UUID as CustomUUID


class TestUUIDTypeDecorator:
    """Testes para o TypeDecorator UUID customizado."""

    def test_process_bind_param_with_uuid(self):
        # Arrange
        uuid_type = CustomUUID()
        test_uuid = uuid.uuid4()
        mock_dialect = type("Dialect", (), {"name": "postgresql"})()

        # Act
        result = uuid_type.process_bind_param(test_uuid, mock_dialect)

        # Assert
        assert result == str(test_uuid)

    def test_process_bind_param_with_none(self):
        # Arrange
        uuid_type = CustomUUID()
        mock_dialect = type("Dialect", (), {"name": "postgresql"})()

        # Act
        result = uuid_type.process_bind_param(None, mock_dialect)

        # Assert
        assert result is None

    def test_process_result_value_with_string(self):
        # Arrange
        uuid_type = CustomUUID()
        test_uuid_str = "12345678-1234-5678-1234-567812345678"
        mock_dialect = type("Dialect", (), {"name": "postgresql"})()

        # Act
        result = uuid_type.process_result_value(test_uuid_str, mock_dialect)

        # Assert
        assert isinstance(result, uuid.UUID)
        assert str(result) == test_uuid_str

    def test_process_result_value_with_none(self):
        # Arrange
        uuid_type = CustomUUID()
        mock_dialect = type("Dialect", (), {"name": "postgresql"})()

        # Act
        result = uuid_type.process_result_value(None, mock_dialect)

        # Assert
        assert result is None


class TestUserModel:
    """Testes para o modelo User."""

    def test_user_creation(self, db_session):
        # Arrange
        user_data = {
            "google_id": "google_test_123",
            "name": "Test User",
            "email": "testuser@example.com",
            "photo_url": "https://example.com/photo.jpg",
        }

        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Assert
        assert user.id is not None
        assert user.google_id == user_data["google_id"]
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.photo_url == user_data["photo_url"]
        assert user.created_at is not None

    def test_user_creation_without_photo(self, db_session):
        # Arrange
        user_data = {
            "google_id": "google_no_photo",
            "name": "No Photo User",
            "email": "nophoto@example.com",
        }

        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()

        # Assert
        assert user.photo_url is None

    def test_user_google_id_unique_constraint(self, db_session, sample_user):
        # Arrange
        duplicate_user = User(
            google_id=sample_user.google_id,
            name="Duplicate User",
            email="duplicate@example.com",
        )

        # Act & Assert
        db_session.add(duplicate_user)
        with pytest.raises(Exception):
            db_session.commit()

    def test_user_email_unique_constraint(self, db_session, sample_user):
        # Arrange
        duplicate_user = User(
            google_id="different_google_id",
            name="Duplicate Email User",
            email=sample_user.email,
        )

        # Act & Assert
        db_session.add(duplicate_user)
        with pytest.raises(Exception):
            db_session.commit()

    def test_user_has_profile_relationship(self, db_session, sample_user, sample_profile):
        # Arrange & Act
        db_session.refresh(sample_user)

        # Assert
        assert sample_user.profile is not None
        assert sample_user.profile.id == sample_profile.id

    def test_user_has_plans_relationship(self, db_session, sample_user, sample_plan):
        # Arrange & Act
        db_session.refresh(sample_user)

        # Assert
        assert len(sample_user.plans) == 1
        assert sample_user.plans[0].id == sample_plan.id
