## Why

習慣其他輸入法（如拼音、倉頡）的使用者想學習注音輸入法，但缺乏一個簡單、可測試的練習工具。建立一個最小可行的練習網站，讓使用者能夠看中文字並練習輸入對應的注音符號。

## What Changes

- 新增注音輸入法練習網站的 MVP 功能
- 提供看中文字打注音的核心練習流程
- 顯示虛擬注音鍵盤供參考
- 提供按鍵視覺回饋（高亮按下的鍵）
- 前端使用 Vanilla JS + HTML + CSS，後端使用 Python Flask
- 每個模組可獨立測試

## Capabilities

### New Capabilities
- `zhuyin-keyboard-display`: 顯示注音鍵盤配置和按鍵視覺回饋
- `zhuyin-input-validation`: 驗證使用者輸入的注音是否正確
- `practice-word-api`: 提供練習用的中文字詞和對應注音資料

### Modified Capabilities
<!-- 無現有功能需要修改 -->

## Impact

- 新增 `frontend/` 目錄：HTML、CSS、JavaScript 模組
- 新增 `backend/` 目錄：Flask API、練習資料
- 新增 `tests/` 目錄：前端和後端測試
- 每個模組可獨立測試，確保功能正確性
