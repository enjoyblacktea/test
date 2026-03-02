## MODIFIED Requirements

### Requirement: Highlight keys on user input
The system SHALL provide visual feedback by highlighting the corresponding key when the user presses a keyboard key, using high-contrast cyan color that matches the dark theme.

#### Scenario: User presses valid zhuyin key
- **WHEN** user presses a key that maps to a zhuyin symbol
- **THEN** the system highlights the corresponding virtual keyboard key with cyan color (#00d9ff)
- **THEN** the highlight is visible for a minimum of 200ms
- **THEN** the highlight includes a subtle scale transform animation

#### Scenario: User presses invalid key
- **WHEN** user presses a key that does not map to any zhuyin symbol
- **THEN** the system does not highlight any key
- **THEN** the system does not show any error feedback

#### Scenario: Highlight uses dark theme colors
- **WHEN** a key is highlighted
- **THEN** the system applies --color-accent-primary (#00d9ff) as background color
- **THEN** the system uses black text color for contrast on cyan background
- **THEN** the highlight includes glow effect with rgba(0, 217, 255, 0.5) box-shadow

## REMOVED Requirements

### Requirement: Apply seal stamp visual design to keys
**Reason**: Seal stamp aesthetic replaced by modern flat design with dark theme.
**Migration**: Keys now use simple dark gray background (#2a2a2a) with subtle borders, no stamp shadows or warm tones.

### Requirement: Provide brush touch visual feedback on key press
**Reason**: Brush touch effect replaced by simpler scale/glow animation matching modern dark theme.
**Migration**: Key press now uses simple scale (1.0 → 1.05) with cyan glow, no shadow depth changes or ink-colored transitions.

## ADDED Requirements

### Requirement: Constrain spacebar to fixed width
The system SHALL render the spacebar with a fixed width of approximately 300px (equivalent to 6 key widths) instead of spanning the full keyboard width.

#### Scenario: Spacebar has fixed width
- **WHEN** the keyboard is rendered
- **THEN** the spacebar has a fixed width of 300px
- **THEN** the spacebar does not use flex-grow or percentage-based width
- **THEN** the spacebar maintains consistent size across all screen sizes

#### Scenario: Spacebar is centered in its row
- **WHEN** the spacebar is rendered
- **THEN** the system centers the spacebar horizontally in row 5
- **THEN** the system applies margin: 0 auto or equivalent centering
- **THEN** equal spacing appears on left and right sides of spacebar

#### Scenario: Spacebar maintains visual proportion
- **WHEN** the spacebar is displayed
- **THEN** the spacebar width visually aligns with approximately 6 standard key widths
- **THEN** the spacebar does not dominate the keyboard layout
- **THEN** the spacebar remains clearly identifiable as the space key

### Requirement: Style keyboard with dark theme colors
The system SHALL apply the dark color system to keyboard keys for visual consistency with the overall dark theme.

#### Scenario: Keyboard background is dark
- **WHEN** the keyboard is rendered
- **THEN** the system applies dark gray background (#1a1a1a) to keyboard container
- **THEN** the keyboard background matches other card/panel backgrounds

#### Scenario: Keys use elevated dark background
- **WHEN** individual keys are rendered
- **THEN** the system applies slightly lighter background (#2a2a2a) to keys
- **THEN** keys visually stand out from keyboard background
- **THEN** key borders are subtle (#333) for definition

#### Scenario: Key text uses high contrast
- **WHEN** key labels are rendered
- **THEN** zhuyin symbols use white color (#ffffff) for primary text
- **THEN** QWERTY letters use light gray (#a0a0a0) for secondary text
- **THEN** all text meets WCAG AA contrast requirements
