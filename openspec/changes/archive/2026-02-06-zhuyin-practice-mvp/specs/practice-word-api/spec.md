## ADDED Requirements

### Requirement: Provide random practice word
The system SHALL provide an API endpoint that returns a random Chinese character with its corresponding zhuyin sequence and keyboard keys.

#### Scenario: Request random word
- **WHEN** client requests GET /api/words/random
- **THEN** the system returns a JSON response with word, zhuyin array, and keys array
- **THEN** the response includes the Chinese character as "word"
- **THEN** the response includes zhuyin symbols as "zhuyin" array
- **THEN** the response includes keyboard keys as "keys" array

#### Scenario: Response format validation
- **WHEN** API returns a word
- **THEN** the "zhuyin" array length matches the "keys" array length
- **THEN** each element in arrays corresponds to one input unit

### Requirement: Maintain practice word data
The system SHALL store a collection of Chinese words with their zhuyin mappings in a data file.

#### Scenario: Data file contains valid mappings
- **WHEN** the system starts
- **THEN** the system loads word data from words.json
- **THEN** each entry contains "word", "zhuyin", and "keys" fields
- **THEN** all zhuyin symbols are valid bopomofo characters

#### Scenario: Handle missing data file
- **WHEN** words.json does not exist
- **THEN** the system returns an error response
- **THEN** the error indicates missing data configuration

### Requirement: Return consistent key mappings
The system SHALL ensure the keyboard keys returned match the standard zhuyin keyboard layout.

#### Scenario: Keys match zhuyin symbols
- **WHEN** API returns a word with zhuyin "ㄋㄧˇ"
- **THEN** the keys array is ["s", "u", "3"]
- **THEN** each key position corresponds to the zhuyin symbol at the same index

#### Scenario: Tone marks use correct keys
- **WHEN** a tone mark is included in zhuyin
- **THEN** first tone maps to space key " "
- **THEN** second tone ˊ maps to key "6"
- **THEN** third tone ˇ maps to key "3"
- **THEN** fourth tone ˋ maps to key "4"
- **THEN** fifth tone ˙ maps to key "7"
