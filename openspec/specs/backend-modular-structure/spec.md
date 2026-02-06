# Backend Modular Structure

## Purpose

This capability defines the modular architecture for Flask backend applications, organizing code into three distinct layers: routes (HTTP handling), services (business logic), and config (configuration management). This architecture promotes separation of concerns, maintainability, and testability.

**Key Benefits:**
- Clear separation between HTTP layer, business logic, and configuration
- Unidirectional dependency flow (routes → services → config)
- Easier testing and mocking at each layer
- Simplified application entry point
- Centralized configuration management

**When to Use:**
- Flask web applications requiring structured organization
- Projects transitioning from monolithic to modular architecture
- Applications where business logic needs to be testable independently of HTTP layer

## Requirements

### Requirement: Backend SHALL organize code into modular layers

The Backend code SHALL be organized into three distinct layers: routes (HTTP handling), services (business logic), and config (configuration management). Each layer SHALL have a clearly defined responsibility with minimal coupling between layers.

#### Scenario: Developer locates API endpoint code
- **WHEN** a developer needs to modify an API endpoint behavior
- **THEN** the developer SHALL find the HTTP handling logic in `routes/` directory and business logic in `services/` directory

#### Scenario: Developer adds new configuration
- **WHEN** a developer needs to add a new configuration value (e.g., file path, port)
- **THEN** the developer SHALL add it to `config.py` class and reference it from other modules

#### Scenario: Code review validates separation of concerns
- **WHEN** reviewing code for a new feature
- **THEN** HTTP request/response logic SHALL be in routes, business logic SHALL be in services, and no business logic SHALL exist in routes

### Requirement: Routes layer SHALL handle HTTP interface only

The routes layer (Flask Blueprints in `routes/`) SHALL be responsible for HTTP request parsing, response formatting, and delegating to services. Routes SHALL NOT contain business logic, data access, or complex computations.

#### Scenario: API endpoint receives HTTP request
- **WHEN** an HTTP request arrives at `/api/words/random`
- **THEN** the route handler SHALL parse the request, call the appropriate service method, and format the response as JSON

#### Scenario: Service returns error condition
- **WHEN** a service method returns `None` or error information
- **THEN** the route handler SHALL convert it to the appropriate HTTP status code (e.g., 500) and error JSON response

#### Scenario: Route does not perform data processing
- **WHEN** implementing a route handler
- **THEN** the handler SHALL NOT contain file I/O, random selection logic, or data validation - these SHALL be delegated to services

### Requirement: Services layer SHALL contain business logic

The services layer (`services/`) SHALL contain all business logic including data loading, data processing, and domain operations. Services SHALL be independent of HTTP and Flask-specific code.

#### Scenario: Service loads application data
- **WHEN** the application starts
- **THEN** `word_service.py` SHALL load `words.json` data into memory at module import time

#### Scenario: Service provides business operation
- **WHEN** a route needs to get a random word
- **THEN** the route SHALL call `word_service.get_random_word()` which returns a word dictionary or `None`

#### Scenario: Service is testable independently
- **WHEN** writing unit tests for service logic
- **THEN** the service SHALL be testable without starting Flask or making HTTP requests

#### Scenario: Service handles data errors gracefully
- **WHEN** `words.json` file is missing or contains invalid JSON
- **THEN** the service SHALL log the error and set words data to empty list, allowing the application to continue running

### Requirement: Config layer SHALL centralize configuration

All configuration values (file paths, ports, environment variables) SHALL be defined in `config.py` as a Config class. Other modules SHALL import and reference Config instead of hardcoding values.

#### Scenario: Developer modifies data file path
- **WHEN** the words data file path needs to change
- **THEN** the developer SHALL modify only `Config.WORDS_DATA_PATH` in `config.py`

#### Scenario: Environment-specific configuration
- **WHEN** running in different environments (development, production)
- **THEN** the Config class SHALL read from environment variables (e.g., `PORT`, `FLASK_ENV`) with sensible defaults

#### Scenario: No hardcoded configuration in modules
- **WHEN** reviewing routes or services code
- **THEN** there SHALL be no hardcoded file paths, ports, or configuration values - all SHALL reference `Config` class

### Requirement: Module dependencies SHALL follow unidirectional flow

Module dependencies SHALL flow in one direction: routes → services → config. There SHALL be no circular dependencies between modules.

