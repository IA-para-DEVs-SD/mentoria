"""
Testes unitários para o módulo auth/schemas.py
"""
import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.auth.schemas import TokenResponse, UserOut


class TestTokenResponse:
    """Testes para o schema TokenResponse."""

    def test_token_response_creation(self):
        # Arrange
        data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "has_profile": True,
        }

        # Act
        response = TokenResponse(**data)

        # Assert
        assert response.access_token == data["access_token"]
        assert response.token_type == "bearer"
        assert response.has_profile is True

    def test_token_response_default_token_type(self):
        # Arrange
        data = {
            "access_token": "test_token",
            "has_profile": False,
        }

        # Act
        response = TokenResponse(**data)

        # Assert
        assert response.token_type == "bearer"

    def test_token_response_custom_token_type(self):
        # Arrange
        data = {
            "access_token": "test_token",
            "token_type": "custom",
            "has_profile": True,
        }

        # Act
        response = TokenResponse(**data)

        # Assert
        assert response.token_type == "custom"

    def test_token_response_missing_access_token_raises_error(self):
        # Arrange
        data = {"has_profile": True}

        # Act & Assert
        with pytest.raises(ValidationError):
            TokenResponse(**data)

    def test_token_response_missing_has_profile_raises_error(self):
        # Arrange
        data = {"access_token": "test_token"}

        # Act & Assert
        with pytest.raises(ValidationError):
            TokenResponse(**data)


class TestUserOut:
    """Testes para o schema UserOut."""

    def test_user_out_creation(self):
        # Arrange
        user_id = uuid.uuid4()
        created_at = datetime.now(timezone.utc)
        data = {
            "id": user_id,
            "name": "Test User",
            "email": "test@example.com",
            "photo_url": "https://example.com/photo.jpg",
            "created_at": created_at,
        }

        # Act
        user_out = UserOut(**data)

        # Assert
        assert user_out.id == user_id
        assert user_out.name == "Test User"
        assert user_out.email == "test@example.com"
        assert user_out.photo_url == "https://example.com/photo.jpg"
        assert user_out.created_at == created_at

    def test_user_out_with_none_photo_url(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "name": "Test User",
            "email": "test@example.com",
            "photo_url": None,
            "created_at": datetime.now(timezone.utc),
        }

        # Act
        user_out = UserOut(**data)

        # Assert
        assert user_out.photo_url is None

    def test_user_out_from_orm_model(self, sample_user):
        # Arrange & Act
        user_out = UserOut.model_validate(sample_user)

        # Assert
        assert user_out.id == sample_user.id
        assert user_out.name == sample_user.name
        assert user_out.email == sample_user.email

    def test_user_out_missing_required_field_raises_error(self):
        # Arrange
        data = {
            "id": uuid.uuid4(),
            "name": "Test User",
            # missing email
            "created_at": datetime.now(timezone.utc),
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            UserOut(**data)
