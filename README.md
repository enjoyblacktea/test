# 注音輸入法練習網站

一個簡單、可測試的注音輸入法練習工具，專為習慣其他輸入法（如拼音、倉頡）想學習注音的使用者設計。

## 功能特色

- ✅ **完整後端認證** - JWT token 認證系統，支援註冊、登入、自動 token 刷新
- ✅ **練習歷史記錄** - PostgreSQL 資料庫持久化儲存每次練習記錄
- ✅ **看中文打注音** - 顯示中文字，使用者輸入對應的注音符號
- ✅ **虛擬鍵盤** - 顯示完整的注音鍵盤配置供參考
- ✅ **即時視覺回饋** - 按下按鍵時虛擬鍵盤會高亮顯示
- ✅ **非阻塞記錄** - 練習記錄異步儲存，不影響使用者體驗
- ✅ **模組化設計** - 每個功能模組都可以獨立測試
- ✅ **無框架** - 使用 Vanilla JS + HTML + CSS，輕量且易於理解

## 系統需求

### 瀏覽器要求
- Chrome 61+ 
- Firefox 60+ 
- Safari 11+

（需要支援 ES6 Modules 的現代瀏覽器）

### 後端要求
- Python 3.10+
- PostgreSQL 12+
- uv（現代 Python 套件管理工具）

