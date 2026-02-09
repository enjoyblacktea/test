## ADDED Requirements

### Requirement: Display ink wash style background
The system SHALL render a background with traditional Chinese ink wash (水墨) aesthetic featuring brush strokes, gradients, and ink splash effects.

#### Scenario: Page displays ink wash background
- **WHEN** the page loads
- **THEN** the system displays decorative brush stroke elements in the background
- **THEN** the background uses warm tone gradients (rust/赭石, vermillion/朱砂, jade/墨綠)

#### Scenario: Background does not interfere with content
- **WHEN** the background is rendered
- **THEN** the system ensures background elements have low opacity (< 0.3)
- **THEN** the content text remains clearly readable against the background

### Requirement: Apply traditional decorative elements
The system SHALL incorporate traditional Chinese decorative elements including seal stamp style and calligraphy brush strokes.

#### Scenario: Header displays calligraphy decorations
- **WHEN** the header is rendered
- **THEN** the system shows decorative elements above and below the title
- **THEN** decorations use traditional patterns (印章/seal stamps, 書法筆觸/brush strokes)

#### Scenario: Decorative elements enhance aesthetics
- **WHEN** decorative elements are displayed
- **THEN** the system uses subtle colors that complement the main theme
- **THEN** decorations do not obscure functional content

### Requirement: Use warm color palette
The system SHALL apply a cohesive warm-toned color scheme derived from traditional Chinese painting pigments.

#### Scenario: Primary colors match theme
- **WHEN** any UI element is styled
- **THEN** the system uses colors from the defined palette:
  - Rust/赭石 (#d97706) for accents
  - Vermillion/朱砂 (#dc2626) for highlights
  - Jade/墨綠 (#059669) for success states
  - Cream/奶油白 (#fffbeb) for backgrounds
  - Ink dark/墨色 (#1a1a1a) for text

#### Scenario: Color palette is consistent
- **WHEN** multiple components use themed colors
- **THEN** the system maintains visual harmony across all elements
- **THEN** color usage follows defined CSS variables

### Requirement: Load and display Chinese fonts
The system SHALL use elegant serif fonts for titles and sans-serif fonts for body text, optimized for Traditional Chinese characters.

#### Scenario: Title uses serif font
- **WHEN** the page title is rendered
- **THEN** the system displays text using Noto Serif TC font family
- **THEN** the font weight is bold (700 or 900)

#### Scenario: Body text uses sans-serif font
- **WHEN** body text and UI labels are rendered
- **THEN** the system displays text using Noto Sans TC font family
- **THEN** the font weight is regular (400) or medium (500)

#### Scenario: Fonts load from CDN
- **WHEN** the page loads
- **THEN** the system fetches fonts from Google Fonts CDN
- **THEN** the system uses font-display: swap to show text immediately
- **THEN** the system falls back to system fonts if CDN fails

### Requirement: Implement CSS variables for theme consistency
The system SHALL define all theme values (colors, fonts, spacing, shadows) as CSS custom properties for centralized management.

#### Scenario: CSS variables are defined
- **WHEN** the stylesheet loads
- **THEN** the system defines CSS variables in :root selector
- **THEN** variables include: colors, fonts, spacing scale, animation durations, shadow depths

#### Scenario: All components use CSS variables
- **WHEN** any component is styled
- **THEN** the system references CSS variables (var(--color-ink-dark)) instead of hardcoded values
- **THEN** changing a variable value updates all components using it
