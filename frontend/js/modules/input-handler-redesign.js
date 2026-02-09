/**
 * Input Handler Module (Redesigned with Particle Effects and Stats)
 * Listens for keyboard input and coordinates validation, feedback, particles, and statistics
 */

import * as keyboard from './keyboard.js';
import * as practice from './practice.js';
import { isZhuyinKey } from './zhuyin-map.js';

let particleSystem = null;
let statsTracker = null;
let animationController = null;
let progressFillElement = null;
let zhuyinDisplayElement = null;

/**
 * Initialize input handler with dependencies
 * @param {Object} deps - Dependencies
 * @param {ParticleSystem} deps.particleSystem - Particle system instance
 * @param {StatsTracker} deps.statsTracker - Stats tracker instance
 * @param {AnimationController} deps.animationController - Animation controller instance
 */
export function init(deps = {}) {
    particleSystem = deps.particleSystem;
    statsTracker = deps.statsTracker;
    animationController = deps.animationController;
    progressFillElement = document.getElementById('progress-fill');
    zhuyinDisplayElement = document.getElementById('zhuyin-display');

    // Listen for keydown events on the document
    document.addEventListener('keydown', handleKeyDown);
    console.log('Input handler (redesigned) initialized');
}

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

    // Get key element for particle emission position
    const keyElement = document.querySelector(`.key[data-key="${key}"]`);

    // Check if input is correct
    const result = practice.checkInput(key);

    if (result.correct) {
        console.log('Correct input:', key);

        // Emit ink drop particles at key position
        if (particleSystem && keyElement) {
            const rect = keyElement.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            particleSystem.emitInkDrops(x, y);
        }

        // Record correct input in stats
        if (statsTracker) {
            statsTracker.recordCorrectInput();
            updateStatsDisplay();
        }

        // Update zhuyin display
        updateZhuyinDisplay();

        // Update progress bar
        updateProgressBar(result.progress);

        // Handle word completion
        if (result.complete) {
            console.log('Word complete!');

            // Emit fireworks at character position
            if (particleSystem) {
                const charElement = document.getElementById('practice-character');
                if (charElement) {
                    const rect = charElement.getBoundingClientRect();
                    const x = rect.left + rect.width / 2;
                    const y = rect.top + rect.height / 2;
                    particleSystem.emitFireworks(x, y);
                }
            }

            // Increment word count in stats
            if (statsTracker) {
                statsTracker.incrementWordCount();
                updateStatsDisplay();
            }

            // Wait briefly to let user see the complete zhuyin before loading next word
            await new Promise(resolve => setTimeout(resolve, 800));

            // If this was an auto-advance situation, handle the next key
            if (result.autoAdvance && result.nextKey) {
                // Load next word first
                await loadNextWord();
                // Then process the key that triggered auto-advance
                const nextEvent = new KeyboardEvent('keydown', { key: result.nextKey });
                await handleKeyDown(nextEvent);
            } else {
                // Normal completion - load next word
                await loadNextWord();
            }
        }
    } else {
        console.log('Incorrect input. Expected:', result.expected, 'Got:', key);

        // Record incorrect input in stats
        if (statsTracker) {
            statsTracker.recordIncorrectInput();
            updateStatsDisplay();
        }

        // No error feedback per specs - just ignore wrong input
    }
}

/**
 * Update progress bar visualization
 * @param {Object} progress - Progress data from practice module
 */
function updateProgressBar(progress) {
    if (!progressFillElement || !animationController || !progress) return;

    const { current, total } = progress;
    const percentage = total > 0 ? (current / total) * 100 : 0;

    animationController.updateProgressBar(progressFillElement, percentage);
}

/**
 * Reset progress bar to 0%
 */
function resetProgressBar() {
    if (!progressFillElement || !animationController) return;

    animationController.resetProgressBar(progressFillElement);
}

/**
 * Update zhuyin display to show progressively typed symbols
 * Reads current practice state and displays all correctly typed zhuyin symbols
 * @example
 * // After typing "ㄓ" and "ㄨ", displays "ㄓㄨ"
 * updateZhuyinDisplay();
 */
function updateZhuyinDisplay() {
    if (!zhuyinDisplayElement) return;

    const state = practice.getState();
    const typedZhuyin = state.zhuyin.slice(0, state.currentIndex);
    zhuyinDisplayElement.textContent = typedZhuyin.join('');
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

    // Pulse animation for updated values
    if (animationController) {
        if (elements.words) animationController.pulseElement(elements.words);
        if (elements.accuracy) animationController.pulseElement(elements.accuracy);
        if (elements.streak) animationController.pulseElement(elements.streak);
    }
}

/**
 * Load the next practice word
 */
async function loadNextWord() {
    try {
        // Reset progress bar before loading new word
        resetProgressBar();

        // Clear zhuyin display
        if (zhuyinDisplayElement) {
            zhuyinDisplayElement.textContent = '';
        }

        const wordData = await practice.fetchNextWord();
        practice.loadWord(wordData);

        // Trigger character animation if available
        if (animationController) {
            const charElement = document.getElementById('practice-character');
            if (charElement) {
                animationController.triggerPracticeCharacterAnimation(charElement);
            }
        }
    } catch (error) {
        console.error('Failed to load next word:', error);
    }
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
