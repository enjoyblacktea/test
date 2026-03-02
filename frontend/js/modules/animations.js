/**
 * Animation Controller for Zhuyin Practice App (Dark Theme - Simplified)
 * Manages simple CSS class-based animations for modern dark theme
 * @module animations
 */

export class AnimationController {
    /**
     * Create an animation controller
     */
    constructor() {
        this.animationClasses = {
            correctPulse: 'correct-pulse',
            completionGlow: 'completion-glow',
            fadeIn: 'fade-in'
        };
    }

    /**
     * Trigger correct input pulse animation on practice character
     * @param {HTMLElement} element - The practice character element
     */
    triggerCorrectPulse(element) {
        if (!element) return;

        // Remove any existing animation
        element.classList.remove(this.animationClasses.correctPulse);

        // Force reflow to restart animation
        void element.offsetWidth;

        // Add animation class
        element.classList.add(this.animationClasses.correctPulse);

        // Remove class after animation completes (0.3s as per spec)
        setTimeout(() => {
            element.classList.remove(this.animationClasses.correctPulse);
        }, 300);
    }

    /**
     * Trigger completion glow animation on practice card
     * @param {HTMLElement} element - The practice card element
     */
    triggerCompletionGlow(element) {
        if (!element) return;

        // Remove any existing animation
        element.classList.remove(this.animationClasses.completionGlow);

        // Force reflow to restart animation
        void element.offsetWidth;

        // Add animation class
        element.classList.add(this.animationClasses.completionGlow);

        // Remove class after animation completes (0.5s as per spec)
        setTimeout(() => {
            element.classList.remove(this.animationClasses.completionGlow);
        }, 500);
    }

    /**
     * Trigger fade-in animation on practice character (for new words)
     * @param {HTMLElement} element - The practice character element
     */
    triggerPracticeCharacterAnimation(element) {
        if (!element) return;

        // Remove any existing animation
        element.classList.remove(this.animationClasses.fadeIn);

        // Force reflow
        void element.offsetWidth;

        // Add animation class
        element.classList.add(this.animationClasses.fadeIn);

        // Remove class after animation completes (0.3s as per spec)
        setTimeout(() => {
            element.classList.remove(this.animationClasses.fadeIn);
        }, 300);
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
