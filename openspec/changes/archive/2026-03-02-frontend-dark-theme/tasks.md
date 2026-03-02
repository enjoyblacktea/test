## 1. CSS Color System Setup

- [x] 1.1 Define dark theme CSS variables in redesign.css :root section
- [x] 1.2 Replace all warm color variables (--color-rust, --color-vermillion, --color-jade, --color-cream) with dark theme variables
- [x] 1.3 Verify CSS variable naming matches dark-theme-system spec (--color-bg-primary, --color-text-primary, etc.)

## 2. HTML Structure Changes - Remove Decorative Elements

- [x] 2.1 Remove `<header>` element containing title "注音輸入練習" from index-redesign.html
- [x] 2.2 Remove `<footer>` element containing "用心練習，字字生花" from index-redesign.html
- [x] 2.3 Remove `.ink-bg` decorative background div and all `.stroke` elements from index-redesign.html
- [x] 2.4 Remove `.ink-splash` decorative elements (ink-splash--left, ink-splash--right) from index-redesign.html
- [x] 2.5 Remove `<canvas id="particles-canvas">` element from index-redesign.html
- [x] 2.6 Remove header-decoration divs (header-decoration--top, header-decoration--bottom) if present

## 3. HTML Structure Changes - Reorganize Layout

- [x] 3.1 Move logout button to be positioned at top-right (update HTML structure if needed)
- [x] 3.2 Move keyboard-hint paragraph above practice-card section (currently below)
- [x] 3.3 Update keyboard-hint text to simplified version: "使用 QWERTY 鍵盤輸入注音符號。"
- [x] 3.4 Verify practice-area structure: hint → practice-card → keyboard-area

## 4. CSS Styling Updates - Backgrounds and Colors

