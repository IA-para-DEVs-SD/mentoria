from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.dependencies import get_current_user, get_db
from app.profile.schemas import ProfileIn, ProfileOut
from app.profile.service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])
profile_service = ProfileService()


@router.get("", response_model=ProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = profile_service.get_profile(db, current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return ProfileOut.model_validate(profile)


@router.post("", response_model=ProfileOut)
def upsert_profile(
    profile_in: ProfileIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return profile_service.upsert_profile(db, current_user.id, profile_in)
