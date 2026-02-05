/**
 * Zhuyin (Bopomofo) keyboard mapping
 * Maps keyboard keys to zhuyin symbols for Taiwan standard keyboard layout
 */

// Keyboard key to zhuyin symbol mapping
export const keyToZhuyin = {
  // Consonants - Row 1
  '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
  '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
  'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
  'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
  '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
  'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
  
  // Vowels
  'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
  '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
  '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
  '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
  '-': 'ㄦ',
  
  // Tones
  ' ': '', // First tone (no mark) - can be space or nothing
  '6': 'ˊ', // Second tone
  '3': 'ˇ', // Third tone
  '4': 'ˋ', // Fourth tone
  '7': '˙'  // Fifth tone (light/neutral)
};

// Reverse mapping: zhuyin symbol to keyboard key
export const zhuyinToKey = {};
for (const [key, zhuyin] of Object.entries(keyToZhuyin)) {
  if (zhuyin) { // Skip empty string for first tone
    zhuyinToKey[zhuyin] = key;
  }
}

// Add special case for first tone (space key)
zhuyinToKey[''] = ' ';

/**
 * Check if a key is a valid zhuyin input key
 * @param {string} key - The keyboard key
 * @returns {boolean} - True if valid zhuyin key
 */
export function isZhuyinKey(key) {
  return key in keyToZhuyin;
}

/**
 * Get zhuyin symbol for a keyboard key
 * @param {string} key - The keyboard key
 * @returns {string|null} - The zhuyin symbol or null if invalid
 */
export function getZhuyin(key) {
  return keyToZhuyin[key] || null;
}

/**
 * Get keyboard key for a zhuyin symbol
 * @param {string} zhuyin - The zhuyin symbol
 * @returns {string|null} - The keyboard key or null if invalid
 */
export function getKey(zhuyin) {
  return zhuyinToKey[zhuyin] || null;
}
