## 1. Preparation and Setup

- [x] 1.1 Create git branch `refactor/backend-modular-structure`
- [x] 1.2 Run existing tests to establish baseline (`pytest tests/backend/ -v`)
- [x] 1.3 Create directory structure: `mkdir -p backend/routes backend/services`
- [x] 1.4 Create `__init__.py` files: `touch backend/routes/__init__.py backend/services/__init__.py`

## 2. Create Configuration Layer

- [x] 2.1 Create `backend/config.py` with Config class
- [x] 2.2 Define `BASE_DIR` using `os.path.dirname(os.path.abspath(__file__))`
- [x] 2.3 Define `WORDS_DATA_PATH` joining BASE_DIR with 'data/words.json'
- [x] 2.4 Define `PORT` reading from environment variable with default 5000
- [x] 2.5 Define `DEBUG` based on FLASK_ENV environment variable
- [x] 2.6 Add Config class docstring explaining usage

## 3. Create Service Layer

- [x] 3.1 Create `backend/services/word_service.py`
- [x] 3.2 Import necessary modules (json, random, os) and Config
- [x] 3.3 Define module-level variable `_words_data = []`
- [x] 3.4 Implement `_load_words()` private function to load words.json
- [x] 3.5 Add try/except for FileNotFoundError in `_load_words()`
- [x] 3.6 Add try/except for JSONDecodeError in `_load_words()`
- [x] 3.7 Add error logging with print statements in exception handlers
- [x] 3.8 Call `_load_words()` at module level to initialize data
- [x] 3.9 Implement `get_random_word()` function returning random word or None
- [x] 3.10 Implement `get_words_count()` function returning len(_words_data)
- [x] 3.11 Add module and function docstrings

## 4. Create Routes Layer - Words Blueprint

- [x] 4.1 Create `backend/routes/words.py`
- [x] 4.2 Import Flask, Blueprint, jsonify
- [x] 4.3 Import word_service
- [x] 4.4 Create Blueprint: `words_bp = Blueprint('words', __name__)`
- [x] 4.5 Define route `@words_bp.route('/random', methods=['GET'])`
- [x] 4.6 Implement `get_random_word()` handler calling word_service
- [x] 4.7 Handle None case returning 500 with error JSON
- [x] 4.8 Handle success case returning 200 with word JSON
- [x] 4.9 Ensure error JSON format matches existing: `{"error": "...", "message": "..."}`
- [x] 4.10 Add route handler docstring

## 5. Create Routes Layer - Health Blueprint

- [x] 5.1 Create `backend/routes/health.py`
- [x] 5.2 Import Flask, Blueprint, jsonify
- [x] 5.3 Import word_service
- [x] 5.4 Create Blueprint: `health_bp = Blueprint('health', __name__)`
- [x] 5.5 Define route `@health_bp.route('/health', methods='/GET'])`
- [x] 5.6 Implement `health()` handler calling word_service.get_words_count()
- [x] 5.7 Return JSON: `{"status": "ok", "words_loaded": count}`
- [x] 5.8 Add route handler docstring

## 6. Update Application Entry Point

- [x] 6.1 Backup current `backend/app.py` (copy to app.py.backup)
- [x] 6.2 Rewrite `backend/app.py` to import Flask, CORS
- [x] 6.3 Import blueprints: `from routes.words import words_bp`
- [x] 6.4 Import blueprints: `from routes.health import health_bp`
- [x] 6.5 Create Flask app: `app = Flask(__name__)`
- [x] 6.6 Configure CORS: `CORS(app)`
- [x] 6.7 Register words blueprint with prefix: `app.register_blueprint(words_bp, url_prefix='/api/words')`
- [x] 6.8 Register health blueprint: `app.register_blueprint(health_bp)`
- [x] 6.9 Add `if __name__ == '__main__':` block with app.run()
- [x] 6.10 Verify app.py is approximately 15-20 lines
- [x] 6.11 Remove app.py.backup after verification

## 7. Testing and Verification

- [x] 7.1 Run existing integration tests: `pytest tests/backend/test_api.py -v`
- [x] 7.2 Verify all tests pass without modification
- [x] 7.3 Start application: `cd backend && python app.py`
- [x] 7.4 Test GET /api/words/random endpoint manually with curl
- [x] 7.5 Test GET /health endpoint manually with curl
- [x] 7.6 Verify response formats match exactly with pre-refactor format
- [x] 7.7 Test error scenario: rename words.json temporarily
- [x] 7.8 Verify 500 error response for /api/words/random
- [x] 7.9 Verify health endpoint shows words_loaded: 0
- [x] 7.10 Restore words.json and verify normal operation
- [x] 7.11 Check for any import errors or circular dependencies

## 8. Code Quality and Documentation

- [x] 8.1 Add docstrings to all modules (config.py, word_service.py, routes/*.py)
- [x] 8.2 Add docstrings to all functions
- [x] 8.3 Review code for consistent style (following existing conventions)
- [x] 8.4 Verify no hardcoded paths or configuration values outside config.py
- [x] 8.5 Verify imports are organized (stdlib, third-party, local)

## 9. Optional: Add Unit Tests

- [ ] 9.1 Create `tests/backend/test_word_service.py` (optional but recommended)
- [ ] 9.2 Test word_service.get_random_word() returns valid word
- [ ] 9.3 Test word_service.get_random_word() returns None when no data
- [ ] 9.4 Test word_service.get_words_count() returns correct count
- [ ] 9.5 Mock file operations to test error handling
- [ ] 9.6 Run unit tests: `pytest tests/backend/test_word_service.py -v`

## 10. Documentation

- [x] 10.1 Update README.md with new backend architecture section
- [x] 10.2 Add architecture diagram showing routes → services → config
- [x] 10.3 Document module responsibilities in README.md
- [x] 10.4 Add "Development" section explaining how to add new endpoints
- [x] 10.5 Document configuration via environment variables

## 11. Git Commit

- [x] 11.1 Review all changes with `git status` and `git diff`
- [x] 11.2 Stage changes: `git add backend/`
- [x] 11.3 Stage documentation: `git add README.md`
- [x] 11.4 Commit with message: "Refactor: Modularize backend structure into routes/services/config"
- [x] 11.5 Add co-author line in commit message
- [x] 11.6 Verify commit with `git log -1 --stat`

## 12. Final Verification

- [x] 12.1 Run full test suite: `pytest tests/ -v`
- [x] 12.2 Verify test coverage: `pytest tests/ --cov=backend`
- [x] 12.3 Check for any TODO or FIXME comments that need addressing
- [x] 12.4 Verify no debugging print statements were left in code
- [x] 12.5 Confirm API endpoints work correctly: test with frontend if available
- [x] 12.6 Review checklist: all tasks completed
