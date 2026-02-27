"""Character service for database-backed character retrieval and zhuyin mapping."""

import logging
import random
from typing import Optional, Dict, List, Tuple
from .db_service import execute_query
from models.character import Character

logger = logging.getLogger(__name__)

# Keyboard key to zhuyin symbol mapping (Taiwan standard keyboard layout)
KEY_TO_ZHUYIN = {
    # Consonants - Row 1
    '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
    '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
    'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
    'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
    '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
    'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
    # Vowels
    'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
    '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
    '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
    '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
    '-': 'ㄦ',
    # Tones
    ' ': '',    # First tone (no mark) - represented as space
    '6': 'ˊ',   # Second tone
    '3': 'ˇ',   # Third tone
    '4': 'ˋ',   # Fourth tone
    '7': '˙'    # Fifth tone (light/neutral)
}

# Reverse mapping: zhuyin symbol to keyboard key
ZHUYIN_TO_KEY = {v: k for k, v in KEY_TO_ZHUYIN.items() if v}  # Exclude empty string
ZHUYIN_TO_KEY[''] = ' '  # Special case for first tone


def parse_input_code(input_code: str) -> Tuple[List[str], List[str]]:
    """Parse input_code string into zhuyin and keys arrays.

    Args:
        input_code: Space-separated keyboard keys (e.g., "j i 3")

    Returns:
        Tuple of (zhuyin_array, keys_array)
        Example: ("j i 3") -> (["ㄨ", "ㄛ", "ˇ"], ["j", "i", "3"])

    Example:
        zhuyin, keys = parse_input_code("s u 3")
        # zhuyin = ["ㄋ", "ㄧ", "ˇ"]
        # keys = ["s", "u", "3"]
    """
    # Split by space (handle multiple spaces)
    keys = input_code.strip().split()

    # Convert each key to zhuyin symbol
    zhuyin = []
    for key in keys:
        symbol = KEY_TO_ZHUYIN.get(key, '')
        zhuyin.append(symbol)

    return zhuyin, keys


def get_random_character(input_method: str = 'bopomofo') -> Optional[Dict]:
    """Get a random character from the database with parsed zhuyin data.

    Args:
        input_method: Input method filter (default: 'bopomofo')

    Returns:
        Dictionary with word, zhuyin array, keys array, and character_id
        Example:
            {
                "id": 1,
                "word": "你",
                "zhuyin": ["ㄋ", "ㄧ", "ˇ"],
                "keys": ["s", "u", "3"]
            }
        Returns None if no characters found or database error

    Example:
        char_data = get_random_character(input_method='bopomofo')
        if char_data:
            print(f"Character: {char_data['word']}")
    """
    try:
        # Query all characters for the specified input method
        query = """
            SELECT id, character, input_code, input_method, created_at
            FROM characters
            WHERE input_method = %s
        """
        rows = execute_query(query, (input_method,), fetch_all=True)

        if not rows:
            logger.warning(f"No characters found for input_method='{input_method}'")
            return None

        # Select random character
        random_row = random.choice(rows)
        character = Character.from_db_row(random_row)

        # Parse input_code to zhuyin and keys arrays
        zhuyin, keys = parse_input_code(character.input_code)

        return {
            'id': character.id,
            'word': character.character,
            'zhuyin': zhuyin,
            'keys': keys
        }

    except Exception as e:
        logger.error(f"Error getting random character: {e}")
        return None


def get_character_by_id(character_id: int) -> Optional[Character]:
    """Retrieve a character by ID.

    Args:
        character_id: Character ID to look up

    Returns:
        Character object if found, None otherwise

    Example:
        char = get_character_by_id(5)
    """
    try:
        query = """
            SELECT id, character, input_code, input_method, created_at
            FROM characters
            WHERE id = %s
        """
        row = execute_query(query, (character_id,), fetch_one=True)

        if row:
            return Character.from_db_row(row)
        return None

    except Exception as e:
        logger.error(f"Error fetching character by ID: {e}")
        return None


def get_character_by_text(text: str, input_method: str = 'bopomofo') -> Optional[Character]:
    """Retrieve a character by text and input method.

    Args:
        text: Chinese character text
        input_method: Input method (default: 'bopomofo')

    Returns:
        Character object if found, None otherwise

    Example:
        char = get_character_by_text("你", "bopomofo")
    """
    try:
        query = """
            SELECT id, character, input_code, input_method, created_at
            FROM characters
            WHERE character = %s AND input_method = %s
        """
        row = execute_query(query, (text, input_method), fetch_one=True)

        if row:
            return Character.from_db_row(row)
        return None

    except Exception as e:
        logger.error(f"Error fetching character by text: {e}")
        return None
