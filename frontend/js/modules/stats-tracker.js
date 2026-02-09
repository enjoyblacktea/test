/**
 * Statistics Tracker for Zhuyin Practice App
 * Tracks learning statistics and persists to LocalStorage
 * @module stats-tracker
 */

export class StatsTracker {
    /**
     * Create a statistics tracker
     */
    constructor() {
        this.storageKey = 'zhuyin-practice-stats';
        this.stats = null;
        this.load();
    }

    /**
     * Get default statistics structure
     * @returns {Object} Default stats object
     */
    getDefaultStats() {
        return {
            totalWords: 0,
            correctInputs: 0,
            totalInputs: 0,
            currentStreak: 0,
            longestStreak: 0,
            lastPracticeDate: new Date().toISOString().split('T')[0],
            sessionStart: new Date().toISOString()
        };
    }

    /**
     * Load statistics from LocalStorage
     */
    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (data) {
                this.stats = JSON.parse(data);
            } else {
                this.stats = this.getDefaultStats();
            }
        } catch (error) {
            console.error('Failed to load stats from LocalStorage:', error);
            this.stats = this.getDefaultStats();
        }
    }

    /**
     * Save statistics to LocalStorage
     */
    save() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.stats));
        } catch (error) {
            console.error('Failed to save stats to LocalStorage:', error);
        }
    }

    /**
     * Record a correct input
     * Increments correctInputs, totalInputs, and currentStreak
     * Updates longestStreak if current streak exceeds it
     */
    recordCorrectInput() {
        this.stats.correctInputs++;
        this.stats.totalInputs++;
        this.stats.currentStreak++;

        // Update longest streak if current exceeds it
        if (this.stats.currentStreak > this.stats.longestStreak) {
            this.stats.longestStreak = this.stats.currentStreak;
        }

        this.stats.lastPracticeDate = new Date().toISOString().split('T')[0];
        this.save();
    }

    /**
     * Record an incorrect input
     * Increments totalInputs and resets currentStreak
     */
    recordIncorrectInput() {
        this.stats.totalInputs++;
        this.stats.currentStreak = 0;

        this.stats.lastPracticeDate = new Date().toISOString().split('T')[0];
        this.save();
    }

    /**
     * Increment word count (when user completes a word)
     */
    incrementWordCount() {
        this.stats.totalWords++;
        this.save();
    }

    /**
     * Calculate accuracy percentage
     * @returns {number} Accuracy percentage (0-100)
     */
    getAccuracy() {
        if (this.stats.totalInputs === 0) {
            return 100;
        }
        return Math.round((this.stats.correctInputs / this.stats.totalInputs) * 100);
    }

    /**
     * Get all statistics
     * @returns {Object} Current stats object
     */
    getStats() {
        return { ...this.stats };
    }

    /**
     * Get total words practiced
     * @returns {number} Total words count
     */
    getTotalWords() {
        return this.stats.totalWords;
    }

    /**
     * Get current streak
     * @returns {number} Current streak count
     */
    getCurrentStreak() {
        return this.stats.currentStreak;
    }

    /**
     * Get longest streak
     * @returns {number} Longest streak count
     */
    getLongestStreak() {
        return this.stats.longestStreak;
    }

    /**
     * Reset all statistics to zero
     */
    reset() {
        this.stats = this.getDefaultStats();
        this.save();
    }

    /**
     * Update statistics display in the UI
     * @param {Object} elements - DOM elements for stats display
     * @param {HTMLElement} elements.words - Words count element
     * @param {HTMLElement} elements.accuracy - Accuracy element
     * @param {HTMLElement} elements.streak - Streak element
     */
    updateDisplay(elements) {
        if (elements.words) {
            elements.words.textContent = this.getTotalWords();
        }
        if (elements.accuracy) {
            elements.accuracy.textContent = `${this.getAccuracy()}%`;
        }
        if (elements.streak) {
            elements.streak.textContent = this.getCurrentStreak();
        }
    }
}
