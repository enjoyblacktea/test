/**
 * Virtual Keyboard Module
 * Renders the zhuyin keyboard and handles visual feedback
 */

import { keyToZhuyin } from './zhuyin-map.js';

// Keyboard layout definition - matches physical QWERTY keyboard
const keyboardLayout = [
  // Row 1: Number row (1-0, -)
  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
  // Row 2: QWERTY row
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  // Row 3: ASDF row
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
  // Row 4: ZXCV row
  ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
  // Row 5: Space bar
  [' ']
];

let currentHighlightedKey = null;
let highlightTimeout = null;

/**
 * Render the virtual keyboard
 */
export function render() {
  const keyboardContainer = document.getElementById('keyboard');
  if (!keyboardContainer) {
    console.error('Keyboard container not found');
    return;
  }

  keyboardContainer.innerHTML = '';

  keyboardLayout.forEach((row, rowIndex) => {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'keyboard-row';

    row.forEach(key => {
      const keyDiv = document.createElement('div');
      keyDiv.className = 'key';
      keyDiv.dataset.key = key;

      // Special styling for spacebar
      if (key === ' ') {
        keyDiv.classList.add('spacebar');
      }

      // Create zhuyin symbol display
      const zhuyinSpan = document.createElement('span');
      zhuyinSpan.className = 'zhuyin';
      const zhuyinSymbol = keyToZhuyin[key];
      zhuyinSpan.textContent = zhuyinSymbol || (key === ' ' ? '(一聲)' : '');

      // Create letter display
      const letterSpan = document.createElement('span');
      letterSpan.className = 'letter';
      letterSpan.textContent = key === ' ' ? 'Space' : key;

      keyDiv.appendChild(zhuyinSpan);
      keyDiv.appendChild(letterSpan);
      rowDiv.appendChild(keyDiv);
    });

    keyboardContainer.appendChild(rowDiv);
  });

  console.log('Keyboard rendered');
}

/**
 * Highlight a key on the virtual keyboard
 * @param {string} key - The keyboard key to highlight
 */
export function highlightKey(key) {
  // Clear any existing highlight
  clearHighlight();

  // Find and highlight the key
  const keyElement = document.querySelector(`.key[data-key="${key}"]`);
  if (keyElement) {
    keyElement.classList.add('highlighted');
    currentHighlightedKey = keyElement;

    // Auto-clear after 200ms
    highlightTimeout = setTimeout(() => {
      clearHighlight();
    }, 200);
  }
}

/**
 * Clear the current highlight
 */
export function clearHighlight() {
  if (highlightTimeout) {
    clearTimeout(highlightTimeout);
    highlightTimeout = null;
  }

  if (currentHighlightedKey) {
    currentHighlightedKey.classList.remove('highlighted');
    currentHighlightedKey = null;
  }
}

/**
 * Initialize the keyboard module
 */
export function init() {
  render();
}
