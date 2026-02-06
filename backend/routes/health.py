"""Health check API routes.

This module provides health check endpoints for monitoring.
"""

from flask import Blueprint, jsonify
from services import word_service


health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint.

    Returns:
        Response: JSON response with status and words count.
                  - 200: {"status": "ok", "words_loaded": <count>}
    """
    return jsonify({
        "status": "ok",
        "words_loaded": word_service.get_words_count()
    })
