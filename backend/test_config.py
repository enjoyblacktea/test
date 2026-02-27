"""
Test Configuration
Separate configuration for testing with test database
"""

import os
from datetime import timedelta

# Test Database Configuration
# Use remote test database (created on same server as production)
DATABASE_URL = os.getenv(
    'TEST_DATABASE_URL',
    'postgresql://postgres:postgres@10.6.142.157:5432/zhuyin_practice_test'
)

# Use smaller pool for tests
DB_POOL_SIZE = 2
DB_MAX_OVERFLOW = 3
DB_POOL_RECYCLE = 3600

# JWT Configuration (use different key for tests)
JWT_SECRET_KEY = 'test-secret-key-do-not-use-in-production'
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
REFRESH_TOKEN_EXPIRY = timedelta(days=7)

# Bcrypt Configuration (lower work factor for faster tests)
BCRYPT_WORK_FACTOR = 4

# Flask Configuration
TESTING = True
DEBUG = False
