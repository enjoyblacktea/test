/**
 * Main entry point for the redesigned Zhuyin practice application
 * Initializes all modules and sets up the application
 */

// Import authentication module
import * as auth from './modules/auth.js';

// Import new modules
import { ParticleSystem } from './modules/particle-system.js';
import { StatsTracker } from './modules/stats-tracker.js';
import { AnimationController } from './modules/animations.js';

// Import existing modules
import * as keyboard from './modules/keyboard.js';
import * as practice from './modules/practice.js';
import * as inputHandler from './modules/input-handler-redesign.js';

// DOM Elements
let loginScreen = null;
let practiceScreen = null;
let loginForm = null;
let usernameInput = null;
let passwordInput = null;
let loginError = null;
let logoutButton = null;

// Global instances
let particleSystem = null;
let statsTracker = null;
let animationController = null;

/**
 * Show login screen and hide practice screen
 */
function showLoginScreen() {
    if (loginScreen) loginScreen.classList.remove('hidden');
    if (practiceScreen) practiceScreen.classList.add('hidden');
}

/**
 * Show practice screen and hide login screen
 */
function showPracticeScreen() {
    if (loginScreen) loginScreen.classList.add('hidden');
    if (practiceScreen) practiceScreen.classList.remove('hidden');
}

/**
 * Initialize the practice application modules
 */
async function initPracticeApp() {
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

/**
 * Handle login form submission
 */
function handleLoginSubmit(event) {
    event.preventDefault();

    const username = usernameInput.value;
    const password = passwordInput.value;

    // Attempt login
    if (auth.login(username, password)) {
        console.log('Login successful');
        // Show practice screen and initialize app
        showPracticeScreen();
        initPracticeApp();
    } else {
        console.log('Login failed');
        // Show error message
        showLoginError('帳號或密碼錯誤');
        // Clear password field
        passwordInput.value = '';
    }
}

/**
 * Show login error message with fade animation
 * @param {string} message - Error message to display
 */
function showLoginError(message) {
    if (!loginError) return;

    loginError.textContent = message;
    loginError.classList.remove('hide');
    loginError.classList.add('show');

    // Auto-hide after 3 seconds
    setTimeout(() => {
        loginError.classList.remove('show');
        loginError.classList.add('hide');
    }, 3000);
}

/**
 * Handle logout button click
 */
function handleLogout() {
    console.log('Logging out...');
    // Clear authentication state
    auth.logout();
    // Show login screen
    showLoginScreen();
}

/**
 * Main initialization function
 */
function init() {
    console.log('Initializing Zhuyin practice app with authentication...');

    // Get DOM element references
    loginScreen = document.getElementById('login-screen');
    practiceScreen = document.getElementById('practice-screen');
    loginForm = document.getElementById('login-form');
    usernameInput = document.getElementById('username');
    passwordInput = document.getElementById('password');
    loginError = document.getElementById('login-error');
    logoutButton = document.getElementById('logout-button');

    // Check authentication status
    if (auth.checkAuth()) {
        console.log('User already authenticated');
        // Show practice screen
        showPracticeScreen();
        // Initialize practice app
        initPracticeApp();
    } else {
        console.log('User not authenticated, showing login screen');
        // Show login screen
        showLoginScreen();
        // Attach login form handler
        if (loginForm) {
            loginForm.addEventListener('submit', handleLoginSubmit);
        }
    }

    // Attach logout button handler
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    console.log('App initialization complete');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
