"""Health check API routes.

This module provides health check endpoints for monitoring.
"""

from flask import Blueprint, jsonify
from services import db_service
import logging
import time

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint with database connectivity test.

    Returns:
        Response: JSON response with status, database connectivity, and character count.
                  - 200: {"status": "ok", "database": "connected", "characters_loaded": <count>, "response_time_ms": <ms>}
                  - 503: {"status": "error", "database": "disconnected", "error": "<message>", "response_time_ms": <ms>}
    """
    start_time = time.time()

    response_data = {
        "status": "ok",
        "database": "disconnected",
        "characters_loaded": 0
    }

    try:
        # Test database connectivity by querying character count
        result = db_service.execute_query(
            "SELECT COUNT(*) FROM characters",
            fetch_one=True
        )

        if result:
            response_data["database"] = "connected"
            response_data["characters_loaded"] = result[0]
            response_data["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
            return jsonify(response_data), 200
        else:
            response_data["status"] = "error"
            response_data["error"] = "No data returned from database"
            response_data["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
            return jsonify(response_data), 503

    except Exception as e:
        logger.error(f"Health check database error: {e}")
        response_data["status"] = "error"
        response_data["error"] = str(e)
        response_data["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
        return jsonify(response_data), 503
