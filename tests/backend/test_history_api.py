"""
Tests for History API endpoints

Tests the REST API endpoints for practice history tracking including
request validation, error handling, and response formats.
"""

import pytest
import json
from datetime import datetime, timedelta
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app import app
from services.db_service import DatabaseService
from config import TestConfig


@pytest.fixture(scope='function')
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function', autouse=True)
def clean_database():
    """Clean database before and after each test."""
    db_service = None
    conn = None
    try:
        db_service = DatabaseService(
            host=TestConfig.POSTGRES_HOST,
            port=TestConfig.POSTGRES_PORT,
            database=TestConfig.POSTGRES_DB,
            user=TestConfig.POSTGRES_USER,
            password=TestConfig.POSTGRES_PASSWORD
        )
        
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
        if conn and db_service:
            db_service.return_connection(conn)
        if db_service:
            db_service.close_all()


def test_record_practice_api_success(client):
    """Test successful practice recording via API."""
    # Prepare request data
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=2.5)
    
    data = {
        'username': 'testuser1',
        'word': '你',
        'is_correct': True,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    }
    
    # Make request
    response = client.post(
        '/api/history/record',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Verify response
    assert response.status_code == 201
    result = json.loads(response.data)
    assert result['success'] is True
    assert 'record_id' in result
    assert isinstance(result['record_id'], int)


def test_record_practice_missing_fields(client):
    """Test API rejects request with missing required fields."""
    # Missing 'word' field
    data = {
        'username': 'testuser2',
        'is_correct': True,
        'start_time': datetime.now().isoformat(),
        'end_time': (datetime.now() + timedelta(seconds=2)).isoformat()
    }
    
    response = client.post(
        '/api/history/record',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Verify error response
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] is False
    assert 'error' in result
    assert 'Missing required fields' in result['error']


def test_record_practice_invalid_timestamp(client):
    """Test API rejects request with invalid timestamp format."""
    data = {
        'username': 'testuser3',
        'word': '好',
        'is_correct': True,
        'start_time': 'invalid-timestamp',
        'end_time': datetime.now().isoformat()
    }
    
    response = client.post(
        '/api/history/record',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Verify error response
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] is False
    assert 'Invalid timestamp format' in result['error']


def test_record_practice_invalid_time_order(client):
    """Test API rejects request where end_time <= start_time."""
    start_time = datetime.now()
    end_time = start_time - timedelta(seconds=1)  # End before start!
    
    data = {
        'username': 'testuser4',
        'word': '的',
        'is_correct': False,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    }
    
    response = client.post(
        '/api/history/record',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Verify error response
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] is False
    assert 'end_time must be after start_time' in result['error']


def test_get_history_api(client):
    """Test querying practice history via API."""
    # First, record some practices
    username = 'testuser5'
    base_time = datetime.now()
    
    for i in range(3):
        start_time = base_time + timedelta(seconds=i*3)
        end_time = start_time + timedelta(seconds=2)
        data = {
            'username': username,
            'word': f'字{i}',
            'is_correct': True,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        }
        client.post('/api/history/record', data=json.dumps(data), content_type='application/json')
    
    # Query history
    response = client.get(f'/api/history?username={username}')
    
    # Verify response
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] is True
    assert result['total'] == 3
    assert len(result['records']) == 3
    
    # Verify record structure
    first_record = result['records'][0]
    assert 'record_id' in first_record
    assert 'word' in first_record
    assert 'is_correct' in first_record
    assert 'start_time' in first_record
    assert 'end_time' in first_record
    assert 'duration_ms' in first_record


def test_get_history_missing_username(client):
    """Test API rejects history query without username parameter."""
    response = client.get('/api/history')
    
    # Verify error response
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] is False
    assert 'Missing username parameter' in result['error']


def test_get_stats_api(client):
    """Test querying practice statistics via API."""
    # First, record some practices
    username = 'testuser6'
    base_time = datetime.now()
    
    # Record 2 correct, 1 incorrect
    records = [
        ('你', True, 2000),
        ('好', True, 3000),
        ('的', False, 1000)
    ]
    
    for i, (word, is_correct, duration_ms) in enumerate(records):
        start_time = base_time + timedelta(seconds=i*5)
        end_time = start_time + timedelta(milliseconds=duration_ms)
        data = {
            'username': username,
            'word': word,
            'is_correct': is_correct,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        }
        client.post('/api/history/record', data=json.dumps(data), content_type='application/json')
    
    # Query stats
    response = client.get(f'/api/history/stats?username={username}')
    
    # Verify response
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] is True
    assert result['total_words'] == 3
    assert result['correct_count'] == 2
    assert result['accuracy'] == pytest.approx(0.667, rel=0.01)  # 2/3
    assert result['avg_duration_ms'] == 2000.0  # (2000+3000+1000)/3
    assert result['practice_days'] == 1


def test_get_stats_missing_username(client):
    """Test API rejects stats query without username parameter."""
    response = client.get('/api/history/stats')
    
    # Verify error response
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] is False
    assert 'Missing username parameter' in result['error']


def test_history_api_invalid_pagination(client):
    """Test API rejects invalid limit/offset parameters."""
    # Test with non-numeric limit
    response = client.get('/api/history?username=test&limit=abc')
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'Invalid limit or offset' in result['error']
    
    # Test with negative offset
    response = client.get('/api/history?username=test&offset=-1')
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'Invalid limit or offset' in result['error']
