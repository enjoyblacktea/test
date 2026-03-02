## REMOVED Requirements

### Requirement: Animate page load with staggered reveals
**Reason**: Title element removed in dark theme; no page load animations needed for simplified layout.
**Migration**: Remove title character animations and AnimationController.triggerPageLoadAnimation(). Practice card appears immediately without animation.

### Requirement: Animate practice word with brush writing effect
**Reason**: Brush calligraphy animation removed in favor of instant character display.
**Migration**: Practice character appears immediately without stroke-by-stroke animation. Keep simple fade-in for card if desired.

### Requirement: Animate keyboard key press with seal stamp effect
**Reason**: Seal stamp aesthetic replaced by simple scale+glow effect.
**Migration**: Use simplified pulse animation defined in MODIFIED requirements below.

### Requirement: Animate progress bar with ink rendering effect
**Reason**: Ink渲染 visual replaced by standard gradient fill.
**Migration**: Progress bar uses simple linear gradient (cyan to green) with ease-out transition. No special ink spreading effect.

## MODIFIED Requirements

### Requirement: Provide smooth CSS transitions for interactive elements
The system SHALL apply CSS transitions to all interactive elements for smooth state changes using modern dark theme styling.

#### Scenario: Hover states transition smoothly
- **WHEN** user hovers over an interactive element (button, logout button)
- **THEN** the system transitions background, border, and color properties
- **THEN** the transition duration is 0.2-0.3s with ease-out timing
- **THEN** hover colors use dark theme palette (cyan highlight, lighter backgrounds)

#### Scenario: Focus states have visual feedback
- **WHEN** an element receives keyboard focus
- **THEN** the system applies a visible focus indicator with cyan (#00d9ff) outline
- **THEN** the focus indicator has 2px width and smooth transition
- **THEN** the focus indicator follows WCAG accessibility guidelines

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

## ADDED Requirements

### Requirement: Provide correct input pulse animation
The system SHALL display a subtle pulse animation when the user inputs a correct zhuyin symbol, using cyan glow effect.

#### Scenario: Correct input triggers pulse
- **WHEN** user inputs a correct zhuyin symbol (not final symbol)
- **THEN** the system briefly scales the practice character (1.0 → 1.1 → 1.0)
- **THEN** the animation duration is 0.3s with ease-out timing

#### Scenario: Pulse uses cyan color
- **WHEN** the pulse animation plays
- **THEN** the system applies cyan glow to the character using text-shadow or filter
- **THEN** the glow uses rgba(0, 217, 255, 0.6) for semi-transparency

#### Scenario: Animation does not block input
- **WHEN** pulse animation is playing
- **THEN** the system continues accepting user keyboard input
- **THEN** subsequent inputs can trigger new animations immediately

### Requirement: Provide completion glow animation
The system SHALL display a completion glow animation when the user successfully completes a word, using green glow effect.

#### Scenario: Word completion triggers glow
- **WHEN** user inputs the final correct zhuyin symbol for a word
- **THEN** the system applies a glowing box-shadow to the practice card
- **THEN** the glow pulses once (0 → full → 0) over 0.5s

#### Scenario: Glow uses green color
- **WHEN** the completion glow animation plays
- **THEN** the system uses rgba(0, 255, 136, 0.8) for bright green glow
- **THEN** the glow is visible against the dark background
- **THEN** the animation completes before loading the next word

#### Scenario: Glow animates box-shadow
- **WHEN** the glow animation is defined
- **THEN** the system animates box-shadow property (not background)
- **THEN** the animation uses @keyframes completion-glow
- **THEN** the shadow spreads from 0 to 30px and back

### Requirement: Provide fade-in animation for practice card
The system SHALL display a simple fade-in animation when the practice card first appears or when a new word loads.

#### Scenario: Card fades in on load
- **WHEN** the page loads or a new word is loaded
- **THEN** the system animates the practice card from opacity 0 to 1
- **THEN** the system animates translateY from 10px to 0
- **THEN** the total animation duration is 0.3-0.4s with ease-out

#### Scenario: Fade-in does not delay interaction
- **WHEN** the fade-in animation is playing
- **THEN** the system allows user input immediately
- **THEN** user can start typing before animation completes

### Requirement: Simplify all animations for performance
The system SHALL use minimal, performant animations that avoid complex physics simulations or heavy Canvas operations.

#### Scenario: No JavaScript animation loops
- **WHEN** animations are implemented
- **THEN** the system does not use requestAnimationFrame loops
- **THEN** all animations are CSS-based or simple class toggles

#### Scenario: Animations respect reduced motion
- **WHEN** user has prefers-reduced-motion enabled
- **THEN** the system disables or drastically shortens all animations
- **THEN** animation durations become 0.01ms or instant
