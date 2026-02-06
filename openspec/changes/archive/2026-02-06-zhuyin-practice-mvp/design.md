## Context

This is a minimal viable product (MVP) for a zhuyin (bopomofo) input practice website. The target users are people familiar with other input methods (pinyin, cangjie) who want to learn zhuyin. The system needs to be testable at every level - each module should be independently verifiable.

**Current State:** New project, no existing codebase.

**Constraints:**
- Must use Vanilla JS + HTML + CSS for frontend (no frameworks)
- Must use Python Flask for backend with uv virtual environment
- Must prioritize testability - each module must be independently testable
- Must be minimal - only core practice functionality

## Goals / Non-Goals

**Goals:**
- Create a working practice flow: see Chinese character → type zhuyin → get next word
- Display virtual keyboard showing zhuyin layout
- Provide visual feedback when keys are pressed
- Maintain clean separation between modules for independent testing
- Establish foundation for future enhancements

**Non-Goals:**
- Statistics tracking (speed, accuracy) - future phase
- Error correction hints or guidance - future phase
- Multiple difficulty levels - future phase
- User accounts or progress persistence - future phase
- Mobile responsiveness - desktop focus for MVP

## Decisions

### Decision 1: ES6 Modules for Frontend Organization

**Chosen:** Organize frontend as ES6 modules (keyboard.js, input-handler.js, practice.js, zhuyin-map.js)

**Rationale:** 
- ES6 modules provide clean separation without build tools
- Each module can be tested independently in test.html
- Browser support is universal for modern browsers
- Easier to reason about dependencies

**Alternatives Considered:**
- Single monolithic JS file → harder to test individual components
- RequireJS/AMD → unnecessary complexity for this scale
- Build tool with bundling → violates "no framework" constraint

### Decision 2: Zhuyin Mapping as Shared Data Module

**Chosen:** Create zhuyin-map.js as a data-only module exporting key-to-zhuyin mappings

**Rationale:**
- Single source of truth for keyboard layout
- Used by keyboard display, input validation, and API
- Easy to test independently
- Can be imported by both frontend and backend tests

**Alternatives Considered:**
- Duplicate mapping in each module → violates DRY, error-prone
- Fetch from API → unnecessary latency for static data
- Hardcode in HTML → not reusable, not testable

### Decision 3: Frontend-Only Validation

**Chosen:** Validation logic lives in frontend (input-handler.js), backend only serves data

**Rationale:**
- Immediate feedback without network latency
- Backend remains simple (stateless data serving)
- Validation logic is deterministic and testable in browser
- For MVP, no need for server-side validation

**Alternatives Considered:**
- Server validates each keystroke → too much latency, poor UX
- Hybrid (frontend + server confirmation) → unnecessary complexity for MVP

### Decision 4: Static JSON Data File

**Chosen:** Store practice words in backend/data/words.json with pre-computed zhuyin and key arrays

**Rationale:**
- Simple to create and maintain
- Fast to load at startup
- Easy to test with sample data
- No database overhead for MVP

**Alternatives Considered:**
- Dynamic zhuyin conversion → requires zhuyin library, adds complexity
- SQLite database → overkill for static word list
- Fetch from external API → network dependency, availability concerns

### Decision 5: Flask with CORS for API

**Chosen:** Flask with flask-cors, serving JSON from /api/words/random endpoint

**Rationale:**
- Flask is lightweight and simple for MVP
- flask-cors handles cross-origin requests cleanly
- JSON API is easy to test with curl or browser
- Stateless design (no sessions, no database)

**Alternatives Considered:**
- FastAPI → more modern but adds learning curve, unnecessary for simple endpoint
- Serve static JSON files → doesn't allow randomization logic
- Frontend-only with imported data → violates separation of concerns

### Decision 6: CSS-Only Keyboard Layout

**Chosen:** Use CSS Grid to layout virtual keyboard, CSS classes for highlighting

**Rationale:**
- No SVG or canvas complexity
- Straightforward to style and maintain
- CSS transitions provide smooth highlight effects
- Easy to inspect and test in browser DevTools

**Alternatives Considered:**
- Canvas drawing → harder to debug, not semantic
- SVG → unnecessary complexity for rectangular keys
- Absolute positioning → harder to maintain, responsive issues

