## Context

目前這是一個注音練習個人 app，後端使用 Flask 3.1（同步）+ 原生 psycopg2 手動連線池，前端使用 Vanilla JavaScript ES6 模組（無框架、無 build tool）。PostgreSQL schema 有 4 張表（users、characters、typing_attempts、keystroke_events），資料與邏輯成熟穩定。此次重構目標是替換技術棧，不改變功能行為。

## Goals / Non-Goals

**Goals:**
- 後端從 Flask 遷移至 FastAPI（async、Pydantic 驗證、自動 OpenAPI 文件）
- 後端從原生 psycopg2 遷移至 SQLAlchemy async ORM + asyncpg
- 後端新增 Alembic 管理 DB migration
- 前端從 Vanilla JS 遷移至 React + TypeScript + Vite
- 保持 API endpoint 路徑與行為完全不變（backward compatible）

**Non-Goals:**
- 不新增任何功能
- 不改變 PostgreSQL schema
- 不改變 JWT 認證邏輯（token 格式、過期時間）
- 不引入 Docker / 容器化
- 不改變 `.env` 環境變數格式

## Decisions

### D1：FastAPI + asyncpg（非 Flask + psycopg2）

FastAPI 原生支援 async/await，配合 asyncpg 可完全非阻塞地處理 DB 操作。Flask 為同步框架，即便搭配 Thread 仍有 GIL 限制。FastAPI 另有 Pydantic 自動驗證 request body，省去手寫 `data.get()` 驗證邏輯，並內建 `/docs` Swagger UI。

**替代方案考量**：Flask + gevent（異步）— 引入複雜度且非主流方向，不採用。

### D2：SQLAlchemy async ORM（非 raw SQL）

目前 `attempt_service.py` 直接拼接 SQL 字串，維護性差且容易出錯。SQLAlchemy ORM 提供型別提示、關聯定義（relationship），配合 Alembic 可版控 schema 變更。asyncpg 為高效能 async PostgreSQL 驅動。

**替代方案考量**：保留 raw psycopg2 但加 async — 需使用 psycopg3（alpha），不採用。

### D3：Alembic migrations（非手動執行 init_db.sql）

目前新增欄位需手動 `ALTER TABLE` 或重建 DB。Alembic 提供版本化 migration，`alembic upgrade head` 即可自動同步 schema。初次遷移從現有 `init_db.sql` 匯入為 `initial_migration`。

### D4：React + TypeScript + Vite（非 Vue / Svelte）

React 生態最大，TypeScript 提供型別安全，Vite 提供極快 HMR。對個人專案而言，React hooks 比 Vanilla JS 全域 state 更易維護。Vite 零設定開箱即用。

**替代方案考量**：Vue 3（學習曲線較低）、Svelte（打包最小）— 使用者明確選擇 React，不採用。

### D5：後端目錄結構調整

```
backend/
  app/
    main.py          # FastAPI app，lifespan 管理 DB pool
    db.py            # async session factory
    routers/         # APIRouter（取代 Flask Blueprint）
      auth.py
      words.py
      attempts.py
      health.py
    models/          # SQLAlchemy ORM models
      user.py
      character.py
      attempt.py
      keystroke.py
    schemas/         # Pydantic request/response schemas
      auth.py
      word.py
      attempt.py
    services/        # 商業邏輯（結構不變，改用 async）
      auth_service.py
      character_service.py
      attempt_service.py
      word_service.py
  alembic/           # Alembic migration 檔案
  alembic.ini
  pyproject.toml
```

### D6：前端目錄結構

```
frontend/
  src/
    pages/
      LoginPage.tsx
      PracticePage.tsx
    components/
      PracticeCard.tsx
      VirtualKeyboard.tsx
      ProgressBar.tsx
    hooks/
      useAuth.ts
      usePractice.ts
      useKeyboard.ts
    api/
      client.ts        # axios instance + JWT interceptor
      auth.ts
      practice.ts
    types/
      index.ts         # 共用 TypeScript types
    utils/
      zhuyin-map.ts    # 直接從 zhuyin-map.js 搬移
    App.tsx
    main.tsx
  index.html
  vite.config.ts
  tsconfig.json
```

## Risks / Trade-offs

- **[風險] async SQLAlchemy 學習曲線** → 使用官方文件範例，session 透過 dependency injection 注入 router
- **[風險] Alembic 首次 migration 與現有 DB 不一致** → 使用 `--autogenerate` 從現有 ORM models 產生，並與 init_db.sql 比對驗證
- **[取捨] React 打包體積較 Vanilla JS 大** → 個人專案可接受，Vite 有 tree-shaking 優化
- **[風險] axios JWT interceptor 邏輯複雜** → 直接移植現有 `api.js` 的 refresh 邏輯，不重新設計

## Migration Plan

1. 建立 feature branch `feature/modernize-stack`
2. **Backend 遷移**（優先）：
   - 安裝新依賴，更新 pyproject.toml
   - 建立 SQLAlchemy ORM models（對應現有 4 張表）
   - 建立 FastAPI routers（對應現有 Flask routes）
   - 建立 Pydantic schemas
   - 設定 Alembic，產生 initial migration（從現有 schema）
   - 移植 services 為 async
   - 驗證：執行現有 `tests/backend/test_api.py`
3. **Frontend 遷移**：
   - `npm create vite@latest frontend -- --template react-ts`
   - 建立元件與 hooks
   - 移植 zhuyin-map、keystroke 邏輯
   - 移植 JWT interceptor
4. 整合測試 → PR → merge

**Rollback**：git revert 即可，DB schema 不變。

## Open Questions

（無 — 設計已在 brainstorming 階段確認）
