"""History service for managing practice history records.

This module provides a HistoryService class that handles all practice history
related operations including recording practice attempts, querying history,
and calculating statistics.
"""

import logging
from datetime import datetime
from psycopg2 import DatabaseError, IntegrityError
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class HistoryService:
    """Manages practice history records and statistics.

    Attributes:
        db_service: DatabaseService instance for database operations
    """

    def __init__(self, db_service):
        """Initialize history service.

        Args:
            db_service: DatabaseService instance
        """
        self.db_service = db_service
        logger.info("HistoryService initialized")

    def get_or_create_user(self, username):
        """Get existing user or create new user.

        Args:
            username: Username to look up or create

        Returns:
            int: user_id of existing or newly created user

        Raises:
            DatabaseError: If database operation fails
        """
        conn = None
        try:
            conn = self.db_service.get_connection()
            cursor = conn.cursor()

            # Try to get existing user
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s",
                (username,)
            )
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                logger.debug(f"Found existing user: {username} (id={user_id})")
                return user_id

            # Create new user
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id",
                (username, '')  # Empty password_hash for now (frontend auth)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Created new user: {username} (id={user_id})")
            return user_id

        except IntegrityError as e:
            # Handle race condition: another request created the user
            conn.rollback()
            logger.warning(f"Race condition creating user {username}, retrying: {e}")
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s",
                (username,)
            )
            return cursor.fetchone()[0]

        except DatabaseError as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error in get_or_create_user: {e}")
            raise

        finally:
            if conn:
                self.db_service.return_connection(conn)

    def record_practice(self, user_id, word, is_correct, start_time, end_time):
        """Record a practice attempt.

        Args:
            user_id: User ID
            word: Practiced word
            is_correct: Whether the attempt was correct
            start_time: Practice start time (datetime or ISO string)
            end_time: Practice end time (datetime or ISO string)

        Returns:
            int: record_id of created practice record

        Raises:
            DatabaseError: If database operation fails
        """
        conn = None
        try:
            # Convert ISO strings to datetime if needed
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

            conn = self.db_service.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO practice_history 
                (user_id, word, is_correct, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING record_id
                """,
                (user_id, word, is_correct, start_time, end_time)
            )
            record_id = cursor.fetchone()[0]
            conn.commit()

            logger.info(
                f"Recorded practice: user={user_id}, word={word}, "
                f"correct={is_correct}, record_id={record_id}"
            )
            return record_id

        except DatabaseError as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error in record_practice: {e}")
            raise

        finally:
            if conn:
                self.db_service.return_connection(conn)

    def get_history(self, user_id, limit=50, offset=0):
        """Get practice history for a user.

        Args:
            user_id: User ID
            limit: Maximum number of records to return (default 50)
            offset: Number of records to skip (default 0)

        Returns:
            dict: {
                'total': total number of records,
                'records': list of practice records
            }

        Raises:
            DatabaseError: If database operation fails
        """
        conn = None
        try:
            conn = self.db_service.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Get total count
            cursor.execute(
                "SELECT COUNT(*) as total FROM practice_history WHERE user_id = %s",
                (user_id,)
            )
            total = cursor.fetchone()['total']

            # Get paginated records
            cursor.execute(
                """
                SELECT 
                    record_id, word, is_correct, 
                    start_time, end_time, duration_ms
                FROM practice_history
                WHERE user_id = %s
                ORDER BY start_time DESC
                LIMIT %s OFFSET %s
                """,
                (user_id, limit, offset)
            )
            records = cursor.fetchall()

            # Convert RealDictRow to regular dict and format timestamps
            records = [
                {
                    **dict(record),
                    'start_time': record['start_time'].isoformat(),
                    'end_time': record['end_time'].isoformat()
                }
                for record in records
            ]

            logger.debug(
                f"Retrieved history: user={user_id}, total={total}, "
                f"returned={len(records)}, offset={offset}"
            )

            return {
                'total': total,
                'records': records
            }

        except DatabaseError as e:
            logger.error(f"Database error in get_history: {e}")
            raise

        finally:
            if conn:
                self.db_service.return_connection(conn)

    def get_stats(self, user_id):
        """Calculate practice statistics for a user.

        Args:
            user_id: User ID

        Returns:
            dict: {
                'total_words': total practice attempts,
                'correct_count': number of correct attempts,
                'accuracy': accuracy rate (0.0 to 1.0),
                'avg_duration_ms': average practice time in milliseconds,
                'practice_days': number of distinct days with practice
            }

        Raises:
            DatabaseError: If database operation fails
        """
        conn = None
        try:
            conn = self.db_service.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total_words,
                    SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct_count,
                    AVG(duration_ms) as avg_duration_ms,
                    COUNT(DISTINCT DATE(start_time)) as practice_days
                FROM practice_history
                WHERE user_id = %s
                """,
                (user_id,)
            )
            result = cursor.fetchone()

            total_words = result['total_words'] or 0
            correct_count = result['correct_count'] or 0
            avg_duration_ms = float(result['avg_duration_ms']) if result['avg_duration_ms'] else 0.0
            practice_days = result['practice_days'] or 0

            # Calculate accuracy
            accuracy = correct_count / total_words if total_words > 0 else 0.0

            stats = {
                'total_words': total_words,
                'correct_count': correct_count,
                'accuracy': accuracy,
                'avg_duration_ms': avg_duration_ms,
                'practice_days': practice_days
            }

            logger.debug(f"Calculated stats for user={user_id}: {stats}")
            return stats

        except DatabaseError as e:
            logger.error(f"Database error in get_stats: {e}")
            raise

        finally:
            if conn:
                self.db_service.return_connection(conn)
