/**
 * Main entry point for the redesigned Zhuyin practice application
 * Initializes all modules and sets up the application
 */

// Import backend authentication module
import * as auth from './modules/auth-backend.js';

// Import new modules
// import { ParticleSystem } from './modules/particle-system.js'; // REMOVED: Particle system removed for dark theme
// import { StatsTracker } from './modules/stats-tracker.js'; // REMOVED: Stats panel removed
import { AnimationController } from './modules/animations.js';

// Import existing modules
import * as keyboard from './modules/keyboard.js';
import * as inputHandler from './modules/input-handler.js';

// DOM Elements
let logoutButton = null;

// Global instances
// let particleSystem = null; // REMOVED: Particle system removed for dark theme
// let statsTracker = null; // REMOVED: Stats panel removed
let animationController = null;

/**
 * Initialize the practice application modules
 */
async function initPracticeApp() {
    console.log('Initializing redesigned Zhuyin practice app...');

    // REMOVED: Particle system initialization (particle system removed for dark theme)
    // const canvas = document.getElementById('particles-canvas');
    // if (canvas) {
    //     particleSystem = new ParticleSystem(canvas);
    //     console.log('Particle system initialized');
    // }

    // REMOVED: Stats tracker initialization (stats panel removed)
    // statsTracker = new StatsTracker();
    // console.log('Stats tracker initialized');

    // Initialize animation controller
    animationController = new AnimationController();
    console.log('Animation controller initialized');

    // REMOVED: Page load animation (no title animation in dark theme)
    // animationController.triggerPageLoadAnimation();

    // Initialize existing modules
    keyboard.init();

    // Initialize input handler with dependencies
    inputHandler.init({
        // particleSystem, // REMOVED: Particle system removed for dark theme
        // statsTracker, // REMOVED: Stats panel removed
        animationController
    });

    // REMOVED: Stats display and reset button (stats panel removed)
    // updateStatsDisplay();
    // setupResetButton();

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

// REMOVED: Stats display and reset functions (stats panel removed)
// function updateStatsDisplay() { ... }
// function setupResetButton() { ... }

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

/**
 * Handle logout button click
 */
async function handleLogout() {
    console.log('Logging out...');

    try {
        // Call backend logout
        await auth.logout();
        console.log('Logout successful');

        // Redirect to login page
        window.location.href = './login.html';
    } catch (error) {
        console.error('Logout error:', error);
        // Even if logout fails, redirect to login
        window.location.href = './login.html';
    }
}

/**
 * Main initialization function
 */
function init() {
    console.log('Initializing Zhuyin practice app...');

    // Check authentication status
    if (!auth.isAuthenticated()) {
        console.log('User not authenticated, redirecting to login...');
        // Redirect to login page
        window.location.href = './login.html';
        return;
    }

    console.log('User authenticated, initializing practice app...');

    // Get logout button reference
    logoutButton = document.getElementById('logout-button');

    // Attach logout button handler
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    // Initialize practice app
    initPracticeApp();

    console.log('App initialization complete');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
