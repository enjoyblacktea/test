## ADDED Requirements

### Requirement: Front-end collects keystroke data during practice
The system SHALL record each valid key press during a practice attempt, capturing the key value, its sequential order, the timestamp at press time, and whether the key was correct.

#### Scenario: Correct key recorded
- **WHEN** the user presses a correct zhuyin key during a practice attempt
- **THEN** the system records `{ key_value, key_order, typed_at, is_correct_key: true }` in the in-memory keystroke list

#### Scenario: Incorrect key recorded
- **WHEN** the user presses an incorrect zhuyin key during a practice attempt
- **THEN** the system records `{ key_value, key_order, typed_at, is_correct_key: false }` in the in-memory keystroke list

#### Scenario: Keystroke list resets on new word
- **WHEN** a new practice word is loaded
- **THEN** the keystroke list is cleared and `key_order` resets to 0

### Requirement: Keystroke data is submitted with the attempt
The system SHALL include the collected keystroke list in the `POST /api/attempts` request body when an attempt is completed.

#### Scenario: Keystrokes sent on word completion
- **WHEN** the user completes a word (all keys entered)
- **THEN** `POST /api/attempts` includes a `keystrokes` array containing one entry per key press in order

#### Scenario: Missing keystrokes field is tolerated
- **WHEN** `POST /api/attempts` is called without a `keystrokes` field
- **THEN** the server accepts the request and records only the `typing_attempts` row without error

### Requirement: Keystroke data is persisted atomically with the attempt
The system SHALL insert `keystroke_events` rows in the same database transaction as the parent `typing_attempts` row, so either both succeed or neither is committed.

#### Scenario: Successful atomic write
- **WHEN** `POST /api/attempts` is called with a valid `keystrokes` array
- **THEN** one row is inserted into `typing_attempts` and one row per keystroke is inserted into `keystroke_events`, all within a single transaction

#### Scenario: Transaction rollback on failure
- **WHEN** the database insert fails partway through
- **THEN** neither the `typing_attempts` row nor any `keystroke_events` rows are committed

### Requirement: keystroke_events table schema
The system SHALL maintain a `keystroke_events` table with the following columns: `id` (PK), `attempt_id` (FK → `typing_attempts.id` CASCADE DELETE), `key_value`, `key_order`, `typed_at`, `is_correct_key`.

#### Scenario: Cascade delete on attempt removal
- **WHEN** a `typing_attempts` row is deleted
- **THEN** all associated `keystroke_events` rows are automatically deleted
