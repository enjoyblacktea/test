/**
 * Practice Logic Module
 * Manages practice state and validates user input
 */

// Practice state
const state = {
  word: '',         // Current Chinese character
  zhuyin: [],       // Array of zhuyin symbols for current word
  keys: [],         // Array of expected keyboard keys
  currentIndex: 0   // Current position in the input sequence
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

  // Update display
  updateDisplay();

  console.log('Loaded word:', state.word, 'zhuyin:', state.zhuyin, 'keys:', state.keys);
}

/**
 * Update the DOM to display current word
 */
function updateDisplay() {
  const display = document.getElementById('practice-word');
  if (display) {
    display.textContent = state.word;
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
  
  console.log(`[checkInput] Incorrect key`);
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
