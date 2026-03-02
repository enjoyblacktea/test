## ADDED Requirements

### Requirement: Record practice attempt
The system SHALL provide an API endpoint for recording user practice attempts.

#### Scenario: Successful attempt recording
- **WHEN** an authenticated user submits a practice attempt with character_id, started_at, ended_at, and is_correct
- **THEN** the system validates the access token and extracts user_id
- **THEN** the system inserts a new record into typing_attempts table
- **THEN** the system returns HTTP status 202 Accepted
- **THEN** the response confirms the attempt was received for recording

#### Scenario: Non-blocking recording
- **WHEN** the frontend submits a practice attempt
- **THEN** the API responds immediately without waiting for database write completion
- **THEN** the response time is under 100ms regardless of database load
- **THEN** recording errors do not interrupt the user's practice flow

#### Scenario: Missing required fields
- **WHEN** a request is missing character_id, started_at, ended_at, or is_correct
- **THEN** the system rejects the request with HTTP status 400 Bad Request
- **THEN** the error message specifies which required fields are missing

#### Scenario: Invalid character reference
- **WHEN** a request includes a character_id that does not exist
- **THEN** the system rejects the request with HTTP status 404 Not Found
- **THEN** the error message indicates the character was not found

#### Scenario: Unauthenticated recording attempt
- **WHEN** a request is made without a valid access token
- **THEN** the system rejects the request with HTTP status 401 Unauthorized
- **THEN** no practice data is recorded

#### Scenario: Duration calculation
- **WHEN** a typing attempt is recorded with started_at and ended_at
- **THEN** the system computes duration_ms as (ended_at - started_at) in milliseconds
- **THEN** the computed duration is stored for later analysis
- **THEN** duration is always a non-negative integer

### Requirement: Query practice history
The system SHALL provide an API endpoint for retrieving user practice history.

#### Scenario: Query user's own history
- **WHEN** an authenticated user requests their practice history
- **THEN** the system returns all typing_attempts for that user
- **THEN** the response includes character information joined from characters table
- **THEN** the response includes attempt metadata (started_at, ended_at, is_correct, duration_ms)
- **THEN** results are ordered by created_at descending (most recent first)

#### Scenario: Pagination support
- **WHEN** a user requests practice history with page and limit parameters
- **THEN** the system returns the specified page of results
- **THEN** the response includes pagination metadata (total_count, page, limit, has_more)
- **THEN** default limit is 50 if not specified

#### Scenario: Filter by correctness
- **WHEN** a user requests history with is_correct filter
- **THEN** the system returns only attempts matching the specified correctness
- **THEN** filtering by is_correct=true shows only successful attempts
- **THEN** filtering by is_correct=false shows only incorrect attempts

#### Scenario: Filter by character
- **WHEN** a user requests history with character_id filter
- **THEN** the system returns only attempts for that specific character
- **THEN** this allows tracking progress on individual characters

#### Scenario: Filter by date range
- **WHEN** a user requests history with start_date and end_date parameters
- **THEN** the system returns only attempts within the specified date range
- **THEN** the date range is inclusive of boundaries

#### Scenario: Empty history response
- **WHEN** a user has no practice attempts
- **THEN** the system returns an empty array
- **THEN** the response includes HTTP status 200 OK
- **THEN** pagination metadata shows total_count of 0

#### Scenario: Unauthorized history access
- **WHEN** a user attempts to access another user's history
- **THEN** the system rejects the request with HTTP status 403 Forbidden
- **THEN** users can only access their own practice data

### Requirement: Recording error handling
The system SHALL handle recording failures gracefully without exposing errors to frontend.

#### Scenario: Database connection failure
- **WHEN** the database is unavailable during attempt recording
- **THEN** the system logs the error with full context (user_id, character_id, timestamp)
- **THEN** the API still returns HTTP status 202 Accepted to the frontend
- **THEN** the user can continue practicing without interruption

#### Scenario: Foreign key constraint violation
- **WHEN** recording fails due to invalid user_id or character_id
- **THEN** the system logs the constraint violation error
- **THEN** the API returns 202 Accepted (non-blocking) or 400/404 (validation caught earlier)

#### Scenario: Error logging for monitoring
- **WHEN** any recording error occurs
- **THEN** the system logs the error with severity level ERROR
- **THEN** the log includes timestamp, user_id, character_id, error message, and stack trace
- **THEN** monitoring systems can alert on high error rates

### Requirement: Character lookup with input method
The system SHALL resolve character references by database ID or character text.

#### Scenario: Lookup character by text and input method
- **WHEN** the frontend needs to record an attempt for character "你" with method "bopomofo"
- **THEN** the system provides an endpoint or service to look up the character_id
- **THEN** the lookup query uses the (character, input_method) unique constraint
- **THEN** the returned character_id can be used in attempt recording

#### Scenario: Character not found
- **WHEN** looking up a character that doesn't exist in the database
- **THEN** the system returns HTTP status 404 Not Found
- **THEN** the error message indicates which character and input method were not found
