## Why

`typing_attempts` 目前只記錄整個字的對錯，無法得知使用者在哪個注音鍵上出錯。新增 `keystroke_events` 表來記錄每一次按鍵，讓後續分析能定位到具體的錯誤按鍵。

## What Changes

- 新增 `keystroke_events` 資料表，以 `attempt_id` 為外鍵關聯 `typing_attempts`
- 擴充 `POST /api/attempts` 請求 body，接受可選的 `keystrokes` 陣列（向下相容）
- 後端在同一 DB transaction 中寫入 `typing_attempts` 和 `keystroke_events`
- 前端 `practice.js` 在每次按鍵時累積 keystroke 紀錄，字完成時一起送出

## Capabilities

### New Capabilities

- `keystroke-recording`: 記錄使用者在每次練習嘗試中的逐鍵輸入，包含按鍵值、順序、時間戳及是否正確

### Modified Capabilities

（無：現有規格的需求不變，此次變更為新增能力）

## Impact

- **資料庫**：新增 `keystroke_events` 表與對應 index，需執行 migration
- **後端**：`backend/services/attempt_service.py`、`backend/routes/attempts.py`、`backend/migrations/init_db.sql`
- **前端**：`frontend/js/modules/practice.js`（input-handler.js 不需改動）
- **API**：`POST /api/attempts` 請求 body 擴充（選填欄位，不破壞現有客戶端）
