from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from src.auth.models import User
from src.config import settings

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
SCOPES = "openid email profile"


class AuthService:
    def get_authorization_url(self) -> str:
        from authlib.integrations.httpx_client import OAuth2Client

        client = OAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            scope=SCOPES,
        )
        url, _ = client.create_authorization_url(GOOGLE_AUTH_URL)
        return url

    def exchange_code(self, code: str) -> dict:
        from authlib.integrations.httpx_client import OAuth2Client

        client = OAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
        try:
            client.fetch_token(
                GOOGLE_TOKEN_URL,
                code=code,
            )
            resp = client.get(GOOGLE_USERINFO_URL)
            resp.raise_for_status()
            user_info = resp.json()
        except Exception:
            raise HTTPException(status_code=401, detail="Código de autorização inválido")

        return {
            "google_id": user_info.get("sub"),
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "photo_url": user_info.get("picture"),
        }

    def get_or_create_user(self, db: Session, user_data: dict) -> User:
        user = db.query(User).filter(User.google_id == user_data["google_id"]).first()
        if user is None:
            user = User(
                google_id=user_data["google_id"],
                name=user_data["name"],
                email=user_data["email"],
                photo_url=user_data.get("photo_url"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def create_jwt(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    def verify_jwt(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return UUID(payload["sub"])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido ou ausente")
