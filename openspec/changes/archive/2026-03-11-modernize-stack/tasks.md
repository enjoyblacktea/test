## 1. 建立 Feature Branch 與環境設定

- [x] 1.1 建立 `feature/modernize-stack` branch
- [x] 1.2 更新 `backend/pyproject.toml`：新增 `fastapi`、`uvicorn[standard]`、`sqlalchemy[asyncio]`、`asyncpg`、`alembic`、`pydantic-settings`，移除 `flask`、`flask-cors`
- [x] 1.3 執行 `uv sync` 安裝新依賴

## 2. Backend：SQLAlchemy ORM Models

- [x] 2.1 建立 `backend/app/` 目錄結構（`routers/`、`models/`、`schemas/`、`services/`）
- [x] 2.2 建立 `backend/app/models/user.py`：SQLAlchemy async ORM `User` model（對應 `users` 表）
- [x] 2.3 建立 `backend/app/models/character.py`：`Character` model（對應 `characters` 表）
- [x] 2.4 建立 `backend/app/models/attempt.py`：`TypingAttempt` model（對應 `typing_attempts` 表，含 `duration_ms` computed column）
- [x] 2.5 建立 `backend/app/models/keystroke.py`：`KeystrokeEvent` model（對應 `keystroke_events` 表，含 FK cascade）
- [x] 2.6 建立 `backend/app/db.py`：async engine、session factory、`get_db` dependency

## 3. Backend：Alembic Migration 設定

- [x] 3.1 執行 `alembic init alembic` 初始化
- [x] 3.2 設定 `alembic.ini` 與 `alembic/env.py`（使用 async engine，讀取 `.env` 的 `DATABASE_URL`）
- [x] 3.3 執行 `alembic revision --autogenerate -m "initial_migration"` 產生首次 migration
- [x] 3.4 比對產生的 migration 與 `backend/migrations/init_db.sql` 確認一致（含 seed data 需手動補入 migration）
- [x] 3.5 在測試 DB 執行 `alembic upgrade head` 驗證 migration 正確

## 4. Backend：Pydantic Schemas

- [x] 4.1 建立 `backend/app/schemas/auth.py`：`RegisterRequest`、`LoginRequest`、`TokenResponse`、`RefreshRequest`
- [x] 4.2 建立 `backend/app/schemas/word.py`：`WordResponse`（含 `character`、`zhuyin`、`keys`）
- [x] 4.3 建立 `backend/app/schemas/attempt.py`：`KeystrokeEventIn`、`RecordAttemptRequest`、`AttemptResponse`

## 5. Backend：FastAPI Routers

- [x] 5.1 建立 `backend/app/routers/auth.py`：`POST /api/auth/register`、`POST /api/auth/login`、`POST /api/auth/refresh`（移植 Flask auth routes）
- [x] 5.2 建立 `backend/app/routers/words.py`：`GET /api/words/random`（移植 Flask words route）
- [x] 5.3 建立 `backend/app/routers/attempts.py`：`POST /api/attempts`、`GET /api/attempts`（移植 Flask attempts routes）
- [x] 5.4 建立 `backend/app/routers/health.py`：`GET /api/health`
- [x] 5.5 建立 `backend/app/main.py`：FastAPI app 初始化、掛載所有 routers、lifespan 管理 DB pool

## 6. Backend：Services 遷移為 Async

- [x] 6.1 移植 `backend/app/services/auth_service.py`：JWT 產生/驗證、bcrypt（async 化）
- [x] 6.2 移植 `backend/app/services/character_service.py`：Zhuyin mapping（邏輯不變）
- [x] 6.3 移植 `backend/app/services/attempt_service.py`：改用 SQLAlchemy async session 寫入 `typing_attempts` + `keystroke_events`（保留 transaction）
- [x] 6.4 移植 `backend/app/services/word_service.py`：改用 SQLAlchemy async ORM 查詢（已整合至 character_service）
- [x] 6.5 建立 `backend/app/dependencies.py`：`require_auth` dependency（取代 Flask decorator）

