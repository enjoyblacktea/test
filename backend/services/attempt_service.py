"""Practice attempt service for recording and retrieving user practice history."""

import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
import psycopg2
from psycopg2.extras import execute_values
from .db_service import execute_query, get_db_connection, return_db_connection
from models.typing_attempt import TypingAttempt

logger = logging.getLogger(__name__)


def record_attempt(
    user_id: int,
    character_id: int,
    started_at: datetime,
    ended_at: datetime,
    is_correct: bool,
    keystrokes: Optional[List[Dict]] = None
) -> Optional[int]:
    """Record a practice attempt and its keystrokes to the database.

    Both typing_attempts and keystroke_events are written in a single transaction.
    If keystrokes is None or empty, only typing_attempts is written.

    Args:
        user_id: User ID
        character_id: Character ID
        started_at: When user started typing
        ended_at: When user finished typing
        is_correct: Whether the attempt was successful
        keystrokes: Optional list of keystroke dicts with keys:
            key (str), order (int), typed_at (str ISO8601), is_correct (bool)

    Returns:
        Attempt ID if successful, None if failed
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.autocommit = False
        cursor = conn.cursor()

        # Insert typing_attempts row
        cursor.execute(
            """
            INSERT INTO typing_attempts (user_id, character_id, started_at, ended_at, is_correct, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id
            """,
            (user_id, character_id, started_at, ended_at, is_correct)
        )
        row = cursor.fetchone()
        if not row:
            conn.rollback()
            logger.error("Failed to record attempt: no ID returned")
            return None

        attempt_id = row[0]

        # Batch insert keystroke_events if provided
        if keystrokes:
            execute_values(
                cursor,
                """
                INSERT INTO keystroke_events (attempt_id, key_value, key_order, typed_at, is_correct_key)
                VALUES %s
                """,
                [
                    (attempt_id, k['key'], k['order'], k['typed_at'], k['is_correct'])
                    for k in keystrokes
                ]
            )

        conn.commit()
        cursor.close()

        logger.info(
            f"Recorded attempt: user={user_id}, character={character_id}, "
            f"correct={is_correct}, id={attempt_id}, keystrokes={len(keystrokes) if keystrokes else 0}"
        )
        return attempt_id

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error recording attempt: {e}")
        logger.error(f"  user_id={user_id}, character_id={character_id}, is_correct={is_correct}")
        return None
    finally:
        if conn:
            conn.autocommit = True
            return_db_connection(conn)


def get_user_attempts(
    user_id: int,
    page: int = 1,
    limit: int = 50,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Get user's practice history with pagination and filtering.

    Args:
        user_id: User ID to query
        page: Page number (1-indexed)
        limit: Results per page (default 50, max 100)
        filters: Optional filters dict with keys:
            - is_correct (bool): Filter by correctness
            - character_id (int): Filter by specific character
            - start_date (datetime): Filter attempts after this date
            - end_date (datetime): Filter attempts before this date

    Returns:
        Dictionary with:
            - attempts: List of attempt dictionaries with character info
            - pagination: {total_count, page, limit, total_pages, has_more}

    Example:
        result = get_user_attempts(
            user_id=1,
            page=1,
            limit=20,
            filters={'is_correct': True}
        )
        for attempt in result['attempts']:
            print(f"{attempt['character']} - {attempt['is_correct']}")
    """
    if filters is None:
        filters = {}

    # Validate and sanitize inputs
    page = max(1, page)
    limit = min(max(1, limit), 100)  # Cap at 100
    offset = (page - 1) * limit

    try:
        # Build query with filters
        where_clauses = ["ta.user_id = %s"]
        params = [user_id]

        # Add filters
        if 'is_correct' in filters:
            where_clauses.append("ta.is_correct = %s")
            params.append(filters['is_correct'])

        if 'character_id' in filters:
            where_clauses.append("ta.character_id = %s")
            params.append(filters['character_id'])

        if 'start_date' in filters:
            where_clauses.append("ta.created_at >= %s")
            params.append(filters['start_date'])

        if 'end_date' in filters:
            where_clauses.append("ta.created_at <= %s")
            params.append(filters['end_date'])

        where_clause = " AND ".join(where_clauses)

        # Count total results (for pagination)
        count_query = f"""
            SELECT COUNT(*)
            FROM typing_attempts ta
            WHERE {where_clause}
        """
        count_row = execute_query(count_query, tuple(params), fetch_one=True)
        total_count = count_row[0] if count_row else 0

        # Get paginated results with character info
        query = f"""
            SELECT
                ta.id,
                ta.user_id,
                ta.character_id,
                ta.started_at,
                ta.ended_at,
                ta.is_correct,
                ta.duration_ms,
                ta.created_at,
                c.character,
                c.input_code,
                c.input_method
            FROM typing_attempts ta
            JOIN characters c ON ta.character_id = c.id
            WHERE {where_clause}
            ORDER BY ta.created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        rows = execute_query(query, tuple(params), fetch_all=True)

        # Format results
        attempts = []
        if rows:
            for row in rows:
                attempts.append({
                    'id': row[0],
                    'user_id': row[1],
                    'character_id': row[2],
                    'started_at': row[3].isoformat() if row[3] else None,
                    'ended_at': row[4].isoformat() if row[4] else None,
                    'is_correct': row[5],
                    'duration_ms': row[6],
                    'created_at': row[7].isoformat() if row[7] else None,
                    'character': row[8],
                    'input_code': row[9],
                    'input_method': row[10]
                })

        # Calculate pagination metadata
        total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0
        has_more = page < total_pages

        return {
            'attempts': attempts,
            'pagination': {
                'total_count': total_count,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
                'has_more': has_more
            }
        }

    except Exception as e:
        logger.error(f"Error retrieving user attempts: {e}")
        logger.error(f"  user_id={user_id}, page={page}, filters={filters}")
        return {
            'attempts': [],
            'pagination': {
                'total_count': 0,
                'page': page,
                'limit': limit,
                'total_pages': 0,
                'has_more': False
            }
        }
