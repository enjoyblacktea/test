"""Words API routes.

This module provides API endpoints for retrieving practice words.
"""

from flask import Blueprint, jsonify
from services import word_service


words_bp = Blueprint('words', __name__)


@words_bp.route('/random', methods=['GET'])
def get_random_word():
    """Return a random practice word with zhuyin and keys.

    Returns:
        Response: JSON response with word data or error message.
                  - 200: {"word": "字", "zhuyin": [...], "keys": [...]}
                  - 500: {"error": "...", "message": "..."}
    """
    word = word_service.get_random_word()

    if word is None:
        return jsonify({
            "error": "No words data available",
            "message": "words.json is missing or empty"
        }), 500

    return jsonify(word)
