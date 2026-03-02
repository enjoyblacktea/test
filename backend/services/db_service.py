"""Database service for connection pooling and query execution."""

import logging
from typing import Optional, Any, List, Tuple
import psycopg2
from psycopg2 import pool, extras
from config import Config

logger = logging.getLogger(__name__)

# Global connection pool
_connection_pool: Optional[pool.SimpleConnectionPool] = None


def init_connection_pool():
    """Initialize the database connection pool.

    Creates a connection pool with settings from Config.
    Should be called once at application startup.

    Raises:
        psycopg2.Error: If database connection fails
    """
    global _connection_pool

    if _connection_pool is not None:
        logger.warning("Connection pool already initialized")
        return

    try:
        _connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=Config.DB_POOL_SIZE + Config.DB_MAX_OVERFLOW,
            dsn=Config.DATABASE_URL
        )
        logger.info(
            f"Database connection pool initialized "
            f"(size={Config.DB_POOL_SIZE}, max_overflow={Config.DB_MAX_OVERFLOW})"
        )
    except psycopg2.Error as e:
        logger.error(f"Failed to initialize connection pool: {e}")
        raise


def get_db_connection():
    """Get a connection from the pool.

    Returns:
        psycopg2 connection object

    Raises:
        RuntimeError: If connection pool not initialized
        psycopg2.Error: If no connections available
    """
    global _connection_pool

    if _connection_pool is None:
        raise RuntimeError("Connection pool not initialized. Call init_connection_pool() first.")

    try:
        conn = _connection_pool.getconn()
        return conn
    except psycopg2.Error as e:
        logger.error(f"Failed to get connection from pool: {e}")
        raise


def return_db_connection(conn):
    """Return a connection to the pool.

    Args:
        conn: psycopg2 connection object to return
    """
    global _connection_pool

    if _connection_pool is None:
        logger.warning("Connection pool not initialized, cannot return connection")
        return

    try:
        _connection_pool.putconn(conn)
    except psycopg2.Error as e:
        logger.error(f"Failed to return connection to pool: {e}")


def close_connection_pool():
    """Close all connections in the pool.

    Should be called at application shutdown.
    """
    global _connection_pool

    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None
        logger.info("Database connection pool closed")


def execute_query(
    query: str,
    params: Optional[Tuple] = None,
    fetch_one: bool = False,
    fetch_all: bool = False,
    commit: bool = False
) -> Optional[Any]:
    """Execute a SQL query with connection pooling.

    Args:
        query: SQL query string (use %s for parameters)
        params: Query parameters tuple
        fetch_one: If True, return single row
        fetch_all: If True, return all rows
        commit: If True, commit transaction (for INSERT/UPDATE/DELETE)

    Returns:
        Query results (None, single row, or list of rows depending on fetch parameters)

    Raises:
        psycopg2.Error: If query execution fails

    Example:
        # Fetch one
        user = execute_query(
            "SELECT * FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )

        # Fetch all
        users = execute_query(
            "SELECT * FROM users WHERE created_at > %s",
            (start_date,),
            fetch_all=True
        )

        # Insert with commit
        execute_query(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
            commit=True
        )
    """
    conn = None
    cursor = None
    result = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()

        if commit:
            conn.commit()

    except psycopg2.Error as e:
        if conn and commit:
            conn.rollback()
        logger.error(f"Database query failed: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)

    return result


def test_connection() -> bool:
    """Test database connectivity.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        result = execute_query("SELECT 1", fetch_one=True)
        return result is not None
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
