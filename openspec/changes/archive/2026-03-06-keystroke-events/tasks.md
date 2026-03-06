## 1. 資料庫 Migration

- [x] 1.1 在 `backend/migrations/init_db.sql` 追加 `CREATE TABLE IF NOT EXISTS keystroke_events` 定義（含 FK、CASCADE DELETE、`idx_keystroke_attempt` index）

## 2. 後端 — attempt_service

- [x] 2.1 修改 `backend/services/attempt_service.py` 的 `record_attempt()`，新增選填參數 `keystrokes: list | None = None`
- [x] 2.2 將 `record_attempt()` 的 DB 寫入改為手動管理 connection + transaction（取得 connection → insert typing_attempts → batch insert keystroke_events → commit）
- [x] 2.3 若 `keystrokes` 為 None 或空串列，跳過 keystroke insert，僅寫入 typing_attempts（向下相容）

## 3. 後端 — attempts route

- [x] 3.1 修改 `backend/routes/attempts.py` 的 `record_attempt()`，從 request body 讀取選填的 `keystrokes` 陣列
- [x] 3.2 將 `keystrokes` 傳入 `attempt_service.record_attempt()`

## 4. 前端 — practice.js

- [x] 4.1 在 `state` 物件新增 `keystrokes: []` 欄位
- [x] 4.2 在 `loadWord()` 中重置 `state.keystrokes = []`
- [x] 4.3 在 `checkInput()` 每次按鍵後，push `{ key: key, order: state.keystrokes.length, typed_at: new Date().toISOString(), is_correct: <result> }` 到 `state.keystrokes`
- [x] 4.4 修改 `recordAttempt()` 將 `state.keystrokes` 加入 API request body 的 `keystrokes` 欄位

## 5. 驗證

- [x] 5.1 執行 migration SQL，確認 `keystroke_events` 表建立成功（`\d keystroke_events`）
- [x] 5.2 手動測試：練習打一個字 → 查詢 DB 確認 `keystroke_events` 有對應紀錄且 `key_order` 連續
- [x] 5.3 手動測試：不帶 `keystrokes` 的 `POST /api/attempts` 請求仍回傳 202 且 `typing_attempts` 正常寫入
- [x] 5.4 手動測試：刪除一筆 `typing_attempts` → 確認關聯的 `keystroke_events` 一併刪除（CASCADE）
