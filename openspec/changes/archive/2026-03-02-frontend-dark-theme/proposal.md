## Why

The current calligraphy-themed interface, while unique, lacks the modern readability and high-contrast design that users expect from contemporary applications. Transitioning to a pure black dark theme with high contrast improves visual clarity, reduces eye strain, and aligns with modern design standards while maintaining focus on the core practice experience.

## What Changes

- **Replace calligraphy theme with modern dark theme**: Pure black (#0a0a0a) background with high-contrast accent colors (cyan, green, red)
- **Remove decorative elements**: Eliminate all ink splashes, brush strokes, particle canvas, decorative headers, and footer text
- **Simplify layout structure**: Remove title "注音輸入練習" and footer "用心練習，字字生花", keep only essential elements (logout button, practice card, keyboard)
- **Update keyboard layout**: Reduce spacebar width from full-width to approximately 6 keys width
- **Simplify animations**: Replace complex ink/firework effects with minimal pulse and glow animations
- **Unify login page styling**: Update login.html to match the dark theme color palette
- **Clean up legacy files**: Delete old index.html, rename index-redesign.html to index.html, update all references

## Capabilities

### New Capabilities
- `dark-theme-system`: Modern dark color system with CSS variables for backgrounds (#0a0a0a, #1a1a1a), text colors (#ffffff, #a0a0a0), and accent colors (#00d9ff, #00ff88, #ff4444)

### Modified Capabilities
- `calligraphy-visual-theme`: **BREAKING** - Complete replacement with dark theme system, removal of all warm-toned colors, decorative elements, and calligraphy aesthetics
- `zhuyin-keyboard-display`: Spacebar width reduced from full-width (flex-grow: 1, min-width: 300px) to fixed width (~300px, centered), maintaining 6-key visual proportion
- `animated-ui-interactions`: **BREAKING** - Simplification from complex ink splash and firework effects to minimal pulse (correct input) and glow (completion) animations
- `particle-effects-system`: **BREAKING** - Complete removal of particle canvas and ParticleSystem module

## Impact

**Frontend Files Modified**:
- `frontend/index-redesign.html` → `frontend/index.html` (rename + restructure)
- `frontend/js/main-redesign.js` → `frontend/js/main.js` (remove ParticleSystem, simplify animations)
- `frontend/styles/redesign.css` → rewrite with dark theme variables
- `frontend/styles/keyboard-redesign.css` → update spacebar styles
- `frontend/styles/login.css` → dark theme update
- `frontend/login.html` → update redirect paths and color variables

**Frontend Files Removed**:
- `frontend/index.html` (old version)
- `frontend/styles/animations.css` (consolidated into main CSS)
- `frontend/styles/particles.css` (no longer needed)

**JavaScript Modules**:
- `js/modules/particle-system.js` - no longer imported
- `js/modules/animations.js` - simplified to remove complex effects
- `js/modules/input-handler-redesign.js` - remove particleSystem dependency

**No Backend Impact**: Backend authentication and database functionality remain unchanged
