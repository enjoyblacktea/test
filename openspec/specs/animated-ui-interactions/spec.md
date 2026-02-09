## ADDED Requirements

### Requirement: Animate page load with staggered reveals
The system SHALL display a coordinated entrance animation sequence when the page first loads, with elements appearing in a staggered timing pattern.

#### Scenario: Title characters appear sequentially
- **WHEN** the page loads
- **THEN** the system animates each title character with fade-in-up effect
- **THEN** each character's animation delays by 100ms relative to the previous character
- **THEN** the total title animation completes within 1 second

#### Scenario: Main content fades in after title
- **WHEN** the title animation is 50% complete
- **THEN** the system begins fading in the practice area
- **THEN** the practice area animation uses smooth easing (ease-out)

#### Scenario: Animations respect reduced motion preference
- **WHEN** user has enabled prefers-reduced-motion in their system settings
- **THEN** the system skips or drastically shortens all animations (duration < 0.01ms)
- **THEN** content appears immediately without motion effects

### Requirement: Animate practice word with brush writing effect
The system SHALL display the practice character with a calligraphy brush writing animation that reveals the character as if being drawn.

#### Scenario: Character appears with stroke animation
- **WHEN** a new practice word loads
- **THEN** the system animates the character appearing stroke by stroke
- **THEN** the animation mimics traditional brush calligraphy timing (0.8-1.2s total)

#### Scenario: Animation completes before user interaction
- **WHEN** the brush writing animation is playing
- **THEN** the system allows user input immediately (does not block interaction)
- **THEN** user keyboard input is processed normally during animation

### Requirement: Animate keyboard key press with seal stamp effect
The system SHALL provide visual feedback when a key is pressed, using an animation that resembles a traditional Chinese seal stamp being pressed down.

#### Scenario: Key press triggers stamp animation
- **WHEN** user presses a valid zhuyin key
- **THEN** the system animates the key with a subtle scale transform (1.0 → 1.05 → 1.0)
- **THEN** the system applies a brief shadow increase to simulate depth
- **THEN** the animation completes within 200-300ms

#### Scenario: Stamp effect uses ink color transition
- **WHEN** the key stamp animation plays
- **THEN** the system transitions key background from white to ink-tinted color
- **THEN** the color uses ink/vermillion tones from the theme palette

### Requirement: Animate progress bar with ink rendering effect
The system SHALL display progress with a smooth fill animation that resembles ink渲染 (rendering/spreading) in water.

#### Scenario: Progress bar fills smoothly
- **WHEN** user completes a zhuyin symbol input
- **THEN** the system animates the progress bar fill with ease-out timing
- **THEN** the fill animation duration is 0.3-0.5s

#### Scenario: Progress bar uses gradient fill
- **WHEN** the progress bar is rendered
- **THEN** the system displays a gradient that mimics ink spreading
- **THEN** the gradient uses colors from the theme palette (jade/rust tones)

#### Scenario: Progress resets with fade transition
- **WHEN** a new word is loaded
- **THEN** the system fades out the old progress bar (0.2s)
- **THEN** the system resets to 0% and begins new progress tracking

### Requirement: Provide smooth CSS transitions for interactive elements
The system SHALL apply CSS transitions to all interactive elements for smooth state changes.

#### Scenario: Hover states transition smoothly
- **WHEN** user hovers over an interactive element (button, stat panel)
- **THEN** the system transitions background, border, and shadow properties
- **THEN** the transition duration is 0.2-0.3s with ease-out timing

#### Scenario: Focus states have visual feedback
- **WHEN** an element receives keyboard focus
- **THEN** the system applies a visible focus indicator with transition
- **THEN** the focus indicator uses theme colors and smooth appearance

### Requirement: Use CSS animations instead of JavaScript where possible
The system SHALL implement animations primarily using CSS @keyframes and transitions, only using JavaScript for triggering and control logic.

#### Scenario: Animations are defined in CSS
- **WHEN** any animation plays
- **THEN** the system uses CSS @keyframes for motion definitions
- **THEN** JavaScript only adds/removes CSS classes to trigger animations

#### Scenario: Animations leverage GPU acceleration
- **WHEN** CSS animations are defined
- **THEN** the system uses transform and opacity properties (GPU-accelerated)
- **THEN** the system avoids animating layout properties (width, height, top, left)
