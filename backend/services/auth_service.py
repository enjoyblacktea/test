"""Authentication service for user management and JWT tokens."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
import bcrypt
import jwt
from config import Config
from .db_service import execute_query
from models.user import User

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Bcrypt hashed password string

    Example:
        hashed = hash_password("my_secure_password")
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_WORK_FACTOR)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a bcrypt hash.

    Args:
        password: Plain text password to verify
        password_hash: Bcrypt hash to compare against

    Returns:
        True if password matches hash, False otherwise

    Example:
        is_valid = verify_password("my_password", stored_hash)
    """
    try:
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def generate_access_token(user_id: int) -> str:
    """Generate a JWT access token.

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT access token string

    Example:
        token = generate_access_token(user_id=123)
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + Config.ACCESS_TOKEN_EXPIRY,
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


def generate_refresh_token(user_id: int) -> str:
    """Generate a JWT refresh token.

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT refresh token string

    Example:
        token = generate_refresh_token(user_id=123)
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + Config.REFRESH_TOKEN_EXPIRY,
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


def verify_token(token: str, token_type: str = 'access') -> Optional[dict]:
    """Decode and validate a JWT token.

    Args:
        token: JWT token string
        token_type: Expected token type ('access' or 'refresh')

    Returns:
        Decoded payload dict if valid, None otherwise

    Example:
        payload = verify_token(token, token_type='access')
        if payload:
            user_id = payload['user_id']
    """
    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        # Verify token type matches
        if payload.get('type') != token_type:
            logger.warning(f"Token type mismatch: expected {token_type}, got {payload.get('type')}")
            return None

        return payload

    except jwt.ExpiredSignatureError:
        logger.info("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None


def create_user(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """Create a new user account.

    Args:
        username: Unique username
        password: Plain text password (will be hashed)

    Returns:
        Tuple of (User object, error message)
        If successful: (User, None)
        If failed: (None, error message string)

    Example:
        user, error = create_user("alice", "secure_password")
        if error:
            print(f"Error: {error}")
    """
    try:
        # Hash password
        password_hash = hash_password(password)

        # Insert user
        query = """
            INSERT INTO users (username, password_hash, created_at, updated_at)
            VALUES (%s, %s, NOW(), NOW())
            RETURNING id, username, password_hash, created_at, updated_at
        """
        row = execute_query(query, (username, password_hash), fetch_one=True, commit=True)

        if row:
            user = User.from_db_row(row)
            logger.info(f"User created: {username} (id={user.id})")
            return user, None
        else:
            return None, "Failed to create user"

    except Exception as e:
        error_msg = str(e)
        if 'unique constraint' in error_msg.lower() or 'duplicate key' in error_msg.lower():
            return None, "Username already exists"
        logger.error(f"Error creating user: {e}")
        return None, "Database error"


def get_user_by_username(username: str) -> Optional[User]:
    """Retrieve a user by username.

    Args:
        username: Username to look up

    Returns:
        User object if found, None otherwise

    Example:
        user = get_user_by_username("alice")
        if user:
            print(f"Found user: {user.id}")
    """
    try:
        query = """
            SELECT id, username, password_hash, created_at, updated_at
            FROM users
            WHERE username = %s
        """
        row = execute_query(query, (username,), fetch_one=True)

        if row:
            return User.from_db_row(row)
        return None

    except Exception as e:
        logger.error(f"Error fetching user by username: {e}")
        return None


def get_user_by_id(user_id: int) -> Optional[User]:
    """Retrieve a user by ID.

    Args:
        user_id: User ID to look up

    Returns:
        User object if found, None otherwise

    Example:
        user = get_user_by_id(123)
    """
    try:
        query = """
            SELECT id, username, password_hash, created_at, updated_at
            FROM users
            WHERE id = %s
        """
        row = execute_query(query, (user_id,), fetch_one=True)

        if row:
            return User.from_db_row(row)
        return None

    except Exception as e:
        logger.error(f"Error fetching user by ID: {e}")
        return None


def authenticate_user(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """Authenticate a user with username and password.

    Args:
        username: Username
        password: Plain text password

    Returns:
        Tuple of (User object, error message)
        If successful: (User, None)
        If failed: (None, error message string)

    Example:
        user, error = authenticate_user("alice", "password123")
        if user:
            print("Authentication successful")
        else:
            print(f"Authentication failed: {error}")
    """
    try:
        # Get user by username
        user = get_user_by_username(username)

        if not user:
            # Don't reveal whether username exists (timing-safe response)
            logger.info(f"Authentication failed: user not found ({username})")
            return None, "Invalid credentials"

        # Verify password
        if not verify_password(password, user.password_hash):
            logger.info(f"Authentication failed: invalid password ({username})")
            return None, "Invalid credentials"

        logger.info(f"Authentication successful: {username} (id={user.id})")
        return user, None

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None, "Authentication error"
