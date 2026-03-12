## Context

目前前後端系統的資料庫有四張表：`users`、`characters`、`typing_attempts`、`keystroke_events`。下游的 dbt + Power BI 管道需要維度豐富的 Star Schema，但現有的 `characters` 表缺乏分類資訊，也沒有使用者目標記錄，無法支援多維度分析。

本設計新增兩張表來豐富維度層：`character_metadata`（字符注音分類與難度）和 `user_goals`（每日練習目標歷史）。

## Goals / Non-Goals

**Goals:**
- 新增 `character_metadata` 表，讓 dbt 能建立 `dim_characters`
- 新增 `user_goals` 表，讓 dbt 能建立 `fct_goal_achievement`
- 提供初始化腳本自動填入 `character_metadata`
- 前端練習頁面顯示當日目標進度

**Non-Goals:**
- 不修改 `typing_attempts`、`keystroke_events` 既有結構
- 不在前後端系統計算統計指標（留給 Power BI）
- 不在前後端系統推算練習場次（留給 dbt）
- 不提供字符元數據的管理 UI

## Decisions

### D1：`character_metadata` 採用獨立表而非擴充 `characters` 欄位

**決策：** 新增 `character_metadata` 表，以 `character_id` 一對一關聯 `characters`。

**理由：** `characters` 表是字符輸入碼的靜態定義，metadata 是分析用的衍生資訊，分開可讓兩者獨立演進。若未來有多種輸入法的 metadata 需求，也不會污染主表。

**替代方案：** 直接在 `characters` 加欄位——較簡單，但混合了輸入法定義與分析維度，語義不清。

---

### D2：`character_metadata` 由初始化腳本填入，不透過 API

**決策：** 提供一次性 Python 腳本（`scripts/seed_character_metadata.py`），從 `input_code` 解析注音成分並批次 UPSERT。

**理由：** 注音符號與鍵盤對應是固定規則，可程式化解析，不需要人工 UI。難度和頻率排名也是靜態參考數據，適合腳本管理。

**替代方案：** Admin API——增加不必要的認證複雜度；手動 SQL seed——不易維護。

---

### D3：`user_goals` 採用 append-only 歷史記錄

**決策：** 每次使用者設定新目標，INSERT 一筆新記錄；查詢時取 `effective_date <= 今日` 且 `id` 最大的一筆。

**理由：** 保留歷史讓 dbt 能還原任意日期的有效目標，從而計算每日目標達成率的時間序列。若 UPDATE 覆蓋，歷史數據遺失。

**替代方案：** 只保留最新一筆——實作最簡，但下游分析無法追溯過去目標。

---

### D4：session 邏輯不在前後端處理

**決策：** `typing_attempts` 維持現狀，不新增 `practice_sessions` 表；session 邏輯完全由 dbt 以時間間隔推算。

**理由：** 讓 dbt 用 window function 推算場次，正好展示 dbt 的原始數據轉換能力。前後端追蹤場次需要處理瀏覽器關閉等邊界情況，複雜度不值得。

---

### D5：注音解析規則

`input_code` 為注音符號字串（如 `ㄋㄧˇ`），解析規則：
- **聲母**：字串首個符號若屬於 21 個聲母（ㄅㄆㄇㄈ...）則取出，否則 `initial = NULL`
- **韻母**：移除聲母與聲調後的剩餘部分
- **聲調**：取最後一個字符若為 ˊˇˋ˙，對應 2–5；無調號或空白鍵 = 聲調 1

## Risks / Trade-offs

| 風險 | 緩解方式 |
|---|---|
| 初始化腳本解析錯誤（罕見注音組合） | 腳本加入 unrecognized 日誌，migration 後手動驗查 |
| `user_goals` 同日多筆造成查詢歧義 | 查詢統一取 `MAX(id)`，文件化此規則 |
| `character_metadata` 缺少部分字符記錄 | dbt 用 LEFT JOIN，Power BI 視 NULL 為「未分類」 |

## Migration Plan

1. 建立新的 Alembic migration，新增 `character_metadata` 與 `user_goals` 兩張表
2. 執行 `alembic upgrade head`
3. 執行 `python scripts/seed_character_metadata.py` 填入元數據
4. 驗查：`SELECT COUNT(*) FROM character_metadata` 應與 `characters` 筆數相符

**Rollback：** `alembic downgrade -1`（刪除兩張新表，不影響既有數據）

## Open Questions

- `difficulty`（1–3）的分級標準尚未定義，初始版本可全部填入預設值 `1`，後續由管理員人工調整
- `frequency_rank` 的數據來源（教育部常用字表或其他）待確認；初始版本可填 NULL
