## MODIFIED Requirements

### Requirement: Validate user input against target word
The system SHALL validate each keystroke input, check if it matches the expected zhuyin sequence, and trigger appropriate visual feedback effects.

#### Scenario: User inputs correct zhuyin symbol
- **WHEN** user presses a key corresponding to the next expected zhuyin symbol
- **THEN** the system accepts the input
- **THEN** the system advances to expect the next symbol in the sequence
- **THEN** the system triggers ink drop particle effect at the key position
- **THEN** the system updates the learning statistics (correct input counter)
- **THEN** the system updates the progress bar visual

#### Scenario: User completes correct word
- **WHEN** user inputs the final correct zhuyin symbol for the current word
- **THEN** the system marks the word as complete
- **THEN** the system triggers fireworks particle effect at the character position
- **THEN** the system increments the "words practiced" statistic
- **THEN** the system loads the next practice word

#### Scenario: User inputs incorrect zhuyin symbol
- **WHEN** user presses a key that does not match the expected symbol
- **THEN** the system rejects the input
- **THEN** the system keeps waiting for the correct symbol
- **THEN** the system updates statistics (increments total inputs, resets streak)
- **THEN** the system does NOT trigger particle effects

## ADDED Requirements

### Requirement: Trigger particle effects on input events
The system SHALL integrate with the particle effects system to provide celebratory visual feedback.

#### Scenario: Correct symbol triggers ink drops
- **WHEN** user inputs a correct zhuyin symbol (not the final symbol)
- **THEN** the system calls particle system to emit ink drop particles
- **THEN** particles emit from the keyboard key position
- **THEN** 5-10 ink drop particles are created

#### Scenario: Word completion triggers fireworks
- **WHEN** user completes typing a word correctly
- **THEN** the system calls particle system to emit fireworks particles
- **THEN** particles emit from the practice character's center position
- **THEN** 20-40 firework particles are created

### Requirement: Update learning statistics on each input
The system SHALL integrate with the statistics tracker to record practice performance.

#### Scenario: Correct input updates stats
- **WHEN** user inputs a correct zhuyin symbol
- **THEN** the system calls stats tracker to record correct input
- **THEN** stats tracker increments correct inputs counter
- **THEN** stats tracker increments total inputs counter
- **THEN** stats tracker increments current streak

#### Scenario: Incorrect input updates stats
- **WHEN** user inputs an incorrect zhuyin symbol
- **THEN** the system calls stats tracker to record incorrect input
- **THEN** stats tracker increments total inputs counter only
- **THEN** stats tracker resets current streak to 0

#### Scenario: Word completion updates word count
- **WHEN** user completes a word
- **THEN** the system calls stats tracker to increment words practiced counter
- **THEN** stats tracker saves updated data to LocalStorage

### Requirement: Update progress bar visualization
The system SHALL update the progress bar to reflect how many zhuyin symbols have been correctly input for the current word.

#### Scenario: Progress bar fills incrementally
- **WHEN** user inputs a correct symbol
- **THEN** the system calculates progress percentage (completed symbols / total symbols)
- **THEN** the system animates the progress bar fill to the new percentage
- **THEN** the animation uses smooth easing (0.3-0.5s duration)

#### Scenario: Progress bar resets on new word
- **WHEN** a new practice word is loaded
- **THEN** the system resets progress bar to 0%
- **THEN** the reset uses a brief fade transition

#### Scenario: Progress bar uses theme styling
- **WHEN** the progress bar is rendered
- **THEN** the system applies ink-gradient fill effect
- **THEN** colors use the calligraphy theme palette (jade, rust tones)
