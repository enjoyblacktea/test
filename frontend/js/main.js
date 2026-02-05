/**
 * Main Application Entry Point
 * Initializes all modules and starts the practice session
 */

import * as keyboard from './modules/keyboard.js';
import * as inputHandler from './modules/input-handler.js';

/**
 * Initialize the application
 */
async function init() {
  console.log('Initializing Zhuyin Practice App...');

  try {
    // Initialize keyboard display
    keyboard.init();
    console.log('✓ Keyboard initialized');

    // Initialize input handler
    inputHandler.init();
    console.log('✓ Input handler initialized');

    // Load first word
    await inputHandler.loadFirstWord();
    console.log('✓ First word loaded');

    console.log('Application ready!');
  } catch (error) {
    console.error('Failed to initialize application:', error);
    
    // Show error message to user
    const practiceWord = document.getElementById('practice-word');
    if (practiceWord) {
      practiceWord.textContent = '無法載入練習資料';
      practiceWord.style.color = 'red';
    }
  }
}

// Start the app when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
