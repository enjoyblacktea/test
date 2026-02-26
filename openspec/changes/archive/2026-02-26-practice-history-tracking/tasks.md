## 1. Database Setup

- [x] 1.1 Install and verify PostgreSQL is running on localhost:5432 (使用遠端 PostgreSQL)
- [x] 1.2 Create database `zhuyin_practice` using psql or pgAdmin (稍後手動執行)
- [x] 1.3 Create `backend/migrations/init_db.sql` with CREATE TABLE statements for users and practice_history
- [x] 1.4 Add indexes: idx_user_time, idx_username, idx_user_correct in init_db.sql
- [x] 1.5 Execute init_db.sql to create tables and indexes (已手動執行)
- [x] 1.6 Verify tables exist with `\dt` command in psql (已驗證，API 測試成功)
- [ ] 1.7 Create test database `zhuyin_practice_test` for testing (稍後手動執行)

## 2. Backend Dependencies

- [x] 2.1 Add `psycopg2-binary>=2.9.9` to `backend/pyproject.toml` dependencies
- [x] 2.2 Run `uv sync` to install new dependencies
- [x] 2.3 Verify psycopg2 imports successfully in Python

## 3. Backend Configuration

- [x] 3.1 Add PostgreSQL connection config to `backend/config.py` (POSTGRES_HOST, PORT, DB, USER, PASSWORD)
- [x] 3.2 Add default values for all PostgreSQL environment variables
- [x] 3.3 Add TestConfig class with `POSTGRES_DB = 'zhuyin_practice_test'`

## 4. Database Service

- [x] 4.1 Create `backend/services/db_service.py`
- [x] 4.2 Implement DatabaseService class with connection pool (minconn=1, maxconn=10)
- [x] 4.3 Implement get_connection() method with error handling
- [x] 4.4 Implement return_connection() method
- [x] 4.5 Implement close_all() method for cleanup
- [x] 4.6 Add logging for connection pool creation and errors

## 5. History Service

- [x] 5.1 Create `backend/services/history_service.py`
- [x] 5.2 Implement HistoryService class with db_service dependency
- [x] 5.3 Implement get_or_create_user(username) method
- [x] 5.4 Implement record_practice(user_id, word, is_correct, start_time, end_time) method
- [x] 5.5 Implement get_history(user_id, limit, offset) method with pagination
- [x] 5.6 Implement get_stats(user_id) method calculating total, correct_count, accuracy, avg_duration, practice_days
- [x] 5.7 Add logging for all service methods
- [x] 5.8 Add error handling with proper exception types

## 6. History API Routes

- [x] 6.1 Create `backend/routes/history.py` with Blueprint
- [x] 6.2 Implement POST /api/history/record endpoint
- [x] 6.3 Add validation for required fields (username, word, is_correct, start_time, end_time)
- [x] 6.4 Add validation for timestamp format (ISO 8601)
- [x] 6.5 Add validation for time logic (end_time > start_time)
- [x] 6.6 Implement GET /api/history endpoint with username, limit, offset parameters
- [x] 6.7 Add parameter validation for limit and offset (numeric, non-negative)
- [x] 6.8 Implement GET /api/history/stats endpoint
- [x] 6.9 Add error responses: 400 (bad request), 503 (database unavailable), 500 (internal error)
- [x] 6.10 Add init_history_routes() function to inject service dependencies

## 7. Backend Integration

- [x] 7.1 Modify `backend/app.py` to import history blueprint
- [x] 7.2 Initialize db_service with config in app.py
- [x] 7.3 Initialize history_service with db_service in app.py
- [x] 7.4 Call init_history_routes() to inject services
- [x] 7.5 Register history blueprint with app
- [x] 7.6 Test backend starts without errors: `uv run python app.py`
- [x] 7.7 Verify /api/history endpoints are registered with `flask routes` or test request

## 8. Frontend History Module

- [x] 8.1 Create `frontend/js/modules/history.js`
- [x] 8.2 Implement recordPractice(data) function with POST request
- [x] 8.3 Add error handling with try/catch, log errors without throwing
- [x] 8.4 Implement getHistory(username, limit, offset) function
- [x] 8.5 Implement getStats(username) function
- [x] 8.6 Implement saveToOfflineQueue(data) function (optional)
- [x] 8.7 Implement flushOfflineQueue() function (optional)
- [x] 8.8 Add API_BASE_URL constant

## 9. Frontend Auth Modifications

- [x] 9.1 Modify `frontend/js/modules/auth.js` login() function to store username in authData
- [x] 9.2 Add getCurrentUsername() function to retrieve username from LocalStorage
- [x] 9.3 Add error handling for JSON parse failures
- [x] 9.4 Test login stores username correctly in browser DevTools

## 10. Frontend Practice Modifications

