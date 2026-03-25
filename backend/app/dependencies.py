import time

import redis
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.service import AuthService
from app.config import settings
from app.database import SessionLocal

bearer_scheme = HTTPBearer()
auth_service = AuthService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    user_id = auth_service.verify_jwt(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    return user


def rate_limiter(
    current_user: User = Depends(get_current_user),
    request: Request = None,
):
    r = redis.from_url(settings.REDIS_URL)
    key = f"rate:{current_user.id}"
    now = time.time()
    window_start = now - 60

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, 60)
    results = pipe.execute()

    count = results[2]
    if count > 60:
        raise HTTPException(
            status_code=429,
            detail="Limite de requisições excedido",
            headers={"Retry-After": "60"},
        )
