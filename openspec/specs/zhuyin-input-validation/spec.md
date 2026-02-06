## ADDED Requirements

### Requirement: Validate user input against target word
The system SHALL validate each keystroke input and check if it matches the expected zhuyin sequence for the current target Chinese character.

#### Scenario: User inputs correct zhuyin symbol
- **WHEN** user presses a key corresponding to the next expected zhuyin symbol
- **THEN** the system accepts the input
- **THEN** the system advances to expect the next symbol in the sequence

#### Scenario: User completes correct word
- **WHEN** user inputs the final correct zhuyin symbol for the current word
- **THEN** the system marks the word as complete
- **THEN** the system loads the next practice word

#### Scenario: User inputs incorrect zhuyin symbol
- **WHEN** user presses a key that does not match the expected symbol
- **THEN** the system rejects the input
- **THEN** the system keeps waiting for the correct symbol

### Requirement: Track input progress for current word
The system SHALL maintain the current position within the zhuyin sequence being typed.

#### Scenario: Track partial completion
- **WHEN** user has typed 2 out of 3 symbols correctly
- **THEN** the system remembers that 2 symbols are complete
- **THEN** the system expects the 3rd symbol next

#### Scenario: Reset progress on new word
- **WHEN** a new word is loaded
- **THEN** the system resets the input position to 0
- **THEN** the system expects the first zhuyin symbol

### Requirement: Handle first tone as space or nothing
The system SHALL accept either spacebar or immediate progression for first tone (no tone mark).

#### Scenario: User presses space for first tone
- **WHEN** the expected tone is first tone (no mark)
- **WHEN** user presses spacebar
- **THEN** the system accepts it as correct first tone

#### Scenario: User skips space for first tone
- **WHEN** the expected tone is first tone (no mark)
- **WHEN** user inputs the next word's first symbol instead
- **THEN** the system treats the previous word as complete
- **THEN** the system processes the current input for the new word
