## Context

目前 `typing_attempts` 表以字為單位記錄練習結果，只有 `is_correct` 布林值表示整個字是否打對。前端 `practice.js` 的 `checkInput()` 已知每個按鍵的正確性，但此資料未被送往後端保存。

現有資料流：
```
前端按鍵 → checkInput() → 字完成 → POST /api/attempts { character_id, started_at, ended_at, is_correct }
```

## Goals / Non-Goals

**Goals:**
- 在 PostgreSQL 新增 `keystroke_events` 表，記錄每次 attempt 的逐鍵資料
- 擴充 `POST /api/attempts` 接受 `keystrokes` 陣列（向下相容，選填）
- attempt 與其 keystrokes 在同一 DB transaction 寫入，確保原子性
- 前端在字完成時將累積的 keystroke 資料一併送出

**Non-Goals:**
- 不新增獨立的 keystroke 查詢 API（此次僅寫入）
- 不修改現有 `GET /api/attempts` 的回應格式
- 不即時串流 keystroke 事件到後端

## Decisions

### 1. 批次寫入而非獨立端點

**決定**：keystroke 隨 attempt 一起送出，後端在同一 transaction 寫入兩張表。

**理由**：
- keystroke 對 attempt 有強依賴（需要 `attempt_id`），先後兩次 API call 若第二次失敗，會產生孤立的 attempt 無 keystroke 資料
- 對前端而言只需一次 fetch，實作更簡單
- 現有 `record_attempt()` 已使用 `execute_query(commit=True)`，擴充為手動管理 connection 的 transaction 即可

**替代方案**：分開端點 `POST /api/keystroke_events` — 被否決，因為會增加失敗點且前端需等待 attempt_id

### 2. keystroke 欄位設計

**決定**：採用使用者提供的 schema：
- `id`、`attempt_id`、`key_value`、`key_order`、`typed_at`、`is_correct_key`

**理由**：`key_order` 確保排序獨立於 `typed_at` 精度；`key_value` 記錄實際按下的鍵（含錯誤鍵），可分析常見混淆鍵組合。

### 3. 前端累積方式

**決定**：在 `practice.js` 的 state 新增 `keystrokes: []`，每次 `checkInput()` 後在模組內部 push，`completeAttempt()` 時一起帶出。

**理由**：keystroke 累積屬於練習狀態，放在 `practice.js` 比放在 `input-handler.js` 更符合職責分離。input-handler 不需改動。

### 4. `typed_at` 產生位置

**決定**：在前端按鍵當下 `new Date().toISOString()` 記錄。

**理由**：後端收到請求時已有網路延遲，前端時間更接近真實按鍵時刻；且 `started_at` / `ended_at` 也是前端產生，保持一致。

## Risks / Trade-offs

- **前端時鐘偏差** → 可接受，此資料用於相對分析而非絕對時間；`key_order` 可作為主要排序依據
- **`keystrokes` 資料量** → 注音字最多約 4–5 鍵，batch size 極小，不是效能問題
- **向下相容性** → `keystrokes` 為選填，現有無認證客戶端（如前端舊版）送出無 keystrokes 的 attempt 仍正常儲存

## Migration Plan

1. 在 `init_db.sql` 追加 `CREATE TABLE IF NOT EXISTS keystroke_events`（idempotent）
2. 對既有資料庫執行此 SQL 片段即完成 migration（無需修改現有表）
3. Rollback：`DROP TABLE IF EXISTS keystroke_events`（不影響 `typing_attempts`）
