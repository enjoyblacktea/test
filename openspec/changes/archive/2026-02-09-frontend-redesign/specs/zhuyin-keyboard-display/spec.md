## MODIFIED Requirements

### Requirement: Highlight keys on user input
The system SHALL provide visual feedback by highlighting the corresponding key when the user presses a keyboard key, using ink-toned gradient styling that matches the calligraphy theme.

#### Scenario: User presses valid zhuyin key
- **WHEN** user presses a key that maps to a zhuyin symbol
- **THEN** the system highlights the corresponding virtual keyboard key with ink-colored gradient (jade/rust tones)
- **THEN** the highlight is visible for a minimum of 200ms
- **THEN** the highlight includes a subtle scale transform animation (seal stamp effect)

#### Scenario: User presses invalid key
- **WHEN** user presses a key that does not map to any zhuyin symbol
- **THEN** the system does not highlight any key
- **THEN** the system does not show any error feedback

#### Scenario: Highlight uses theme colors
- **WHEN** a key is highlighted
- **THEN** the system applies background color from the theme palette (NOT solid green)
- **THEN** the system uses ink-dark, jade, or rust colors with gradient effect
- **THEN** the text color transitions to cream/white for contrast

## ADDED Requirements

### Requirement: Apply seal stamp visual design to keys
The system SHALL style keyboard keys to resemble traditional Chinese seal stamps (印章) with appropriate shadows and borders.

#### Scenario: Keys have stamp-like appearance
- **WHEN** the keyboard is rendered
- **THEN** each key displays with rounded corners and subtle shadows
- **THEN** keys use border styling that mimics carved seal edges
- **THEN** the color scheme uses warm ink tones from the theme palette

#### Scenario: Keys have tactile depth effect
- **WHEN** keys are rendered in default state
- **THEN** the system applies subtle box-shadow to create depth
- **THEN** shadows use warm-toned colors (not plain gray)

### Requirement: Provide brush touch visual feedback on key press
The system SHALL display a visual effect that mimics the feeling of a brush or seal stamp being pressed when a key is activated.

#### Scenario: Key press shows stamp down animation
- **WHEN** user presses a key
- **THEN** the system animates the key with a brief scale increase (1.0 → 1.05)
- **THEN** the system increases shadow depth momentarily
- **THEN** the animation duration is 200-300ms with ease-out timing

#### Scenario: Key release returns to normal state
- **WHEN** the key highlight duration expires
- **THEN** the system animates the key back to default scale (1.0)
- **THEN** the shadow returns to default depth
- **THEN** the background transitions back to default color
