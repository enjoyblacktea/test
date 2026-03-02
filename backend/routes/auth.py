"""Authentication routes for user registration, login, and token refresh."""

import logging
from functools import wraps
from flask import Blueprint, request, jsonify
from services import auth_service

logger = logging.getLogger(__name__)

# Create Blueprint
auth_bp = Blueprint('auth', __name__)


def require_auth(f):
    """Decorator to protect routes requiring authentication.

    Validates JWT access token from Authorization header.
    Extracts user_id and passes it to the route handler.

    Usage:
        @auth_bp.route('/protected')
        @require_auth
        def protected_route(user_id):
            return jsonify({'user_id': user_id})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401

        # Expected format: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format'}), 401

        token = parts[1]

        # Verify token
        payload = auth_service.verify_token(token, token_type='access')
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Extract user_id and pass to route handler
        user_id = payload.get('user_id')
        return f(user_id=user_id, *args, **kwargs)

    return decorated_function


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account.

    Request body:
        {
            "username": "string",
            "password": "string"
        }

    Response (201 Created):
        {
            "user": {
                "id": 1,
                "username": "alice",
                "created_at": "2024-01-01T00:00:00"
            },
            "message": "User registered successfully"
        }

    Error responses:
        400 Bad Request - Missing username or password
        409 Conflict - Username already exists
        500 Internal Server Error - Database error
    """
    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({'error': 'Request body required'}), 400

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        if not password:
            return jsonify({'error': 'Password is required'}), 400

        # Create user
        user, error = auth_service.create_user(username, password)

        if error:
            if 'already exists' in error:
                return jsonify({'error': error}), 409
            return jsonify({'error': error}), 500

        # Return user info (exclude password_hash)
        return jsonify({
            'user': user.to_dict(include_password=False),
            'message': 'User registered successfully'
        }), 201

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens.

    Request body:
        {
            "username": "string",
            "password": "string"
        }

    Response (200 OK):
        {
            "access_token": "jwt_token_string",
            "refresh_token": "jwt_token_string",
            "user": {
                "id": 1,
                "username": "alice",
                "created_at": "2024-01-01T00:00:00"
            }
        }

    Error responses:
        400 Bad Request - Missing username or password
        401 Unauthorized - Invalid credentials
        500 Internal Server Error - Authentication error
    """
    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({'error': 'Request body required'}), 400

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Authenticate user
        user, error = auth_service.authenticate_user(username, password)

        if error:
            # Always return 401 for authentication failures (don't reveal details)
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate tokens
        access_token = auth_service.generate_access_token(user.id)
        refresh_token = auth_service.generate_refresh_token(user.id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(include_password=False)
        }), 200

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token using refresh token.

    Request body:
        {
            "refresh_token": "jwt_token_string"
        }

    Response (200 OK):
        {
            "access_token": "new_jwt_token_string"
        }

    Error responses:
        400 Bad Request - Missing refresh token
        401 Unauthorized - Invalid or expired refresh token
        500 Internal Server Error - Token generation error
    """
    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({'error': 'Request body required'}), 400

        refresh_token = data.get('refresh_token', '').strip()

        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400

        # Verify refresh token
        payload = auth_service.verify_token(refresh_token, token_type='refresh')

        if not payload:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401

        # Get user_id from payload
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token payload'}), 401

        # Generate new access token
        new_access_token = auth_service.generate_access_token(user_id)

        return jsonify({
            'access_token': new_access_token
        }), 200

    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