#### 安裝 uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 安裝 PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Windows:**
下載並安裝 [PostgreSQL](https://www.postgresql.org/download/windows/)

## 快速開始

### 1. 建立資料庫

```bash
# 切換到 postgres 使用者
sudo -u postgres psql

# 在 PostgreSQL shell 中執行
CREATE DATABASE zhuyin_practice;
CREATE USER zhuyin_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE zhuyin_practice TO zhuyin_user;
\q
```

### 2. 初始化資料庫結構

```bash
# 執行資料庫遷移腳本
psql -U zhuyin_user -d zhuyin_practice -f backend/migrations/init_db.sql
```

這會建立 3 個資料表（users, characters, typing_attempts）並載入 30 個練習字詞。

### 3. 設定環境變數

建立 `backend/.env` 檔案：

```bash
# 資料庫連線
DATABASE_URL=postgresql://zhuyin_user:your_password@localhost:5432/zhuyin_practice

# JWT 密鑰（請使用安全的隨機字串）
JWT_SECRET_KEY=your-secret-key-change-in-production

# 可選配置
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
BCRYPT_WORK_FACTOR=12
```

**⚠️ 重要**: 生產環境請使用強密碼和安全的 JWT 密鑰！

### 4. 安裝後端依賴

```bash
cd backend
uv sync
```

這會自動建立虛擬環境（`.venv`）並安裝所有依賴，包括 PostgreSQL 驅動程式。

### 5. 啟動後端伺服器

```bash
cd backend
uv run python app.py
```

伺服器會在 http://localhost:5000 啟動。

如果資料庫連線成功，你會看到：
```
✓ Database connection established
Flask app running on http://localhost:5000
```

### 6. 開啟前端網頁

**方法 A: 使用 HTTP 伺服器（推薦）**

```bash
cd frontend
python3 -m http.server 8000
```

然後在瀏覽器開啟 http://localhost:8000

**方法 B: 直接開啟檔案**

直接用瀏覽器開啟 `frontend/login.html` 檔案。

> **注意**: 部分瀏覽器可能因為 CORS 政策限制，直接開啟檔案時無法正常呼叫 API。建議使用方法 A。

### 7. 註冊並登入

首次開啟應用程式時，會顯示登入畫面：

1. **註冊新帳號**：點擊「註冊」標籤，輸入帳號（至少 3 字元）和密碼（至少 6 字元）
2. **登入**：使用剛註冊的帳號登入，系統會自動儲存 JWT token

> ✅ **安全**：密碼使用 bcrypt 加密儲存，JWT token 有效期限 1 小時（自動刷新）

### 8. 開始練習

1. 查看螢幕上顯示的中文字
2. 參考虛擬鍵盤，使用實體鍵盤輸入對應的注音符號
3. 輸入正確時，虛擬鍵盤會高亮顯示
4. 完成一個字後，自動載入下一個字並記錄練習結果
5. 若要登出，點擊畫面右上角的「登出」按鈕

**練習記錄**：每次完成的字都會自動儲存到資料庫，包括：
- 練習的字
- 是否正確完成
- 開始和結束時間
- 完成所需時間（毫秒）

## 專案結構

```
zhuyin-practice/
├── frontend/                    # 前端檔案
│   ├── login.html              # 登入/註冊頁面
│   ├── index.html              # 主練習頁面（需要認證）
│   ├── styles/                 # CSS 樣式
│   │   ├── main.css           # 全域樣式
│   │   ├── keyboard.css       # 鍵盤樣式
│   │   ├── practice.css       # 練習區樣式
│   │   └── login.css          # 登入畫面樣式
│   └── js/                     # JavaScript 檔案
│       ├── main.js            # 入口點（檢查認證狀態）
│       └── modules/           # ES6 模組
│           ├── api.js         # API 客戶端（JWT token 管理）
│           ├── auth-backend.js # 後端認證模組（註冊、登入、登出）
│           ├── zhuyin-map.js  # 注音映射表
│           ├── keyboard.js    # 虛擬鍵盤
│           ├── practice.js    # 練習邏輯（含記錄功能）
│           └── input-handler.js # 輸入處理
│
├── backend/                     # 後端檔案
│   ├── app.py                  # Flask 應用程式入口點
│   ├── config.py               # 配置管理（資料庫、JWT 設定）
│   ├── routes/                 # API 路由層
│   │   ├── words.py           # 字詞 API 端點
│   │   ├── auth.py            # 認證 API 端點（註冊、登入、token 刷新）
│   │   ├── attempts.py        # 練習記錄 API 端點
│   │   └── health.py          # 健康檢查端點
│   ├── services/               # 業務邏輯層
│   │   ├── db_service.py      # 資料庫連線池管理
│   │   ├── auth_service.py    # JWT 和密碼加密服務
│   │   ├── character_service.py # 字詞查詢和注音轉換
│   │   └── attempt_service.py  # 練習記錄管理
│   ├── migrations/             # 資料庫遷移腳本
│   │   └── init_db.sql        # 初始化資料庫結構和種子資料
│   ├── pyproject.toml         # 專案配置與依賴定義
│   ├── uv.lock                # 依賴鎖定檔（確保可重現建置）
│   └── data/                   # 資料檔案（已棄用，改用資料庫）
│       └── words.json         # [已棄用] 練習字詞資料
│
└── tests/                       # 測試檔案
    ├── frontend/               # 前端測試
    │   └── test.html          # 單元測試頁面
    ├── backend/                # 後端測試
    │   └── test_api.py        # API 測試
    └── INTEGRATION_TEST_CHECKLIST.md  # 整合測試清單
```

## 後端架構

後端採用簡潔的三層模組化架構，支援 PostgreSQL 資料庫和 JWT 認證：

```
┌─────────────────────────────────┐
│      app.py (入口點)            │
│  建立 Flask app、CORS、連線池  │
└────────────┬────────────────────┘
             │
    ┌────────┴────────────────────┐
    │                             │
┌───▼──────┐    ┌────▼──────────┐
│  routes/ │    │   services/    │
│ (HTTP層) │───>│ (業務邏輯層)   │
│          │    │                │
│ auth.py  │    │ db_service.py  │
│ words.py │    │ auth_service.py│
│attempts.py    │character_srv.js│
│ health.py│    │ attempt_srv.js │
└──────────┘    └─────┬──────────┘
                      │
           ┌──────────┴──────────┐
           │                     │
     ┌─────▼──────┐    ┌────────▼──────┐
     │ config.py  │    │  PostgreSQL   │
     │ (配置層)   │    │  (資料持久層) │
     └────────────┘    └───────────────┘
```

### 架構原則

1. **單向依賴流**：routes → services → (config + database)（無循環依賴）
2. **關注點分離**：HTTP 處理、業務邏輯、資料庫存取、配置管理各司其職
3. **連線池管理**：使用 psycopg2 連線池提升效能
4. **JWT 認證**：所有需要認證的端點使用 @require_auth 裝飾器
5. **易於測試**：每一層都可以獨立測試和 mock

### 模組職責

#### `app.py` - 應用程式入口點
- 建立 Flask 應用程式
- 配置 CORS
- 初始化資料庫連線池
- 註冊所有 Blueprints（auth, words, attempts, health）

#### `config.py` - 配置管理
- 集中管理所有配置值
  - 資料庫連線（DATABASE_URL, 連線池設定）
  - JWT 設定（密鑰、過期時間、演算法）
  - Bcrypt 工作因子
- 提供 `Config` 類別供其他模組引用
- 支援環境變數覆寫（透過 .env 檔案）

#### `routes/` - 路由層
- 處理 HTTP 請求和回應
- 將請求委派給 services 處理
- 將回應格式化為 JSON
- **不包含業務邏輯**
- `auth.py`: 提供 @require_auth 裝飾器保護需要認證的端點

#### `services/` - 業務邏輯層
- 包含所有業務邏輯（資料查詢、處理、驗證）
- 獨立於 HTTP 和 Flask
- 易於單元測試
- **db_service**: 管理 PostgreSQL 連線池，提供 execute_query 統一介面
- **auth_service**: JWT token 生成/驗證、bcrypt 密碼加密
- **character_service**: 字詞查詢、input_code 轉 zhuyin 陣列
- **attempt_service**: 練習記錄儲存和查詢（含分頁、篩選）

### 新增功能範例

假設要添加一個新的 API 端點 `GET /api/words/list`：

1. **在 services 添加業務邏輯**：
   ```python
   # services/word_service.py
   def get_all_words():
       return _words_data
   ```

2. **在 routes 添加端點**：
   ```python
   # routes/words.py
   @words_bp.route('/list', methods=['GET'])
   def list_words():
       words = word_service.get_all_words()
       return jsonify(words)
   ```

3. **完成！** 不需要修改 `app.py`，Blueprint 會自動處理路由

## API 文件

### 認證端點

#### POST /api/auth/register
註冊新使用者帳號。

**請求:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**成功回應 (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "user123",
    "created_at": "2026-02-27T10:00:00Z"
  }
}
```

**錯誤回應:**
- `409 Conflict`: 使用者名稱已存在
- `400 Bad Request`: 缺少欄位或格式錯誤

#### POST /api/auth/login
使用者登入，返回 JWT tokens。

**請求:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**成功回應 (200 OK):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "user123"
  }
}
```

