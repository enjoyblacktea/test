## MODIFIED Requirements

### Requirement: Maintain practice word data
The system SHALL store a collection of Chinese words with their zhuyin mappings in a PostgreSQL database.

#### Scenario: Data loaded from database
- **WHEN** the system starts
- **THEN** the system connects to the characters table in the database
- **THEN** each character record contains "character", "input_code", and "input_method" fields
- **THEN** all zhuyin symbols in input_code are valid bopomofo characters

#### Scenario: Character retrieval from database
- **WHEN** the API needs to return a random word
- **THEN** the system queries the characters table with input_method filter
- **THEN** the system converts input_code string to zhuyin and keys arrays
- **THEN** the conversion uses backend key-to-zhuyin mapping service

#### Scenario: Handle database connection failure
- **WHEN** the database is unavailable
- **THEN** the system returns an error response with HTTP status 503 Service Unavailable
- **THEN** the error indicates the database service is temporarily unavailable
- **THEN** the system logs the connection failure for monitoring

#### Scenario: Input method filtering
- **WHEN** the API request includes an input_method query parameter
- **THEN** the system filters characters by that input_method value
- **THEN** only characters matching the specified method are eligible for selection
- **THEN** if input_method is omitted, the system defaults to "bopomofo"

## ADDED Requirements

### Requirement: Random character selection from database
The system SHALL select random characters efficiently from the database.

#### Scenario: Random selection query
- **WHEN** the API needs to return a random word
- **THEN** the system uses a database query to randomly select one character
- **THEN** the query filters by input_method (e.g., "bopomofo")
- **THEN** the selection is uniformly random across all matching characters

#### Scenario: Performance of random query
- **WHEN** the characters table contains 30 to 1000 characters
- **THEN** the random selection query completes in under 50ms
- **THEN** the query uses the input_method index for filtering efficiency

#### Scenario: Empty result set
- **WHEN** no characters exist for the specified input_method
- **THEN** the system returns HTTP status 404 Not Found
- **THEN** the error message indicates no characters available for that input method
