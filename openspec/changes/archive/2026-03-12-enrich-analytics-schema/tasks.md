## 1. 資料庫 Migration

- [x] 1.1 新增 `CharacterMetadata` SQLAlchemy ORM model（欄位：character_id FK、initial、final、tone、difficulty、frequency_rank）
- [x] 1.2 新增 `UserGoal` SQLAlchemy ORM model（欄位：id、user_id FK、daily_target、effective_date、created_at）
- [x] 1.3 在 `backend/app/models/__init__.py` 匯出兩個新 model
- [x] 1.4 建立 Alembic migration（`alembic revision --autogenerate -m "add character_metadata and user_goals"`）
- [x] 1.5 執行 `alembic upgrade head` 並驗查兩張新表存在於 DB

## 2. 字符元數據初始化腳本

- [x] 2.1 建立 `backend/scripts/seed_character_metadata.py`
- [x] 2.2 實作注音解析函式：從 `input_code` 提取 `initial`（聲母）、`final`（韻母）、`tone`（聲調 1–5）
- [x] 2.3 腳本批次讀取所有 `characters` 記錄，UPSERT 對應的 `character_metadata`（已存在則跳過）
- [x] 2.4 腳本加入 unrecognized 輸入碼的日誌警告
- [x] 2.5 執行腳本並驗查：`SELECT COUNT(*) FROM character_metadata` 與 `characters` 筆數相符

## 3. 後端：UserGoal API

- [x] 3.1 新增 Pydantic schema：`GoalCreate`（daily_target: int ≥ 1）、`GoalTodayResponse`（daily_target: int | None、completed_today: int）
- [x] 3.2 新增 `backend/app/services/goal_service.py`：`get_today_goal(db, user_id)` 與 `create_goal(db, user_id, daily_target)`
- [x] 3.3 `get_today_goal` 邏輯：查 `effective_date <= 今日` 且 `id` 最大的一筆；計算今日 `typing_attempts` 筆數
- [x] 3.4 新增 `backend/app/routers/goals.py`：`GET /api/goals/today`、`POST /api/goals`（需 `require_auth`）
- [x] 3.5 在 `backend/app/main.py` 掛載 `goals` router

## 4. 前端：目標進度顯示

- [x] 4.1 新增 `frontend/src/api/goals.ts`：`fetchTodayGoal()` 與 `setGoal(daily_target: number)`
- [x] 4.2 新增 `frontend/src/hooks/useGoal.ts`：呼叫 API，管理 `dailyTarget`、`completedToday` 狀態
- [x] 4.3 在 `PracticePage` 引入 `useGoal`，進入頁面時呼叫 `fetchTodayGoal()`
- [x] 4.4 練習頁面顯示進度文字（`N / M 題`；未設定目標時顯示「尚未設定目標」）
- [x] 4.5 新增目標設定 UI：數字輸入欄 + 送出按鈕，呼叫 `setGoal()` 後更新進度顯示
- [x] 4.6 每完成一次 attempt 後，`completedToday` 本地 +1（不重新呼叫 API）