**Token 有效期:**
- Access token: 1 小時
- Refresh token: 7 天

**錯誤回應:**
- `401 Unauthorized`: 帳號或密碼錯誤

#### POST /api/auth/refresh
使用 refresh token 取得新的 access token。

**請求:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**成功回應 (200 OK):**
```json
{
  "access_token": "eyJhbGc..."
}
```

**錯誤回應:**
- `401 Unauthorized`: Refresh token 無效或已過期

### 字詞端點

#### GET /api/words/random
返回一個隨機的練習字詞（從資料庫）。

**查詢參數:**
- `input_method` (選填): 輸入法類型，預設 `bopomofo`

**回應格式:**
```json
{
  "id": 1,
  "word": "你",
  "zhuyin": ["ㄋ", "ㄧ", "ˇ"],
  "keys": ["s", "u", "3"]
}
```

- `id`: 字詞資料庫 ID（用於記錄練習）
- `word`: 中文字
- `zhuyin`: 注音符號陣列
- `keys`: 對應的鍵盤按鍵陣列

### 練習記錄端點（需要認證）

#### POST /api/attempts
記錄一次練習嘗試（非阻塞，立即返回 202）。

**Headers:**
```
Authorization: Bearer <access_token>
```

**請求:**
```json
{
  "character_id": 1,
  "started_at": "2026-02-27T10:00:00.000Z",
  "ended_at": "2026-02-27T10:00:02.500Z",
  "is_correct": true
}
```

**成功回應 (202 Accepted):**
```json
{
  "message": "Attempt recorded"
}
```

**錯誤回應:**
- `401 Unauthorized`: 缺少或無效的 token
- `400 Bad Request`: 缺少必要欄位

#### GET /api/attempts
查詢使用者的練習歷史（分頁）。

**Headers:**
```
Authorization: Bearer <access_token>
```

**查詢參數:**
- `page` (選填): 頁碼，預設 1
- `limit` (選填): 每頁筆數，預設 50，最大 100
- `is_correct` (選填): 篩選正確/錯誤，`true` 或 `false`
- `character_id` (選填): 篩選特定字詞
- `start_date` (選填): 開始日期 ISO 8601 格式
- `end_date` (選填): 結束日期 ISO 8601 格式

**成功回應 (200 OK):**
```json
{
  "attempts": [
    {
      "id": 123,
      "character": "你",
      "is_correct": true,
      "started_at": "2026-02-27T10:00:00.000Z",
      "ended_at": "2026-02-27T10:00:02.500Z",
      "duration_ms": 2500
    }
  ],
  "pagination": {
    "total_count": 150,
    "page": 1,
    "limit": 50,
    "has_more": true
  }
}
```

