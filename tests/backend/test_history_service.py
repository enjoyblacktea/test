"""
Tests for HistoryService

Tests the history service business logic including user management,
practice recording, history queries, and statistics calculation.

Note: These tests require a PostgreSQL test database to be set up.
Use POSTGRES_DB='zhuyin_practice_test' environment variable.
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from services.db_service import DatabaseService
from services.history_service import HistoryService
from config import TestConfig


@pytest.fixture(scope='function')
def db_service():
    """Create database service for testing."""
    service = DatabaseService(
        host=TestConfig.POSTGRES_HOST,
        port=TestConfig.POSTGRES_PORT,
        database=TestConfig.POSTGRES_DB,
        user=TestConfig.POSTGRES_USER,
        password=TestConfig.POSTGRES_PASSWORD,
        minconn=1,
        maxconn=5
    )
    yield service
    service.close_all()


@pytest.fixture(scope='function')
def history_service(db_service):
    """Create history service for testing."""
    return HistoryService(db_service)


@pytest.fixture(scope='function', autouse=True)
def clean_database(db_service):
    """Clean database before and after each test."""
    conn = None
    try:
        conn = db_service.get_connection()
        cursor = conn.cursor()
        
        # Clean tables
        cursor.execute("DELETE FROM practice_history")
        cursor.execute("DELETE FROM users")
        conn.commit()
        
        yield
        
        # Clean again after test
        cursor.execute("DELETE FROM practice_history")
        cursor.execute("DELETE FROM users")
        conn.commit()
        
    finally:
        if conn:
            db_service.return_connection(conn)


def test_get_or_create_user(history_service):
    """Test creating a new user."""
    username = "testuser1"
    
    # Create user
    user_id = history_service.get_or_create_user(username)
    
    # Verify user_id is returned
    assert user_id is not None
    assert isinstance(user_id, int)
    assert user_id > 0


def test_get_or_create_user_idempotent(history_service):
    """Test that getting the same user multiple times returns same ID."""
    username = "testuser2"
    
    # Create user first time
    user_id1 = history_service.get_or_create_user(username)
    
    # Get same user again
    user_id2 = history_service.get_or_create_user(username)
    
    # Should return same ID
    assert user_id1 == user_id2


def test_record_practice(history_service):
    """Test recording a practice attempt."""
    # Create user
    user_id = history_service.get_or_create_user("testuser3")
    
    # Record practice
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=2.5)
    
    record_id = history_service.record_practice(
        user_id=user_id,
        word="你",
        is_correct=True,
        start_time=start_time,
        end_time=end_time
    )
    
    # Verify record_id is returned
    assert record_id is not None
    assert isinstance(record_id, int)
    assert record_id > 0


def test_get_history(history_service):
    """Test querying practice history with pagination."""
    # Create user
    username = "testuser4"
    user_id = history_service.get_or_create_user(username)
    
    # Record multiple practices
    base_time = datetime.now()
    for i in range(5):
        start_time = base_time + timedelta(seconds=i*3)
        end_time = start_time + timedelta(seconds=2)
        history_service.record_practice(
            user_id=user_id,
            word=f"字{i}",
            is_correct=i % 2 == 0,  # Alternate correct/incorrect
            start_time=start_time,
            end_time=end_time
        )
    
    # Query history with default pagination
    result = history_service.get_history(user_id)
    
    # Verify result structure
    assert 'total' in result
    assert 'records' in result
    assert result['total'] == 5
    assert len(result['records']) == 5
    
    # Verify records are sorted by start_time DESC (most recent first)
    assert result['records'][0]['word'] == "字4"
    assert result['records'][4]['word'] == "字0"
    
    # Verify record structure
    first_record = result['records'][0]
    assert 'record_id' in first_record
    assert 'word' in first_record
    assert 'is_correct' in first_record
    assert 'start_time' in first_record
    assert 'end_time' in first_record
    assert 'duration_ms' in first_record
    
    # Test pagination
    result_page = history_service.get_history(user_id, limit=2, offset=1)
    assert result_page['total'] == 5
    assert len(result_page['records']) == 2
    assert result_page['records'][0]['word'] == "字3"


def test_get_stats(history_service):
    """Test calculating practice statistics."""
    # Create user
    username = "testuser5"
    user_id = history_service.get_or_create_user(username)
    
    # Record practices with known values
    base_time = datetime.now()
    
    # 3 correct, 2 incorrect = 60% accuracy
    records = [
        ("你", True, 2000),   # 2 seconds
        ("好", True, 3000),   # 3 seconds
        ("的", False, 1000),  # 1 second
        ("了", True, 4000),   # 4 seconds
        ("是", False, 2000),  # 2 seconds
    ]
    
    for i, (word, is_correct, duration_ms) in enumerate(records):
        start_time = base_time + timedelta(seconds=i*5)
        end_time = start_time + timedelta(milliseconds=duration_ms)
        history_service.record_practice(
            user_id=user_id,
            word=word,
            is_correct=is_correct,
            start_time=start_time,
            end_time=end_time
        )
    
    # Get stats
    stats = history_service.get_stats(user_id)
    
    # Verify stats structure
    assert 'total_words' in stats
    assert 'correct_count' in stats
    assert 'accuracy' in stats
    assert 'avg_duration_ms' in stats
    assert 'practice_days' in stats
    
    # Verify values
    assert stats['total_words'] == 5
    assert stats['correct_count'] == 3
    assert stats['accuracy'] == 0.6  # 3/5 = 0.6
    assert stats['avg_duration_ms'] == 2400.0  # (2000+3000+1000+4000+2000)/5
    assert stats['practice_days'] == 1  # All on same day


def test_get_stats_zero_records(history_service):
    """Test statistics for user with no practice records."""
    # Create user but don't record any practices
    username = "testuser6"
    user_id = history_service.get_or_create_user(username)
    
    # Get stats
    stats = history_service.get_stats(user_id)
    
    # Verify zero values without errors
    assert stats['total_words'] == 0
    assert stats['correct_count'] == 0
    assert stats['accuracy'] == 0.0
    assert stats['avg_duration_ms'] == 0.0
    assert stats['practice_days'] == 0
