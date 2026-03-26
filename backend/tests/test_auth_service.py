"""
Testes unitários para o módulo auth/service.py
"""
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.auth.models import User
from app.auth.service import AuthService


class TestAuthServiceGetAuthorizationUrl:
    """Testes para AuthService.get_authorization_url"""

    def test_returns_google_auth_url(self):
        # Arrange
        service = AuthService()
        expected_url_prefix = "https://accounts.google.com/o/oauth2/v2/auth"

        with patch("authlib.integrations.httpx_client.OAuth2Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.create_authorization_url.return_value = (
                f"{expected_url_prefix}?client_id=test",
                "state123",
            )
            mock_client_class.return_value = mock_client

            # Act
            url = service.get_authorization_url()

            # Assert
            assert url.startswith(expected_url_prefix)
            mock_client.create_authorization_url.assert_called_once()


class TestAuthServiceExchangeCode:
    """Testes para AuthService.exchange_code"""

    def test_exchange_code_success(self):
        # Arrange
        service = AuthService()
        code = "valid_auth_code"
        expected_user_info = {
            "sub": "google_123",
            "name": "Test User",
            "email": "test@example.com",
            "picture": "https://example.com/photo.jpg",
        }

        with patch("authlib.integrations.httpx_client.OAuth2Client") as mock_client_class:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = expected_user_info
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client

            # Act
            result = service.exchange_code(code)

            # Assert
            assert result["google_id"] == "google_123"
            assert result["name"] == "Test User"
            assert result["email"] == "test@example.com"
            assert result["photo_url"] == "https://example.com/photo.jpg"

    def test_exchange_code_invalid_code_raises_401(self):
        # Arrange
        service = AuthService()
        code = "invalid_code"

        with patch("authlib.integrations.httpx_client.OAuth2Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.fetch_token.side_effect = Exception("Invalid code")
            mock_client_class.return_value = mock_client

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                service.exchange_code(code)

            assert exc_info.value.status_code == 401
            assert "Código de autorização inválido" in exc_info.value.detail


class TestAuthServiceGetOrCreateUser:
    """Testes para AuthService.get_or_create_user"""

    def test_creates_new_user_when_not_exists(self, db_session, sample_user_data):
        # Arrange
        service = AuthService()

        # Act
        user = service.get_or_create_user(db_session, sample_user_data)

        # Assert
        assert user.google_id == sample_user_data["google_id"]
        assert user.name == sample_user_data["name"]
        assert user.email == sample_user_data["email"]
        assert user.photo_url == sample_user_data["photo_url"]
        assert user.id is not None

    def test_returns_existing_user_when_exists(self, db_session, sample_user, sample_user_data):
        # Arrange
        service = AuthService()

        # Act
        user = service.get_or_create_user(db_session, sample_user_data)

        # Assert
        assert user.id == sample_user.id
        assert user.google_id == sample_user.google_id


class TestAuthServiceCreateJwt:
    """Testes para AuthService.create_jwt"""

    def test_creates_valid_jwt_token(self, sample_user_id):
        # Arrange
        service = AuthService()

        # Act
        token = service.create_jwt(sample_user_id)

        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_jwt_contains_user_id(self, sample_user_id):
        # Arrange
        service = AuthService()
        from jose import jwt
        from app.config import settings

        # Act
        token = service.create_jwt(sample_user_id)
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        # Assert
        assert payload["sub"] == str(sample_user_id)

    def test_jwt_has_expiration(self, sample_user_id):
        # Arrange
        service = AuthService()
        from jose import jwt
        from app.config import settings

        # Act
        token = service.create_jwt(sample_user_id)
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        # Assert
        assert "exp" in payload
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp_time > datetime.now(timezone.utc)


class TestAuthServiceVerifyJwt:
    """Testes para AuthService.verify_jwt"""

    def test_verify_valid_token_returns_user_id(self, valid_jwt_token, sample_user_id):
        # Arrange
        service = AuthService()

        # Act
        result = service.verify_jwt(valid_jwt_token)

        # Assert
        assert result == sample_user_id

    def test_verify_expired_token_raises_401(self, expired_jwt_token):
        # Arrange
        service = AuthService()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.verify_jwt(expired_jwt_token)

        assert exc_info.value.status_code == 401
        assert "Token expirado" in exc_info.value.detail

    def test_verify_invalid_token_raises_401(self):
        # Arrange
        service = AuthService()
        invalid_token = "invalid.token.here"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.verify_jwt(invalid_token)

        assert exc_info.value.status_code == 401
        assert "Token inválido ou ausente" in exc_info.value.detail

    def test_verify_malformed_token_raises_401(self):
        # Arrange
        service = AuthService()
        malformed_token = "not_a_jwt"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.verify_jwt(malformed_token)

        assert exc_info.value.status_code == 401
