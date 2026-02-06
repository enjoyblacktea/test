## ADDED Requirements

### Requirement: Display standard zhuyin keyboard layout
The system SHALL display a virtual keyboard showing the standard zhuyin (bopomofo) key mapping layout that matches traditional Taiwan keyboard configuration.

#### Scenario: Initial keyboard render
- **WHEN** the page loads
- **THEN** the system displays all zhuyin symbols arranged in keyboard layout
- **THEN** each key shows both the keyboard letter and corresponding zhuyin symbol

#### Scenario: Keyboard includes all symbol types
- **WHEN** the keyboard is rendered
- **THEN** the system displays consonants (ㄅㄆㄇㄈ...)
- **THEN** the system displays vowels (ㄧㄨㄩ...)
- **THEN** the system displays tone marks (ˊˇˋ˙) including space for first tone

### Requirement: Highlight keys on user input
The system SHALL provide visual feedback by highlighting the corresponding key when the user presses a keyboard key.

#### Scenario: User presses valid zhuyin key
- **WHEN** user presses a key that maps to a zhuyin symbol
- **THEN** the system highlights the corresponding virtual keyboard key
- **THEN** the highlight is visible for a minimum of 200ms

#### Scenario: User presses invalid key
- **WHEN** user presses a key that does not map to any zhuyin symbol
- **THEN** the system does not highlight any key
- **THEN** the system does not show any error feedback

### Requirement: Clear highlight after input
The system SHALL clear the key highlight after a short duration to prepare for the next input.

#### Scenario: Highlight auto-clears
- **WHEN** a key has been highlighted for 200ms
- **THEN** the system removes the highlight styling
- **THEN** the key returns to its default visual state
