"""Configuration management for Zhuyin Practice Backend.

This module centralizes all configuration values including file paths,
server settings, and environment-specific configurations.
"""

import os


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
