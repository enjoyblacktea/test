# Practice History Tracking

## Purpose

This capability enables the system to automatically track and store users' practice history, including which words were practiced, timing information, and correctness. It provides APIs for querying historical data and computing practice statistics, supporting features like progress tracking, performance analysis, and personalized learning insights.

## Requirements

### Requirement: Record practice attempts
The system SHALL provide an API endpoint to record individual practice attempts with complete metadata including the practiced word, correctness, and timing information.

#### Scenario: Successfully record a correct practice attempt
- **WHEN** a user completes practicing a word correctly
- **THEN** the system SHALL accept a POST request to `/api/history/record` with username, word, is_correct=true, start_time, and end_time
- **THEN** the system SHALL store the record in the database
- **THEN** the system SHALL return HTTP 201 with success=true and a record_id

#### Scenario: Successfully record an incorrect practice attempt
- **WHEN** a user completes practicing a word incorrectly
- **THEN** the system SHALL accept a POST request to `/api/history/record` with is_correct=false
- **THEN** the system SHALL store the record with is_correct=false
- **THEN** the system SHALL return HTTP 201 with success confirmation

#### Scenario: Reject request with missing required fields
- **WHEN** a POST request to `/api/history/record` is missing username, word, is_correct, start_time, or end_time
- **THEN** the system SHALL return HTTP 400 with error message "Missing required fields"
- **THEN** the system SHALL NOT create any database record

#### Scenario: Reject request with invalid timestamp format
- **WHEN** a POST request contains start_time or end_time in non-ISO 8601 format
- **THEN** the system SHALL return HTTP 400 with error message "Invalid timestamp format"
- **THEN** the system SHALL NOT create any database record

#### Scenario: Reject request with invalid time order
- **WHEN** a POST request has end_time earlier than or equal to start_time
- **THEN** the system SHALL return HTTP 400 with error message "end_time must be after start_time"
- **THEN** the system SHALL NOT create any database record

#### Scenario: Handle database unavailability
- **WHEN** the database connection fails during a record request
- **THEN** the system SHALL return HTTP 503 with error message "Database unavailable"
- **THEN** the system SHALL log the error for monitoring

### Requirement: Query practice history
The system SHALL provide an API endpoint to retrieve a user's practice history with pagination support.

#### Scenario: Query history with default pagination
- **WHEN** a GET request to `/api/history?username=user` is made without limit/offset parameters
- **THEN** the system SHALL return the 50 most recent practice records for that username
- **THEN** the response SHALL include total count and an array of records
- **THEN** each record SHALL contain record_id, word, is_correct, start_time, end_time, and duration_ms

#### Scenario: Query history with custom pagination
- **WHEN** a GET request to `/api/history?username=user&limit=20&offset=10` is made
- **THEN** the system SHALL return 20 records starting from offset 10
- **THEN** the system SHALL order records by start_time in descending order (most recent first)

#### Scenario: Query history for non-existent user
- **WHEN** a GET request queries a username that has no practice records
- **THEN** the system SHALL return HTTP 200 with total=0 and empty records array
- **THEN** the system SHALL NOT return an error

#### Scenario: Reject query without username parameter
- **WHEN** a GET request to `/api/history` is made without username parameter
- **THEN** the system SHALL return HTTP 400 with error message "Missing username parameter"

#### Scenario: Reject query with invalid pagination parameters
- **WHEN** a GET request has non-numeric limit or offset values
- **THEN** the system SHALL return HTTP 400 with error message "Invalid limit or offset"

### Requirement: Compute practice statistics
The system SHALL provide an API endpoint to compute and return aggregate statistics for a user's practice history.

#### Scenario: Calculate statistics for active user
- **WHEN** a GET request to `/api/history/stats?username=user` is made for a user with practice records
- **THEN** the system SHALL return total_words (count of all practice attempts)
- **THEN** the system SHALL return correct_count (count of is_correct=true records)
- **THEN** the system SHALL return accuracy (correct_count / total_words as a decimal between 0 and 1)
- **THEN** the system SHALL return avg_duration_ms (average practice time per word in milliseconds)
- **THEN** the system SHALL return practice_days (count of distinct dates with practice activity)

#### Scenario: Calculate statistics for user with no records
- **WHEN** a GET request to `/api/history/stats?username=newuser` is made for a user with zero records
- **THEN** the system SHALL return total_words=0, correct_count=0, accuracy=0.0, avg_duration_ms=0, practice_days=0
- **THEN** the system SHALL NOT divide by zero or return errors

#### Scenario: Reject stats query without username
- **WHEN** a GET request to `/api/history/stats` is made without username parameter
- **THEN** the system SHALL return HTTP 400 with error message "Missing username parameter"

### Requirement: Automatically track practice timing
The system SHALL track the start and end time of each practice attempt on the frontend.

#### Scenario: Record start time when word loads
- **WHEN** a new word is loaded for practice
- **THEN** the frontend SHALL capture the current timestamp as start_time
- **THEN** the start_time SHALL be stored in the practice state

#### Scenario: Record end time when word completes
- **WHEN** a user successfully completes all keystrokes for a word
- **THEN** the frontend SHALL capture the current timestamp as end_time
- **THEN** the end_time SHALL be stored in the practice state

