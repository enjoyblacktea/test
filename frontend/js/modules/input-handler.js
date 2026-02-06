/**
 * Input Handler Module
 * Listens for keyboard input and coordinates validation and feedback
 */

import * as keyboard from './keyboard.js';
import * as practice from './practice.js';
import { isZhuyinKey } from './zhuyin-map.js';

/**
 * Handle keydown events
 * @param {KeyboardEvent} event - The keyboard event
 */
async function handleKeyDown(event) {
  const key = event.key;

  // Ignore non-zhuyin keys
  if (!isZhuyinKey(key)) {
    return;
  }

  // Prevent default browser behavior for zhuyin keys (e.g., '/' triggering quick find)
  event.preventDefault();

  // Highlight the key on virtual keyboard
  keyboard.highlightKey(key);

  // Check if input is correct
  const result = practice.checkInput(key);

  if (result.correct) {
    console.log('Correct input:', key);

    // Handle word completion
    if (result.complete) {
      console.log('Word complete!');
      
      // If this was an auto-advance situation, handle the next key
      if (result.autoAdvance && result.nextKey) {
        // Load next word first
        await loadNextWord();
        // Then process the key that triggered auto-advance
        // by recursing with the next key
        const nextEvent = new KeyboardEvent('keydown', { key: result.nextKey });
        await handleKeyDown(nextEvent);
      } else {
        // Normal completion - load next word
        await loadNextWord();
      }
    }
  } else {
    console.log('Incorrect input. Expected:', result.expected, 'Got:', key);
    // No error feedback per specs - just ignore wrong input
  }
}

/**
 * Load the next practice word
 */
async function loadNextWord() {
  try {
    const wordData = await practice.fetchNextWord();
    practice.loadWord(wordData);
  } catch (error) {
    console.error('Failed to load next word:', error);
    // Could show error message to user here
  }
}

/**
 * Initialize input handler
 */
export function init() {
  // Listen for keydown events on the document
  document.addEventListener('keydown', handleKeyDown);
  console.log('Input handler initialized');
}

/**
 * Remove event listeners (for cleanup)
 */
export function cleanup() {
  document.removeEventListener('keydown', handleKeyDown);
}

/**
 * Trigger loading the first word (exposed for main.js)
 */
export async function loadFirstWord() {
  await loadNextWord();
}
