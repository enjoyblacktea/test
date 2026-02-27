"""Configuration management for Zhuyin Practice Backend.

This module centralizes all configuration values including file paths,
server settings, and environment-specific configurations.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration.

    All configuration values should be defined here as class attributes.
    Other modules should import and reference this Config class instead
    of hardcoding values.

    Attributes:
        BASE_DIR: Absolute path to the backend directory
        WORDS_DATA_PATH: Path to words.json data file
        PORT: Server port number (from PORT env var, default 5000)
        DEBUG: Debug mode flag (from FLASK_ENV env var)
    """

    # Directory paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WORDS_DATA_PATH = os.path.join(BASE_DIR, 'data', 'words.json')

    # Server configuration
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # Database configuration
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/zhuyin_practice'
    )
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '10'))
    DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '3600'))  # 1 hour

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRY = timedelta(days=7)

    # Security configuration
    BCRYPT_WORK_FACTOR = int(os.getenv('BCRYPT_WORK_FACTOR', '12'))
