## ADDED Requirements

### Requirement: Display real-time practice statistics
The system SHALL show a statistics panel that displays current learning progress metrics in real-time.

#### Scenario: Stats panel shows words practiced
- **WHEN** the stats panel is rendered
- **THEN** the system displays total number of words practiced in current session
- **THEN** the count updates immediately when a word is completed

#### Scenario: Stats panel shows accuracy percentage
- **WHEN** the stats panel is rendered
- **THEN** the system displays accuracy percentage (correct inputs / total inputs × 100)
- **THEN** the percentage updates immediately after each input attempt
- **THEN** the percentage displays as integer (rounded) with % symbol

#### Scenario: Stats panel shows current streak
- **WHEN** the stats panel is rendered
- **THEN** the system displays current streak (consecutive correct inputs)
- **THEN** the streak increments on each correct input
- **THEN** the streak resets to 0 on first incorrect input

### Requirement: Track correct and incorrect inputs
The system SHALL maintain counters for correct and incorrect inputs to calculate accuracy.

#### Scenario: Correct input increments counters
- **WHEN** user inputs a correct zhuyin symbol
- **THEN** the system increments correctInputs counter by 1
- **THEN** the system increments totalInputs counter by 1
- **THEN** the system increments currentStreak counter by 1

#### Scenario: Incorrect input increments total only
- **WHEN** user inputs an incorrect zhuyin symbol
- **THEN** the system increments totalInputs counter by 1
- **THEN** the system does NOT increment correctInputs
- **THEN** the system resets currentStreak to 0

#### Scenario: Initial state starts at zero
- **WHEN** stats tracking begins for the first time
- **THEN** correctInputs = 0
- **THEN** totalInputs = 0
- **THEN** currentStreak = 0
- **THEN** accuracy displays as 100% (no errors yet)

### Requirement: Track longest streak achieved
The system SHALL record and display the longest consecutive correct input streak achieved in the session.

#### Scenario: Longest streak updates when surpassed
- **WHEN** currentStreak exceeds longestStreak
- **THEN** the system updates longestStreak = currentStreak
- **THEN** the stats panel displays the new longest streak value

#### Scenario: Longest streak persists after reset
- **WHEN** currentStreak resets to 0 (due to incorrect input)
- **THEN** the system maintains longestStreak value unchanged
- **THEN** longestStreak remains the maximum achieved value

### Requirement: Persist statistics to LocalStorage
The system SHALL save statistics data to browser LocalStorage for persistence across page reloads.

#### Scenario: Stats save after each update
- **WHEN** any statistic value changes
- **THEN** the system saves the entire stats object to LocalStorage
- **THEN** the storage key is 'zhuyin-practice-stats'

#### Scenario: Stats load on page initialization
- **WHEN** the page loads
- **THEN** the system attempts to read stats from LocalStorage
- **THEN** if data exists, the system restores previous stats
- **THEN** if no data exists, the system initializes with default values (all zeros)

#### Scenario: LocalStorage data structure
- **WHEN** stats are saved to LocalStorage
- **THEN** the data is stored as JSON string
- **THEN** the object contains: totalWords, correctInputs, totalInputs, currentStreak, longestStreak
- **THEN** the object includes lastPracticeDate and sessionStart timestamps

### Requirement: Provide visual display for statistics
The system SHALL present statistics in a visually appealing panel with icons and labels.

#### Scenario: Each stat has an icon
- **WHEN** the stats panel is rendered
- **THEN** each statistic displays with a representative icon/emoji
- **THEN** icons are: 📖 (words), ✨ (accuracy), 🔥 (streak)

#### Scenario: Stats have clear labels
- **WHEN** the stats panel is rendered
- **THEN** each stat displays a label below the value
- **THEN** labels are: "已練習" (practiced), "準確率" (accuracy), "連續正確" (streak)

#### Scenario: Large values are emphasized
- **WHEN** the stats panel is rendered
- **THEN** the numeric values use larger font size than labels
- **THEN** values use bold or medium weight font

#### Scenario: Stats panel uses theme colors
- **WHEN** the stats panel is styled
- **THEN** the system applies colors from the calligraphy theme palette
- **THEN** the panel background, borders, and text use cohesive theme colors

### Requirement: Provide reset functionality for statistics
The system SHALL allow users to reset their statistics to start fresh.

#### Scenario: Reset button is available
- **WHEN** the stats panel is rendered
- **THEN** the system displays a reset button or link
- **THEN** the button is clearly labeled (e.g., "重置統計")

#### Scenario: Reset requires confirmation
- **WHEN** user clicks the reset button
- **THEN** the system shows a confirmation dialog
- **THEN** the dialog warns that this action cannot be undone

#### Scenario: Confirmed reset clears all stats
- **WHEN** user confirms the reset action
- **THEN** the system sets all counters to 0 (totalWords, correctInputs, totalInputs, streaks)
- **THEN** the system updates LocalStorage with reset values
- **THEN** the stats panel immediately reflects the reset (all zeros)

#### Scenario: Cancelled reset maintains current stats
- **WHEN** user cancels the reset confirmation
- **THEN** the system does not modify any statistics
- **THEN** the confirmation dialog closes
- **THEN** the stats panel remains unchanged
