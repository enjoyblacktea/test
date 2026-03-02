## Context

The current zhuyin practice application uses:
- **Frontend-only authentication**: Hardcoded credentials (user/1234) stored in localStorage
- **Static JSON data**: 30 practice characters in `backend/data/words.json`
- **No persistence**: Practice history is lost on page reload
- **No analytics capability**: Cannot track user progress or identify learning patterns

This architecture limits the application's educational value. To enable data-driven insights and proper user management, we need:
1. Backend authentication with secure credential storage
2. Database persistence for practice history
3. API infrastructure for data recording and retrieval

**Constraints**:
- Maintain current user experience (no interruption during practice)
- Minimize frontend disruption (keep existing modules where possible)
- Support future expansion (multi-input methods, keystroke analytics)
- Development timeline: ~2 weeks for Phase 1

## Goals / Non-Goals

**Goals:**
- Replace frontend-only auth with JWT-based backend authentication
- Store practice data in PostgreSQL for analysis capability
- Implement Phase 1 schema: users, characters, typing_attempts (3 tables)
- Record practice attempts without blocking user flow
- Migrate character data from JSON to database
- Support future multi-input method expansion through schema design

**Non-Goals:**
- Phase 2 keystroke_events table (deferred to future work)
- Statistics/analytics API endpoints (analysis done separately on raw data)
- Actual multi-input method implementation (only architectural reservation)
- Mobile app support or responsive design changes
- Real-time leaderboards or social features

## Decisions

### 1. PostgreSQL as Database

**Decision**: Use PostgreSQL 12+ for persistent storage.

**Rationale**:
- Mature, ACID-compliant relational database
- Excellent Python ecosystem support (psycopg2, SQLAlchemy)
- Strong data integrity with foreign key constraints
- Good indexing performance for query patterns (random character selection, user history)
- Team familiarity with SQL

**Alternatives Considered**:
- SQLite: Too limited for multi-user production use, no connection pooling
- MongoDB: Overkill for structured relational data, loses referential integrity
- MySQL: Similar capability to PostgreSQL, but PostgreSQL preferred for JSON support in future

### 2. JWT-Based Authentication

**Decision**: Use JWT (JSON Web Tokens) with bcrypt password hashing.

**Configuration**:
- Access token expiry: 1 hour
- Refresh token expiry: 7 days
- Algorithm: HS256 (HMAC with SHA-256)
- Password hashing: bcrypt with default work factor (12 rounds)

**Rationale**:
- Stateless authentication (no server-side session storage)
- Industry standard, well-understood security model
- Easy to implement in Flask with PyJWT library
- Supports distributed/scaled deployments (no session affinity needed)
- Refresh token pattern allows secure long-term sessions

**Alternatives Considered**:
- Session-based auth: Requires session storage, complicates scaling
- OAuth2: Overkill for simple username/password auth, no external identity providers needed
- Basic Auth: Insecure for production, credentials sent with every request

### 3. Progressive Implementation (Phase 1: 3 Tables)

**Decision**: Implement in two phases. Phase 1 includes users, characters, typing_attempts. Phase 2 (future) adds keystroke_events.

**Rationale**:
- Reduces initial implementation risk and complexity
- Delivers value faster (~2 weeks vs ~4 weeks)
- Allows validation of architecture before investing in granular keystroke tracking
- Most analytics value comes from attempt-level data (correctness, duration)
- Keystroke-level data useful for advanced analysis, can be added later

**Phase 1 Deliverables**:
- User authentication and registration
- Character database with zhuyin mappings
- Practice attempt recording (per-character correctness and timing)

**Phase 2 Scope (Future)**:
- Keystroke_events table for granular per-key tracking
- Advanced analytics (error patterns, typing rhythm)

### 4. Backend Key→Zhuyin Mapping

**Decision**: Calculate zhuyin arrays and key sequences in backend service layer, not stored in database.

**Rationale**:
- Database stores only: character text, input_code string (e.g., "j i 3"), input_method type
- Backend service converts input_code to arrays when serving random character API
- Keeps schema clean and normalized (no redundant JSON columns)
- Single source of truth: zhuyin-map.js logic moved to Python service
- Easier to maintain mapping logic in one place