### 健康檢查端點

#### GET /health
系統健康檢查，包含資料庫連線測試。

**回應格式 (200 OK):**
```json
{
  "status": "ok",
  "database": "connected",
  "characters_loaded": 30
}
```

**錯誤回應 (503 Service Unavailable):**
```json
{
  "status": "error",
  "database": "disconnected",
  "error": "Database connection failed"
}
```

## 執行測試

### 前端測試

在瀏覽器中開啟 `tests/frontend/test.html`

測試包含:
- 注音映射表完整性
- 鍵盤高亮功能
- 輸入驗證邏輯
- 一聲處理（空格和自動前進）

### 後端測試

```bash
cd backend
uv run pytest ../tests/backend/ -v
```

測試包含:
- API 端點格式驗證
- 資料格式檢查
- 錯誤處理

### 整合測試

參考 `tests/INTEGRATION_TEST_CHECKLIST.md` 執行完整的端對端測試。

## 注音鍵盤對應表

### 聲母
| 注音 | 鍵盤 | 注音 | 鍵盤 | 注音 | 鍵盤 |
|-----|------|-----|------|-----|------|
| ㄅ  | 1    | ㄉ  | 2    | ㄍ  | e    |
| ㄆ  | q    | ㄊ  | w    | ㄎ  | d    |
| ㄇ  | a    | ㄋ  | s    | ㄏ  | c    |
| ㄈ  | z    | ㄌ  | x    | ㄐ  | r    |
| ㄓ  | 5    | ㄗ  | y    | ㄑ  | f    |
| ㄔ  | t    | ㄘ  | h    | ㄒ  | v    |
| ㄕ  | g    | ㄙ  | n    | ㄖ  | b    |

### 韻母
| 注音 | 鍵盤 | 注音 | 鍵盤 | 注音 | 鍵盤 |
|-----|------|-----|------|-----|------|
| ㄧ  | u    | ㄚ  | 8    | ㄞ  | 9    |
| ㄨ  | j    | ㄛ  | i    | ㄟ  | o    |
| ㄩ  | m    | ㄜ  | k    | ㄠ  | l    |
| ㄝ  | ,    | ㄡ  | .    | ㄢ  | 0    |
| ㄣ  | p    | ㄤ  | ;    | ㄥ  | /    |
| ㄦ  | -    |

### 聲調
| 聲調 | 符號 | 鍵盤 |
|-----|------|------|
| 一聲 | (無)  | Space |
| 二聲 | ˊ    | 6     |
| 三聲 | ˇ    | 3     |
| 四聲 | ˋ    | 4     |
| 輕聲 | ˙    | 7     |

## words.json 格式範例

```json
[
  {
    "word": "你",
    "zhuyin": ["ㄋ", "ㄧ", "ˇ"],
    "keys": ["s", "u", "3"]
  },
  {
    "word": "好",
    "zhuyin": ["ㄏ", "ㄠ", "ˇ"],
    "keys": ["c", "l", "3"]
  }
]
```

每個字詞包含:
- `word`: 中文字（字串）
- `zhuyin`: 注音符號陣列（包含聲母、韻母、聲調）
- `keys`: 對應的鍵盤按鍵陣列（與 zhuyin 一一對應）

> **注意**: 一聲用空格 `" "` 表示，可以明確按空格鍵，或在輸入下一個字時自動跳過。

## 技術決策

### 前端
- **ES6 Modules**: 模組化設計，無需建置工具
- **CSS Grid**: 虛擬鍵盤排版
- **前端驗證**: 即時回饋，無需伺服器往返

### 後端
- **Flask**: 輕量級框架，簡單易用
- **Flask Blueprints**: 模組化路由組織
- **flask-cors**: 處理跨域請求
- **靜態 JSON**: 簡單可靠的資料儲存
- **uv + pyproject.toml**: 現代 Python 套件管理，提供快速安裝與可重現建置（透過 `uv.lock`）
- **模組化架構**: routes → services → config 三層分離

### 環境變數配置

後端支援以下環境變數（透過 `.env` 檔案或環境變數設定）：

#### 必要設定

- `DATABASE_URL`: PostgreSQL 連線字串
  - 格式: `postgresql://username:password@host:port/database`
  - 範例: `postgresql://zhuyin_user:password@localhost:5432/zhuyin_practice`

