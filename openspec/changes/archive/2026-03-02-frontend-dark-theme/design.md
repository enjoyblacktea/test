## Context

The Zhuyin practice app currently uses a "筆墨童趣" (calligraphy/ink playfulness) visual theme with warm colors (cream #fffbeb, rust #d97706, jade #059669), decorative elements (ink splashes, brush strokes, particle effects), and a distinctive aesthetic. While unique, this theme:

- Lacks the high-contrast readability expected in modern applications
- Uses warm/light colors that may cause eye strain during extended practice
- Includes heavy decorative elements that distract from core functionality
- Does not align with contemporary dark mode design patterns

**Stakeholders**: End users (learners), development team
**Constraints**:
- Must maintain all existing functionality (authentication, practice flow, input validation)
- Backend remains unchanged
- Responsive design must continue working across desktop/tablet/mobile
- No framework dependencies (Vanilla JS, CSS only)

## Goals / Non-Goals

**Goals:**
- Replace calligraphy theme with modern pure black (#0a0a0a) + high-contrast design
- Remove all decorative elements while maintaining visual polish
- Simplify animations to minimal, modern effects (pulse, glow)
- Create unified dark theme across main app and login page
- Improve readability and reduce visual clutter
- Maintain all existing functionality and responsive behavior

**Non-Goals:**
- Adding theme switcher (light/dark toggle) - single dark theme only
- Rewriting JavaScript logic or refactoring module structure beyond animation simplification
- Changing authentication flow, input validation, or practice mechanics
- Adding new features or functionality
- Redesigning keyboard layout beyond spacebar width adjustment

## Decisions

### Decision 1: CSS Variables for Dark Theme System

**Choice**: Define all colors as CSS custom properties in `:root`

**Rationale**:
- Centralizes color management in one location
- Enables easy future adjustments without touching multiple files
- Standard approach for theme systems
- No build tools or preprocessors required

**Implementation**:
```css
:root {
    --color-bg-primary: #0a0a0a;
    --color-bg-secondary: #1a1a1a;
    --color-text-primary: #ffffff;
    --color-text-secondary: #a0a0a0;
    --color-accent-primary: #00d9ff;    /* Cyan */
    --color-accent-success: #00ff88;    /* Green */
    --color-accent-error: #ff4444;      /* Red */
}
```

**Alternatives Considered**:
- Hardcode colors: Would require find-replace across files, harder to maintain
- Use SCSS/LESS: Adds build complexity for minimal benefit

---

### Decision 2: Complete Removal of Decorative Elements

**Choice**: Remove all ink-bg, ink-splash, particles-canvas, header decorations, footer

**Rationale**:
- Aligns with user requirement for "純黑+高對比" modern aesthetic
- Reduces visual noise and improves focus on core practice elements
- Simplifies HTML structure and reduces CSS complexity
- Eliminates unnecessary JavaScript (ParticleSystem module)

**Impact**:
- HTML: Remove `<header>`, `<footer>`, `.ink-bg`, `.ink-splash`, `<canvas id="particles-canvas">`
- CSS: Delete animations.css, particles.css; remove related styles from redesign.css
- JS: Remove ParticleSystem import and initialization in main.js

**Alternatives Considered**:
- Adapt decorations to dark theme: User explicitly requested complete removal
- Keep particle effects: User chose "完全移除" over partial retention

---

### Decision 3: Spacebar Width Reduction Method

**Choice**: Change from `flex-grow: 1` + `min-width: 300px` to fixed `width: 300px` + centering

**Rationale**:
- User specified "約 6 個鍵寬" - fixed width ensures predictable sizing
- Centered spacebar maintains visual balance
- Prevents spacebar from stretching on wide screens
- Matches user's expectation: "在原 spacebar 位置，但縮小"

**Implementation**:
```css
.key.spacebar {
    width: 300px;              /* Fixed width ~6 keys */
    margin: 0 auto;            /* Center in row */
    flex-grow: 0;              /* Prevent stretching */
}
```

**Alternatives Considered**:
- Span multiple keys in row 4: User rejected this layout
- Percentage-based width: Less predictable across screen sizes

---

### Decision 4: Animation Simplification Strategy

**Choice**: Replace complex animations with simple CSS keyframes (pulse, glow)

**Rationale**:
- User requested "保留並調整為簡潔效果" - keep feedback but simplify
- Pure CSS animations are performant and don't require canvas or heavy JS
- Maintains core feedback (correct input, completion) without visual complexity

**Implementation**:
- Correct input: `@keyframes correct-pulse` - scale + fade
- Completion: `@keyframes completion-glow` - box-shadow glow
- Remove: Particle bursts, fireworks, ink splash effects

**JavaScript Changes**:
- Simplify AnimationController to only trigger CSS classes
- Remove triggerPageLoadAnimation (no title animation)
- Remove complex particle burst logic

**Alternatives Considered**:
- Remove all animations: User wanted to keep feedback
- Keep fireworks/particles: User chose simplified modern effects

---

### Decision 5: File Reorganization Approach

**Choice**: Delete old index.html, rename index-redesign.html → index.html atomically

**Rationale**:
- Eliminates confusion between old/new versions
- index.html as single entry point aligns with convention
- Reduces maintenance burden (single codebase)

**Migration Steps**:
1. Verify all changes complete in index-redesign.html
2. Update login.html redirect: `./index-redesign.html` → `./index.html`
3. Delete `frontend/index.html`
4. Rename `frontend/index-redesign.html` → `frontend/index.html`
5. Rename `frontend/js/main-redesign.js` → `frontend/js/main.js`
6. Update script tag in index.html

**Risk Mitigation**: Perform in feature branch, test thoroughly before merging

**Alternatives Considered**:
- Keep both files: Confusing, requires maintaining two codepases
- Gradual migration: Unnecessary complexity for frontend-only change

---

### Decision 6: Login Page Color Matching

**Choice**: Override login.css CSS variables to match dark theme, keep structure unchanged

**Rationale**:
- Minimal changes to login functionality
- Reuses existing component structure
- CSS variables make color updates straightforward

**Implementation**:
```css
/* login.css */
:root {
    --color-bg-primary: #0a0a0a;      /* Match main app */
    --color-bg-secondary: #1a1a1a;
    --color-text-primary: #ffffff;
    --color-accent-primary: #00d9ff;
}
```

**Alternatives Considered**:
- Separate login theme: Would create visual disconnect
- Rebuild login page: Unnecessary churn for color-only change

## Risks / Trade-offs

### Risk 1: Loss of Unique Visual Identity
**Risk**: Removing calligraphy theme eliminates distinctive branding
**Trade-off**: Gains modern readability and accessibility at cost of uniqueness
**Mitigation**: Focus on functional excellence as differentiator; consider subtle typography choices in future if branding needed

### Risk 2: User Adjustment Period
**Risk**: Existing users familiar with calligraphy theme may find change jarring
**Trade-off**: Short-term friction for long-term improved UX
**Mitigation**: Document change in release notes; gather user feedback post-launch

### Risk 3: Incomplete Removal of Decorative Elements
**Risk**: Missing CSS references could cause broken styles or layout issues
**Trade-off**: Clean break reduces maintenance complexity
**Mitigation**: Thorough testing across breakpoints; grep for removed class names to catch references

### Risk 4: Animation Regression
**Risk**: Simplified animations may feel less polished initially
**Trade-off**: Performance and maintenance benefits outweigh complexity
**Mitigation**: Fine-tune timing/easing in testing; keep animations subtle but noticeable

### Risk 5: File Renaming Disrupts Development
**Risk**: Other branches or in-progress work may reference old file names
**Trade-off**: Clean structure worth coordination cost
**Mitigation**: Coordinate with team; merge to main promptly; communicate file name changes

## Migration Plan

**Not Applicable**: This is a frontend visual update with no backend changes, database migrations, or API versioning requirements.

**Deployment**:
- Standard static file deployment (replace frontend/ directory)
- No feature flags needed - visual changes are immediately visible
- Rollback: Revert commit to previous main branch state if critical issues found

**Testing Checklist**:
- [ ] Visual regression across breakpoints (desktop 1920px, tablet 768px, mobile 375px/414px)
- [ ] Keyboard input and highlighting still works
- [ ] Animations trigger correctly (correct input, completion)
- [ ] Login page matches dark theme
- [ ] Logout button visible and functional
- [ ] No console errors from removed modules

## Open Questions

None - design decisions finalized through user brainstorming session. All color choices, layout changes, and simplification approaches confirmed by user.
