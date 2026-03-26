"""
Testes unitários para o módulo dependencies.py
"""
import time
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth.models import User
from app.dependencies import get_current_user, get_db, rate_limiter


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
        with patch("app.dependencies.SessionLocal") as mock_session_local:
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


class TestRateLimiter:
    """Testes para a função rate_limiter."""

    def test_allows_request_under_limit(self, sample_user):
        # Arrange
        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_redis.pipeline.return_value = mock_pipe
        mock_pipe.__enter__ = MagicMock(return_value=mock_pipe)
        mock_pipe.__exit__ = MagicMock(return_value=False)
        mock_pipe.execute.return_value = [None, None, 10, None]  # 10 requests

        with patch("app.dependencies.redis") as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis

            # Act & Assert (should not raise)
            rate_limiter(current_user=sample_user, request=None)

    def test_raises_429_when_limit_exceeded(self, sample_user):
        # Arrange
        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_redis.pipeline.return_value = mock_pipe
        mock_pipe.__enter__ = MagicMock(return_value=mock_pipe)
        mock_pipe.__exit__ = MagicMock(return_value=False)
        mock_pipe.execute.return_value = [None, None, 61, None]  # 61 requests (over limit)

        with patch("app.dependencies.redis") as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                rate_limiter(current_user=sample_user, request=None)

            assert exc_info.value.status_code == 429
            assert "Limite de requisições excedido" in exc_info.value.detail
            assert exc_info.value.headers["Retry-After"] == "60"

    def test_uses_user_id_as_rate_limit_key(self, sample_user):
        # Arrange
        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_redis.pipeline.return_value = mock_pipe
        mock_pipe.__enter__ = MagicMock(return_value=mock_pipe)
        mock_pipe.__exit__ = MagicMock(return_value=False)
        mock_pipe.execute.return_value = [None, None, 1, None]

        with patch("app.dependencies.redis") as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis

            # Act
            rate_limiter(current_user=sample_user, request=None)

            # Assert
            expected_key = f"rate:{sample_user.id}"
            mock_pipe.zremrangebyscore.assert_called()
            call_args = mock_pipe.zremrangebyscore.call_args[0]
            assert call_args[0] == expected_key

    def test_sets_expiration_on_rate_limit_key(self, sample_user):
        # Arrange
        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_redis.pipeline.return_value = mock_pipe
        mock_pipe.__enter__ = MagicMock(return_value=mock_pipe)
        mock_pipe.__exit__ = MagicMock(return_value=False)
        mock_pipe.execute.return_value = [None, None, 1, None]

        with patch("app.dependencies.redis") as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis

            # Act
            rate_limiter(current_user=sample_user, request=None)

            # Assert
            mock_pipe.expire.assert_called()
            call_args = mock_pipe.expire.call_args[0]
            assert call_args[1] == 60  # 60 seconds expiration
