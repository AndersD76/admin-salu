import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    get_current_admin,
)
from app.models.user import User, UserRole
from app.schemas import LoginRequest, TokenResponse, MeResponse

router = APIRouter()

# Simple in-memory rate limiter for login
_login_attempts: dict[str, list[float]] = defaultdict(list)
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutes


def _check_rate_limit(ip: str):
    now = time.time()
    # Clean old attempts
    _login_attempts[ip] = [
        t for t in _login_attempts[ip]
        if now - t < LOGIN_WINDOW_SECONDS
    ]
    if len(_login_attempts[ip]) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later."
        )
    _login_attempts[ip].append(now)


@router.post("/login", response_model=TokenResponse)
async def login(
    request_body: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Login admin user"""
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)

    user = db.query(User).filter(
        User.email == request_body.email
    ).first()

    if not user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(request_body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=MeResponse)
async def get_me(
    current_user: User = Depends(get_current_admin),
):
    """Get current admin user info"""
    return current_user
