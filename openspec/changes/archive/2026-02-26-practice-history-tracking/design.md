## Context

目前的注音輸入練習應用程式是一個純前端應用，使用 LocalStorage 進行簡單的認證。所有練習資料都存在於當前 session 中，關閉瀏覽器或切換裝置後就無法追蹤歷史。

**現有架構**:
- Frontend: Vanilla JavaScript (ES6 modules), 無框架
- Backend: Flask API，只提供隨機字詞服務
- 資料儲存: JSON 檔案 (words.json)
- 認證: LocalStorage 存 `{ isLoggedIn: true }`
- 統計: 僅在當前 session 的記憶體中

**限制**:
- 沒有持久化的練習記錄
- 無法跨 session 追蹤進步
- 無法識別不同使用者的練習資料

**利害關係人**:
- 學習者：需要長期追蹤學習進度
- 開發者：需要簡單、可維護的解決方案

## Goals / Non-Goals

**Goals:**
1. **完整歷史記錄** - 記錄每個練習的字、時間、正確性，建立完整學習日誌
2. **進步分析** - 提供統計資料（總練習數、正確率、平均時間、練習天數）
3. **持久化儲存** - 使用 PostgreSQL 永久保存，支援跨裝置存取
4. **最小改動** - 保持現有前端認證和練習流程，降低風險
5. **非阻塞式** - 記錄失敗不影響使用者繼續練習
6. **向後相容** - 不破壞現有功能

**Non-Goals:**
1. ❌ **真實後端認證** - 不在此階段實作 JWT/Session，繼續使用前端認證
2. ❌ **歷史記錄 UI** - 不實作查看歷史的前端介面，只建立 API
3. ❌ **進階分析** - 不實作趨勢圖表、學習建議等複雜分析
4. ❌ **多使用者隔離** - 不強制使用者隔離（可用相同 username 查詢）
5. ❌ **資料遷移** - 不遷移現有的記憶體統計資料到資料庫

## Decisions

### 1. 資料庫選擇：PostgreSQL vs SQLite

**決定**: 使用 **PostgreSQL**

**理由**:
- ✅ 企業級，適合未來擴展到生產環境
- ✅ 原生支援 BOOLEAN 和複雜查詢
- ✅ 更好的並發支援
- ✅ 符合使用者需求（使用者明確要求 PostgreSQL）

**替代方案考慮**:
- SQLite: 簡單、無需額外安裝，但擴展性有限
- MongoDB: NoSQL 彈性高，但這個場景不需要 schema-less

**Trade-off**: 需要額外安裝和配置 PostgreSQL，增加部署複雜度

### 2. 實作方案：最小改動 vs 完整後端認證

**決定**: **最小改動方案** - 保持前端 LocalStorage 認證

**理由**:
- ✅ 快速實現功能，降低開發風險
- ✅ 不需要重寫認證系統
- ✅ 前端邏輯改動最小
- ✅ 資料庫設計已預留升級空間（password_hash 欄位）

**替代方案考慮**:
- 完整後端認證：更安全，但需要大幅重寫前端和後端
- OAuth 第三方登入：過於複雜，不符合簡單應用的定位

**Trade-off**:
- ⚠️ 缺乏真實認證，username 可被偽造
- ⚠️ 同一 username 在不同瀏覽器的記錄會混在一起
- ✅ 已規劃清晰的升級路徑（Phase 2）

### 3. 資料表設計：Session-based vs Flat records

**決定**: **Flat records** - 不使用 session grouping

**理由**:
- ✅ 結構更簡單，查詢更直觀
- ✅ 可以在查詢時動態按時間分組
- ✅ 不需要管理 session 生命週期

**替代方案考慮**:
- Session-based (每 10 個字一個 session): 複雜度增加，但可以更好地組織資料

**Schema**:
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- 預留給未來
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE practice_history (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    word VARCHAR(10) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_ms INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (end_time - start_time)) * 1000
    ) STORED,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

**關鍵設計點**:
- `duration_ms` 使用 GENERATED ALWAYS 自動計算
- `ON DELETE CASCADE` 刪除使用者時清理記錄
- 索引設計：`idx_user_time` 優化查詢效能

### 4. API 設計：RESTful vs GraphQL

**決定**: **RESTful API**

**理由**:
- ✅ 符合現有 Flask 架構
- ✅ 簡單直觀，不需要額外框架
- ✅ 三個端點足以滿足需求

**API 端點**:
1. `POST /api/history/record` - 記錄練習
2. `GET /api/history?username=X&limit=N&offset=M` - 查詢歷史
3. `GET /api/history/stats?username=X` - 查詢統計

**替代方案考慮**:
- GraphQL: 彈性高，但對這個簡單場景過於複雜

### 5. 前端整合：同步 vs 非同步記錄

**決定**: **非阻塞式非同步記錄**