**Example Flow**:
```
Database: {character: "字", input_code: "j 3", input_method: "bopomofo"}
   ↓
Service: Parse "j 3" → zhuyin: ["ㄐ", "ˋ"], keys: ["j", "3"]
   ↓
API Response: {word: "字", zhuyin: ["ㄐ", "ˋ"], keys: ["j", "3"]}
```

**Alternatives Considered**:
- Store zhuyin/keys as JSON in database: Redundant, harder to maintain consistency
- Client-side calculation only: Requires duplicating mapping logic in frontend

### 5. Non-Blocking Practice Recording

**Decision**: Practice attempt recording is asynchronous and does not block user flow.

**Rationale**:
- User experience priority: Don't interrupt practice with network delays
- Frontend fires recording request and immediately loads next character
- Recording failures don't crash the practice session
- Acceptable data loss risk for MVP (user can retry character later)

**Implementation**:
- Frontend calls POST /api/attempts with started_at, ended_at, is_correct
- API responds quickly (< 100ms) with 202 Accepted
- Any recording errors logged server-side, not shown to user

**Alternatives Considered**:
- Synchronous blocking: Bad UX, network latency affects practice flow
- Client-side buffering with batch upload: More complex, risks losing buffered data

### 6. Three-Layer Backend Architecture

**Decision**: Organize backend as Routes → Services → Database.

**Layers**:
- **Routes** (`backend/routes/`): HTTP request/response handling, input validation, JWT middleware
- **Services** (`backend/services/`): Business logic, data transformations, orchestration
- **Database** (`backend/models/` or raw SQL): Data access, queries, transactions

**Rationale**:
- Separation of concerns: easier to test and maintain
- Routes stay thin (no business logic)
- Services can be reused across different routes
- Clear dependency flow: Routes → Services → Database (no circular dependencies)

**Example**:
```
POST /api/attempts (Route)
   ↓
attempt_service.record_attempt() (Service)
   ↓
INSERT INTO typing_attempts (Database)
```

### 7. Database Schema with Future Multi-Input Support

**Decision**: Design schema to support multiple input methods, but implement only bopomofo initially.

**Schema Design**:
- `characters` table has `input_method` column (VARCHAR)
- Unique constraint: (character, input_method) - same character can have different input codes per method
- Indexes on `input_method` for efficient filtering

**Rationale**:
- Extensible architecture without over-engineering current implementation
- When adding pinyin/cangjie later, just insert new rows with different input_method
- No schema migration needed for multi-input support
- Query API supports filtering: GET /api/characters/random?input_method=bopomofo

**Current Scope**:
- Only "bopomofo" method implemented
- API defaults to bopomofo if input_method not specified
- Frontend remains single-input-method for now

### 8. Connection Pooling for Database Efficiency

**Decision**: Use connection pooling with psycopg2 or SQLAlchemy.

**Configuration** (recommended starting point):
- Pool size: 5-10 connections
- Max overflow: 10 additional connections
- Recycle time: 3600 seconds (1 hour)

**Rationale**:
- Avoid connection overhead for every API request
- Better performance under concurrent load
- Prevent connection exhaustion
- Standard practice for production Flask + PostgreSQL

## Risks / Trade-offs