## 7. Backend：驗證

- [x] 7.1 執行 `tests/backend/test_api.py`，確認所有測試通過
- [x] 7.2 瀏覽 `http://localhost:8000/docs` 確認 Swagger UI 顯示所有 endpoints

## 8. Frontend：React + TypeScript + Vite 初始化

- [x] 8.1 在 `frontend/` 目錄執行 `npm create vite@latest . -- --template react-ts`（覆蓋現有目錄）
- [x] 8.2 安裝依賴：`npm install axios`
- [x] 8.3 設定 `vite.config.ts`：proxy `/api` 到 `http://localhost:8000`
- [x] 8.4 建立 `src/` 目錄結構（`pages/`、`components/`、`hooks/`、`api/`、`types/`、`utils/`）

## 9. Frontend：TypeScript 型別定義

- [x] 9.1 建立 `src/types/index.ts`：`User`、`WordResponse`、`AttemptRequest`、`KeystrokeEvent`、`TokenResponse`、`ApiError` interfaces

## 10. Frontend：API Client

- [x] 10.1 建立 `src/api/client.ts`：axios instance（baseURL `/api`）+ JWT interceptor（自動 refresh + 401 導向登入）
- [x] 10.2 建立 `src/api/auth.ts`：`login`、`register`、`refresh` 函式（型別安全）
- [x] 10.3 建立 `src/api/practice.ts`：`getWord`、`recordAttempt` 函式（型別安全）

## 11. Frontend：Utilities

- [x] 11.1 建立 `src/utils/zhuyin-map.ts`：從 `frontend/js/modules/zhuyin-map.js` 搬移並加 TypeScript 型別

## 12. Frontend：自訂 Hooks

- [x] 12.1 建立 `src/hooks/useAuth.ts`：管理 token localStorage、`isAuthenticated`、`login`、`logout`
- [x] 12.2 建立 `src/hooks/usePractice.ts`：載入字符、`checkInput`、累積 keystroke events、`completeAttempt`
- [x] 12.3 建立 `src/hooks/useKeyboard.ts`：監聽 `keydown` 事件，呼叫 `usePractice` 的 `checkInput`

## 13. Frontend：元件

- [x] 13.1 建立 `src/components/ProgressBar.tsx`：顯示輸入進度（props: `current`, `total`）
- [x] 13.2 建立 `src/components/VirtualKeyboard.tsx`：根據 zhuyin-map 渲染按鍵（props: `activeKeys`）
- [x] 13.3 建立 `src/components/PracticeCard.tsx`：顯示字符與輸入區（props: `character`, `progress`）

## 14. Frontend：頁面

- [x] 14.1 建立 `src/pages/LoginPage.tsx`：登入 / 註冊 tabs（使用 `useAuth` hook）
- [x] 14.2 建立 `src/pages/PracticePage.tsx`：主練習頁（使用 `usePractice`、`useKeyboard` hooks，組合 PracticeCard + VirtualKeyboard）
- [x] 14.3 建立 `src/App.tsx`：路由（登入狀態判斷 → LoginPage 或 PracticePage）
- [x] 14.4 建立 `src/main.tsx`：React 入口，掛載 App

## 15. Frontend：樣式

- [x] 15.1 建立 `src/styles/variables.css`：深色主題 CSS 變數（--bg-primary: #0a0a0a、--accent-cyan: #00d9ff、--success: #00ff88）
- [x] 15.2 移植現有 `frontend/styles/styles.css` 的主要樣式到元件對應 CSS 檔案或 CSS modules

## 16. 整合測試

- [x] 16.1 啟動 FastAPI backend（`uvicorn app.main:app --reload`）與 Vite dev server（`npm run dev`）
- [x] 16.2 手動測試完整流程：註冊 → 登入 → 練習字符 → 確認 `typing_attempts` 與 `keystroke_events` 有資料寫入
- [x] 16.3 確認深色主題視覺風格與原版一致
- [x] 16.4 確認 token 自動 refresh 邏輯運作正常
