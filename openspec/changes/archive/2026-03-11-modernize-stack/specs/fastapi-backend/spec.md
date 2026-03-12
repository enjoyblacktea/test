## ADDED Requirements

### Requirement: FastAPI 應用程式入口

系統 SHALL 使用 FastAPI 作為 web 框架，透過 uvicorn 執行，並在 `lifespan` context manager 中管理 DB 連線池的建立與關閉。

#### Scenario: 應用程式啟動
- **WHEN** uvicorn 啟動 FastAPI app
- **THEN** 系統建立 async DB 連線池，並掛載所有 APIRouter

#### Scenario: 自動 API 文件
- **WHEN** 使用者瀏覽 `/docs`
- **THEN** 系統顯示 Swagger UI，列出所有可用 endpoints 及其 request/response schema

---

### Requirement: SQLAlchemy async ORM models

系統 SHALL 使用 SQLAlchemy async ORM 定義所有資料表對應的 Python model，取代原生 SQL 字串操作。

#### Scenario: ORM model 對應現有 schema
- **WHEN** Alembic 執行 `autogenerate`
- **THEN** 產生的 migration 與現有 PostgreSQL schema（users、characters、typing_attempts、keystroke_events）完全一致，無多餘差異

#### Scenario: 關聯查詢
- **WHEN** service 查詢 typing_attempts 並需要 keystroke_events
- **THEN** 可透過 ORM relationship 取得，無需手寫 JOIN SQL

---

### Requirement: Pydantic schemas 自動驗證

系統 SHALL 使用 Pydantic BaseModel 定義所有 API 的 request body 與 response schema，FastAPI 自動執行驗證與序列化。

#### Scenario: 合法 request
- **WHEN** 客戶端送出符合 schema 的 POST /api/attempts body
- **THEN** FastAPI 自動解析並注入型別化物件到 router function

#### Scenario: 非法 request
- **WHEN** 客戶端送出缺少必填欄位的 request body
- **THEN** FastAPI 自動回傳 422 Unprocessable Entity，附帶欄位驗證錯誤詳情

---

### Requirement: Alembic DB migration 管理

系統 SHALL 使用 Alembic 管理所有 PostgreSQL schema 變更，取代手動執行 `init_db.sql`。

#### Scenario: 初次建立 schema
- **WHEN** 在空白 DB 執行 `alembic upgrade head`
- **THEN** 系統建立 users、characters、typing_attempts、keystroke_events 四張表及所有 indexes

#### Scenario: 增量 migration
- **WHEN** 開發者新增 ORM model 欄位並執行 `alembic revision --autogenerate`
- **THEN** 系統產生對應的 migration 檔案，執行 `alembic upgrade head` 後 DB 同步更新

---

### Requirement: API endpoint 路徑與行為向後相容

系統 SHALL 保持所有 API endpoint 路徑、HTTP 方法、request/response 格式與現有 Flask 實作完全一致。

#### Scenario: 認證 endpoint 相容
- **WHEN** 客戶端呼叫 POST /api/auth/register 或 POST /api/auth/login
- **THEN** 回傳格式與現有 Flask 實作相同（含 access_token、refresh_token）

#### Scenario: 練習 endpoint 相容
- **WHEN** 客戶端呼叫 GET /api/words/random 或 POST /api/attempts
- **THEN** 回傳格式與現有 Flask 實作相同

#### Scenario: 現有 backend 測試通過
- **WHEN** 執行 `tests/backend/test_api.py`
- **THEN** 所有測試通過，無需修改測試檔案
