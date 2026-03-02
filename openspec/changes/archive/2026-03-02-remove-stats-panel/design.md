## Context

The frontend currently has two parallel statistics tracking systems:
1. **Client-side**: `StatsTracker` module using localStorage to track practice count, accuracy, and streak
2. **Server-side**: PostgreSQL database storing complete practice history via `typing_attempts` table

This duplication occurred during the transition from MVP (local-only stats) to the database-backed authentication system. Now that all practice data is persisted server-side, the frontend stats are redundant and potentially confusing.

**Current State**:
- `index-redesign.html` displays stats panel with 3 metrics (已練習、準確率、連續正確)
- `main-redesign.js` initializes `StatsTracker` and updates the UI
- `input-handler-redesign.js` calls stats tracking methods on each keystroke
- All stats data is duplicated in both localStorage and PostgreSQL

**Constraints**:
- Must not affect backend API or database tracking
- Must maintain existing practice recording functionality
- Should not introduce console errors or broken references

## Goals / Non-Goals

**Goals:**
- Remove all frontend statistics UI and tracking logic
- Simplify codebase by eliminating redundant StatsTracker usage
- Reduce page load by removing stats-panel.css
- Clean up event handlers and DOM references to stats elements

**Non-Goals:**
- Not removing backend practice data tracking (this remains intact)
- Not adding replacement analytics UI (future enhancement)
- Not deleting StatsTracker module file (may be used elsewhere, cleanup separately)
- Not modifying the original `index.html` (only affects redesigned version)

## Decisions

### 1. Complete Removal vs. Hidden/Disabled
**Decision**: Completely remove HTML, CSS link, and JavaScript initialization
**Rationale**:
- Cleaner than hiding with CSS (reduces DOM size and complexity)
- Prevents confusion from dead code
- Easier to reintroduce later if needed (git history preserved)
- **Alternative considered**: Hide with `display: none` → Rejected (leaves unused code)

### 2. Null Check Preservation in input-handler-redesign.js
**Decision**: Keep existing null checks (`if (statsTracker) { ... }`)
**Rationale**:
- Already implemented graceful degradation pattern
- No need to remove defensive code
- Makes code more resilient to future changes
- **Alternative considered**: Remove all statsTracker references → Rejected (reduces code safety)

### 3. Order of Removal
**Decision**: Remove in this order: HTML → CSS link → JS initialization → JS calls
**Rationale**:
- HTML removal prevents UI rendering immediately
- CSS link removal after HTML (no visual impact)
- JS changes can be batched (already null-safe)
- **Alternative considered**: Remove JS first → Rejected (could cause DOM errors if HTML remains)

### 4. StatsTracker Module File
**Decision**: Leave `frontend/js/modules/stats-tracker.js` file intact
**Rationale**:
- May be used by `index.html` (original version, not redesigned)
- Separate cleanup PR can handle module deletion after verification
- Low risk to leave file (unused imports don't load in ES modules)
- **Alternative considered**: Delete file immediately → Rejected (requires checking all imports first)

## Risks / Trade-offs

**Risk**: Users who refreshed during deployment might see layout shift when stats panel disappears
→ **Mitigation**: Low impact (internal MVP, small user base). Stats panel removal is immediate and clean.

**Risk**: localStorage stats data becomes orphaned (still exists but not displayed)
→ **Mitigation**: Acceptable. localStorage data is per-browser and doesn't affect functionality. Can add cleanup script later if needed.

**Risk**: Future feature might want to re-add frontend stats
→ **Mitigation**: Git history preserves all code. Can revert this change or rebuild from scratch with backend data source.

**Trade-off**: Simpler codebase vs. Loss of instant visual feedback
→ **Accepted**: Users can still see practice data in backend (future analytics page). Focus on core practice experience.

## Migration Plan

**Deployment**: Single-step (no backend changes, frontend-only)

1. Deploy updated frontend files to server
2. Hard refresh clears cached JavaScript modules
3. Users see stats panel removed immediately

**Rollback**:
- Revert commit and redeploy frontend
- localStorage data still intact if rollback needed
- No data loss (backend database unaffected)

**Validation**:
- Load `index-redesign.html` and verify stats panel not visible
- Type practice characters and verify no console errors
- Check Network tab for no 404s on stats-panel.css
- Verify practice recording still works (check database)

## Open Questions

None - this is a straightforward removal change.
