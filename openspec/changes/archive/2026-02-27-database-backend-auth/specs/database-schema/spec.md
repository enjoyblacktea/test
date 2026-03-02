## ADDED Requirements

### Requirement: Users table schema
The system SHALL maintain a users table with proper columns and constraints.

#### Scenario: Users table structure
- **WHEN** the database is initialized
- **THEN** the users table contains an auto-incrementing id column as primary key
- **THEN** the table contains a username column (VARCHAR, NOT NULL, UNIQUE)
- **THEN** the table contains a password_hash column (VARCHAR, NOT NULL)
- **THEN** the table contains created_at and updated_at timestamp columns

#### Scenario: Username uniqueness constraint
- **WHEN** attempting to insert a duplicate username
- **THEN** the database rejects the insert with a unique constraint violation
- **THEN** the application can detect and handle the conflict appropriately

#### Scenario: Users table index
- **WHEN** querying users by username
- **THEN** the query uses an index on the username column for performance
- **THEN** login queries complete efficiently even with many users

### Requirement: Characters table schema
The system SHALL maintain a characters table supporting multiple input methods.

#### Scenario: Characters table structure
- **WHEN** the database is initialized
- **THEN** the characters table contains an auto-incrementing id column as primary key
- **THEN** the table contains a character column (VARCHAR, NOT NULL) for the Chinese character
- **THEN** the table contains an input_code column (VARCHAR, NOT NULL) for the zhuyin sequence
- **THEN** the table contains an input_method column (VARCHAR, NOT NULL) for the input method type
- **THEN** the table contains a created_at timestamp column

#### Scenario: Character uniqueness per input method
- **WHEN** the database stores characters
- **THEN** the table has a UNIQUE constraint on (character, input_method)
- **THEN** the same character can exist multiple times with different input_method values
- **THEN** duplicate (character, input_method) pairs are rejected

#### Scenario: Input method filtering index
- **WHEN** querying characters by input_method
- **THEN** the query uses an index on the input_method column
- **THEN** random character selection for "bopomofo" is efficient

#### Scenario: Character data seeding
- **WHEN** the database is initialized
- **THEN** the system seeds the characters table with 30 bopomofo practice characters
- **THEN** each seeded character has input_method set to "bopomofo"
- **THEN** the input_code contains space-separated zhuyin keys (e.g., "j i 3")

### Requirement: Typing attempts table schema
The system SHALL maintain a typing_attempts table linking users to practice history.

#### Scenario: Typing attempts table structure
- **WHEN** the database is initialized
- **THEN** the typing_attempts table contains an auto-incrementing id column as primary key
- **THEN** the table contains a user_id column (INTEGER, NOT NULL) as foreign key to users.id
- **THEN** the table contains a character_id column (INTEGER, NOT NULL) as foreign key to characters.id
- **THEN** the table contains started_at and ended_at timestamp columns (NOT NULL)
- **THEN** the table contains an is_correct column (BOOLEAN, NOT NULL)
- **THEN** the table contains a duration_ms computed column (ended_at - started_at in milliseconds)
- **THEN** the table contains a created_at timestamp column

#### Scenario: Foreign key to users with cascade delete
- **WHEN** a user is deleted
- **THEN** all typing_attempts records for that user are automatically deleted (CASCADE)
- **THEN** this prevents orphaned practice records

#### Scenario: Foreign key to characters with restrict delete
- **WHEN** attempting to delete a character that has typing_attempts
- **THEN** the database rejects the delete with a foreign key constraint violation (RESTRICT)
- **THEN** this preserves historical practice data integrity

#### Scenario: User attempts index
- **WHEN** querying typing attempts by user_id
- **THEN** the query uses an index on user_id for efficient retrieval
- **THEN** fetching user practice history is performant

#### Scenario: Character attempts index
- **WHEN** querying typing attempts by character_id
- **THEN** the query uses an index on character_id for analysis queries
- **THEN** finding all attempts for a specific character is efficient

#### Scenario: User correctness index
- **WHEN** querying correct or incorrect attempts by user
- **THEN** the query uses a composite index on (user_id, is_correct)
- **THEN** filtering user attempts by correctness is performant

### Requirement: Database migration script
The system SHALL provide an idempotent migration script to initialize the schema.

#### Scenario: Initial migration execution
- **WHEN** the migration script runs on an empty database
- **THEN** all three tables (users, characters, typing_attempts) are created
- **THEN** all indexes and constraints are applied
- **THEN** the characters table is seeded with 30 bopomofo practice characters

#### Scenario: Idempotent migration
- **WHEN** the migration script runs on a database with existing schema
- **THEN** the script detects existing tables and skips creation
- **THEN** no errors occur from attempting to create existing objects
- **THEN** the database state remains consistent

### Requirement: Connection pooling configuration
The system SHALL use connection pooling for database access efficiency.

#### Scenario: Connection pool initialization
- **WHEN** the application starts
- **THEN** the system creates a connection pool with 5-10 connections
- **THEN** the pool supports up to 10 additional overflow connections
- **THEN** connections are recycled after 3600 seconds (1 hour)

#### Scenario: Connection reuse
- **WHEN** multiple API requests access the database
- **THEN** connections are reused from the pool rather than creating new ones
- **THEN** this reduces connection overhead and improves performance

#### Scenario: Connection pool exhaustion handling
- **WHEN** the connection pool is exhausted (all connections in use)
- **THEN** new requests wait for an available connection up to a timeout
- **THEN** if timeout is exceeded, the request fails with a database connection error
- **THEN** the application logs the pool exhaustion event for monitoring
