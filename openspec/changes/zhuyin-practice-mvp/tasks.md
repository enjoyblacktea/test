## 1. Project Setup

- [ ] 1.1 Create directory structure (frontend, backend, tests)
- [ ] 1.2 Create uv virtual environment for backend
- [ ] 1.3 Create requirements.txt with Flask and flask-cors
- [ ] 1.4 Install Python dependencies with uv

## 2. Backend - Practice Word API

- [ ] 2.1 Create backend/data/words.json with 20-30 common characters
- [ ] 2.2 Implement backend/app.py Flask app with CORS
- [ ] 2.3 Implement GET /api/words/random endpoint
- [ ] 2.4 Add error handling for missing words.json
- [ ] 2.5 Test API with curl or browser

## 3. Frontend - Zhuyin Mapping Module

- [ ] 3.1 Create frontend/js/modules/zhuyin-map.js
- [ ] 3.2 Implement keyToZhuyin mapping (all consonants, vowels, tones)
- [ ] 3.3 Implement zhuyinToKey reverse mapping
- [ ] 3.4 Verify space key maps to first tone

## 4. Frontend - Virtual Keyboard Module

- [ ] 4.1 Create frontend/styles/keyboard.css
- [ ] 4.2 Design CSS Grid layout for keyboard rows
- [ ] 4.3 Create frontend/js/modules/keyboard.js
- [ ] 4.4 Implement render() function to generate keyboard HTML
- [ ] 4.5 Implement highlightKey(key) function with CSS class
- [ ] 4.6 Implement clearHighlight() function
- [ ] 4.7 Add CSS transition for highlight effect (200ms)

## 5. Frontend - Practice Logic Module

- [ ] 5.1 Create frontend/js/modules/practice.js
- [ ] 5.2 Implement state object (word, zhuyin, keys, currentIndex)
- [ ] 5.3 Implement fetchNextWord() to call /api/words/random
- [ ] 5.4 Implement loadWord(data) to update state and display
- [ ] 5.5 Implement checkInput(key) validation logic
- [ ] 5.6 Handle first tone as space or auto-advance
- [ ] 5.7 Update DOM to display current word

## 6. Frontend - Input Handler Module

- [ ] 6.1 Create frontend/js/modules/input-handler.js
- [ ] 6.2 Implement keydown event listener
- [ ] 6.3 Filter non-zhuyin keys (ignore invalid keys)
- [ ] 6.4 Call practice.checkInput(key) for validation
- [ ] 6.5 Call keyboard.highlightKey(key) on valid input
- [ ] 6.6 Trigger keyboard.clearHighlight() after 200ms
- [ ] 6.7 Handle word completion and load next word

## 7. Frontend - Main Integration

- [ ] 7.1 Create frontend/index.html structure
- [ ] 7.2 Add practice display area (show current word)
- [ ] 7.3 Add keyboard container div
- [ ] 7.4 Create frontend/js/main.js
- [ ] 7.5 Import all modules in main.js
- [ ] 7.6 Initialize keyboard on DOMContentLoaded
- [ ] 7.7 Initialize input handler
- [ ] 7.8 Load first word from API

## 8. Frontend - Styling

- [ ] 8.1 Create frontend/styles/main.css
- [ ] 8.2 Style practice display area (large, centered text)
- [ ] 8.3 Create frontend/styles/practice.css
- [ ] 8.4 Add basic page layout and typography
- [ ] 8.5 Style keyboard keys (size, spacing, borders)
- [ ] 8.6 Add highlight state styling (background color change)

## 9. Testing - Frontend Unit Tests

- [ ] 9.1 Create tests/frontend/test.html
- [ ] 9.2 Write test for keyToZhuyin completeness
- [ ] 9.3 Write test for keyboard.highlightKey() DOM manipulation
- [ ] 9.4 Write test for practice.checkInput() validation logic
- [ ] 9.5 Write test for first tone handling (space and auto-advance)

## 10. Testing - Backend Tests

- [ ] 10.1 Create tests/backend/test_api.py
- [ ] 10.2 Write test for /api/words/random JSON format
- [ ] 10.3 Write test for zhuyin and keys array length match
- [ ] 10.4 Write test for missing words.json error handling
- [ ] 10.5 Run backend tests with pytest

## 11. Integration Testing

- [ ] 11.1 Start Flask backend server
- [ ] 11.2 Open frontend/index.html in browser
- [ ] 11.3 Verify keyboard renders with all symbols
- [ ] 11.4 Verify current word displays
- [ ] 11.5 Press valid zhuyin key and verify highlight
- [ ] 11.6 Complete a word and verify next word loads
- [ ] 11.7 Test invalid key press (no highlight, no error)

## 12. Documentation

- [ ] 12.1 Create README.md with setup instructions
- [ ] 12.2 Document browser requirements (Chrome 61+, Firefox 60+, Safari 11+)
- [ ] 12.3 Document how to run backend (uv run python backend/app.py)
- [ ] 12.4 Document how to run tests
- [ ] 12.5 Add example words.json format