**理由**:
- ✅ 記錄失敗不影響練習繼續
- ✅ 使用者體驗優先
- ✅ 可選功能，不應阻斷核心流程

**實作方式**:
```javascript
recordPractice(data).catch(err => {
  console.warn('Failed to record, but continuing:', err);
  // 可選：存到離線佇列
});
```

**替代方案考慮**:
- 同步記錄：更可靠，但會阻塞使用者體驗

**Trade-off**:
- ⚠️ 網路錯誤時可能丟失記錄
- ✅ 可選實作離線佇列機制緩解

### 6. 連線池 vs 單一連線

**決定**: 使用 **psycopg2 SimpleConnectionPool**

**理由**:
- ✅ 高效處理並發請求
- ✅ 避免頻繁建立/關閉連線
- ✅ psycopg2 內建，無需額外依賴

**配置**: minconn=1, maxconn=10

### 7. 時間追蹤：前端 vs 後端

**決定**: **前端記錄時間**，後端儲存

**理由**:
- ✅ 準確反映使用者實際練習時間
- ✅ 包含使用者思考時間
- ✅ 後端僅驗證邏輯（end_time > start_time）

**替代方案考慮**:
- 後端記錄時間：不準確，會包含網路延遲

## Risks / Trade-offs

### Risk 1: 資料庫連線失敗
**風險**: PostgreSQL 無法連線時，所有記錄 API 會失敗

**緩解措施**:
- ✅ 前端非阻塞式呼叫，失敗不影響練習
- ✅ 返回 503 Service Unavailable，前端可降級處理
- ✅ 可選實作離線佇列，網路恢復後重試

### Risk 2: Username 偽造
**風險**: 任何人都可以用任意 username 記錄或查詢資料

**緩解措施**:
- ⚠️ 當前方案接受此風險（教育用途）
- ✅ 已規劃 Phase 2 升級到真實後端認證
- ✅ 資料庫已預留 password_hash 欄位

### Risk 3: 資料庫容量
**風險**: 長期使用後 practice_history 表可能變得很大

**緩解措施**:
- ✅ PostgreSQL 可處理百萬級記錄
- ✅ 索引優化查詢效能
- 🔮 未來可實作資料保留政策（如保留 1 年）

### Risk 4: 時間戳不同步
**風險**: 前端時間可能不準確（系統時間錯誤）

**緩解措施**:
- ✅ 後端驗證 end_time > start_time
- ⚠️ 接受使用者系統時間為準（記錄仍有意義）

### Risk 5: 網路延遲導致記錄丟失
**風險**: 快速練習時，網路慢可能導致部分記錄未成功

**緩解措施**:
- ✅ 可選實作離線佇列（localStorage）
- ✅ 前端 console 記錄失敗，方便除錯
- ⚠️ MVP 階段接受此風險

### Risk 6: 同一 username 多裝置記錄混淆
**風險**: 不同人使用相同 username 會共用歷史記錄

**緩解措施**:
- ⚠️ 當前方案接受此風險
- ✅ Phase 2 升級後解決

## Migration Plan

### Phase 1: 資料庫設置
1. 安裝 PostgreSQL (如尚未安裝)
2. 建立資料庫: `CREATE DATABASE zhuyin_practice;`
3. 執行初始化腳本: `backend/migrations/init_db.sql`
4. 設定環境變數（或使用預設值）

### Phase 2: 後端部署
1. 更新 `pyproject.toml` 新增 psycopg2-binary 依賴
2. 執行 `uv sync` 安裝依賴
3. 新增檔案: db_service.py, history_service.py, routes/history.py
4. 修改 app.py 註冊 history blueprint
5. 測試後端 API

### Phase 3: 前端部署
1. 新增 history.js 模組
2. 修改 auth.js, practice.js, main-redesign.js
3. 測試前端整合

### Phase 4: 驗證
1. 執行單元測試
2. 執行整合測試
3. 手動測試完整流程

### Rollback 策略
- 資料庫變更是**累加的**（不影響現有功能）
- 可以隨時刪除新增的 API 和前端程式碼
- 資料庫可以保留（不影響現有功能）或刪除

## Open Questions

1. ❓ **資料保留政策**: 歷史記錄應該永久保留還是設定過期時間？
   - **建議**: MVP 階段永久保留，Phase 2 可考慮保留 1 年

2. ❓ **離線佇列**: 是否實作 localStorage 離線佇列？
   - **建議**: 可選功能，Phase 1 可以跳過，Phase 2 再加

3. ❓ **統計 API**: 是否在 Phase 1 實作 `/api/history/stats`？
   - **建議**: 實作，程式碼量少且有用

4. ❓ **測試資料庫**: 是否建立獨立的測試資料庫？
   - **建議**: 是，使用 `zhuyin_practice_test`

5. ❓ **部署環境**: 開發環境的 PostgreSQL 設定？
   - **建議**: 本機安裝，使用預設 localhost:5432
