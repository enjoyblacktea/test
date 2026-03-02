"""
Backend API Tests
Tests for Flask API endpoints with database backend

Requirements:
- PostgreSQL test database must be created before running tests
- Run: createdb -U zhuyin_user zhuyin_practice_test
- Run migrations: psql -U zhuyin_user -d zhuyin_practice_test -f backend/migrations/init_db.sql
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest

# Override config before importing app
os.environ['TESTING'] = 'true'
import test_config
import config
for attr in dir(test_config):
    if not attr.startswith('_'):
        setattr(config.Config, attr, getattr(test_config, attr))

from app import app
from services import db_service, auth_service


@pytest.fixture(scope='session', autouse=True)
def init_db():
    """Initialize database connection pool once for all tests"""
    db_service.init_connection_pool()
    yield
    db_service.close_connection_pool()


@pytest.fixture(scope='function')
def client():
    """Create test client with clean database for each test"""
    app.config['TESTING'] = True

    with app.test_client() as client:
        # Clean up test data before each test
        cleanup_test_data()
        yield client
        # Clean up test data after each test
        cleanup_test_data()


def cleanup_test_data():
    """Clean up test data from database"""
    try:
        # Delete test users and their attempts (cascade)
        db_service.execute_query(
            "DELETE FROM users WHERE username LIKE 'test_%'",
            commit=True
        )
    except Exception as e:
        print(f"Cleanup warning: {e}")


def create_test_user(username='test_user', password='test_password'):
    """Helper to create a test user"""
    password_hash = auth_service.hash_password(password)
    result = db_service.execute_query(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
        (username, password_hash),
        fetch_one=True,
        commit=True
    )
    return {'id': result[0], 'username': result[1]}


def get_auth_headers(client, username='test_user', password='test_password'):
    """Helper to get authentication headers"""
    # Create user if doesn't exist
    try:
        create_test_user(username, password)
    except:
        pass  # User might already exist

    # Login to get token
    response = client.post('/api/auth/login',
        json={'username': username, 'password': password})

    if response.status_code == 200:
        data = json.loads(response.data)
        return {'Authorization': f"Bearer {data['access_token']}"}
    return {}


# ============================================================================
# Health Check Tests
# ============================================================================

def test_health_endpoint(client):
    """Test health check endpoint with database connectivity"""
    response = client.get("/health")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "status" in data
    assert data["status"] == "ok"
    assert "database" in data
    assert data["database"] == "connected"
    assert "characters_loaded" in data
    assert data["characters_loaded"] >= 30


def test_health_endpoint_database_info(client):
    """Test health endpoint returns database connection status"""
    response = client.get("/health")
    data = json.loads(response.data)

    # Should have database field
    assert "database" in data
    # Should show as connected if tests are running
    assert data["database"] in ["connected", "disconnected"]


# ============================================================================
# Authentication Endpoint Tests (Task 12.2, 12.3, 12.4)
# ============================================================================

def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'username': 'test_new_user',
        'password': 'secure_password'
    })

    assert response.status_code == 201
    data = json.loads(response.data)

    assert 'user' in data
    assert data['user']['username'] == 'test_new_user'
    assert 'id' in data['user']
    assert 'password' not in data['user']  # Should not return password


def test_register_duplicate_username(client):
    """Test registration with duplicate username returns 409 Conflict"""
    # Create first user
    client.post('/api/auth/register', json={
        'username': 'test_duplicate',
        'password': 'password1'
    })

    # Try to create duplicate
    response = client.post('/api/auth/register', json={
        'username': 'test_duplicate',
        'password': 'password2'
    })

    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data


def test_register_missing_username(client):
    """Test registration without username returns 400 Bad Request"""
    response = client.post('/api/auth/register', json={
        'password': 'password'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_register_missing_password(client):
    """Test registration without password returns 400 Bad Request"""
    response = client.post('/api/auth/register', json={
        'username': 'testuser'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_login_success(client):
    """Test successful login returns tokens"""
    # Create user first
    create_test_user('test_login_user', 'test_password')

    # Login
    response = client.post('/api/auth/login', json={
        'username': 'test_login_user',
        'password': 'test_password'
    })

    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'user' in data
    assert data['user']['username'] == 'test_login_user'


def test_login_invalid_username(client):
    """Test login with non-existent username returns 401"""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent_user',
        'password': 'any_password'
    })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


def test_login_invalid_password(client):
    """Test login with wrong password returns 401"""
    create_test_user('test_wrong_pass', 'correct_password')

    response = client.post('/api/auth/login', json={
        'username': 'test_wrong_pass',
        'password': 'wrong_password'
    })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


def test_refresh_token_success(client):
    """Test refresh token endpoint returns new access token"""
    # Create user and login
    create_test_user('test_refresh', 'password')
    login_response = client.post('/api/auth/login', json={
        'username': 'test_refresh',
        'password': 'password'
    })
    login_data = json.loads(login_response.data)
    refresh_token = login_data['refresh_token']

    # Use refresh token
    response = client.post('/api/auth/refresh', json={
        'refresh_token': refresh_token
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data


def test_refresh_token_invalid(client):
    """Test refresh with invalid token returns 401"""
    response = client.post('/api/auth/refresh', json={
        'refresh_token': 'invalid_token_string'
    })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


# ============================================================================
# Words Endpoint Tests (Task 12.5)
# ============================================================================

def test_random_word_endpoint_format(client):
    """Test /api/words/random returns valid JSON format from database"""
    response = client.get("/api/words/random")
    assert response.status_code == 200

    data = json.loads(response.data)

    # Check required fields exist
    assert "id" in data, "Response should contain 'id' field"
    assert "word" in data, "Response should contain 'word' field"
    assert "zhuyin" in data, "Response should contain 'zhuyin' field"
    assert "keys" in data, "Response should contain 'keys' field"

    # Check field types
    assert isinstance(data["id"], int), "id should be integer"
    assert isinstance(data["word"], str), "word should be string"
    assert isinstance(data["zhuyin"], list), "zhuyin should be list"
    assert isinstance(data["keys"], list), "keys should be list"


def test_zhuyin_keys_array_length_match(client):
    """Test that zhuyin and keys arrays have matching lengths"""
    response = client.get("/api/words/random")
    data = json.loads(response.data)

    zhuyin_length = len(data["zhuyin"])
    keys_length = len(data["keys"])

    assert zhuyin_length == keys_length, (
        f"zhuyin length ({zhuyin_length}) should match keys length ({keys_length})"
    )


def test_random_word_returns_variety(client):
    """Test that random endpoint returns variety of words"""
    words_seen = set()

    # Make multiple requests
    for _ in range(10):
        response = client.get("/api/words/random")
        data = json.loads(response.data)
        words_seen.add(data["word"])

    # Should see at least 2 different words in 10 requests
    assert len(words_seen) >= 2, "Random endpoint should return variety of words"


def test_random_word_with_input_method(client):
    """Test random word endpoint with input_method parameter"""
    response = client.get("/api/words/random?input_method=bopomofo")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "word" in data


# ============================================================================
# Attempts Endpoint Tests (Task 12.6, 12.7)
# ============================================================================

def test_record_attempt_success(client):
    """Test recording a practice attempt"""
    headers = get_auth_headers(client, 'test_attempt_user', 'password')

    # Get a character ID first
    word_response = client.get('/api/words/random')
    word_data = json.loads(word_response.data)
    character_id = word_data['id']

    # Record attempt
    response = client.post('/api/attempts',
        headers=headers,
        json={
            'character_id': character_id,
            'started_at': '2026-02-27T10:00:00.000Z',
            'ended_at': '2026-02-27T10:00:02.500Z',
            'is_correct': True
        })

    assert response.status_code == 202
    data = json.loads(response.data)
    assert 'message' in data


def test_record_attempt_unauthorized(client):
    """Test recording attempt without authentication returns 401"""
    response = client.post('/api/attempts', json={
        'character_id': 1,
        'started_at': '2026-02-27T10:00:00.000Z',
        'ended_at': '2026-02-27T10:00:02.500Z',
        'is_correct': True
    })

    assert response.status_code == 401


def test_record_attempt_missing_fields(client):
    """Test recording attempt with missing required fields returns 400"""
    headers = get_auth_headers(client)

    response = client.post('/api/attempts',
        headers=headers,
        json={
            'character_id': 1
            # Missing other required fields
        })

    assert response.status_code == 400


def test_get_attempts_success(client):
    """Test retrieving user's practice attempts"""
    headers = get_auth_headers(client, 'test_history_user', 'password')

    # Get attempts (might be empty)
    response = client.get('/api/attempts', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'attempts' in data
    assert 'pagination' in data
    assert isinstance(data['attempts'], list)


def test_get_attempts_pagination(client):
    """Test attempts pagination parameters"""
    headers = get_auth_headers(client)

    response = client.get('/api/attempts?page=1&limit=10', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'pagination' in data
    assert data['pagination']['page'] == 1
    assert data['pagination']['limit'] == 10


def test_get_attempts_filtering(client):
    """Test attempts filtering by correctness"""
    headers = get_auth_headers(client)

    response = client.get('/api/attempts?is_correct=true', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'attempts' in data


def test_get_attempts_unauthorized(client):
    """Test getting attempts without authentication returns 401"""
    response = client.get('/api/attempts')

    assert response.status_code == 401


# ============================================================================
# Integration Tests (Task 12.11)
# ============================================================================

def test_full_user_flow(client):
    """Test complete user flow: register → login → practice → view history"""

    # 1. Register
    register_response = client.post('/api/auth/register', json={
        'username': 'test_flow_user',
        'password': 'flow_password'
    })
    assert register_response.status_code == 201

    # 2. Login
    login_response = client.post('/api/auth/login', json={
        'username': 'test_flow_user',
        'password': 'flow_password'
    })
    assert login_response.status_code == 200
    login_data = json.loads(login_response.data)
    access_token = login_data['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    # 3. Get a word to practice
    word_response = client.get('/api/words/random')
    assert word_response.status_code == 200
    word_data = json.loads(word_response.data)

    # 4. Record practice attempt
    attempt_response = client.post('/api/attempts',
        headers=headers,
        json={
            'character_id': word_data['id'],
            'started_at': datetime.utcnow().isoformat() + 'Z',
            'ended_at': (datetime.utcnow() + timedelta(seconds=2)).isoformat() + 'Z',
            'is_correct': True
        })
    assert attempt_response.status_code == 202

    # 5. View history
    history_response = client.get('/api/attempts', headers=headers)
    assert history_response.status_code == 200
    history_data = json.loads(history_response.data)
    assert 'attempts' in history_data


# ============================================================================
# Password Security Tests
# ============================================================================

def test_password_is_hashed(client):
    """Test that passwords are not stored in plain text"""
    client.post('/api/auth/register', json={
        'username': 'test_hash_check',
        'password': 'my_password'
    })

    # Query database directly
    result = db_service.execute_query(
        "SELECT password_hash FROM users WHERE username = %s",
        ('test_hash_check',),
        fetch_one=True
    )

    password_hash = result[0]

    # Hash should not equal plain text password
    assert password_hash != 'my_password'
    # Should be bcrypt hash (starts with $2b$)
    assert password_hash.startswith('$2b$')


# ============================================================================
# Token Validation Tests
# ============================================================================

def test_expired_token_rejected(client):
    """Test that expired tokens are rejected"""
    # This test would require mocking time or creating an actually expired token
    # For now, we test with an invalid token structure
    headers = {'Authorization': 'Bearer invalid_token'}

    response = client.get('/api/attempts', headers=headers)
    assert response.status_code == 401


def test_missing_authorization_header(client):
    """Test that requests without Authorization header are rejected"""
    response = client.get('/api/attempts')
    assert response.status_code == 401


if __name__ == "__main__":
    # Run tests with pytest
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])
