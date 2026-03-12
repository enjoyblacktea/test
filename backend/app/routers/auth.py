import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse, AccessTokenResponse, UserOut
from app.services import auth_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    username = body.username.strip()
    password = body.password
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")

    user, error = await auth_service.create_user(db, username, password)
    if error:
        if "already exists" in error:
            raise HTTPException(status_code=409, detail=error)
        raise HTTPException(status_code=500, detail=error)

    return {"user": UserOut.model_validate(user), "message": "User registered successfully"}


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    username = body.username.strip()
    password = body.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    user, error = await auth_service.authenticate_user(db, username, password)
    if error:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenResponse(
        access_token=auth_service.generate_access_token(user.id),
        refresh_token=auth_service.generate_refresh_token(user.id),
        user=UserOut.model_validate(user),
    )


@router.post("/refresh")
async def refresh(body: RefreshRequest):
    token = body.refresh_token.strip()
    if not token:
        raise HTTPException(status_code=400, detail="Refresh token is required")

    payload = auth_service.verify_token(token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return AccessTokenResponse(access_token=auth_service.generate_access_token(user_id))
