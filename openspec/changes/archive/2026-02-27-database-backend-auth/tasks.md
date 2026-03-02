## 1. Database Schema Setup

- [x] 1.1 Create backend/migrations/init_db.sql with users table (id, username, password_hash, created_at, updated_at)
- [x] 1.2 Add characters table to migration (id, character, input_code, input_method, created_at, UNIQUE constraint)
- [x] 1.3 Add typing_attempts table to migration (id, user_id, character_id, started_at, ended_at, is_correct, duration_ms, created_at)
- [x] 1.4 Add all indexes to migration (idx_username, idx_input_method, idx_user_attempts, idx_character_attempts, idx_user_correct)
- [x] 1.5 Add foreign key constraints (user_id CASCADE, character_id RESTRICT)
- [x] 1.6 Add seed data for 30 bopomofo characters from words.json to migration
- [x] 1.7 Test migration script on local PostgreSQL instance
- [x] 1.8 Verify all tables, indexes, and constraints created correctly

## 2. Backend Configuration and Dependencies

- [x] 2.1 Update backend/pyproject.toml with new dependencies (PyJWT, bcrypt, psycopg2-binary, SQLAlchemy)
- [x] 2.2 Run uv sync to install dependencies
- [x] 2.3 Create backend/config.py with database configuration (DATABASE_URL from env)
- [x] 2.4 Add JWT configuration to config.py (JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRY=1h, REFRESH_TOKEN_EXPIRY=7d)
- [x] 2.5 Add connection pool configuration (pool_size=5-10, max_overflow=10, pool_recycle=3600)
- [x] 2.6 Create .env.example with required environment variables (DATABASE_URL, JWT_SECRET_KEY)

## 3. Database Models and Services

- [x] 3.1 Create backend/models/__init__.py for models package
- [x] 3.2 Create backend/models/user.py with User model (SQLAlchemy or dataclass)
- [x] 3.3 Create backend/models/character.py with Character model
- [x] 3.4 Create backend/models/typing_attempt.py with TypingAttempt model
- [x] 3.5 Create backend/services/db_service.py with connection pool initialization
- [x] 3.6 Add get_db_connection() function in db_service.py
- [x] 3.7 Add execute_query() helper for running SQL queries
- [x] 3.8 Test database connection and basic queries

## 4. Authentication Service and Utilities

- [x] 4.1 Create backend/services/auth_service.py
- [x] 4.2 Implement hash_password() using bcrypt with work factor 12
- [x] 4.3 Implement verify_password() using bcrypt.checkpw()
- [x] 4.4 Implement generate_access_token() with 1-hour expiry and user_id payload
- [x] 4.5 Implement generate_refresh_token() with 7-day expiry
- [x] 4.6 Implement verify_token() to decode and validate JWT tokens
- [x] 4.7 Implement create_user(username, password) to insert user with hashed password
- [x] 4.8 Implement get_user_by_username(username) to query user from database
- [x] 4.9 Implement authenticate_user(username, password) to validate credentials
- [x] 4.10 Add unit tests for auth_service functions

## 5. Authentication Routes

- [x] 5.1 Create backend/routes/auth.py Blueprint
- [x] 5.2 Implement POST /api/auth/register endpoint (validate input, create user, return 201)
- [x] 5.3 Add duplicate username handling (return 409 Conflict)
- [x] 5.4 Implement POST /api/auth/login endpoint (authenticate, generate tokens, return user info)
- [x] 5.5 Add invalid credentials handling (return 401 Unauthorized)
- [x] 5.6 Implement POST /api/auth/refresh endpoint (validate refresh token, issue new access token)
- [x] 5.7 Create JWT middleware decorator @require_auth for protected routes
- [x] 5.8 Extract user_id from token in middleware and pass to route handler
- [x] 5.9 Register auth Blueprint in backend/app.py
- [x] 5.10 Test all auth endpoints with curl or Postman

## 6. Character Service and API Migration

- [x] 6.1 Create backend/services/character_service.py
- [x] 6.2 Implement get_random_character(input_method='bopomofo') to query database
- [x] 6.3 Add key-to-zhuyin mapping logic (convert input_code string to arrays)
- [x] 6.4 Implement parse_input_code(input_code) to split "j i 3" → ["ㄐ", "ㄧ", "ˇ"] and ["j", "i", "3"]
- [x] 6.5 Modify backend/routes/words.py GET /api/words/random to use database
- [x] 6.6 Update word_service.py to call character_service instead of reading JSON
- [x] 6.7 Add input_method query parameter support (?input_method=bopomofo)
- [x] 6.8 Add 503 error handling for database connection failures
- [x] 6.9 Test random character endpoint returns correct format (word, zhuyin, keys)
- [x] 6.10 Verify response matches existing API contract from specs

## 7. Practice Recording Service and API

