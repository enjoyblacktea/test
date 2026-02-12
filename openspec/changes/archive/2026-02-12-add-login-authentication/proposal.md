## Why

目前任何人都可以直接進入注音練習頁面，缺乏使用者識別和存取控制機制。為了確保只有授權使用者能夠使用練習功能，需要新增登入驗證功能，要求使用者在進入練習前輸入正確的帳號密碼。

## What Changes

- 新增登入畫面，包含帳號和密碼輸入欄位
- 新增前端認證模組 (`auth.js`)，處理登入驗證邏輯
- 使用 LocalStorage 儲存登入狀態，實現持久化登入（remember me）
- 修改應用程式初始化流程，在 DOMContentLoaded 時檢查認證狀態
- 新增登出按鈕，允許使用者登出並返回登入畫面
- 採用預配置的單一帳號（帳號: `user`, 密碼: `1234`）
- 登入畫面樣式符合現有「筆墨童趣」書法主題

## Capabilities

### New Capabilities

- `user-authentication`: 使用者認證系統，包含登入驗證、登入狀態持久化（LocalStorage）、登出功能、以及預配置帳號管理

### Modified Capabilities

<!-- 無需修改現有 capability 的 REQUIREMENTS。現有的練習功能不改變行為規格，只是在認證後才可存取 -->

## Impact

**前端模組**:
- 新增 `frontend/js/modules/auth.js` - 認證模組（約 60 行）
- 修改 `frontend/js/main-redesign.js` - 加入認證流程和畫面切換邏輯（約 90 行新增/修改）

**HTML 結構**:
- 修改 `frontend/index-redesign.html` - 新增登入畫面區塊、修改練習畫面結構以支援顯示/隱藏切換、新增登出按鈕（約 50 行）

**CSS 樣式**:
- 新增 `frontend/styles/login.css` - 登入畫面樣式，符合書法主題（約 80 行）

**瀏覽器儲存**:
- 使用 LocalStorage 鍵 `zhuyin-practice-auth` 儲存認證狀態

**無後端影響** - 此為純前端認證實作，不涉及後端 API 修改
