## Why

The current implementation uses frontend-only authentication and static JSON data files, which limits data analysis capabilities and prevents tracking user practice history. To enable data-driven insights and improve learning outcomes, we need persistent storage of practice data with proper user authentication.

## What Changes

- Add PostgreSQL database with normalized schema (Phase 1: users, characters, typing_attempts tables)
- Replace frontend-only authentication with JWT-based backend authentication using bcrypt password hashing
- Create REST API endpoints for user registration, login, token refresh, and practice recording
- Migrate character data from static JSON to database with support for future multi-input methods
- Add non-blocking practice attempt recording that doesn't interrupt user flow
- Implement frontend integration with centralized API client and token management

## Capabilities

### New Capabilities

- `backend-authentication`: JWT-based user authentication system with secure password hashing (bcrypt), token generation, refresh mechanism, and protected route middleware
- `database-schema`: PostgreSQL database schema with three normalized tables (users, characters, typing_attempts) including proper indexes, foreign key constraints, and migration scripts
- `practice-data-recording`: API endpoints for recording practice attempts and querying practice history with pagination support

### Modified Capabilities

- `practice-word-api`: Change from static JSON file-based character retrieval to database-backed queries with support for input method filtering

## Impact

**Backend**:
- `backend/app.py` - Add database connection and JWT configuration
- `backend/routes/` - New auth.py blueprint, modified words.py
- `backend/services/` - New auth_service.py, db_service.py, modified word_service.py
- `backend/models/` - New SQLAlchemy models for User, Character, TypingAttempt
- `backend/migrations/` - New init_db.sql with schema and seed data
- `backend/config.py` - New database and JWT configuration

**Frontend**:
- `frontend/js/modules/api.js` - New centralized API client with JWT token handling
- `frontend/js/modules/auth-backend.js` - New backend-integrated auth module (replaces auth.js)
- `frontend/js/modules/practice.js` - Modified to record attempts via API
- `frontend/login.html` - New login/registration page

**Dependencies**:
- PyJWT (^2.8.0) - JWT token generation and validation
- bcrypt (^4.1.2) - Password hashing
- psycopg2-binary (^2.9.9) - PostgreSQL adapter
- SQLAlchemy (^2.0.25) - Database ORM (optional, for cleaner models)

**Database**:
- Requires PostgreSQL 12+ instance
- Connection pooling configuration
- Initial migration to create schema
