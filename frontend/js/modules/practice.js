/**
 * Practice Logic Module
 * Manages practice state and validates user input
 */

import * as api from './api.js';

// Practice state
const state = {
  word: '',         // Current Chinese character
  zhuyin: [],       // Array of zhuyin symbols for current word
  keys: [],         // Array of expected keyboard keys
  currentIndex: 0,  // Current position in the input sequence
  characterId: null,      // Character ID from API for recording
  characterText: '',      // Character text for lookup
  startedAt: null,        // Timestamp when word was loaded
  attemptRecorded: false, // Track if attempt already recorded
  hasErrors: false        // Track if user made any mistakes
};

/**
 * Fetch next word from API
 * @returns {Promise<Object>} Word data from API
 */
export async function fetchNextWord() {
  try {
    // Use authenticated API if available, fallback to unauthenticated
    const response = await fetch('http://localhost:5000/api/words/random');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    // Look up character_id for recording (make separate API call if needed)
    // For now, we'll use character text to look up ID when recording
    return data;
  } catch (error) {
    console.error('Error fetching word:', error);
    throw error;
  }
}

/**
 * Load a new word into the practice state
 * @param {Object} data - Word data {word, zhuyin, keys, id?}
 */
export function loadWord(data) {
  state.word = data.word;
  state.zhuyin = data.zhuyin;
  state.keys = data.keys;
  state.currentIndex = 0;

  // Store character metadata for recording
  state.characterId = data.id || null;
  state.characterText = data.word;

  // Record start time and reset error tracking
  state.startedAt = new Date();
  state.attemptRecorded = false;
  state.hasErrors = false;

  // Update display
  updateDisplay();

  console.log('Loaded word:', state.word, 'zhuyin:', state.zhuyin, 'keys:', state.keys);
  console.log('Attempt tracking started:', state.startedAt.toISOString());
}

/**
 * Record a practice attempt to the backend (non-blocking)
 * @param {number} characterId - Character ID from state
 * @param {string} character - Character text (for logging)
 * @param {boolean} isCorrect - Whether the attempt was successful
 * @param {Date} startTime - When user started typing
 * @param {Date} endTime - When user finished typing
 */
async function recordAttempt(characterId, character, isCorrect, startTime, endTime) {
  // Skip if no character ID available
  if (!characterId) {
    console.warn('No character ID available, skipping recording');
    return;
  }

  try {
    // Record attempt via authenticated API (non-blocking)
    const attemptData = {
      character_id: characterId,
      started_at: startTime.toISOString(),
      ended_at: endTime.toISOString(),
      is_correct: isCorrect
    };

    // Use apiPost but don't wait for response (fire and forget)
    api.apiPost('/attempts', attemptData)
      .then(() => {
        console.log('✓ Attempt recorded:', character, isCorrect ? 'correct' : 'incorrect');
      })
      .catch((error) => {
        console.warn('Failed to record attempt (non-blocking):', error.message);
        // Don't throw - this is non-blocking, we don't want to interrupt practice
      });
  } catch (error) {
    console.warn('Error in recordAttempt (non-blocking):', error.message);
    // Don't throw - practice should continue even if recording fails
  }
}

/**
 * Complete current attempt and record it
 * is_correct=true means perfect (no errors), false means completed with errors
 */
export function completeAttempt() {
  if (!state.startedAt || state.attemptRecorded) {
    return; // Already recorded or no start time
  }

  const endTime = new Date();

  // is_correct indicates if user completed without any errors
  const isPerfect = !state.hasErrors;

  // Record attempt (non-blocking)
  recordAttempt(state.characterId, state.characterText, isPerfect, state.startedAt, endTime);

  state.attemptRecorded = true;
}

/**
 * Update the DOM to display current word
 */
function updateDisplay() {
  // Support both original and redesigned HTML
  const display = document.getElementById('practice-word') || document.getElementById('practice-character');
  if (display) {
    display.textContent = state.word;
    // Reset any error styling
    display.style.fontSize = '';
    display.style.color = '';
  }

  const zhuyinDisplay = document.getElementById('target-zhuyin');
  if (zhuyinDisplay) {
    zhuyinDisplay.textContent = state.zhuyin.join('');
  }
}

/**
 * Check if user input is correct
 * @param {string} key - The keyboard key pressed
 * @returns {Object} Result {correct, complete, expected}
 */
export function checkInput(key) {
  const expectedKey = state.keys[state.currentIndex];
  
  console.log(`[checkInput] key='${key}', expected='${expectedKey}', currentIndex=${state.currentIndex}, totalKeys=${state.keys.length}`);
  
  // Handle first tone (space) - can be space or auto-advance
  if (expectedKey === ' ' && key === ' ') {
    // User explicitly pressed space for first tone
    state.currentIndex++;
    const complete = state.currentIndex >= state.keys.length;
    console.log(`[checkInput] Space pressed, complete=${complete}`);
    return { correct: true, complete, expected: ' ' };
  }
  
  // Check if this is trying to start a new word (first tone auto-advance)
  if (expectedKey === ' ' && key !== ' ') {
    // Treat previous word as complete, but don't process current key yet
    // The caller should handle loading next word
    console.log(`[checkInput] Auto-advance on space, nextKey='${key}'`);
    return { correct: true, complete: true, expected: ' ', autoAdvance: true, nextKey: key };
  }
  
  // Normal key validation
  if (key === expectedKey) {
    state.currentIndex++;
    const complete = state.currentIndex >= state.keys.length;
    console.log(`[checkInput] Correct! complete=${complete}, newIndex=${state.currentIndex}`);
    return { correct: true, complete, expected: expectedKey };
  }

  // Mark that user made an error
  state.hasErrors = true;
  console.log(`[checkInput] Incorrect key - errors tracked`);
  return { correct: false, complete: false, expected: expectedKey };
}

/**
 * Get current practice state (for debugging/display)
 * @returns {Object} Current state
 */
export function getState() {
  return { ...state };
}

/**
 * Reset practice state
 */
export function reset() {
  state.word = '';
  state.zhuyin = [];
  state.keys = [];
  state.currentIndex = 0;
}
