"""
Testes unitários para o módulo dependencies.py
"""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.models import User
from src.dependencies import get_current_user, get_db


class TestGetDb:
    """Testes para a função get_db."""

    def test_yields_session(self):
        # Arrange & Act
        gen = get_db()
        session = next(gen)

        # Assert
        assert session is not None

        # Cleanup
        try:
            next(gen)
        except StopIteration:
            pass

    def test_closes_session_after_use(self):
        # Arrange
        with patch("src.dependencies.SessionLocal") as mock_session_local:
            mock_session = MagicMock()
            mock_session_local.return_value = mock_session

            # Act
            gen = get_db()
            next(gen)
            try:
                next(gen)
            except StopIteration:
                pass

            # Assert
            mock_session.close.assert_called_once()


class TestGetCurrentUser:
    """Testes para a função get_current_user."""

    def test_returns_user_with_valid_token(self, db_session, sample_user, valid_jwt_token):
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=valid_jwt_token,
        )

        # Act
        result = get_current_user(credentials, db_session)

        # Assert
        assert result.id == sample_user.id
        assert result.email == sample_user.email

    def test_raises_401_with_expired_token(self, db_session, sample_user, expired_jwt_token):
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=expired_jwt_token,
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, db_session)

        assert exc_info.value.status_code == 401
        assert "Token expirado" in exc_info.value.detail

    def test_raises_401_with_invalid_token(self, db_session):
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token",
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, db_session)

        assert exc_info.value.status_code == 401

    def test_raises_401_when_user_not_found(self, db_session, valid_jwt_token):
        # Arrange
        # User doesn't exist in this session
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=valid_jwt_token,
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, db_session)

        assert exc_info.value.status_code == 401
        assert "Token inválido ou ausente" in exc_info.value.detail