#### Scenario: Routes import services
- **WHEN** a route module needs business logic
- **THEN** routes MAY import from services, but services SHALL NOT import from routes

#### Scenario: Services import config
- **WHEN** a service needs configuration values
- **THEN** services MAY import from config, but config SHALL NOT import from any project modules

#### Scenario: No circular imports occur
- **WHEN** the application starts
- **THEN** all modules SHALL load successfully without `ImportError` due to circular dependencies

### Requirement: API endpoints SHALL remain unchanged

All existing API endpoints, request/response formats, and HTTP behaviors SHALL remain exactly the same after refactoring. This ensures zero breaking changes for frontend clients.

#### Scenario: GET /api/words/random returns same format
- **WHEN** a client requests `GET /api/words/random`
- **THEN** the response SHALL be JSON with format `{"word": "字", "zhuyin": [...], "keys": [...]}`

#### Scenario: GET /health returns same format
- **WHEN** a client requests `GET /health`
- **THEN** the response SHALL be JSON with format `{"status": "ok", "words_loaded": 30}`

#### Scenario: Error responses remain consistent
- **WHEN** words data is unavailable and client requests `/api/words/random`
- **THEN** the response SHALL be HTTP 500 with JSON `{"error": "...", "message": "..."}`

#### Scenario: CORS configuration unchanged
- **WHEN** a browser makes cross-origin requests
- **THEN** CORS headers SHALL be present and allow the same origins as before refactoring

### Requirement: Existing tests SHALL pass without modification

All existing integration tests in `tests/backend/test_api.py` SHALL pass without any modifications to the test code, verifying API behavior is preserved.

#### Scenario: Integration test suite passes
- **WHEN** running `pytest tests/backend/test_api.py`
- **THEN** all tests SHALL pass with the same behavior as before refactoring

#### Scenario: Test coverage is maintained
- **WHEN** measuring test coverage after refactoring
- **THEN** coverage SHALL be equal to or greater than pre-refactoring coverage

### Requirement: Application entry point SHALL be simplified

The `app.py` file SHALL serve only as the application entry point, creating the Flask app and registering blueprints. It SHALL NOT contain business logic, data loading, or route definitions.

#### Scenario: app.py creates Flask application
- **WHEN** the application starts
- **THEN** `app.py` SHALL create a Flask instance, configure CORS, and register all blueprints

#### Scenario: app.py is concise
- **WHEN** reviewing `app.py`
- **THEN** the file SHALL be approximately 15-20 lines, containing only application initialization logic

#### Scenario: Blueprints are registered with correct prefixes
- **WHEN** `app.py` registers blueprints
- **THEN** `words_bp` SHALL be registered with URL prefix `/api/words` and `health_bp` with no prefix

### Requirement: Error handling SHALL be layered

Error handling SHALL be split between layers: services handle data/domain errors, routes handle HTTP errors. Each layer SHALL handle errors appropriate to its abstraction level.

#### Scenario: Service handles file not found
- **WHEN** `words.json` file does not exist
- **THEN** `word_service` SHALL catch `FileNotFoundError`, log the error, and set words data to empty list

#### Scenario: Service handles JSON parsing error
- **WHEN** `words.json` contains invalid JSON
- **THEN** `word_service` SHALL catch `JSONDecodeError`, log the error, and set words data to empty list

#### Scenario: Route handles service error response
- **WHEN** `word_service.get_random_word()` returns `None`
- **THEN** the route SHALL return HTTP 500 with appropriate error message JSON

#### Scenario: Errors are logged for debugging
- **WHEN** any error occurs during data loading or request processing
- **THEN** the error SHALL be logged with sufficient context for debugging (file path, error type, message)

### Requirement: Module initialization SHALL be predictable

Services that require initialization (e.g., loading data) SHALL perform initialization at module import time using module-level code. This ensures data is loaded once when the application starts.

#### Scenario: Word service loads data on import
- **WHEN** the application imports `word_service` module
- **THEN** the module SHALL automatically load `words.json` into module-level variable `_words_data`

#### Scenario: Data is loaded only once
- **WHEN** multiple route handlers call `word_service.get_random_word()`
- **THEN** the data SHALL be loaded only once at startup, not on every request

#### Scenario: Module initialization errors are handled
- **WHEN** data loading fails during module initialization
- **THEN** the module SHALL still load successfully (not crash) and provide error information through its API