- [x] 7.1 Create backend/services/attempt_service.py
- [x] 7.2 Implement record_attempt(user_id, character_id, started_at, ended_at, is_correct)
- [x] 7.3 Add duration_ms calculation in record_attempt function
- [x] 7.4 Implement get_user_attempts(user_id, page=1, limit=50, filters={}) for history queries
- [x] 7.5 Add pagination logic with total_count, has_more metadata
- [x] 7.6 Add filtering by is_correct, character_id, date_range
- [x] 7.7 Create backend/routes/attempts.py Blueprint
- [x] 7.8 Implement POST /api/attempts endpoint with @require_auth middleware
- [x] 7.9 Add input validation for required fields (character_id, started_at, ended_at, is_correct)
- [x] 7.10 Return 202 Accepted immediately (non-blocking recording)
- [x] 7.11 Implement GET /api/attempts endpoint with @require_auth middleware
- [x] 7.12 Add query parameter parsing (page, limit, is_correct, character_id, start_date, end_date)
- [x] 7.13 Ensure users can only access their own attempts (403 for unauthorized access)
- [x] 7.14 Register attempts Blueprint in backend/app.py
- [x] 7.15 Add error logging for recording failures
- [x] 7.16 Test practice recording and retrieval endpoints

## 8. Frontend API Client

- [x] 8.1 Create frontend/js/modules/api.js
- [x] 8.2 Implement getToken() to retrieve access_token from localStorage
- [x] 8.3 Implement saveTokens(access_token, refresh_token) to store in localStorage
- [x] 8.4 Implement clearTokens() to remove tokens on logout
- [x] 8.5 Implement authFetch(url, options) wrapper that adds Authorization header
- [x] 8.6 Add automatic 401 handling to redirect to login page
- [x] 8.7 Add token refresh logic when access token expires (call /api/auth/refresh)
- [x] 8.8 Export convenience methods: apiGet(), apiPost(), apiPut(), apiDelete()
- [x] 8.9 Test API client with mock endpoints

## 9. Frontend Authentication Integration

- [x] 9.1 Create frontend/login.html page with registration and login forms
- [x] 9.2 Add CSS styling for login page (match existing style)
- [x] 9.3 Create frontend/js/modules/auth-backend.js (replaces auth.js)
- [x] 9.4 Implement register(username, password) that calls POST /api/auth/register
- [x] 9.5 Implement login(username, password) that calls POST /api/auth/login
- [x] 9.6 Save tokens and user info to localStorage on successful login
- [x] 9.7 Implement logout() that clears localStorage and redirects to login
- [x] 9.8 Implement isAuthenticated() that checks token existence and expiry
- [x] 9.9 Implement getCurrentUser() that retrieves user from localStorage
- [x] 9.10 Update frontend/index-redesign.html to check authentication on load
- [x] 9.11 Redirect to login.html if not authenticated
- [x] 9.12 Update existing auth.js references to use auth-backend.js
- [x] 9.13 Test registration flow (create account → login → practice)
- [x] 9.14 Test login flow with existing account
- [x] 9.15 Test logout and re-authentication

## 10. Frontend Practice Recording Integration

- [x] 10.1 Update frontend/js/modules/practice.js to import api.js
- [x] 10.2 Add recordAttempt(character, isCorrect, startTime, endTime) function
- [x] 10.3 Lookup character_id by character text (add helper or use character data from API)
- [x] 10.4 Call POST /api/attempts in recordAttempt (don't await response)
- [x] 10.5 Add error handling that logs failures but doesn't interrupt practice
- [x] 10.6 Call recordAttempt() in input-handler-redesign.js after word completion
- [x] 10.7 Pass started_at timestamp when loading new word
- [x] 10.8 Calculate ended_at timestamp when word completes
- [x] 10.9 Store character metadata (id, text) from API response for recording
- [x] 10.10 Test practice flow records attempts to database
- [x] 10.11 Verify non-blocking behavior (practice continues even if recording fails)

## 11. Health Check and Monitoring

- [x] 11.1 Update GET /health endpoint to test database connectivity
- [x] 11.2 Return 503 if database connection fails in health check
- [x] 11.3 Add response time measurement to health check
- [x] 11.4 Add logging configuration in backend/app.py (ERROR level for production)
- [x] 11.5 Test health check with database running and stopped

## 12. Testing and Validation

- [x] 12.1 Update backend tests in tests/backend/test_api.py for new endpoints
- [x] 12.2 Add tests for POST /api/auth/register (success, duplicate, invalid input)
- [x] 12.3 Add tests for POST /api/auth/login (success, invalid credentials)
- [x] 12.4 Add tests for POST /api/auth/refresh (success, expired token)
- [x] 12.5 Add tests for GET /api/words/random with database
- [x] 12.6 Add tests for POST /api/attempts (success, unauthorized, invalid data)
- [x] 12.7 Add tests for GET /api/attempts (pagination, filtering, authorization)
- [x] 12.8 Run all backend tests with pytest (requires test database setup)
- [x] 12.9 Update frontend tests if needed for new auth module (no changes needed)
- [x] 12.10 Run integration test checklist (manual or automated)
- [x] 12.11 Test full user flow: register → login → practice → view history → logout
- [ ] 12.12 Verify all 62 spec scenarios are covered by tests or manual validation

## 13. Documentation and Cleanup

- [x] 13.1 Update README.md with database setup instructions
- [x] 13.2 Add section on environment variables (DATABASE_URL, JWT_SECRET_KEY)
- [x] 13.3 Document PostgreSQL installation and database creation steps
- [x] 13.4 Add API documentation for new endpoints (auth, attempts)
- [x] 13.5 Update development setup section with migration instructions
- [x] 13.6 Remove or deprecate old auth.js file (keep for reference during transition)
- [x] 13.7 Remove dependency on words.json or mark as deprecated
- [x] 13.8 Add notes on connection pooling configuration
- [x] 13.9 Document rollback strategy in case of issues
- [x] 13.10 Verify all code follows existing project conventions
