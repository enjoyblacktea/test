## ADDED Requirements

### Requirement: Render particles on HTML5 Canvas
The system SHALL use HTML5 Canvas API to render animated particle effects with efficient frame-based rendering.

#### Scenario: Canvas overlay is created
- **WHEN** the page loads
- **THEN** the system creates a full-viewport Canvas element
- **THEN** the Canvas is positioned as an overlay (z-index above content)
- **THEN** the Canvas has pointer-events: none to allow interaction with underlying elements

#### Scenario: Canvas context is 2D
- **WHEN** the Canvas is initialized
- **THEN** the system obtains a 2D rendering context
- **THEN** the system uses requestAnimationFrame for rendering loop

#### Scenario: Canvas clears before each frame
- **WHEN** the rendering loop executes
- **THEN** the system clears the entire Canvas before drawing new frame
- **THEN** particles are redrawn at their updated positions

### Requirement: Emit fireworks particles on correct input
The system SHALL trigger a celebratory fireworks particle effect when the user successfully completes typing a character.

#### Scenario: Fireworks emit on word completion
- **WHEN** user inputs the final correct zhuyin symbol for a word
- **THEN** the system emits 20-40 firework particles from the character's center position
- **THEN** particles radiate outward in a circular pattern

#### Scenario: Fireworks use warm colors
- **WHEN** firework particles are created
- **THEN** the system uses colors from theme palette (rust, vermillion, jade)
- **THEN** each particle may have a randomized color from the palette

#### Scenario: Fireworks have physics simulation
- **WHEN** firework particles move
- **THEN** the system applies outward velocity (radial from origin)
- **THEN** the system applies gravity effect (downward acceleration)
- **THEN** particles fade out over 1-2 seconds

#### Scenario: Fireworks particles are removed when dead
- **WHEN** a particle's opacity reaches 0
- **THEN** the system removes the particle from the active particles array
- **THEN** the particle no longer consumes processing resources

### Requirement: Emit ink drop particles for visual flair
The system SHALL provide decorative ink drop particle effects for ambient visual interest and correct inputs.

#### Scenario: Ink drops emit on individual symbol input
- **WHEN** user inputs a correct zhuyin symbol (not final symbol)
- **THEN** the system emits 5-10 ink drop particles near the keyboard key
- **THEN** particles splash outward briefly then fall

#### Scenario: Ink drops use dark colors
- **WHEN** ink drop particles are created
- **THEN** the system uses ink-dark (#1a1a1a) or jade (#059669) colors
- **THEN** particles have semi-transparent appearance (opacity 0.6-0.9)

#### Scenario: Ink drops have splash physics
- **WHEN** ink drop particles move
- **THEN** the system applies random outward velocity (splash effect)
- **THEN** the system applies gravity to pull particles downward
- **THEN** particles fade out over 0.5-1.0 seconds

### Requirement: Limit maximum particle count for performance
The system SHALL enforce a maximum particle limit to prevent performance degradation on lower-end devices.

#### Scenario: Particle count is capped at 300
- **WHEN** particle emission is requested
- **WHEN** current particle count >= 300
- **THEN** the system does not create new particles
- **THEN** the system waits for existing particles to expire

#### Scenario: Oldest particles removed if limit exceeded
- **WHEN** particle count exceeds the maximum limit
- **THEN** the system removes the oldest particles first
- **THEN** the total count is maintained at or below 300

### Requirement: Use object pooling to optimize memory allocation
The system SHALL reuse particle objects instead of creating and destroying them frequently.

#### Scenario: Particle pool is initialized
- **WHEN** the particle system initializes
- **THEN** the system creates a pool of 100 pre-allocated particle objects
- **THEN** particles are marked as inactive

#### Scenario: Particles are borrowed from pool
- **WHEN** new particles are needed
- **THEN** the system reuses inactive particles from the pool
- **THEN** the system only allocates new objects if pool is exhausted

#### Scenario: Particles are returned to pool
- **WHEN** a particle expires (opacity reaches 0)
- **THEN** the system marks the particle as inactive
- **THEN** the particle is available for reuse

### Requirement: Provide configurable particle parameters
The system SHALL allow customization of particle appearance and behavior through configuration options.

#### Scenario: Particle color is configurable
- **WHEN** particles are emitted
- **THEN** the system accepts a color parameter (default: theme palette)
- **THEN** particles use the specified color

#### Scenario: Particle velocity is configurable
- **WHEN** particles are emitted
- **THEN** the system accepts min/max velocity parameters
- **THEN** each particle's initial velocity is randomized within the range

#### Scenario: Particle count is configurable
- **WHEN** an emission event occurs
- **THEN** the system accepts a particle count parameter
- **THEN** the system emits the specified number of particles

#### Scenario: Particle lifetime is configurable
- **WHEN** particles are created
- **THEN** the system accepts a lifetime parameter (in seconds)
- **THEN** particles fade out over the specified duration
