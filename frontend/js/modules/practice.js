/**
 * Practice Logic Module
 * Manages practice state and validates user input
 */

// Practice state
const state = {
  word: '',         // Current Chinese character
  zhuyin: [],       // Array of zhuyin symbols for current word
  keys: [],         // Array of expected keyboard keys
  currentIndex: 0,  // Current position in the input sequence
  startTime: null,  // Practice start time (Date object)
  endTime: null,    // Practice end time (Date object)
  hasError: false   // Whether any incorrect key was pressed
};

/**
 * Fetch next word from API
 * @returns {Promise<Object>} Word data from API
 */
export async function fetchNextWord() {
  try {
    const response = await fetch('http://localhost:5000/api/words/random');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching word:', error);
    throw error;
  }
}

/**
 * Load a new word into the practice state
 * @param {Object} data - Word data {word, zhuyin, keys}
 */
export function loadWord(data) {
  state.word = data.word;
  state.zhuyin = data.zhuyin;
  state.keys = data.keys;
  state.currentIndex = 0;

  // Reset timing and correctness tracking
  state.startTime = new Date();
  state.endTime = null;
  state.hasError = false;

  // Update display
  updateDisplay();
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

  // Handle first tone (space) - can be space or auto-advance
  if (expectedKey === ' ' && key === ' ') {
    // User explicitly pressed space for first tone
    state.currentIndex++;
    const complete = state.currentIndex >= state.keys.length;

    // Set end time when word is complete
    if (complete) {
      state.endTime = new Date();
    }

    return { correct: true, complete, expected: ' ' };
  }

  // Check if this is trying to start a new word (first tone auto-advance)
  if (expectedKey === ' ' && key !== ' ') {
    // Treat previous word as complete, but don't process current key yet
    // The caller should handle loading next word
    // Set end time for completed word
    state.endTime = new Date();

    return { correct: true, complete: true, expected: ' ', autoAdvance: true, nextKey: key };
  }
  
  // Normal key validation
  if (key === expectedKey) {
    state.currentIndex++;
    const complete = state.currentIndex >= state.keys.length;

    // Set end time when word is complete
    if (complete) {
      state.endTime = new Date();
    }

    return { correct: true, complete, expected: expectedKey };
  }

  // Mark as having error
  state.hasError = true;

  return { correct: false, complete: false, expected: expectedKey };
}

/**
 * Get current practice state (for debugging/display)
 * @returns {Object} Current state with isCorrect computed
 */
export function getState() {
  return {
    ...state,
    isCorrect: !state.hasError  // Compute isCorrect based on hasError
  };
}

/**
 * Reset practice state
 */
export function reset() {
  state.word = '';
  state.zhuyin = [];
  state.keys = [];
  state.currentIndex = 0;
  state.startTime = null;
  state.endTime = null;
  state.hasError = false;
}
