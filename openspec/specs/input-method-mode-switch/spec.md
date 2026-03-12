## ADDED Requirements

### Requirement: Toggle input method mode in header
系統必須（SHALL）在練習頁面標頭提供注音 / 雙拼模式切換按鈕，讓使用者可隨時切換輸入法。

#### Scenario: Toggle buttons rendered
- **WHEN** 練習頁面載入
- **THEN** 標頭顯示兩個模式按鈕：「注音」與「雙拼」
- **THEN** 當前模式的按鈕以視覺方式標示為選中狀態（高亮）
- **THEN** 非選中按鈕保持正常樣式

#### Scenario: Switch to shuangpin mode
- **WHEN** 使用者點擊「雙拼」按鈕
- **THEN** 系統切換至雙拼模式
- **THEN** 「雙拼」按鈕顯示選中樣式
- **THEN** 頁面重新載入一個雙拼字庫的練習字

#### Scenario: Switch to zhuyin mode
- **WHEN** 使用者點擊「注音」按鈕
- **THEN** 系統切換至注音模式
- **THEN** 「注音」按鈕顯示選中樣式
- **THEN** 頁面重新載入一個注音字庫的練習字

### Requirement: Persist mode preference in localStorage
系統必須（SHALL）將使用者的輸入法模式偏好儲存於 `localStorage`，在頁面重新整理後保持選擇。

#### Scenario: Mode saved on switch
- **WHEN** 使用者切換輸入法模式
- **THEN** 系統將新模式值（`'zhuyin'` 或 `'shuangpin'`）存入 `localStorage['inputMethod']`

#### Scenario: Mode restored on load
- **WHEN** 使用者重新整理或開啟新分頁
- **THEN** 系統從 `localStorage['inputMethod']` 讀取上次選擇的模式
- **THEN** 頁面以儲存的模式初始化

#### Scenario: Default mode
- **WHEN** `localStorage` 中無模式記錄（首次使用）
- **THEN** 系統預設為注音模式（`'zhuyin'`）

### Requirement: useInputMethod hook manages mode state
系統必須（SHALL）透過 `useInputMethod` hook 集中管理輸入法模式狀態，供頁面元件使用。

#### Scenario: Hook provides mode and setter
- **WHEN** 元件呼叫 `useInputMethod()`
- **THEN** hook 回傳當前模式值（`'zhuyin'` | `'shuangpin'`）
- **THEN** hook 回傳切換模式的函式
- **THEN** 切換函式同步更新 state 並寫入 localStorage
