"""Word service module for managing practice word data.

DEPRECATED: This module is being migrated to use database-backed character_service.
The get_random_word() function now calls character_service instead of loading from JSON.
"""

import json
import logging
from config import Config

# Import character service for database-backed retrieval
try:
    from services import character_service
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False
    logging.warning("character_service not available, falling back to JSON")

logger = logging.getLogger(__name__)

# Module-level data storage (kept for backwards compatibility/fallback)
_words_data = []


def _load_words():
    """Load words data from JSON file into module-level cache.

    DEPRECATED: Used only as fallback if database is unavailable.
    """
    global _words_data
    try:
        with open(Config.WORDS_DATA_PATH, 'r', encoding='utf-8') as f:
            _words_data = json.load(f)
        logger.info(f"Loaded {len(_words_data)} words from words.json (fallback)")
    except FileNotFoundError:
        logger.warning(f"words.json not found at {Config.WORDS_DATA_PATH}")
        _words_data = []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in words.json: {e}")
        _words_data = []


# Initialize fallback data on module import
_load_words()


def get_random_word():
    """Get a random practice word.

    Now uses character_service to retrieve from database.
    Falls back to JSON data if database is unavailable.

    Returns:
        dict: A word dictionary with 'word', 'zhuyin', and 'keys' fields,
              or None if no data is available.

    Example:
        >>> word = get_random_word()
        >>> if word:
        ...     print(word['word'], word['zhuyin'], word['keys'])
    """
    # Try database first
    if USE_DATABASE:
        try:
            word_data = character_service.get_random_character(input_method='bopomofo')
            if word_data:
                # Return in same format as JSON (without 'id' field)
                return {
                    'word': word_data['word'],
                    'zhuyin': word_data['zhuyin'],
                    'keys': word_data['keys']
                }
        except Exception as e:
            logger.error(f"Database retrieval failed, falling back to JSON: {e}")

    # Fallback to JSON data
    if not _words_data:
        return None
    import random
    return random.choice(_words_data)


def get_words_count():
    """Get the number of loaded practice words.

    Returns:
        int: The count of loaded words (0 if no data available).
    """
    return len(_words_data)