#### Scenario: Reset timing for next word
- **WHEN** a new word loads after completing the previous word
- **THEN** the frontend SHALL clear previous timing data
- **THEN** the frontend SHALL start fresh timing for the new word

### Requirement: Track practice correctness
The system SHALL track whether each practice attempt was completed without errors.

#### Scenario: Mark word as correct when all keystrokes match
- **WHEN** a user completes a word with all correct keystrokes
- **THEN** the system SHALL set is_correct=true for that practice record
- **THEN** the system SHALL send this correctness status to the backend

#### Scenario: Mark word as incorrect when any keystroke is wrong
- **WHEN** a user presses at least one incorrect key during practice
- **THEN** the system SHALL set is_correct=false for that practice record
- **THEN** the system SHALL maintain this status even if subsequent keys are correct

### Requirement: Persist username in frontend
The system SHALL store the username in the frontend for associating practice records with users.

#### Scenario: Store username on successful login
- **WHEN** a user successfully logs in with valid credentials
- **THEN** the system SHALL save the username to LocalStorage in the auth data object
- **THEN** the username SHALL be available for subsequent API calls

#### Scenario: Retrieve username for history recording
- **WHEN** the frontend needs to record a practice attempt
- **THEN** the system SHALL retrieve the username from LocalStorage
- **THEN** the system SHALL include this username in the API request

#### Scenario: Handle missing username gracefully
- **WHEN** the username is not found in LocalStorage
- **THEN** the system SHALL NOT send practice records to the backend
- **THEN** the system SHALL log a warning but continue allowing practice

### Requirement: Non-blocking history recording
The system SHALL record practice history without interrupting the user's practice flow.

#### Scenario: Continue practice after successful recording
- **WHEN** a practice record is successfully sent to the backend
- **THEN** the system SHALL immediately load the next word
- **THEN** the user SHALL experience no delay or interruption

#### Scenario: Continue practice after failed recording
- **WHEN** a practice record fails to send (network error, API error, etc.)
- **THEN** the system SHALL log the error to console
- **THEN** the system SHALL immediately load the next word without showing error to user
- **THEN** the user SHALL be able to continue practicing normally

#### Scenario: Record asynchronously without blocking
- **WHEN** the frontend sends a practice record to the backend
- **THEN** the system SHALL NOT wait for the API response before proceeding
- **THEN** the system SHALL handle the response asynchronously

### Requirement: Manage user records
The system SHALL automatically create user records when needed and associate practice history with user IDs.

#### Scenario: Create new user on first practice record
- **WHEN** a practice record is received for a username that doesn't exist in the database
- **THEN** the system SHALL automatically create a new user record with that username
- **THEN** the system SHALL return a user_id for the new user
- **THEN** the system SHALL associate the practice record with this user_id

#### Scenario: Reuse existing user for subsequent records
- **WHEN** a practice record is received for a username that already exists
- **THEN** the system SHALL retrieve the existing user_id
- **THEN** the system SHALL associate the new practice record with the existing user_id
- **THEN** the system SHALL NOT create duplicate user records

### Requirement: Calculate practice duration
The system SHALL automatically calculate the duration of each practice attempt.

#### Scenario: Calculate duration from timestamps
- **WHEN** a practice record is stored with start_time and end_time
- **THEN** the database SHALL automatically compute duration_ms as (end_time - start_time) in milliseconds
- **THEN** the duration_ms SHALL be available in query results without manual calculation

#### Scenario: Return duration in query results
- **WHEN** practice history is queried
- **THEN** each record SHALL include the computed duration_ms field
- **THEN** the duration SHALL be an integer representing milliseconds

### Requirement: Maintain data integrity
The system SHALL ensure referential integrity and prevent data corruption.

#### Scenario: Cascade delete practice records when user is deleted
- **WHEN** a user record is deleted from the users table
- **THEN** the system SHALL automatically delete all associated practice_history records
- **THEN** the system SHALL NOT leave orphaned practice records

#### Scenario: Prevent duplicate usernames
- **WHEN** attempting to create a user with an existing username
- **THEN** the system SHALL enforce UNIQUE constraint on username
- **THEN** the system SHALL return the existing user_id instead of creating a duplicate

### Requirement: Optimize query performance
The system SHALL provide efficient queries for common access patterns.

#### Scenario: Fast user history lookup
- **WHEN** querying practice history for a specific user ordered by time
- **THEN** the system SHALL use the idx_user_time index (user_id, start_time DESC)
- **THEN** the query SHALL complete efficiently even with thousands of records

#### Scenario: Fast username lookup
- **WHEN** looking up a user by username
- **THEN** the system SHALL use the idx_username index
- **THEN** the lookup SHALL complete in O(log n) time

### Requirement: Support database connection pooling
The system SHALL manage database connections efficiently using connection pooling.

#### Scenario: Reuse connections for multiple requests
- **WHEN** multiple API requests are processed
- **THEN** the system SHALL reuse database connections from the pool
- **THEN** the system SHALL NOT create a new connection for each request

#### Scenario: Handle connection pool exhaustion
- **WHEN** all connections in the pool are in use
- **THEN** the system SHALL queue new requests until a connection becomes available
- **THEN** the system SHALL NOT crash or reject requests immediately

#### Scenario: Return connections to pool after use
- **WHEN** a database operation completes
- **THEN** the system SHALL return the connection to the pool
- **THEN** the connection SHALL be available for subsequent requests
