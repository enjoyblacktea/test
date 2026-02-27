"""Words API routes.

This module provides API endpoints for retrieving practice words.
"""

from flask import Blueprint, jsonify, request
from services import word_service, character_service
from services.db_service import test_connection
import logging

logger = logging.getLogger(__name__)

words_bp = Blueprint('words', __name__)


@words_bp.route('/random', methods=['GET'])
def get_random_word():
    """Return a random practice word with zhuyin and keys.

    Query Parameters:
        input_method (str, optional): Input method filter (default: 'bopomofo')

    Returns:
        Response: JSON response with word data or error message.
                  - 200: {"word": "字", "zhuyin": [...], "keys": [...]}
                  - 404: {"error": "No characters available"}
                  - 503: {"error": "Database service unavailable"}
    """
    # Get input_method query parameter (default to 'bopomofo')
    input_method = request.args.get('input_method', 'bopomofo')

    # Check database connectivity
    if not test_connection():
        logger.error("Database connection failed for /api/words/random")
        return jsonify({
            "error": "Database service unavailable",
            "message": "Unable to connect to database"
        }), 503

    # Get random character from database
    try:
        word_data = character_service.get_random_character(input_method=input_method)

        if word_data is None:
            return jsonify({
                "error": "No characters available",
                "message": f"No characters found for input_method='{input_method}'"
            }), 404

        # Return character data including ID (needed for practice recording)
        return jsonify({
            "id": word_data["id"],
            "word": word_data["word"],
            "zhuyin": word_data["zhuyin"],
            "keys": word_data["keys"]
        })

    except Exception as e:
        logger.error(f"Error retrieving random character: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to retrieve character"
        }), 500
