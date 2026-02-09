## Why（為什麼）

目前使用者在練習輸入注音時，雖然可以透過鍵盤高亮、粒子效果和進度條獲得回饋，但無法即時看到自己已經輸入的注音符號。這在輸入與視覺確認之間造成了斷層，使得學習者更難建立信心並逐字驗證自己的輸入進度。

## What Changes（變更內容）

- 在練習區域新增已輸入注音符號的即時顯示
- 隨著使用者輸入逐步顯示（例如：ㄓ → ㄓㄨ → ㄓㄨˋ）
- 完成字詞後保持顯示完整注音，直到載入下一個字
- 載入下一個練習字時自動清空顯示
- 使用現有的 `.zhuyin-display` CSS 樣式（無需新的 UI 設計）
- 整合至現有的 `input-handler-redesign.js` 輸入驗證流程

## Capabilities（能力規格）

### New Capabilities（新增能力）
- `realtime-input-feedback`：顯示已正確輸入的注音符號，提供即時的視覺確認回饋

### Modified Capabilities（修改的能力）
<!-- 無需修改現有能力規格。此功能整合現有驗證機制，但不改變其需求定義。 -->

## Impact（影響範圍）

**前端程式碼：**
- `frontend/js/modules/input-handler-redesign.js` - 新增注音顯示的 DOM 更新
  - 在 `init()` 中初始化注音顯示元素引用
  - 新增 `updateZhuyinDisplay()` 函式以顯示已輸入符號
  - 在 `handleKeyDown()` 每次正確輸入後呼叫更新
  - 在 `loadNextWord()` 載入新字時清空顯示

**CSS 樣式：**
- 無需變更 - `.zhuyin-display` 類別已存在於 `styles/redesign.css`

**HTML 結構：**
- 無需變更 - `<div id="zhuyin-display">` 已存在於 `index-redesign.html`

**相依性：**
- 從 `practice.getState()` 讀取狀態以取得當前輸入進度
- 無新增外部相依套件
