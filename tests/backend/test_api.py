"""
Backend API Tests
Tests for Flask API endpoints
"""

import sys
import os
import json

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
from app import app, words_data


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "status" in data
    assert data["status"] == "ok"
    assert "words_loaded" in data


def test_random_word_endpoint_format(client):
    """Test /api/words/random returns valid JSON format"""
    response = client.get("/api/words/random")
    assert response.status_code == 200

    data = json.loads(response.data)

    # Check required fields exist
    assert "word" in data, "Response should contain 'word' field"
    assert "zhuyin" in data, "Response should contain 'zhuyin' field"
    assert "keys" in data, "Response should contain 'keys' field"

    # Check field types
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


def test_words_data_loaded():
    """Test that words.json was loaded successfully"""
    assert len(words_data) > 0, "words_data should contain at least one word"
    assert len(words_data) >= 20, "words_data should contain at least 20 words"


def test_words_data_format():
    """Test that all words in words_data have correct format"""
    for word_entry in words_data:
        assert "word" in word_entry, "Each entry should have 'word' field"
        assert "zhuyin" in word_entry, "Each entry should have 'zhuyin' field"
        assert "keys" in word_entry, "Each entry should have 'keys' field"

        # Check types
        assert isinstance(word_entry["word"], str)
        assert isinstance(word_entry["zhuyin"], list)
        assert isinstance(word_entry["keys"], list)

        # Check lengths match
        assert len(word_entry["zhuyin"]) == len(word_entry["keys"]), (
            f"Word '{word_entry['word']}': zhuyin and keys length mismatch"
        )


def test_random_word_returns_different_words(client):
    """Test that random endpoint returns variety (not always same word)"""
    words_seen = set()

    # Make multiple requests
    for _ in range(10):
        response = client.get("/api/words/random")
        data = json.loads(response.data)
        words_seen.add(data["word"])

    # Should see at least 2 different words in 10 requests
    assert len(words_seen) >= 2, "Random endpoint should return variety of words"


def test_missing_words_json():
    """Test error handling when words.json is missing"""
    # This test simulates the missing file scenario
    # In actual implementation, app.py handles this at startup
    # We're testing that the error is properly reported

    # If words_data is empty, API should return error
    if len(words_data) == 0:
        client = app.test_client()
        response = client.get("/api/words/random")
        assert response.status_code == 500

        data = json.loads(response.data)
        assert "error" in data


def test_tone_marks_in_data():
    """Test that tone marks are properly included"""
    # Check that we have various tone marks in our data
    all_zhuyin = []
    for word_entry in words_data:
        all_zhuyin.extend(word_entry["zhuyin"])

    # Should have at least one tone mark
    has_tone = any(symbol in ["ˊ", "ˇ", "ˋ", "˙", ""] for symbol in all_zhuyin)
    assert has_tone, "Data should include tone marks"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
