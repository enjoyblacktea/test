"""History API routes for practice history tracking.

This module provides REST API endpoints for recording practice attempts,
querying history, and retrieving statistics.
"""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from psycopg2 import OperationalError, DatabaseError

logger = logging.getLogger(__name__)

# Create blueprint (will be registered in app.py)
history_bp = Blueprint('history', __name__, url_prefix='/api/history')

# Service dependencies (injected via init_history_routes)
_history_service = None


def init_history_routes(history_service):
    """Initialize history routes with service dependencies.

    Args:
        history_service: HistoryService instance

    This function must be called before registering the blueprint.
    """
    global _history_service
    _history_service = history_service
    logger.info("History routes initialized with dependencies")


@history_bp.route('/record', methods=['POST'])
def record_practice():
    """Record a practice attempt.

    Request JSON:
        {
            "username": str,
            "word": str,
            "is_correct": bool,
            "start_time": str (ISO 8601),
            "end_time": str (ISO 8601)
        }

    Returns:
        201: {"success": true, "record_id": int}
        400: {"success": false, "error": str} - Bad request
        503: {"success": false, "error": str} - Database unavailable
        500: {"success": false, "error": str} - Internal error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400

        # Validate required fields
        required_fields = ['username', 'word', 'is_correct', 'start_time', 'end_time']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        username = data['username']
        word = data['word']
        is_correct = data['is_correct']
        start_time_str = data['start_time']
        end_time_str = data['end_time']

        # Validate timestamp format (ISO 8601)
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            return jsonify({
                "success": False,
                "error": f"Invalid timestamp format: {e}. Use ISO 8601 format"
            }), 400

        # Validate time logic
        if end_time <= start_time:
            return jsonify({
                "success": False,
                "error": "end_time must be after start_time"
            }), 400

        # Get or create user
        user_id = _history_service.get_or_create_user(username)

        # Record practice
        record_id = _history_service.record_practice(
            user_id, word, is_correct, start_time, end_time
        )

        return jsonify({
            "success": True,
            "record_id": record_id
        }), 201

    except OperationalError as e:
        logger.error(f"Database unavailable: {e}")
        return jsonify({
            "success": False,
            "error": "Database unavailable"
        }), 503

    except DatabaseError as e:
        logger.error(f"Database error in record_practice: {e}")
        return jsonify({
            "success": False,
            "error": "Database error occurred"
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error in record_practice: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@history_bp.route('', methods=['GET'])
def get_history():
    """Get practice history for a user.

    Query Parameters:
        username (required): Username to query
        limit (optional): Max records to return (default 50)
        offset (optional): Number of records to skip (default 0)

    Returns:
        200: {"success": true, "total": int, "records": [...]}
        400: {"success": false, "error": str} - Bad request
        503: {"success": false, "error": str} - Database unavailable
        500: {"success": false, "error": str} - Internal error
    """
    try:
        # Validate username parameter
        username = request.args.get('username')
        if not username:
            return jsonify({
                "success": False,
                "error": "Missing username parameter"
            }), 400

        # Validate and parse limit and offset
        try:
            limit = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))

            if limit < 0 or offset < 0:
                return jsonify({
                    "success": False,
                    "error": "Invalid limit or offset: must be non-negative"
                }), 400

        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid limit or offset: must be numeric"
            }), 400

        # Get user (returns None if user doesn't exist)
        user_id = _history_service.get_or_create_user(username)

        # Get history
        result = _history_service.get_history(user_id, limit, offset)

        return jsonify({
            "success": True,
            **result  # Includes 'total' and 'records'
        }), 200

    except OperationalError as e:
        logger.error(f"Database unavailable: {e}")
        return jsonify({
            "success": False,
            "error": "Database unavailable"
        }), 503

    except DatabaseError as e:
        logger.error(f"Database error in get_history: {e}")
        return jsonify({
            "success": False,
            "error": "Database error occurred"
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error in get_history: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@history_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get practice statistics for a user.

    Query Parameters:
        username (required): Username to query

    Returns:
        200: {
            "success": true,
            "total_words": int,
            "correct_count": int,
            "accuracy": float,
            "avg_duration_ms": float,
            "practice_days": int
        }
        400: {"success": false, "error": str} - Bad request
        503: {"success": false, "error": str} - Database unavailable
        500: {"success": false, "error": str} - Internal error
    """
    try:
        # Validate username parameter
        username = request.args.get('username')
        if not username:
            return jsonify({
                "success": False,
                "error": "Missing username parameter"
            }), 400

        # Get user
        user_id = _history_service.get_or_create_user(username)

        # Get stats
        stats = _history_service.get_stats(user_id)

        return jsonify({
            "success": True,
            **stats
        }), 200

    except OperationalError as e:
        logger.error(f"Database unavailable: {e}")
        return jsonify({
            "success": False,
            "error": "Database unavailable"
        }), 503

    except DatabaseError as e:
        logger.error(f"Database error in get_stats: {e}")
        return jsonify({
            "success": False,
            "error": "Database error occurred"
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error in get_stats: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500
