import logging
from datetime import datetime, timezone
from typing import Optional, Tuple
import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=settings.bcrypt_work_factor)
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def generate_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + settings.access_token_expiry,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def generate_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + settings.refresh_token_expiry,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != token_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def create_user(db: AsyncSession, username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    try:
        password_hash = hash_password(password)
        user = User(username=username, password_hash=password_hash)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"User created: {username} (id={user.id})")
        return user, None
    except Exception as e:
        await db.rollback()
        msg = str(e)
        if "unique" in msg.lower() or "duplicate" in msg.lower():
            return None, "Username already exists"
        logger.error(f"Error creating user: {e}")
        return None, "Database error"


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    user = await get_user_by_username(db, username)
    if not user:
        return None, "Invalid credentials"
    if not verify_password(password, user.password_hash):
        return None, "Invalid credentials"
    return user, None