- [x] 10.1 Add startTime, endTime, hasError fields to practice.js state object
- [x] 10.2 Modify loadWord() to set startTime = new Date() and reset hasError = false
- [x] 10.3 Modify checkInput() to set hasError = true on incorrect key
- [x] 10.4 Modify checkInput() to set endTime = new Date() when word completes
- [x] 10.5 Modify getState() to return isCorrect = !hasError
- [x] 10.6 Test timing and correctness tracking in browser console

## 11. Frontend Main Integration

- [x] 11.1 Import history.js functions in `frontend/js/modules/input-handler-redesign.js`
- [x] 11.2 Import getCurrentUsername from auth.js
- [x] 11.3 Create handleWordComplete() function
- [x] 11.4 In handleWordComplete(), get practice state and username
- [x] 11.5 Call recordPractice() with non-blocking .catch() handler
- [x] 11.6 Load next word immediately without waiting for API response
- [x] 11.7 Integrate handleWordComplete() into existing word completion logic
- [x] 11.8 Test end-to-end: practice a word, verify API request in Network tab

## 12. Backend Unit Tests

- [x] 12.1 Create `tests/backend/test_history_service.py`
- [x] 12.2 Write test_get_or_create_user() test
- [x] 12.3 Write test_get_or_create_user_idempotent() test
- [x] 12.4 Write test_record_practice() test
- [x] 12.5 Write test_get_history() test with pagination
- [x] 12.6 Write test_get_stats() test
- [x] 12.7 Write test_get_stats_zero_records() test
- [x] 12.8 Add pytest fixtures for test database setup/teardown

## 13. Backend API Tests

- [x] 13.1 Create `tests/backend/test_history_api.py`
- [x] 13.2 Write test_record_practice_api_success() test
- [x] 13.3 Write test_record_practice_missing_fields() test
- [x] 13.4 Write test_record_practice_invalid_timestamp() test
- [x] 13.5 Write test_record_practice_invalid_time_order() test
- [x] 13.6 Write test_get_history_api() test
- [x] 13.7 Write test_get_history_missing_username() test
- [x] 13.8 Write test_get_stats_api() test
- [x] 13.9 Add Flask test client fixture
- [x] 13.10 Run all backend tests: `uv run pytest tests/backend/test_history* -v`

## 14. Frontend Tests

- [x] 14.1 Create `tests/frontend/test-history.html` with history module tests
- [x] 14.2 Write test for recordPractice() successful request
- [x] 14.3 Write test for recordPractice() network error handling
- [x] 14.4 Write test for getCurrentUsername() retrieval
- [x] 14.5 Write test for practice.js timing and correctness tracking
- [x] 14.6 Open test-history.html in browser and verify all tests pass

## 15. Integration Testing

- [x] 15.1 Create `tests/HISTORY_FEATURE_TEST_CHECKLIST.md`
- [x] 15.2 Start backend server: `cd backend && uv run python app.py`
- [x] 15.3 Start frontend server: `cd frontend && python3 -m http.server 8000`
- [x] 15.4 Open http://localhost:8000/index-redesign.html in browser (已完成)
- [x] 15.5 Log in with user/1234 (已完成，修復 checkAuth bug)
- [x] 15.6 Practice 5-10 words, verify no errors in console (已完成)
- [x] 15.7 Check Network tab: verify POST /api/history/record requests succeed (201) (已驗證成功)
- [x] 15.8 Query database: verify user created (已透過 API 測試驗證)
- [x] 15.9 Query database: verify records exist (已透過 API 測試驗證)
- [x] 15.10 Verify duration_ms is calculated correctly (已驗證：3000ms, 5000ms)
- [x] 15.11 Test GET /api/history?username=test_user (已通過 curl 測試)
- [x] 15.12 Test GET /api/history/stats?username=test_user (已通過 curl 測試)
- [x] 15.13 Simulate network error (disconnect wifi), verify practice continues without blocking (已驗證通過)

## 16. Documentation

- [x] 16.1 Update README.md with PostgreSQL setup instructions
- [x] 16.2 Add section about history tracking feature to README.md
- [x] 16.3 Document API endpoints in README.md or separate API.md
- [x] 16.4 Add environment variables documentation for PostgreSQL config
- [x] 16.5 Update project structure in README.md to include new files

## 17. Cleanup and Review

- [ ] 17.1 Review all code for TODO comments and address them
- [ ] 17.2 Verify all error messages are user-friendly
- [ ] 17.3 Check all logging statements are at appropriate levels
- [ ] 17.4 Ensure no sensitive data (passwords) is logged
- [ ] 17.5 Run linters if available (flake8, eslint)
- [ ] 17.6 Verify all files use consistent formatting (2-space indentation for JS)
- [x] 17.7 Remove any debug console.log statements from production code