- [x] 4.1 Update body background to use --color-bg-primary (#0a0a0a) solid color (remove gradients)
- [x] 4.2 Update .practice-card background to --color-bg-secondary (#1a1a1a)
- [x] 4.3 Update .practice-card border to 1px solid #333
- [x] 4.4 Update .practice-card box-shadow to use neutral black rgba(0, 0, 0, 0.6)
- [x] 4.5 Update .practice-character color to --color-text-primary (#ffffff)
- [x] 4.6 Update .zhuyin-display color to --color-accent-primary (#00d9ff)
- [x] 4.7 Update .keyboard-hint color to --color-text-secondary (#a0a0a0)

## 5. CSS Styling Updates - Keyboard

- [x] 5.1 Update .keyboard background to --color-bg-secondary (#1a1a1a)
- [x] 5.2 Update .key background to --color-bg-elevated (#2a2a2a)
- [x] 5.3 Update .key border to 1px solid #333
- [x] 5.4 Update .key.highlighted background to --color-accent-primary (#00d9ff)
- [x] 5.5 Update .key.highlighted text color to #000000 (black for contrast on cyan)
- [x] 5.6 Update .key.highlighted box-shadow to cyan glow: 0 0 20px rgba(0, 217, 255, 0.5)
- [x] 5.7 Update .zhuyin text color to --color-text-primary (#ffffff)
- [x] 5.8 Update .letter text color to --color-text-secondary (#a0a0a0)
- [x] 5.9 Change .key.spacebar from flex-grow:1 + min-width:300px to fixed width:300px + margin:0 auto
- [x] 5.10 Verify spacebar no longer uses flex-grow property

## 6. CSS Styling Updates - Progress Bar

- [x] 6.1 Update .progress-fill gradient from jade/rust to cyan/green: linear-gradient(90deg, #00d9ff, #00ff88)
- [x] 6.2 Remove .progress-ink shimmer animation if present (simplified theme)

## 7. CSS Styling Updates - Logout Button

- [x] 7.1 Update .logout-button position to fixed with top:1.5rem, right:1.5rem
- [x] 7.2 Update .logout-button colors to use --color-text-secondary for text and border
- [x] 7.3 Update .logout-button:hover to use --color-accent-primary (#00d9ff)

## 8. CSS File Consolidation

- [x] 8.1 Remove link to styles/animations.css from index-redesign.html
- [x] 8.2 Remove link to styles/particles.css from index-redesign.html
- [x] 8.3 Verify only 4 stylesheets remain: redesign.css, keyboard-redesign.css (update with dark colors later)

## 9. CSS Styling Updates - Remove Decorative Styles

- [x] 9.1 Remove all .ink-bg, .stroke, .ink-splash related CSS from redesign.css
- [x] 9.2 Remove .header-decoration CSS rules from redesign.css
- [x] 9.3 Remove .footer and .footer-text CSS rules from redesign.css
- [x] 9.4 Remove .title-char animation-related CSS from redesign.css

## 10. Animation Updates - Add New Keyframes

- [x] 10.1 Add @keyframes correct-pulse animation (scale 1.0 → 1.1 → 1.0, duration 0.3s)
- [x] 10.2 Add @keyframes completion-glow animation (box-shadow pulse with green glow, duration 0.5s)
- [x] 10.3 Add @keyframes fade-in animation for practice card (opacity 0→1, translateY 10px→0, duration 0.3s)
- [x] 10.4 Remove @keyframes ink-shimmer if present
- [x] 10.5 Remove any stamp-press or seal-related keyframe animations

## 11. JavaScript Updates - Remove ParticleSystem

- [x] 11.1 Remove ParticleSystem import from main-redesign.js
- [x] 11.2 Remove particleSystem variable declaration and initialization in main-redesign.js
- [x] 11.3 Remove particleSystem from inputHandler.init() dependencies in main-redesign.js
- [x] 11.4 Comment out or remove canvas element check and ParticleSystem initialization block

## 12. JavaScript Updates - Simplify AnimationController

- [x] 12.1 Remove AnimationController.triggerPageLoadAnimation() call from main-redesign.js (no title animation)
- [x] 12.2 Update AnimationController module to remove complex particle/firework logic
- [x] 12.3 Keep AnimationController for simple CSS class toggling (correct-pulse, completion-glow)
- [x] 12.4 Verify AnimationController only adds/removes CSS classes, no canvas operations

## 13. JavaScript Updates - Update input-handler-redesign.js

- [x] 13.1 Verify particleSystem dependency removal doesn't break input-handler logic
- [x] 13.2 Update correct input feedback to trigger correct-pulse CSS animation
- [x] 13.3 Update completion feedback to trigger completion-glow CSS animation
- [x] 13.4 Remove any particle emission calls

## 14. Login Page CSS Updates

- [x] 14.1 Update login.css :root variables to match dark theme (--color-bg-primary: #0a0a0a, etc.)
- [x] 14.2 Update .login-container background to --color-bg-secondary (#1a1a1a)
- [x] 14.3 Update .login-card background colors to dark theme
- [x] 14.4 Update button colors to use --color-accent-primary (#00d9ff)
- [x] 14.5 Update text colors to --color-text-primary and --color-text-secondary
- [x] 14.6 Update form input backgrounds and borders to dark theme colors

## 15. Login Page Redirect Updates

- [x] 15.1 Update login.html redirect on successful login from ./index-redesign.html to ./index.html (line 113, 187)
- [x] 15.2 Update login.html redirect on already authenticated from ./index-redesign.html to ./index.html

## 16. File Cleanup - Delete Old Files

- [x] 16.1 Delete frontend/index.html (old version)
- [x] 16.2 Delete frontend/styles/animations.css if not already deleted
- [x] 16.3 Delete frontend/styles/particles.css if not already deleted

## 17. File Renaming

- [x] 17.1 Rename frontend/index-redesign.html to frontend/index.html
- [x] 17.2 Rename frontend/js/main-redesign.js to frontend/js/main.js
- [x] 17.3 Update script src in index.html from "js/main-redesign.js" to "js/main.js"
- [x] 17.4 Verify all file references are updated

## 18. Responsive Design Verification

- [x] 18.1 Test layout at desktop breakpoint (1920px) - verify logout position, card layout, keyboard
- [x] 18.2 Test layout at tablet breakpoint (768px) - verify responsive adjustments work
- [x] 18.3 Test layout at mobile breakpoint (375px, 414px) - verify keyboard sizing, spacebar width
- [x] 18.4 Verify all dark theme colors are visible across all breakpoints

## 19. Functional Testing

- [x] 19.1 Test keyboard input - verify keys highlight correctly with cyan color
- [x] 19.2 Test correct input animation - verify correct-pulse triggers on valid symbol
- [x] 19.3 Test completion animation - verify completion-glow triggers on word completion
- [x] 19.4 Test progress bar - verify cyan-to-green gradient displays and fills correctly
- [x] 19.5 Test logout button - verify visible, clickable, and functional
- [x] 19.6 Test login page - verify dark theme applied and login flow works
- [x] 19.7 Verify no console errors from removed modules (ParticleSystem, etc.)

## 20. Visual Polish and Accessibility

- [x] 20.1 Verify text contrast ratios meet WCAG AA standards (white on black: 7:1+)
- [x] 20.2 Verify focus indicators are visible with cyan outline
- [x] 20.3 Verify animations respect prefers-reduced-motion if implemented
- [x] 20.4 Check for any remaining warm-toned colors and replace with dark theme colors
- [x] 20.5 Verify all CSS variable references are correct (no undefined variables)

## 21. Final Verification

- [x] 21.1 Run through complete practice flow (login → practice → logout)
- [x] 21.2 Check browser console for any warnings or errors
- [x] 21.3 Verify spacebar shows correct width (~6 keys, 300px)
- [x] 21.4 Verify all decorative elements are completely removed (no ink splashes, particles, header/footer)
- [x] 21.5 Take screenshots for documentation if needed
