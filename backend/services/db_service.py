"""Database connection service with connection pooling.

This module provides a DatabaseService class that manages PostgreSQL
connections using psycopg2's SimpleConnectionPool for efficient
connection reuse across requests.
"""

import logging
from psycopg2 import pool, OperationalError, DatabaseError

logger = logging.getLogger(__name__)


class DatabaseService:
    """Manages PostgreSQL database connections with connection pooling.

    Attributes:
        _pool: psycopg2 SimpleConnectionPool instance
        host: PostgreSQL host
        port: PostgreSQL port
        database: Database name
        user: Database user
        password: Database password
    """

    def __init__(self, host, port, database, user, password, minconn=1, maxconn=10):
        """Initialize database service with connection pool.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Database user
            password: Database password
            minconn: Minimum number of connections in pool (default 1)
            maxconn: Maximum number of connections in pool (default 10)

        Raises:
            OperationalError: If connection pool creation fails
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        try:
            self._pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            logger.info(
                f"Database connection pool created: "
                f"{database}@{host}:{port} (min={minconn}, max={maxconn})"
            )
        except OperationalError as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise

    def get_connection(self):
        """Get a connection from the pool.

        Returns:
            psycopg2 connection object

        Raises:
            pool.PoolError: If no connections available
            OperationalError: If connection cannot be established
        """
        try:
            conn = self._pool.getconn()
            if conn:
                logger.debug("Connection retrieved from pool")
                return conn
            else:
                logger.error("Failed to get connection from pool")
                raise OperationalError("Connection pool exhausted")
        except Exception as e:
            logger.error(f"Error getting connection: {e}")
            raise

    def return_connection(self, conn):
        """Return a connection to the pool.

        Args:
            conn: psycopg2 connection object to return

        Note:
            Should be called in finally block to ensure connection is returned
            even if an error occurs during query execution.
        """
        try:
            self._pool.putconn(conn)
            logger.debug("Connection returned to pool")
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")

    def close_all(self):
        """Close all connections in the pool.

        Should be called on application shutdown to cleanly close all
        database connections.
        """
        try:
            self._pool.closeall()
            logger.info("All database connections closed")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")
