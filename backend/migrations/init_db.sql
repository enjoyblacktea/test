-- Database initialization script for Zhuyin Practice application
-- This script is idempotent and can be run multiple times safely

-- ============================================================================
-- TABLES
-- ============================================================================

-- Users table: Store user accounts with hashed passwords
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Characters table: Store Chinese characters with input method mappings
CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    character VARCHAR(10) NOT NULL,
    input_code VARCHAR(50) NOT NULL,
    input_method VARCHAR(20) NOT NULL DEFAULT 'bopomofo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(character, input_method)
);

-- Typing attempts table: Store user practice history
CREATE TABLE IF NOT EXISTS typing_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ended_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_correct BOOLEAN NOT NULL,
    duration_ms INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (ended_at - started_at)) * 1000
    ) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_character
        FOREIGN KEY (character_id)
        REFERENCES characters(id)
        ON DELETE RESTRICT
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Index for fast username lookups during login
CREATE INDEX IF NOT EXISTS idx_username ON users(username);

-- Index for filtering characters by input method
CREATE INDEX IF NOT EXISTS idx_input_method ON characters(input_method);

-- Index for querying user's practice history
CREATE INDEX IF NOT EXISTS idx_user_attempts ON typing_attempts(user_id);

-- Index for analyzing specific character attempts
CREATE INDEX IF NOT EXISTS idx_character_attempts ON typing_attempts(character_id);

-- Composite index for filtering user attempts by correctness
CREATE INDEX IF NOT EXISTS idx_user_correct ON typing_attempts(user_id, is_correct);

-- ============================================================================
-- SEED DATA
-- ============================================================================

-- Insert 31 common Chinese characters with bopomofo input codes
-- Format: character, input_code (space-separated keyboard keys), input_method
INSERT INTO characters (character, input_code, input_method)
VALUES
    ('你', 's u 3', 'bopomofo'),
    ('好', 'c l 3', 'bopomofo'),
    ('我', 'j i 3', 'bopomofo'),
    ('是', 'g 4', 'bopomofo'),
    ('的', '2 k 7', 'bopomofo'),
    ('了', 'x k 7', 'bopomofo'),
    ('人', 'b p 6', 'bopomofo'),
    ('在', 'y 9 4', 'bopomofo'),
    ('有', 'u . 3', 'bopomofo'),
    ('他', 'w 8  ', 'bopomofo'),
    ('這', '5 k 4', 'bopomofo'),
    ('中', '5 j /  ', 'bopomofo'),
    ('大', '2 8 4', 'bopomofo'),
    ('來', 'x 9 6', 'bopomofo'),
    ('上', 'g ; 4', 'bopomofo'),
    ('國', 'e j i 6', 'bopomofo'),
    ('個', 'e k 7', 'bopomofo'),
    ('到', '2 l 4', 'bopomofo'),
    ('說', 'g j i  ', 'bopomofo'),
    ('們', 'a p 7', 'bopomofo'),
    ('為', 'j o 4', 'bopomofo'),
    ('子', 'y 3', 'bopomofo'),
    ('學', 'v m , 6', 'bopomofo'),
    ('生', 'g /  ', 'bopomofo'),
    ('可', 'd k 3', 'bopomofo'),
    ('以', 'u 3', 'bopomofo'),
    ('會', 'c j o 4', 'bopomofo'),
    ('家', 'r u 8  ', 'bopomofo'),
    ('天', 'w u 0  ', 'bopomofo'),
    ('年', 's u 0 6', 'bopomofo')
ON CONFLICT (character, input_method) DO NOTHING;

-- ============================================================================
-- VERIFICATION QUERIES (commented out - uncomment to verify after running)
-- ============================================================================

-- SELECT COUNT(*) AS user_count FROM users;
-- SELECT COUNT(*) AS character_count FROM characters;
-- SELECT COUNT(*) AS attempt_count FROM typing_attempts;
-- SELECT * FROM pg_indexes WHERE tablename IN ('users', 'characters', 'typing_attempts');
