/**
 * Main entry point for the redesigned Zhuyin practice application
 * Initializes all modules and sets up the application
 */

// Import new modules
import { ParticleSystem } from './modules/particle-system.js';
import { StatsTracker } from './modules/stats-tracker.js';
import { AnimationController } from './modules/animations.js';

// Import existing modules
import * as keyboard from './modules/keyboard.js';
import * as practice from './modules/practice.js';
import * as inputHandler from './modules/input-handler-redesign.js';

// Global instances
let particleSystem = null;
let statsTracker = null;
let animationController = null;

/**
 * Initialize the application
 */
async function init() {
    console.log('Initializing redesigned Zhuyin practice app...');

    // Initialize particle system
    const canvas = document.getElementById('particles-canvas');
    if (canvas) {
        particleSystem = new ParticleSystem(canvas);
        console.log('Particle system initialized');
    }

    // Initialize stats tracker
    statsTracker = new StatsTracker();
    console.log('Stats tracker initialized');

    // Initialize animation controller
    animationController = new AnimationController();
    console.log('Animation controller initialized');

    // Trigger page load animations
    animationController.triggerPageLoadAnimation();

    // Initialize existing modules
    keyboard.init();

    // Initialize input handler with dependencies
    inputHandler.init({
        particleSystem,
        statsTracker,
        animationController
    });

    // Load initial stats display
    updateStatsDisplay();

    // Set up reset button event listener
    setupResetButton();

    // Load first practice word
    try {
        await inputHandler.loadFirstWord();
        console.log('First word loaded');
    } catch (error) {
        console.error('Failed to load first word:', error);
        showError('無法載入練習字。請確認後端伺服器正在運行。');
    }

    console.log('App initialization complete');
}

/**
 * Update statistics display in UI
 */
function updateStatsDisplay() {
    if (!statsTracker) return;

    const elements = {
        words: document.getElementById('stat-words'),
        accuracy: document.getElementById('stat-accuracy'),
        streak: document.getElementById('stat-streak')
    };

    statsTracker.updateDisplay(elements);
}

/**
 * Setup reset button event listener
 */
function setupResetButton() {
    const resetButton = document.getElementById('reset-stats');
    if (!resetButton) return;

    resetButton.addEventListener('click', () => {
        // Show confirmation dialog
        const confirmed = confirm(
            '確定要重置所有統計資料嗎？\n' +
            '這個動作無法復原。\n\n' +
            '目前統計：\n' +
            `已練習：${statsTracker.getTotalWords()} 字\n` +
            `準確率：${statsTracker.getAccuracy()}%\n` +
            `最長連續：${statsTracker.getLongestStreak()}`
        );

        if (confirmed) {
            // Reset stats
            statsTracker.reset();

            // Update display
            updateStatsDisplay();

            // Show success feedback
            alert('統計資料已重置！');

            console.log('Stats reset by user');
        }
    });
}

/**
 * Show error message to user
 * @param {string} message - Error message
 */
function showError(message) {
    const characterElement = document.getElementById('practice-character');
    if (characterElement) {
        characterElement.textContent = message;
        characterElement.style.fontSize = '1.5rem';
        characterElement.style.color = 'var(--color-vermillion)';
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
