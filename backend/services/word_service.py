"""Word service module for managing practice word data.

This module handles loading and providing access to the practice words data.
Data is loaded once at module import time and cached in memory.
"""

import json
import random
from config import Config


# Module-level data storage (loaded once at startup)
_words_data = []


def _load_words():
    """Load words data from JSON file into module-level cache.

    This function is called automatically when the module is imported.
    Errors are logged but do not prevent the module from loading.
    """
    global _words_data
    try:
        with open(Config.WORDS_DATA_PATH, 'r', encoding='utf-8') as f:
            _words_data = json.load(f)
        print(f"Loaded {len(_words_data)} words from words.json")
    except FileNotFoundError:
        print(f"Error: words.json not found at {Config.WORDS_DATA_PATH}")
        _words_data = []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in words.json: {e}")
        _words_data = []


# Initialize data on module import
_load_words()


def get_random_word():
    """Get a random practice word from the loaded data.

    Returns:
        dict: A word dictionary with 'word', 'zhuyin', and 'keys' fields,
              or None if no data is available.

    Example:
        >>> word = get_random_word()
        >>> if word:
        ...     print(word['word'], word['zhuyin'], word['keys'])
    """
    if not _words_data:
        return None
    return random.choice(_words_data)


def get_words_count():
    """Get the number of loaded practice words.

    Returns:
        int: The count of loaded words (0 if no data available).
    """
    return len(_words_data)
