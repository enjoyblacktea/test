## Why

The frontend statistics panel (已練習、準確率、連續正確) is redundant now that practice data is being tracked in the PostgreSQL database. The backend provides comprehensive analytics through the practice history API, making the client-side localStorage-based stats unnecessary and potentially confusing with duplicate data sources.

## What Changes

- Remove statistics panel HTML section from `index-redesign.html` (lines 51-69)
- Remove `StatsTracker` module import and initialization from `main-redesign.js`
- Remove `updateStatsDisplay()` and `setupResetButton()` functions from `main-redesign.js`
- Remove stats tracking calls from `input-handler-redesign.js` (recordCorrectInput, recordIncorrectInput, incrementWordCount)
- Remove `stats-panel.css` stylesheet link from `index-redesign.html`
- Clean up stats-related function calls throughout the codebase

## Capabilities

### New Capabilities
<!-- No new capabilities - this is a removal change -->

### Modified Capabilities
<!-- No modified capabilities - not changing any spec requirements, just removing UI elements -->

## Impact

**Affected Files**:
- `frontend/index-redesign.html` - Remove stats panel HTML and CSS link
- `frontend/js/main-redesign.js` - Remove StatsTracker import, initialization, and related functions
- `frontend/js/modules/input-handler-redesign.js` - Remove stats tracking calls (already has null checks, so graceful degradation)

**No Breaking Changes**: The backend API and database continue to track all practice data. Users can still view their complete practice history through the backend API (future feature).

**User Experience**: Cleaner, simpler interface focused on practice. Historical data remains available in the database for future analytics features.
