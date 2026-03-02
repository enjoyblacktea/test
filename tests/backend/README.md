# Backend API Tests

完整的後端 API 測試套件，測試所有端點和業務邏輯。

## 測試覆蓋範圍

### 認證端點 (POST /api/auth/*)
- ✅ 註冊成功
- ✅ 註冊重複使用者名稱（409 Conflict）
- ✅ 註冊缺少欄位（400 Bad Request）
- ✅ 登入成功並返回 tokens
- ✅ 登入帳號不存在（401）
- ✅ 登入密碼錯誤（401）
- ✅ Refresh token 成功
- ✅ Refresh token 無效（401）

### 字詞端點 (GET /api/words/random)
- ✅ 返回正確的 JSON 格式（含 id, word, zhuyin, keys）
- ✅ zhuyin 和 keys 陣列長度匹配
- ✅ 隨機性（返回不同的字）
- ✅ 支援 input_method 參數

### 練習記錄端點 (POST /api/attempts, GET /api/attempts)
- ✅ 記錄練習成功（202 Accepted）
- ✅ 未認證返回 401
- ✅ 缺少必要欄位返回 400
- ✅ 查詢練習歷史成功
- ✅ 分頁功能（page, limit）
- ✅ 篩選功能（is_correct）

### 健康檢查端點 (GET /health)
- ✅ 返回狀態和資料庫連線狀態
- ✅ 顯示已載入的字詞數量

### 整合測試
- ✅ 完整使用者流程：註冊 → 登入 → 練習 → 查看歷史

### 安全性測試
- ✅ 密碼使用 bcrypt 加密
- ✅ 過期/無效 token 被拒絕
- ✅ 缺少 Authorization header 被拒絕

## 前置需求

### 1. PostgreSQL 測試資料庫

創建測試專用資料庫：

```bash
# 方案 A: 使用 createdb 指令
createdb -U zhuyin_user zhuyin_practice_test

# 方案 B: 使用 psql
sudo -u postgres psql
CREATE DATABASE zhuyin_practice_test;
GRANT ALL PRIVILEGES ON DATABASE zhuyin_practice_test TO zhuyin_user;
\q
```

### 2. 初始化測試資料庫結構

執行遷移腳本：

```bash
cd /home/vboxuser/Downloads/Claude/test
psql -U zhuyin_user -d zhuyin_practice_test -f backend/migrations/init_db.sql
```

### 3. 設定測試環境變數（選填）

創建 `.env.test` 檔案或設定環境變數：

```bash
export TEST_DATABASE_URL="postgresql://zhuyin_user:your_password@localhost:5432/zhuyin_practice_test"
```

## 執行測試

### 執行所有測試

```bash
cd tests/backend
pytest test_api.py -v
```

### 執行特定測試

```bash
# 只測試認證端點
pytest test_api.py::test_register_success -v

# 只測試登入
pytest test_api.py::test_login_success -v

# 只測試完整流程
pytest test_api.py::test_full_user_flow -v
```

### 執行測試並顯示詳細輸出

```bash
pytest test_api.py -v -s
```

### 執行測試並產生覆蓋率報告

```bash
pytest test_api.py --cov=../../backend --cov-report=html
```

## 測試結構

```python
# Fixtures
- client: Flask 測試客戶端（每個測試自動清理資料）

# Helper Functions
- cleanup_test_data(): 清理測試資料
- create_test_user(username, password): 創建測試使用者
- get_auth_headers(client, username, password): 取得認證 headers
```

## 測試資料清理

測試使用 `test_*` 開頭的使用者名稱，測試完成後自動清理。不會影響生產資料。

## 常見問題

### Q: 測試失敗提示「database connection failed」

A: 確認：
1. PostgreSQL 服務正在運行：`sudo systemctl status postgresql`
2. 測試資料庫已創建：`psql -U zhuyin_user -l | grep test`
3. 連線資訊正確：檢查 `backend/test_config.py`

### Q: 測試失敗提示「relation does not exist」

A: 測試資料庫未初始化，執行：
```bash
psql -U zhuyin_user -d zhuyin_practice_test -f backend/migrations/init_db.sql
```

### Q: 如何重置測試資料庫？

A: 刪除並重新創建：
```bash
dropdb -U zhuyin_user zhuyin_practice_test
createdb -U zhuyin_user zhuyin_practice_test
psql -U zhuyin_user -d zhuyin_practice_test -f backend/migrations/init_db.sql
```

### Q: 測試很慢怎麼辦？

A: 測試配置使用較低的 bcrypt work factor (4) 以加快速度。如果仍然慢，檢查：
1. 資料庫連線池設定（test_config.py）
2. 每個測試的資料清理邏輯

## CI/CD 整合

在 CI/CD 環境中運行測試：

```yaml
# GitHub Actions 範例
- name: Set up PostgreSQL
  run: |
    sudo systemctl start postgresql
    sudo -u postgres psql -c "CREATE DATABASE zhuyin_practice_test;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE zhuyin_practice_test TO zhuyin_user;"

- name: Run migrations
  run: psql -U zhuyin_user -d zhuyin_practice_test -f backend/migrations/init_db.sql

- name: Run tests
  run: |
    cd tests/backend
    pytest test_api.py -v --tb=short
```

## 測試覆蓋率目標

- **端點覆蓋**: 100% (所有 API 端點)
- **狀態碼覆蓋**: 100% (成功和錯誤情況)
- **業務邏輯覆蓋**: ≥80%
- **整合測試**: 完整使用者流程

## 維護

新增功能時，請同時更新測試：
1. 新增對應的測試函式
2. 更新本 README 的測試覆蓋範圍列表
3. 確保所有測試通過後再提交
