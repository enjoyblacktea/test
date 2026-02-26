/**
 * History module for recording and querying practice history.
 *
 * This module handles communication with the backend history API
 * for recording practice attempts, querying history, and retrieving statistics.
 */

const API_BASE_URL = 'http://localhost:5000/api/history';

/**
 * Record a practice attempt.
 *
 * @param {Object} data - Practice data
 * @param {string} data.username - Username
 * @param {string} data.word - Practiced word
 * @param {boolean} data.isCorrect - Whether the attempt was correct
 * @param {Date|string} data.startTime - Practice start time
 * @param {Date|string} data.endTime - Practice end time
 * @returns {Promise<Object>} API response
 *
 * Note: Errors are logged but not thrown to avoid blocking practice flow.
 */
export async function recordPractice(data) {
  try {
    // Convert Date objects to ISO strings if needed
    const payload = {
      username: data.username,
      word: data.word,
      is_correct: data.isCorrect,
      start_time: data.startTime instanceof Date 
        ? data.startTime.toISOString() 
        : data.startTime,
      end_time: data.endTime instanceof Date 
        ? data.endTime.toISOString() 
        : data.endTime
    };

    const response = await fetch(`${API_BASE_URL}/record`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      console.warn(`Failed to record practice: ${result.error || 'Unknown error'}`);
      return null;
    }

    console.log('Practice recorded successfully:', result.record_id);
    return result;

  } catch (error) {
    // Log error but don't throw - recording failures shouldn't block practice
    console.warn('Error recording practice (continuing anyway):', error.message);
    // Optional: save to offline queue for later retry
    // saveToOfflineQueue(data);
    return null;
  }
}

/**
 * Get practice history for a user.
 *
 * @param {string} username - Username to query
 * @param {number} [limit=50] - Maximum number of records to return
 * @param {number} [offset=0] - Number of records to skip
 * @returns {Promise<Object>} History data with total count and records
 */
export async function getHistory(username, limit = 50, offset = 0) {
  try {
    const url = new URL(API_BASE_URL);
    url.searchParams.append('username', username);
    url.searchParams.append('limit', limit);
    url.searchParams.append('offset', offset);

    const response = await fetch(url);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Failed to fetch history');
    }

    return result;

  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
}

/**
 * Get practice statistics for a user.
 *
 * @param {string} username - Username to query
 * @returns {Promise<Object>} Statistics including total_words, correct_count, accuracy, etc.
 */
export async function getStats(username) {
  try {
    const url = new URL(`${API_BASE_URL}/stats`);
    url.searchParams.append('username', username);

    const response = await fetch(url);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Failed to fetch stats');
    }

    return result;

  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
}

/**
 * Save practice data to offline queue (optional feature).
 *
 * Stores failed practice records in LocalStorage for retry when network recovers.
 *
 * @param {Object} data - Practice data to save
 */
export function saveToOfflineQueue(data) {
  try {
    const queue = JSON.parse(localStorage.getItem('practiceQueue') || '[]');
    queue.push({
      ...data,
      timestamp: new Date().toISOString()
    });
    localStorage.setItem('practiceQueue', JSON.stringify(queue));
    console.log('Saved to offline queue');
  } catch (error) {
    console.error('Error saving to offline queue:', error);
  }
}

/**
 * Flush offline queue (optional feature).
 *
 * Attempts to send all queued practice records to the server.
 * Successfully sent records are removed from the queue.
 *
 * @returns {Promise<Object>} Result with success/failure counts
 */
export async function flushOfflineQueue() {
  try {
    const queue = JSON.parse(localStorage.getItem('practiceQueue') || '[]');
    
    if (queue.length === 0) {
      return { success: 0, failed: 0 };
    }

    let successCount = 0;
    let failedCount = 0;
    const remainingQueue = [];

    for (const data of queue) {
      const result = await recordPractice(data);
      if (result) {
        successCount++;
      } else {
        failedCount++;
        remainingQueue.push(data);
      }
    }

    // Update queue with only failed records
    localStorage.setItem('practiceQueue', JSON.stringify(remainingQueue));

    console.log(`Flushed offline queue: ${successCount} success, ${failedCount} failed`);
    return { success: successCount, failed: failedCount };

  } catch (error) {
    console.error('Error flushing offline queue:', error);
    return { success: 0, failed: queue.length };
  }
}
