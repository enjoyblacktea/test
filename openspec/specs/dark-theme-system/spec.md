## Purpose

Provides a modern dark color theme system for the Zhuyin practice application, replacing the previous calligraphy-inspired warm color palette with a high-contrast pure black and cyan aesthetic for improved readability and modern visual design.

## Requirements

### Requirement: Define dark color system with CSS variables
The system SHALL define a cohesive dark color palette using CSS custom properties for centralized theme management.

#### Scenario: Primary background colors are defined
- **WHEN** the stylesheet loads
- **THEN** the system defines --color-bg-primary as pure black (#0a0a0a)
- **THEN** the system defines --color-bg-secondary as dark gray (#1a1a1a) for cards and elevated elements
- **THEN** the system defines --color-bg-elevated as medium gray (#2a2a2a) for hover states

#### Scenario: Text colors are defined
- **WHEN** the stylesheet loads
- **THEN** the system defines --color-text-primary as white (#ffffff) for primary text
- **THEN** the system defines --color-text-secondary as light gray (#a0a0a0) for secondary text
- **THEN** the system defines --color-text-disabled as medium gray (#6a6a6a) for disabled states

#### Scenario: Accent colors are defined
- **WHEN** the stylesheet loads
- **THEN** the system defines --color-accent-primary as cyan (#00d9ff) for highlights and keyboard feedback
- **THEN** the system defines --color-accent-success as green (#00ff88) for success states and completion
- **THEN** the system defines --color-accent-error as red (#ff4444) for error states
- **THEN** the system defines --color-accent-warning as orange (#ffaa00) for warning states

### Requirement: Apply pure black background to body
The system SHALL render the main application background as pure black for maximum contrast and modern aesthetic.

#### Scenario: Body uses primary background color
- **WHEN** the page loads
- **THEN** the system applies --color-bg-primary (#0a0a0a) to body background
- **THEN** the background remains solid black without gradients or decorative elements

#### Scenario: Background covers full viewport
- **WHEN** content height is less than viewport
- **THEN** the system ensures black background extends to full viewport height
- **THEN** no white gaps appear at bottom of page

### Requirement: Use high-contrast text colors
The system SHALL apply high-contrast text colors (#ffffff, #a0a0a0) for maximum readability on dark backgrounds.

#### Scenario: Primary text is white
- **WHEN** primary content is rendered (practice character, important labels)
- **THEN** the system applies --color-text-primary (#ffffff) for text color
- **THEN** text contrast ratio meets WCAG AA standards (minimum 7:1)

#### Scenario: Secondary text is light gray
- **WHEN** secondary content is rendered (hints, subtitles, metadata)
- **THEN** the system applies --color-text-secondary (#a0a0a0) for text color
- **THEN** text remains readable with adequate contrast (minimum 4.5:1)

### Requirement: Apply cyan accent for interactive highlights
The system SHALL use cyan (#00d9ff) as the primary accent color for interactive elements and keyboard feedback.

#### Scenario: Keyboard highlights use cyan
- **WHEN** a keyboard key is highlighted on user input
- **THEN** the system applies --color-accent-primary (#00d9ff) to key background
- **THEN** the highlight creates clear visual feedback with high visibility

#### Scenario: Progress bar uses cyan gradient
- **WHEN** the progress bar fills
- **THEN** the system applies gradient from cyan (#00d9ff) to green (#00ff88)
- **THEN** the gradient provides clear visual progress indication

### Requirement: Style practice card with elevated dark background
The system SHALL render the practice card with a dark gray background (#1a1a1a) to create visual elevation above the pure black background.

#### Scenario: Practice card uses secondary background
- **WHEN** the practice card is rendered
- **THEN** the system applies --color-bg-secondary (#1a1a1a) to card background
- **THEN** the card visually stands out from the pure black body background

#### Scenario: Practice card has subtle border
- **WHEN** the practice card is rendered
- **THEN** the system applies a subtle 1px border with color #333
- **THEN** the border provides additional visual definition without being harsh

#### Scenario: Practice card has neutral shadow
- **WHEN** the practice card is rendered
- **THEN** the system applies box-shadow using rgba(0, 0, 0, 0.6) for depth
- **THEN** the shadow is neutral black (not warm-toned from old theme)

### Requirement: Maintain consistent dark theme across all pages
The system SHALL apply the dark color system consistently to all pages including main app and login screen.

#### Scenario: Login page uses same color variables
- **WHEN** the login page loads
- **THEN** the system applies identical CSS variable definitions to login.css
- **THEN** the login page visual appearance matches the main app dark theme

#### Scenario: All interactive elements use accent colors
- **WHEN** any button, input, or interactive element is rendered
- **THEN** the system uses accent colors from the CSS variable palette
- **THEN** visual consistency is maintained across all pages

### Requirement: Remove all warm-toned colors from previous theme
The system SHALL eliminate all references to the calligraphy theme's warm color palette (rust #d97706, vermillion #dc2626, jade #059669, cream #fffbeb).

#### Scenario: Warm colors are not present
- **WHEN** the dark theme is applied
- **THEN** the system does not use rust, vermillion, jade, or cream colors
- **THEN** only the new dark theme colors (black, white, cyan, green, red) are present

#### Scenario: CSS variables use new color names
- **WHEN** CSS variables are defined
- **THEN** variable names reflect the new color system (--color-bg-primary, not --color-cream)
- **THEN** old color variable names (--color-rust, --color-jade, etc.) are not present