- `JWT_SECRET_KEY`: JWT token 簽署密鑰
  - **重要**: 生產環境必須使用強隨機密鑰
  - 產生方式: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
  - 範例: `your-secret-key-change-in-production`

#### 可選設定

- `PORT`: 伺服器端口（預設：5000）
- `FLASK_ENV`: 環境模式（`development` 啟用除錯模式）
- `DB_POOL_SIZE`: 連線池最小連線數（預設：5）
- `DB_MAX_OVERFLOW`: 連線池最大溢出連線數（預設：10）
- `DB_POOL_RECYCLE`: 連線回收時間秒數（預設：3600）
- `BCRYPT_WORK_FACTOR`: Bcrypt 工作因子（預設：12）

#### .env 檔案範例

建立 `backend/.env`：

```env
# 資料庫配置
DATABASE_URL=postgresql://zhuyin_user:your_password@localhost:5432/zhuyin_practice
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_RECYCLE=3600

# JWT 安全配置
JWT_SECRET_KEY=your-secret-key-change-in-production

# 密碼加密
BCRYPT_WORK_FACTOR=12

# 伺服器配置
PORT=5000
FLASK_ENV=development
```

#### 生產環境安全建議

1. **JWT_SECRET_KEY**: 使用至少 32 字元的隨機字串
2. **DATABASE_URL**: 使用強密碼，不要使用預設密碼
3. **BCRYPT_WORK_FACTOR**: 根據伺服器效能調整（8-14 之間）
4. **FLASK_ENV**: 生產環境移除或設為 `production`

### 測試
- **前端**: 獨立的 HTML 測試頁面
- **後端**: pytest 單元測試
- **整合**: 手動測試清單

## 資料庫遷移和維護

### 初始化資料庫

使用 `backend/migrations/init_db.sql` 建立資料庫結構：

```bash
psql -U zhuyin_user -d zhuyin_practice -f backend/migrations/init_db.sql
```

此腳本會建立：
- 3 個資料表（users, characters, typing_attempts）
- 5 個索引（提升查詢效能）
- 外鍵約束（資料完整性）
- 30 個練習字詞的種子資料

### 回滾策略

如果遷移到資料庫後遇到問題，可以使用以下策略回滾：

#### 方案 A: 保留資料庫，切換回舊版本（推薦）

1. 切換到舊的 git 分支：
   ```bash
   git checkout main
   ```

2. 資料庫保持運行，舊版本會使用 `words.json` 檔案

3. 新資料不會遺失，未來可以再次切換回新版本

#### 方案 B: 完全移除資料庫

1. 停止後端伺服器

2. 移除資料庫：
   ```bash
   sudo -u postgres psql
   DROP DATABASE zhuyin_practice;
   DROP USER zhuyin_user;
   \q
   ```

3. 切換到舊的 git 分支

### 資料庫維護

#### 查看資料庫狀態

```bash
# 連線到資料庫
psql -U zhuyin_user -d zhuyin_practice

# 查看所有資料表
\dt

# 查看使用者數量
SELECT COUNT(*) FROM users;

# 查看練習記錄總數
SELECT COUNT(*) FROM typing_attempts;

# 查看最近 10 筆練習記錄
SELECT * FROM typing_attempts ORDER BY created_at DESC LIMIT 10;
```

#### 清除測試資料

```sql
-- 清除所有練習記錄（保留使用者和字詞）
DELETE FROM typing_attempts;

-- 清除測試使用者（會連帶刪除其練習記錄）
DELETE FROM users WHERE username = 'test_user';
```

#### 重建索引（如果查詢變慢）

```sql
-- 重建所有索引
REINDEX DATABASE zhuyin_practice;
```

## 已實作功能

- ✅ 後端認證和進度儲存（PostgreSQL + JWT）
- ✅ 練習歷史記錄（時間、正確性、完成時間）
- ✅ 使用者帳戶管理（註冊、登入、安全密碼加密）
- ✅ 連線池管理（可配置的連線數量和回收時間）
- ✅ 非阻塞練習記錄（不影響使用者體驗）
- ✅ API 查詢和篩選（分頁、日期範圍、正確性篩選）

## 未來改進

此專案持續演進中，未來可以加入：

- 統計功能視覺化（速度趨勢圖、準確率分析）
- 按鍵層級記錄（keystroke_events 表）
- 錯誤提示和引導
- 多種難度級別
- 多輸入法支援（拼音、倉頡等）
- 行動裝置支援和響應式設計
- 更多練習字詞
- 詞組練習（多字詞）
- 文章打字練習
- 社群功能（排行榜、挑戰）

