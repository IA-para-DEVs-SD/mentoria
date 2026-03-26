from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.schemas import TokenResponse
from app.auth.service import AuthService
from app.config import settings
from app.dependencies import get_db

router = APIRouter()
auth_service = AuthService()


@router.get("/google/login")
def google_login():
    url = auth_service.get_authorization_url()
    return RedirectResponse(url=url)


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    user_data = auth_service.exchange_code(code)
    user = auth_service.get_or_create_user(db, user_data)

    has_profile = (
        user.profile is not None
        and bool(user.profile.career_goal)
        and bool(user.profile.skills)
    )

    token = auth_service.create_jwt(user.id)
    params = urlencode({"token": token, "has_profile": str(has_profile).lower()})
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth/callback?{params}")
