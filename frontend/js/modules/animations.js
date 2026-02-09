/**
 * Animation Controller for Zhuyin Practice App
 * Manages CSS animations and provides animation control APIs
 * @module animations
 */

export class AnimationController {
    /**
     * Create an animation controller
     */
    constructor() {
        this.animationClasses = {
            fadeInUp: 'fade-in-up',
            brushStroke: 'practice-character--brush-writing',
            stampPress: 'stamp-press',
            inkSpread: 'ink-spread'
        };
    }

    /**
     * Trigger page load animations (title character stagger)
     * This is automatically handled by CSS, but can be retriggered if needed
     */
    triggerPageLoadAnimation() {
        const titleChars = document.querySelectorAll('.title-char');
        titleChars.forEach((char, index) => {
            char.style.setProperty('--char-index', index);
            // Force reflow to restart animation
            char.style.animation = 'none';
            setTimeout(() => {
                char.style.animation = '';
            }, 10);
        });
    }

    /**
     * Trigger practice character writing animation
     * @param {HTMLElement} element - The practice character element
     */
    triggerPracticeCharacterAnimation(element) {
        if (!element) return;

        // Remove any existing animation
        element.classList.remove(this.animationClasses.brushStroke);

        // Force reflow
        void element.offsetWidth;

        // Add animation class
        element.classList.add(this.animationClasses.brushStroke);

        // Remove class after animation completes
        setTimeout(() => {
            element.classList.remove(this.animationClasses.brushStroke);
        }, 1200);
    }

    /**
     * Update progress bar with smooth animation
     * @param {HTMLElement} progressFill - The progress fill element
     * @param {number} percentage - Progress percentage (0-100)
     * @param {number} duration - Animation duration in ms (default: 400ms)
     */
    updateProgressBar(progressFill, percentage, duration = 400) {
        if (!progressFill) return;

        // Ensure percentage is within bounds
        const clampedPercentage = Math.max(0, Math.min(100, percentage));

        // Update width with CSS transition
        progressFill.style.transition = `width ${duration}ms ease-out`;
        progressFill.style.width = `${clampedPercentage}%`;
    }

    /**
     * Reset progress bar to 0%
     * @param {HTMLElement} progressFill - The progress fill element
     * @param {number} duration - Animation duration in ms (default: 200ms)
     */
    resetProgressBar(progressFill, duration = 200) {
        if (!progressFill) return;

        // Fade out transition
        progressFill.style.transition = `width ${duration}ms ease-out, opacity ${duration}ms ease-out`;
        progressFill.style.opacity = '0.5';
        progressFill.style.width = '0%';

        // Restore opacity after reset
        setTimeout(() => {
            progressFill.style.opacity = '1';
        }, duration);
    }

    /**
     * Trigger keyboard key stamp press animation
     * @param {HTMLElement} keyElement - The keyboard key element
     */
    triggerKeyStampAnimation(keyElement) {
        if (!keyElement) return;

        // Add stamp press class
        keyElement.classList.add(this.animationClasses.stampPress);

        // Remove class after animation completes (matches CSS duration)
        setTimeout(() => {
            keyElement.classList.remove(this.animationClasses.stampPress);
        }, 300);
    }

    /**
     * Manage animation sequence (ensure animations play in correct order)
     * @param {Array<Function>} animationFunctions - Array of animation functions to execute in sequence
     * @param {number} delay - Delay between animations in ms (default: 100ms)
     */
    async playSequence(animationFunctions, delay = 100) {
        for (const animFn of animationFunctions) {
            await animFn();
            await this.sleep(delay);
        }
    }

    /**
     * Sleep utility for animation sequences
     * @param {number} ms - Milliseconds to sleep
     * @returns {Promise} Promise that resolves after delay
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Add pulse animation to an element (for value updates)
     * @param {HTMLElement} element - Element to pulse
     */
    pulseElement(element) {
        if (!element) return;

        element.classList.add('stats-panel__value--updated');

        setTimeout(() => {
            element.classList.remove('stats-panel__value--updated');
        }, 300);
    }
}
