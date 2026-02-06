## 1. Project Setup

- [x] 1.1 Create directory structure (frontend, backend, tests)
- [x] 1.2 Create uv virtual environment for backend
- [x] 1.3 Create requirements.txt with Flask and flask-cors
- [x] 1.4 Install Python dependencies with uv

## 2. Backend - Practice Word API

- [x] 2.1 Create backend/data/words.json with 20-30 common characters
- [x] 2.2 Implement backend/app.py Flask app with CORS
- [x] 2.3 Implement GET /api/words/random endpoint
- [x] 2.4 Add error handling for missing words.json
- [x] 2.5 Test API with curl or browser

## 3. Frontend - Zhuyin Mapping Module

- [x] 3.1 Create frontend/js/modules/zhuyin-map.js
- [x] 3.2 Implement keyToZhuyin mapping (all consonants, vowels, tones)
- [x] 3.3 Implement zhuyinToKey reverse mapping
- [x] 3.4 Verify space key maps to first tone

## 4. Frontend - Virtual Keyboard Module

- [x] 4.1 Create frontend/styles/keyboard.css
- [x] 4.2 Design CSS Grid layout for keyboard rows
- [x] 4.3 Create frontend/js/modules/keyboard.js
- [x] 4.4 Implement render() function to generate keyboard HTML
- [x] 4.5 Implement highlightKey(key) function with CSS class
- [x] 4.6 Implement clearHighlight() function
- [x] 4.7 Add CSS transition for highlight effect (200ms)

## 5. Frontend - Practice Logic Module

- [x] 5.1 Create frontend/js/modules/practice.js
- [x] 5.2 Implement state object (word, zhuyin, keys, currentIndex)
- [x] 5.3 Implement fetchNextWord() to call /api/words/random
- [x] 5.4 Implement loadWord(data) to update state and display
- [x] 5.5 Implement checkInput(key) validation logic
- [x] 5.6 Handle first tone as space or auto-advance
- [x] 5.7 Update DOM to display current word

## 6. Frontend - Input Handler Module

- [x] 6.1 Create frontend/js/modules/input-handler.js
- [x] 6.2 Implement keydown event listener
- [x] 6.3 Filter non-zhuyin keys (ignore invalid keys)
- [x] 6.4 Call practice.checkInput(key) for validation
- [x] 6.5 Call keyboard.highlightKey(key) on valid input
- [x] 6.6 Trigger keyboard.clearHighlight() after 200ms
- [x] 6.7 Handle word completion and load next word

## 7. Frontend - Main Integration

- [x] 7.1 Create frontend/index.html structure
- [x] 7.2 Add practice display area (show current word)
- [x] 7.3 Add keyboard container div
- [x] 7.4 Create frontend/js/main.js
- [x] 7.5 Import all modules in main.js
- [x] 7.6 Initialize keyboard on DOMContentLoaded
- [x] 7.7 Initialize input handler
- [x] 7.8 Load first word from API

## 8. Frontend - Styling

- [x] 8.1 Create frontend/styles/main.css
- [x] 8.2 Style practice display area (large, centered text)
- [x] 8.3 Create frontend/styles/practice.css
- [x] 8.4 Add basic page layout and typography
- [x] 8.5 Style keyboard keys (size, spacing, borders)
- [x] 8.6 Add highlight state styling (background color change)

## 9. Testing - Frontend Unit Tests

- [x] 9.1 Create tests/frontend/test.html
- [x] 9.2 Write test for keyToZhuyin completeness
- [x] 9.3 Write test for keyboard.highlightKey() DOM manipulation
- [x] 9.4 Write test for practice.checkInput() validation logic
- [x] 9.5 Write test for first tone handling (space and auto-advance)

## 10. Testing - Backend Tests

- [x] 10.1 Create tests/backend/test_api.py
- [x] 10.2 Write test for /api/words/random JSON format
- [x] 10.3 Write test for zhuyin and keys array length match
- [x] 10.4 Write test for missing words.json error handling
- [x] 10.5 Run backend tests with pytest

## 11. Integration Testing

- [x] 11.1 Start Flask backend server
- [x] 11.2 Open frontend/index.html in browser
- [x] 11.3 Verify keyboard renders with all symbols
- [x] 11.4 Verify current word displays
- [x] 11.5 Press valid zhuyin key and verify highlight
- [x] 11.6 Complete a word and verify next word loads
- [x] 11.7 Test invalid key press (no highlight, no error)

## 12. Documentation

- [x] 12.1 Create README.md with setup instructions
- [x] 12.2 Document browser requirements (Chrome 61+, Firefox 60+, Safari 11+)
- [x] 12.3 Document how to run backend (uv run python backend/app.py)
- [x] 12.4 Document how to run tests
- [x] 12.5 Add example words.json format
