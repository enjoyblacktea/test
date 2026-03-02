# Specs Not Applicable

This change does not require capability specifications because:

1. **No New Capabilities**: This is a removal change - no new features or capabilities are being introduced.

2. **No Modified Capabilities**: No existing capability specifications are being changed. The change only removes UI elements and related code without affecting:
   - Backend API contracts
   - Database schema
   - User authentication flow
   - Practice recording functionality
   - Any other specified system behavior

3. **Pure Implementation Change**: The removal of the frontend statistics panel is purely an implementation detail that doesn't change any externally-visible system requirements or capabilities.

## What's Being Removed

The frontend statistics panel (已練習、準確率、連續正確) displayed:
- Practice word count
- Accuracy percentage
- Correct streak count

This data was stored in browser localStorage via the `StatsTracker` module. Since all practice data is now persisted in the PostgreSQL database, the frontend stats are redundant.

## Impact on Specifications

**None**. All existing capability specifications remain valid:
- Practice word display and input validation continues to work
- Backend practice recording continues to work
- User authentication continues to work
- All API endpoints remain unchanged

The removal only affects the frontend UI presentation layer, which is not specified at the capability level.

## Testing Approach

Testing will verify:
- Stats panel HTML is removed from the DOM
- No JavaScript console errors occur
- Practice recording still functions correctly
- No broken references to removed code

See `tasks.md` for the implementation checklist.