## Risks / Trade-offs

**[Risk] First tone handling is ambiguous** → Mitigation: Specs define both spacebar and auto-advance behavior; input-handler.js implements both paths with clear comments

**[Risk] ES6 modules don't work in older browsers** → Mitigation: Accept this limitation for MVP; document modern browser requirement (Chrome 61+, Firefox 60+, Safari 11+)

**[Risk] No build step means no minification or optimization** → Mitigation: For MVP scale (4-5 small JS files), performance impact is negligible; can add build step later if needed

**[Risk] Frontend-only validation could be bypassed** → Mitigation: Acceptable for MVP since there's no competitive element or data persistence; backend validation can be added later

**[Risk] Static word list limits variety** → Mitigation: Start with 20-30 common characters; adding more is just editing words.json; sufficient for MVP validation

**[Trade-off] No error feedback on wrong input** → Conscious choice for MVP to reduce scope; specs explicitly state "system does not show any error feedback" for invalid keys

## Architecture

```
┌─────────────────────────────────────┐
│         Frontend (Browser)          │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      index.html              │  │
│  │  ┌────────────────────────┐  │  │
│  │  │  Virtual Keyboard      │  │  │
│  │  │  (keyboard.js)         │  │  │
│  │  └────────────────────────┘  │  │
│  │  ┌────────────────────────┐  │  │
│  │  │  Practice Display      │  │  │
│  │  │  (shows current word)  │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
│                                     │
│  JS Modules:                        │
│  • zhuyin-map.js (data)             │
│  • keyboard.js (render & highlight) │
│  • input-handler.js (validation)    │
│  • practice.js (state & API calls)  │
│  • main.js (initialization)         │
│                                     │
└─────────────────────────────────────┘
              │
              │ HTTP GET /api/words/random
              ▼
┌─────────────────────────────────────┐
│      Backend (Flask + uv)           │
│                                     │
│  app.py                             │
│   └─ /api/words/random              │
│       └─ loads backend/data/words.json│
│       └─ returns random word        │
│                                     │
└─────────────────────────────────────┘
```

## Module Responsibilities

**frontend/js/modules/zhuyin-map.js**
- Export `keyToZhuyin` object mapping keyboard keys to zhuyin symbols
- Export `zhuyinToKey` reverse mapping (for testing)
- No dependencies

**frontend/js/modules/keyboard.js**
- Render virtual keyboard on page load
- Expose `highlightKey(key)` to highlight a key
- Expose `clearHighlight()` to remove highlight
- Depends on: zhuyin-map.js

**frontend/js/modules/input-handler.js**
- Listen for keydown events
- Validate input against current expected zhuyin sequence
- Call keyboard.highlightKey() on valid input
- Notify practice.js when word is complete
- Depends on: keyboard.js, zhuyin-map.js

**frontend/js/modules/practice.js**
- Maintain current word state (word, zhuyin, keys, currentIndex)
- Fetch next word from API
- Expose `checkInput(key)` for input-handler to call
- Update display when word changes
- Depends on: none (is called by input-handler)

**frontend/js/main.js**
- Initialize all modules on DOMContentLoaded
- Load first word
- Wire up event listeners
- Depends on: all modules

**backend/app.py**
- Flask app with CORS enabled
- Route `/api/words/random` returns random word from words.json
- Load words.json at startup, error if missing
- No state (stateless API)

**backend/data/words.json**
- JSON array of objects: `[{"word": "你", "zhuyin": ["ㄋ","ㄧ","ˇ"], "keys": ["s","u","3"]}]`
- Start with 20-30 common single characters

## Testing Strategy

**Frontend Unit Tests (tests/frontend/test.html)**
- Test zhuyin-map.js: verify key mappings are complete and correct
- Test keyboard.js: verify highlightKey/clearHighlight manipulate DOM correctly
- Test input-handler.js: mock keyboard events, verify validation logic
- Test practice.js: mock API responses, verify state transitions

**Backend Tests (tests/backend/test_api.py)**
- Test /api/words/random returns valid JSON format
- Test words.json loads correctly
- Test error handling for missing words.json

**Integration Test**
- Load index.html in browser
- Verify keyboard displays
- Press keys and verify highlighting
- Complete a word and verify next word loads

## Open Questions

None - all decisions made for MVP scope.
