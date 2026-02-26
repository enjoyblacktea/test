## Why

使用者希望追蹤完整的練習歷史並分析學習進度，但目前應用程式沒有提供任何歷史記錄功能。練習資料在每次 session 結束後就消失，使用者無法回顧學習歷程或分析哪些字需要加強練習。這限制了應用程式的學習價值。

## What Changes

- **新增 PostgreSQL 資料庫**：建立 `users` 和 `practice_history` 兩個資料表，永久儲存練習記錄
- **新增後端服務層**：
  - `db_service.py`：管理資料庫連線池
  - `history_service.py`：處理歷史記錄的業務邏輯（記錄練習、查詢歷史、計算統計）
- **新增 API 端點**：
  - `POST /api/history/record`：記錄單次練習
  - `GET /api/history`：查詢使用者的練習歷史
  - `GET /api/history/stats`：查詢統計資料（總練習數、正確率、平均時間等）
- **前端自動記錄**：
  - 新增 `history.js` 模組處理 API 呼叫
  - 修改 `auth.js` 儲存 username 到 LocalStorage
  - 修改 `practice.js` 追蹤每個字的開始/結束時間和正確性
  - 修改 `main-redesign.js` 在字完成時自動發送記錄到後端
- **保持現有認證機制**：繼續使用前端 LocalStorage 認證，降低改動風險

## Capabilities

### New Capabilities
- `practice-history-tracking`: 完整的練習歷史記錄與進步分析功能，包含資料儲存、API 端點、前端整合，以及統計分析能力

### Modified Capabilities
<!-- 無修改現有 capabilities -->

## Impact

**後端 (Backend)**:
- 新增依賴：`psycopg2-binary` (PostgreSQL adapter)
- 新增檔案：`backend/services/db_service.py`, `backend/services/history_service.py`, `backend/routes/history.py`
- 新增資料庫初始化腳本：`backend/migrations/init_db.sql`
- 修改 `backend/config.py` 新增 PostgreSQL 連線配置
- 修改 `backend/app.py` 註冊新的 history blueprint

**前端 (Frontend)**:
- 新增檔案：`frontend/js/modules/history.js`
- 修改檔案：`frontend/js/modules/auth.js` (儲存 username), `frontend/js/modules/practice.js` (時間追蹤), `frontend/js/main-redesign.js` (整合記錄)

**基礎設施 (Infrastructure)**:
- 需要安裝並配置 PostgreSQL 資料庫
- 需要建立資料庫 `zhuyin_practice` 和相關資料表
- 需要設定環境變數（POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD）

**測試 (Testing)**:
- 新增後端單元測試：`tests/backend/test_history_service.py`, `tests/backend/test_history_api.py`
- 新增前端測試：在 `tests/frontend/test.html` 新增 history 模組測試
- 新增整合測試檢查清單：`tests/HISTORY_FEATURE_TEST_CHECKLIST.md`

**向後相容性**:
- ✅ 完全向後相容，不影響現有功能
- ✅ 歷史記錄為可選功能，失敗不影響練習繼續進行
