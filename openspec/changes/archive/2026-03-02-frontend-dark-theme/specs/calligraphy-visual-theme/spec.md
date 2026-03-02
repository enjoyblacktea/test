## REMOVED Requirements

### Requirement: Display ink wash style background
**Reason**: Replaced by dark-theme-system which uses pure black background without decorative elements.
**Migration**: Remove all .ink-bg, .stroke, and related HTML/CSS. Background is now solid --color-bg-primary (#0a0a0a).

### Requirement: Apply traditional decorative elements
**Reason**: Dark theme removes all decorative elements for modern minimalist aesthetic.
**Migration**: Remove header-decoration, footer, title element, and all calligraphy-related HTML/CSS.

### Requirement: Use warm color palette
**Reason**: Replaced by high-contrast dark color system with cyan/green/red accents.
**Migration**: Replace all warm color CSS variables (--color-rust, --color-vermillion, --color-jade, --color-cream) with dark theme variables (--color-accent-primary, --color-bg-primary, etc.). See dark-theme-system spec.

### Requirement: Load and display Chinese fonts
**Reason**: Font loading remains but styling context changes - requirements move to dark-theme-system.
**Migration**: Font loading (Noto Serif TC, Noto Sans TC) continues unchanged. CSS styling now uses dark theme colors instead of warm tones.

### Requirement: Implement CSS variables for theme consistency
**Reason**: CSS variable approach continues but with completely new color palette.
**Migration**: Replace :root CSS variable definitions with dark theme color system. Variable structure (var(--color-*)) remains, but all color values and names change. See dark-theme-system spec.
