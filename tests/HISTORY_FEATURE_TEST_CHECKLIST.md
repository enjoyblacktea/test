# Practice History Tracking - Integration Test Checklist

## Prerequisites

- [ ] PostgreSQL server is running and accessible
- [ ] Backend environment variables are configured
- [ ] Backend server is running (`cd backend && uv run python app.py`)
- [ ] Frontend server is running (`cd frontend && python3 -m http.server 8000`)

## Database Setup Tests

- [ ] **1.1** Database `zhuyin_practice` exists
- [ ] **1.2** Table `users` exists with correct schema
- [ ] **1.3** Table `practice_history` exists with correct schema
- [ ] **1.4** Indexes are created (`idx_user_time`, `idx_username`, `idx_user_correct`)
- [ ] **1.5** Test database `zhuyin_practice_test` exists

## Backend Unit Tests

- [ ] **2.1** Run `cd backend && uv run pytest tests/backend/test_history_service.py -v`
- [ ] **2.2** All history service tests pass
- [ ] **2.3** Run `cd backend && uv run pytest tests/backend/test_history_api.py -v`
- [ ] **2.4** All API tests pass

## Backend API Tests (Manual)

- [ ] **3.1** POST `/api/history/record` with valid data returns 201
- [ ] **3.2** POST `/api/history/record` with missing fields returns 400
- [ ] **3.3** POST `/api/history/record` with invalid timestamp returns 400
- [ ] **3.4** GET `/api/history?username=test` returns 200 with records
- [ ] **3.5** GET `/api/history` without username returns 400
- [ ] **3.6** GET `/api/history/stats?username=test` returns statistics

## Frontend Tests

- [ ] **4.1** Open `tests/frontend/test-history.html` in browser
- [ ] **4.2** All auth module tests pass
- [ ] **4.3** All practice module timing tests pass
- [ ] **4.4** History module tests pass (or gracefully fail if backend unavailable)
- [ ] **4.5** Integration tests pass

## End-to-End Integration Tests

### Test 1: User Login and Practice Recording

- [ ] **5.1** Open `http://localhost:8000/index-redesign.html` in browser
- [ ] **5.2** Log in with `user` / `1234`
- [ ] **5.3** Login succeeds and practice screen is shown
- [ ] **5.4** Open browser DevTools > Console (check for errors)
- [ ] **5.5** Open browser DevTools > Network tab

### Test 2: Practice and Verify Recording

- [ ] **6.1** Practice 5-10 words correctly
- [ ] **6.2** No console errors appear
- [ ] **6.3** Network tab shows `POST /api/history/record` requests
- [ ] **6.4** All POST requests return status 201 (Created)
- [ ] **6.5** Response contains `{"success": true, "record_id": <number>}`

### Test 3: Database Verification

- [ ] **7.1** Connect to PostgreSQL: `psql -U postgres -d zhuyin_practice`
- [ ] **7.2** Check user created: `SELECT * FROM users;`
- [ ] **7.3** Verify username matches logged-in user
- [ ] **7.4** Check practice records: `SELECT * FROM practice_history ORDER BY start_time DESC LIMIT 10;`
- [ ] **7.5** Verify word, is_correct, timestamps are correct
- [ ] **7.6** Verify duration_ms is calculated correctly (end_time - start_time in ms)

### Test 4: API Query Tests

- [ ] **8.1** Test history query in browser:
  - Navigate to: `http://localhost:5000/api/history?username=user`
- [ ] **8.2** Verify JSON response contains `total` and `records` array
- [ ] **8.3** Verify records are sorted by `start_time DESC` (most recent first)
- [ ] **8.4** Test stats query:
  - Navigate to: `http://localhost:5000/api/history/stats?username=user`
- [ ] **8.5** Verify stats: `total_words`, `correct_count`, `accuracy`, `avg_duration_ms`, `practice_days`

### Test 5: Error Handling

- [ ] **9.1** Stop backend server (Ctrl+C)
- [ ] **9.2** Continue practicing words in browser
- [ ] **9.3** Verify practice continues without blocking
- [ ] **9.4** Verify console shows warning: "Error recording practice (continuing anyway)"
- [ ] **9.5** Network tab shows failed POST requests (status 0 or 500)
- [ ] **9.6** Restart backend server
- [ ] **9.7** Practice more words
- [ ] **9.8** Verify recording resumes successfully

### Test 6: Correctness Tracking

- [ ] **10.1** Practice a word and deliberately make mistakes
- [ ] **10.2** Complete the word
- [ ] **10.3** Check database: verify `is_correct = false` for that record
- [ ] **10.4** Practice a word without mistakes
- [ ] **10.5** Check database: verify `is_correct = true` for that record

### Test 7: Pagination

- [ ] **11.1** Practice 60+ words to exceed default limit
- [ ] **11.2** Query: `http://localhost:5000/api/history?username=user&limit=20&offset=0`
- [ ] **11.3** Verify returns 20 records
- [ ] **11.4** Query: `http://localhost:5000/api/history?username=user&limit=20&offset=20`
- [ ] **11.5** Verify returns next 20 records

### Test 8: Statistics Calculation

- [ ] **12.1** Practice exactly 10 words: 7 correct, 3 incorrect
- [ ] **12.2** Query stats API
- [ ] **12.3** Verify: `total_words = 10`
- [ ] **12.4** Verify: `correct_count = 7`
- [ ] **12.5** Verify: `accuracy = 0.7`
- [ ] **12.6** Verify: `avg_duration_ms` is reasonable (1000-5000ms)
- [ ] **12.7** Verify: `practice_days = 1` (same day)

## Performance Tests

- [ ] **13.1** Practice 100+ words continuously
- [ ] **13.2** Verify no memory leaks in browser (check DevTools > Memory)
- [ ] **13.3** Verify backend handles concurrent requests smoothly
- [ ] **13.4** Check PostgreSQL connection pool usage (no exhaustion warnings)

## Cross-Browser Tests

- [ ] **14.1** Test on Chrome/Chromium
- [ ] **14.2** Test on Firefox
- [ ] **14.3** Test on Safari (if available)
- [ ] **14.4** Test on Edge (if available)

## Summary

**Total Tests**: ~70
**Passed**: ___ / 70
**Failed**: ___ / 70

**Critical Issues Found**: ___

**Notes**: ___
