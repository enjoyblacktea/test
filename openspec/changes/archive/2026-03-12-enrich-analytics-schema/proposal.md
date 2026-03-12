## Why

目前資料庫的數據結構過於扁平，`characters` 表缺乏分類維度，也沒有使用者目標記錄，導致 dbt 無法建立有意義的維度模型，Power BI 也無法進行多維度分析。透過新增字符元數據與使用者每日目標，讓數據管道具備足夠的維度深度以展現 Star Schema 的完整價值。

## What Changes

- 新增 `character_metadata` 表，儲存每個注音字符的聲母、韻母、聲調、難度等級與常用字頻率排名
- 新增 `user_goals` 表，儲存使用者每日練習目標題數（含歷史記錄）
- 新增後端初始化腳本，從現有 `input_code` 自動解析並填入 `character_metadata`
- 新增 API 端點供前端查詢今日目標與提交新目標
- 前端練習頁面顯示今日目標進度（已完成 / 目標題數）

## Capabilities

### New Capabilities

- `character-metadata`：字符元數據管理，包含注音聲母/韻母/聲調分類、難度等級、常用字頻率排名，以及初始化解析腳本
- `user-goals`：使用者每日練習目標設定與查詢，支援目標歷史追蹤，前端顯示當日進度

### Modified Capabilities

（無）

## Impact

- **資料庫**：新增兩張表，需要一版新的 Alembic migration
- **後端**：新增 `GoalRouter`、`goal_service`、`character_metadata` ORM model
- **前端**：練習頁面新增目標進度顯示與設定入口
- **dbt（下游）**：可建立 `dim_characters`（含 metadata）、`fct_goal_achievement`（goals JOIN attempts）
- **不影響**：現有 `typing_attempts`、`keystroke_events`、所有既有 API 端點