## 授權

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 常見問題

### Q: uv 是什麼？為什麼使用它？
A: uv 是新一代的 Python 套件管理工具，提供：
- **極快的速度**：比 pip 快 10-100 倍
- **可重現建置**：透過 `uv.lock` 鎖定所有依賴版本
- **自動管理虛擬環境**：無需手動建立和啟動 venv
- **現代化標準**：完全支援 PEP 621（pyproject.toml）

常用指令：
- `uv sync` - 安裝所有依賴（根據 pyproject.toml 和 uv.lock）
- `uv add <package>` - 新增依賴套件
- `uv run <command>` - 在虛擬環境中執行指令

### Q: 如果我想使用 pip 而不是 uv？
A: `pyproject.toml` 是標準格式，pip 也支援：
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

但使用 uv 可以獲得更快的速度和可重現的建置。

### Q: 為什麼使用 uv 而不是 pip？
A: uv 是更快的 Python 套件管理工具，但如果你習慣 pip 也可以使用：
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Q: 一聲為什麼可以不按空格？
A: 這是注音輸入法的常見設計。當字詞的最後一個符號是一聲時，可以：
1. 明確按空格鍵
2. 或直接開始輸入下一個字（自動前進）

兩種方式都被支援。

### Q: 可以新增自己的練習字詞嗎？
A: 可以！編輯 `backend/data/words.json`，按照格式新增字詞即可。確保 `zhuyin` 和 `keys` 陣列長度一致。

### Q: 為什麼前端使用 ES6 Modules 而不是打包工具？
A: 為了保持 MVP 的簡單性和可測試性。所有現代瀏覽器都支援 ES6 Modules，不需要額外的建置步驟。

### Q: 登入功能安全嗎？
A: **是的**，本專案使用業界標準的安全實作：
- ✅ 密碼使用 bcrypt 加密（work factor 12）
- ✅ JWT token 認證（access token 1 小時，refresh token 7 天）
- ✅ PostgreSQL 資料庫持久化儲存
- ✅ 自動 token 刷新機制
- ✅ 所有需要認證的 API 端點都有保護

**生產環境建議**：
- 使用 HTTPS
- 設定強 JWT 密鑰
- 使用強資料庫密碼
- 限制資料庫存取（防火牆規則）

### Q: 如何重設登入狀態？
A: 可以透過以下方式：
1. **點擊「登出」按鈕**（推薦）- 清除 tokens 並重新導向登入頁
2. 清除瀏覽器的 LocalStorage（開發者工具 → Application → Local Storage → 刪除 tokens）
3. 等待 token 過期（access token 1 小時後自動失效）

### Q: 忘記密碼怎麼辦？
A: 目前版本尚未實作密碼重設功能。可以透過以下方式處理：
1. **開發環境**: 直接在資料庫中更新密碼 hash
2. **未來功能**: 計畫加入電子郵件驗證的密碼重設流程

### Q: 如何備份練習資料？
A: 練習記錄儲存在 PostgreSQL 資料庫中，可以使用標準工具備份：

```bash
# 備份整個資料庫
pg_dump -U zhuyin_user zhuyin_practice > backup.sql

# 恢復資料庫
psql -U zhuyin_user zhuyin_practice < backup.sql

# 僅備份練習記錄
pg_dump -U zhuyin_user -t typing_attempts zhuyin_practice > attempts_backup.sql
```

### Q: 可以在不同電腦同步練習進度嗎？
A: 可以！練習資料儲存在後端資料庫中，只要：
1. 使用相同帳號登入
2. 連接到同一個後端伺服器（DATABASE_URL）

所有練習記錄都會自動同步。

### Q: 資料庫連線池是什麼？如何調整？
A: 連線池（Connection Pool）是資料庫連線的快取機制，可以提升效能：

**預設設定**:
- `DB_POOL_SIZE=5`: 最小連線數
- `DB_MAX_OVERFLOW=10`: 最大溢出連線數
- `DB_POOL_RECYCLE=3600`: 連線回收時間（秒）

**調整建議**:
- 低流量（個人使用）: 5-10 連線
- 中流量（小班級）: 10-20 連線
- 高流量（大班級）: 20-50 連線

在 `.env` 檔案中調整這些值。

## 開發團隊

使用 OpenSpec 工作流程開發