### 1. Database Connection Failures
**Risk**: Database downtime breaks entire application (frontend can't load characters).

**Mitigation**:
- Connection pooling with retry logic (3 retries with exponential backoff)
- Health check endpoint (GET /health) that tests database connectivity
- Graceful degradation: Cache last N characters in memory for temporary fallback
- Monitor database health and set up alerts

### 2. JWT Token Security
**Risk**: Stolen access tokens allow unauthorized access until expiry.

**Mitigation**:
- Short access token lifetime (1 hour) limits exposure window
- Refresh tokens allow re-authentication without re-entering password
- HTTPS-only deployment (tokens never transmitted over plaintext)
- Tokens stored in localStorage (XSS risk exists but acceptable for MVP)
- Future: Consider httpOnly cookies for refresh tokens

### 3. Performance of Random Character Selection
**Risk**: Random character query may be slow as database grows.

**Mitigation**:
- Index on `input_method` column for filtering
- Initial dataset small (30 characters), performance not critical for MVP
- Future: If dataset grows (1000+ characters), use optimized random sampling:
  - Pre-compute random ordering on application startup
  - Use TABLESAMPLE for large datasets
  - Consider weighted random (favor characters user struggles with)

### 4. Migration Complexity
**Risk**: Moving from static JSON to database requires careful data migration and testing.

**Mitigation**:
- Progressive implementation reduces scope (3 tables vs 4)
- Keep `words.json` as reference during migration
- Comprehensive testing before removing JSON dependency
- Database seed script (`init_db.sql`) with all 30 characters for repeatability

### 5. Non-Blocking Recording Data Loss
**Risk**: Asynchronous practice recording may fail silently, losing user progress data.

**Mitigation**:
- Server-side logging of all recording failures for debugging
- 202 Accepted response confirms server received request
- Future: Add client-side retry queue for failed requests
- Acceptable trade-off: Data loss risk < UX degradation from blocking

### 6. Password Security
**Risk**: Weak passwords or compromised database exposes user credentials.

**Mitigation**:
- Bcrypt hashing with work factor 12 (industry standard)
- No password complexity requirements in MVP (UX priority)
- Database access restricted to application service account only
- Future: Add password strength requirements, optional 2FA

## Migration Plan

### Phase 1: Setup and Authentication (Week 1)

1. **Database Setup**:
   - Install PostgreSQL, create database `zhuyin_practice`
   - Run `backend/migrations/init_db.sql` to create schema
   - Seed `characters` table with data from `words.json`
   - Verify schema with test queries

2. **Backend Authentication**:
   - Install dependencies: PyJWT, bcrypt, psycopg2-binary
   - Implement `backend/config.py` with database and JWT config
   - Create User model and auth_service
   - Implement auth routes: POST /api/auth/register, /api/auth/login, /api/auth/refresh
   - Add JWT middleware for protected routes
   - Test with Postman/curl

3. **Frontend Authentication Integration**:
   - Create `frontend/login.html` page
   - Implement `frontend/js/modules/api.js` wrapper with JWT token handling
   - Replace `auth.js` with `auth-backend.js` that calls real API
   - Update index.html to redirect to login if not authenticated
   - Test registration and login flows

### Phase 2: Practice Recording (Week 2)

4. **Database-Backed Character API**:
   - Modify `word_service.py` to query `characters` table
   - Update GET /api/words/random to return database characters
   - Add input_method filtering support
   - Test API returns correct format (word, zhuyin, keys)

5. **Practice Recording API**:
   - Create TypingAttempt model
   - Implement attempt_service.record_attempt()
   - Add routes: POST /api/attempts, GET /api/attempts?user_id=X
   - Add pagination for history queries
   - Test recording and retrieval

6. **Frontend Practice Integration**:
   - Modify `practice.js` to call POST /api/attempts after each character
   - Implement non-blocking recording (don't wait for response)
   - Add error handling (log failures, don't crash)
   - Test practice flow end-to-end

### Rollback Strategy

- **Keep `words.json` during migration**: Frontend can fallback if database fails
- **Feature flag**: Environment variable `USE_DATABASE=true/false` to toggle data source
- **Database rollback**: Drop database and remove dependency installations
- **Frontend rollback**: Git revert to previous auth.js and static API version

### Deployment Checklist

- [ ] PostgreSQL instance provisioned and accessible
- [ ] Database initialized with `init_db.sql`
- [ ] Environment variables set: DATABASE_URL, JWT_SECRET_KEY
- [ ] Backend dependencies installed (`uv sync`)
- [ ] Health check endpoint returning 200
- [ ] Frontend login page accessible
- [ ] End-to-end test: Register → Login → Practice → History
- [ ] Monitor logs for recording failures

## Open Questions

1. **Database Hosting**: Where will PostgreSQL be deployed? (Local dev vs cloud service like Heroku Postgres, AWS RDS, or DigitalOcean)
   - Recommendation: Start with local PostgreSQL for development, evaluate cloud options for production

2. **Character Dataset Expansion**: Current plan has 30 characters. What's the target dataset size?
   - Affects indexing strategy and random selection algorithm

3. **User Management**: Do we need email verification, password reset, or account deletion?
   - Not in MVP scope, but may be needed for production

4. **Data Retention Policy**: How long should practice history be kept?
   - No limit for now, but consider archival strategy if database grows large

5. **Analytics Access**: Who will analyze the practice data, and how?
   - Clarify whether we need read-only database access for data scientists or export functionality
