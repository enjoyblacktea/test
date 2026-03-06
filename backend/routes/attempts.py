"""Practice attempt routes for recording and retrieving practice history."""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from .auth import require_auth
from services import attempt_service

logger = logging.getLogger(__name__)

# Create Blueprint
attempts_bp = Blueprint('attempts', __name__)


@attempts_bp.route('', methods=['POST'])
@require_auth
def record_attempt(user_id):
    """Record a practice attempt (non-blocking).

    Requires authentication via JWT access token.

    Request body:
        {
            "character_id": 1,
            "started_at": "2024-01-01T00:00:00Z",
            "ended_at": "2024-01-01T00:00:05Z",
            "is_correct": true
        }

    Response (202 Accepted):
        {
            "message": "Attempt recorded",
            "attempt_id": 123
        }

    Error responses:
        400 Bad Request - Missing required fields
        401 Unauthorized - Invalid or missing token
        404 Not Found - Character ID not found
        500 Internal Server Error - Recording failed
    """
    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({'error': 'Request body required'}), 400

        # Required fields
        character_id = data.get('character_id')
        started_at_str = data.get('started_at')
        ended_at_str = data.get('ended_at')
        is_correct = data.get('is_correct')

        # Check required fields
        missing_fields = []
        if character_id is None:
            missing_fields.append('character_id')
        if not started_at_str:
            missing_fields.append('started_at')
        if not ended_at_str:
            missing_fields.append('ended_at')
        if is_correct is None:
            missing_fields.append('is_correct')

        if missing_fields:
            return jsonify({
                'error': f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Parse timestamps
        try:
            started_at = datetime.fromisoformat(started_at_str.replace('Z', '+00:00'))
            ended_at = datetime.fromisoformat(ended_at_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            return jsonify({
                'error': 'Invalid timestamp format. Use ISO 8601 format (e.g., 2024-01-01T00:00:00Z)'
            }), 400

        # Optional keystrokes array (backward-compatible)
        keystrokes = data.get('keystrokes') or None

        # Record attempt (non-blocking - return immediately)
        attempt_id = attempt_service.record_attempt(
            user_id=user_id,
            character_id=character_id,
            started_at=started_at,
            ended_at=ended_at,
            is_correct=is_correct,
            keystrokes=keystrokes
        )

        if attempt_id is None:
            # Log error but return 202 to maintain non-blocking behavior
            logger.error(
                f"Failed to record attempt for user={user_id}, character={character_id}"
            )
            # Still return success to frontend (don't interrupt practice)
            return jsonify({
                'message': 'Attempt received (recording in progress)',
                'attempt_id': None
            }), 202

        return jsonify({
            'message': 'Attempt recorded',
            'attempt_id': attempt_id
        }), 202

    except Exception as e:
        logger.error(f"Error in record_attempt endpoint: {e}")
        # Return 202 even on error (non-blocking behavior)
        return jsonify({
            'message': 'Attempt received (processing)',
            'error': str(e)
        }), 202


@attempts_bp.route('', methods=['GET'])
@require_auth
def get_attempts(user_id):
    """Get user's practice history with pagination and filtering.

    Requires authentication via JWT access token.
    Users can only access their own practice history.

    Query Parameters:
        page (int): Page number (default: 1)
        limit (int): Results per page (default: 50, max: 100)
        is_correct (bool): Filter by correctness (optional)
        character_id (int): Filter by character (optional)
        start_date (str): Filter attempts after date (ISO 8601) (optional)
        end_date (str): Filter attempts before date (ISO 8601) (optional)

    Response (200 OK):
        {
            "attempts": [
                {
                    "id": 123,
                    "character_id": 1,
                    "character": "你",
                    "input_code": "s u 3",
                    "started_at": "2024-01-01T00:00:00Z",
                    "ended_at": "2024-01-01T00:00:05Z",
                    "is_correct": true,
                    "duration_ms": 5000,
                    "created_at": "2024-01-01T00:00:05Z"
                }
            ],
            "pagination": {
                "total_count": 150,
                "page": 1,
                "limit": 50,
                "total_pages": 3,
                "has_more": true
            }
        }

    Error responses:
        401 Unauthorized - Invalid or missing token
        500 Internal Server Error - Query failed
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)

        # Build filters
        filters = {}

        if 'is_correct' in request.args:
            # Parse boolean (handle "true"/"false" strings)
            is_correct_str = request.args.get('is_correct', '').lower()
            filters['is_correct'] = is_correct_str in ('true', '1', 'yes')

        if 'character_id' in request.args:
            filters['character_id'] = request.args.get('character_id', type=int)

        if 'start_date' in request.args:
            try:
                start_date_str = request.args.get('start_date')
                filters['start_date'] = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return jsonify({'error': 'Invalid start_date format'}), 400

        if 'end_date' in request.args:
            try:
                end_date_str = request.args.get('end_date')
                filters['end_date'] = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return jsonify({'error': 'Invalid end_date format'}), 400

        # Get user's attempts
        result = attempt_service.get_user_attempts(
            user_id=user_id,
            page=page,
            limit=limit,
            filters=filters
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in get_attempts endpoint: {e}")
        return jsonify({'error': 'Failed to retrieve attempts'}), 500
