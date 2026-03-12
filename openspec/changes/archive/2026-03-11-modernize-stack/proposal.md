## Why

目前前後端使用 Flask（同步）+ 原生 psycopg2 手動連線池，以及無框架的 Vanilla JavaScript ES6 模組。技術棧偏舊，缺乏型別安全、自動驗證與現代開發體驗。藉此機會全面升級為業界主流的現代技術棧，提升開發效率與可維護性。

## What Changes

- **Backend**: Flask 替換為 FastAPI（async/await、自動 OpenAPI 文件）
- **Backend**: 原生 psycopg2 手動連線池替換為 SQLAlchemy async ORM + asyncpg
- **Backend**: 新增 Alembic 管理 DB schema 版本（取代手動執行 init_db.sql）
- **Backend**: 新增 Pydantic schemas 自動驗證 request / response
- **Frontend**: Vanilla JavaScript 替換為 React + TypeScript + Vite
- **Frontend**: 全域 state 物件替換為 React hooks（useState、自訂 hooks）
- **Frontend**: 新增 TypeScript 型別覆蓋全部 API 介面與元件 props
- **保留**: PostgreSQL schema（4 張表結構不變）
- **保留**: JWT 認證邏輯與 API endpoint 路徑（/api/auth、/api/words、/api/attempts）
- **保留**: 深色主題設計風格

## Capabilities

### New Capabilities

- `fastapi-backend`: FastAPI 後端，包含 async SQLAlchemy ORM models、Pydantic schemas、Alembic migrations、uvicorn 執行
- `react-frontend`: React + TypeScript + Vite 前端，包含元件架構、自訂 hooks、axios API client、TypeScript 型別定義

### Modified Capabilities

（無 — API 行為與 spec 層級需求不變，僅實作技術替換）

## Impact

- **替換**: `backend/app.py`（Flask）→ `backend/app/main.py`（FastAPI）
- **替換**: `backend/services/db_service.py`（psycopg2）→ SQLAlchemy async session
- **替換**: `backend/routes/`（Flask Blueprint）→ `backend/app/routers/`（FastAPI APIRouter）
- **新增**: `backend/app/models/`（SQLAlchemy ORM）、`backend/app/schemas/`（Pydantic）、`backend/alembic/`
- **替換**: `frontend/js/`（Vanilla JS）→ `frontend/src/`（React + TypeScript）
- **移除**: `backend/config.py`（改用 pydantic-settings）
- **保留**: `.env` 格式（DATABASE_URL 等環境變數不變）
- **依賴新增**: `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic-settings`（backend）；`react`, `typescript`, `vite`, `axios`（frontend）
