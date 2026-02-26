# 注音輸入法練習網站

一個簡單、可測試的注音輸入法練習工具，專為習慣其他輸入法（如拼音、倉頡）想學習注音的使用者設計。

## 功能特色

- ✅ **使用者認證** - 簡單的登入系統，需要帳號密碼才能使用練習功能
- ✅ **練習歷史追蹤** - 自動記錄每次練習的字詞、正確性、用時，支援統計查詢
- ✅ **看中文打注音** - 顯示中文字，使用者輸入對應的注音符號
- ✅ **虛擬鍵盤** - 顯示完整的注音鍵盤配置供參考
- ✅ **即時視覺回饋** - 按下按鍵時虛擬鍵盤會高亮顯示
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
- uv（現代 Python 套件管理工具）
- PostgreSQL 12+（用於練習歷史記錄功能）

#### 安裝 uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 快速開始

### 1. PostgreSQL 資料庫設置

練習歷史記錄功能需要 PostgreSQL 資料庫。如果您不需要此功能，可以跳過此步驟。

#### 1.1 安裝 PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
從 [PostgreSQL 官網](https://www.postgresql.org/download/windows/) 下載安裝程式。

#### 1.2 建立資料庫

```bash
# 連線到 PostgreSQL
sudo -u postgres psql

# 在 psql 命令列中執行
CREATE DATABASE zhuyin_practice;

# 離開 psql
\q
```

#### 1.3 執行資料庫 Migration

```bash
cd backend
psql -U postgres -d zhuyin_practice -f migrations/init_db.sql
```

如果遇到權限問題，可能需要設置 PostgreSQL 密碼或使用 sudo。

#### 1.4 配置環境變數

在 `backend/` 目錄下建立 `.env` 檔案：

```bash
cd backend
cat > .env << EOF
# PostgreSQL 連線配置
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=zhuyin_practice
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
EOF
```

根據您的 PostgreSQL 設置調整 `POSTGRES_USER` 和 `POSTGRES_PASSWORD`。

> **遠端資料庫**: 如果使用遠端 PostgreSQL，請修改 `POSTGRES_HOST` 為遠端 IP 位址。

#### 1.5 驗證資料庫連線

```bash
cd backend
psql -U postgres -d zhuyin_practice -c "\dt"
```

應該會看到 `users` 和 `practice_history` 兩個資料表。

### 2. 安裝後端依賴

```bash
cd backend
uv sync
```

這會自動建立虛擬環境（`.venv`）並安裝所有依賴，包括開發工具。

### 3. 啟動後端伺服器

```bash
cd backend
uv run python app.py
```

伺服器會在 http://localhost:5000 啟動。

### 4. 開啟前端網頁

**方法 A: 使用 HTTP 伺服器（推薦）**

```bash
cd frontend
python3 -m http.server 8000
```

然後在瀏覽器開啟 http://localhost:8000

**方法 B: 直接開啟檔案**

直接用瀏覽器開啟 `frontend/index.html` 檔案。

> **注意**: 部分瀏覽器可能因為 CORS 政策限制，直接開啟檔案時無法正常呼叫 API。建議使用方法 A。

### 5. 登入系統

首次開啟應用程式時，會顯示登入畫面。請使用以下憑證登入：

- **帳號**: `user`
- **密碼**: `1234`

> ⚠️ **注意**：這是教育用途的簡化實作，帳號密碼儲存在前端程式碼中，不適合生產環境使用。

### 6. 開始練習

1. 查看螢幕上顯示的中文字
2. 參考虛擬鍵盤，使用實體鍵盤輸入對應的注音符號
3. 輸入正確時，虛擬鍵盤會高亮顯示
4. 完成一個字後，自動載入下一個字
5. 若要登出，點擊畫面右上角的「登出」按鈕

## 專案結構

```
zhuyin-practice/
├── frontend/                    # 前端檔案
│   ├── index.html              # 主頁面
│   ├── index-redesign.html     # 重新設計的主頁面（書法主題 + 登入功能）
│   ├── styles/                 # CSS 樣式
│   │   ├── main.css           # 全域樣式
│   │   ├── keyboard.css       # 鍵盤樣式
│   │   ├── practice.css       # 練習區樣式
│   │   └── login.css          # 登入畫面樣式
│   └── js/                     # JavaScript 檔案
│       ├── main.js            # 入口點
│       ├── main-redesign.js   # 重新設計的入口點（含認證流程）
│       └── modules/           # ES6 模組
│           ├── zhuyin-map.js  # 注音映射表
│           ├── keyboard.js    # 虛擬鍵盤
│           ├── practice.js    # 練習邏輯
│           ├── input-handler.js # 輸入處理
│           └── auth.js        # 認證模組
│
├── backend/                     # 後端檔案
│   ├── app.py                  # Flask 應用程式入口點
│   ├── config.py               # 配置管理
│   ├── .env                    # 環境變數設定（PostgreSQL 連線資訊）
│   ├── routes/                 # API 路由層
│   │   ├── words.py           # 字詞 API 端點
│   │   ├── health.py          # 健康檢查端點
│   │   └── history.py         # 練習歷史 API 端點
│   ├── services/               # 業務邏輯層
│   │   ├── word_service.py    # 字詞資料管理
│   │   ├── db_service.py      # PostgreSQL 連線池管理
│   │   └── history_service.py # 練習歷史記錄服務
│   ├── migrations/             # 資料庫 Migration 檔案
│   │   └── init_db.sql        # 建立資料表和索引
│   ├── pyproject.toml         # 專案配置與依賴定義
│   ├── uv.lock                # 依賴鎖定檔（確保可重現建置）
│   └── data/                   # 資料檔案
│       └── words.json         # 練習字詞資料
│
└── tests/                       # 測試檔案
    ├── frontend/               # 前端測試
    │   └── test.html          # 單元測試頁面
    ├── backend/                # 後端測試
    │   └── test_api.py        # API 測試
    └── INTEGRATION_TEST_CHECKLIST.md  # 整合測試清單
```

## 後端架構

後端採用簡潔的模組化架構，將程式碼組織為三個清晰的層次：

```
┌─────────────────────────────────┐
│      app.py (入口點)            │
│   建立 Flask app 並註冊路由     │
│   初始化資料庫連線池            │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──────┐    ┌────▼────────────┐
│  routes/ │    │   services/     │
│ (HTTP層) │───>│ (業務邏輯層)    │
│          │    │  - word_service │
│          │    │  - db_service   │
│          │    │  - history_svc  │
└──────────┘    └─────┬───────────┘
                      │
                ┌─────▼──────────┐
                │  config.py      │
                │  (配置層)       │
                │  + PostgreSQL   │
                └────────┬────────┘
                         │
                   ┌─────▼─────┐
                   │PostgreSQL │
                   │ Database  │
                   └───────────┘
```

### 架構原則

1. **單向依賴流**：routes → services → config（無循環依賴）
2. **關注點分離**：HTTP 處理、業務邏輯、配置管理各司其職
3. **易於測試**：每一層都可以獨立測試和 mock

### 模組職責

#### `app.py` - 應用程式入口點
- 建立 Flask 應用程式
- 配置 CORS
- 註冊所有 Blueprints
- 簡潔明瞭（~15 行）

#### `config.py` - 配置管理
- 集中管理所有配置值（檔案路徑、端口、環境變數）
- 提供 `Config` 類別供其他模組引用
- 避免硬編碼，支援環境變數覆寫

#### `routes/` - 路由層
- 處理 HTTP 請求和回應
- 將請求委派給 services 處理
- 將回應格式化為 JSON
- **不包含業務邏輯**

#### `services/` - 業務邏輯層
- 包含所有業務邏輯（資料載入、處理）
- 獨立於 HTTP 和 Flask
- 易於單元測試
- 模組啟動時自動初始化資料

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

## 練習歷史追蹤功能

### 功能概述

練習歷史追蹤功能會自動記錄每次練習的詳細資料，包括：
- 練習的字詞
- 輸入是否正確
- 練習開始和結束時間
- 用時（毫秒）

所有記錄都會儲存到 PostgreSQL 資料庫中，並提供 API 查詢統計資料。

### 自動記錄

當使用者完成一個字的練習時，前端會自動呼叫 API 記錄練習資料，整個過程**不會阻塞練習流程**：
- 記錄請求以非同步方式發送（non-blocking）
- 即使 API 失敗，練習仍會繼續進行
- 網路離線時，練習不受影響

### 資料庫結構

系統使用兩個資料表：

#### `users` 資料表
- `id`: 使用者 ID（主鍵）
- `username`: 使用者名稱（唯一）
- `created_at`: 建立時間

#### `practice_history` 資料表
- `id`: 記錄 ID（主鍵）
- `user_id`: 使用者 ID（外鍵）
- `word`: 練習的字詞
- `is_correct`: 是否正確
- `duration_ms`: 用時（毫秒）
- `practiced_at`: 練習時間

### 索引優化

系統建立了以下索引以提升查詢效能：
- `idx_user_time`: (user_id, practiced_at DESC) - 用於歷史查詢
- `idx_username`: (username) - 用於使用者查詢
- `idx_user_correct`: (user_id, is_correct) - 用於統計計算

### 可用的 API

系統提供三個 API 端點：
1. **記錄練習** - `POST /api/history/record` - 記錄單次練習
2. **查詢歷史** - `GET /api/history?username=<user>&limit=<n>&offset=<n>` - 分頁查詢歷史
3. **統計資料** - `GET /api/history/stats?username=<user>` - 查詢練習統計

詳細的 API 文件請參考下方的 **API 文件** section。

### 設計特點

1. **非阻塞設計** - 記錄 API 失敗不影響練習
2. **自動建立使用者** - 首次記錄時自動建立使用者記錄
3. **時間驗證** - 確保結束時間晚於開始時間
4. **分頁支援** - 歷史查詢支援 limit/offset 分頁
5. **連線池管理** - 使用 PostgreSQL 連線池提升效能

## API 文件

### 字詞 API

#### GET /api/words/random

返回一個隨機的練習字詞。

**回應格式:**
```json
{
  "word": "你",
  "zhuyin": ["ㄋ", "ㄧ", "ˇ"],
  "keys": ["s", "u", "3"]
}
```

**欄位說明:**
- `word`: 中文字
- `zhuyin`: 注音符號陣列
- `keys`: 對應的鍵盤按鍵陣列

---

### 練習歷史 API

#### POST /api/history/record

記錄一次練習。系統會自動建立使用者（如果不存在）。

**請求格式:**
```json
{
  "username": "user",
  "word": "你",
  "is_correct": true,
  "start_time": "2026-02-26T10:30:00.000Z",
  "end_time": "2026-02-26T10:30:03.500Z"
}
```

**欄位說明:**
- `username` (string, 必填): 使用者名稱
- `word` (string, 必填): 練習的字詞
- `is_correct` (boolean, 必填): 是否正確輸入
- `start_time` (string, 必填): 開始時間（ISO 8601 格式）
- `end_time` (string, 必填): 結束時間（ISO 8601 格式）

**成功回應 (201 Created):**
```json
{
  "message": "Practice recorded successfully",
  "record_id": 123
}
```

**錯誤回應:**
- `400 Bad Request`: 缺少必填欄位或格式錯誤
  ```json
  {
    "error": "Missing required field: username"
  }
  ```
- `503 Service Unavailable`: 資料庫連線失敗
  ```json
  {
    "error": "Database unavailable"
  }
  ```

#### GET /api/history

查詢使用者的練習歷史（支援分頁）。

**查詢參數:**
- `username` (string, 必填): 使用者名稱
- `limit` (integer, 選填): 返回記錄數量（預設：50，最大：100）
- `offset` (integer, 選填): 跳過的記錄數量（預設：0）

**請求範例:**
```
GET /api/history?username=user&limit=10&offset=0
```

**成功回應 (200 OK):**
```json
{
  "username": "user",
  "total": 45,
  "limit": 10,
  "offset": 0,
  "history": [
    {
      "id": 123,
      "word": "你",
      "is_correct": true,
      "duration_ms": 3500,
      "practiced_at": "2026-02-26T10:30:03.500Z"
    },
    {
      "id": 122,
      "word": "好",
      "is_correct": false,
      "duration_ms": 5200,
      "practiced_at": "2026-02-26T10:29:55.000Z"
    }
  ]
}
```

**欄位說明:**
- `total`: 總記錄數
- `limit`: 當前查詢的限制數量
- `offset`: 當前查詢的起始位置
- `history`: 練習記錄陣列（依時間倒序）
  - `id`: 記錄 ID
  - `word`: 練習的字詞
  - `is_correct`: 是否正確
  - `duration_ms`: 用時（毫秒）
  - `practiced_at`: 練習時間

**錯誤回應:**
- `400 Bad Request`: 缺少 username 參數
- `404 Not Found`: 使用者不存在

#### GET /api/history/stats

查詢使用者的統計資料。

**查詢參數:**
- `username` (string, 必填): 使用者名稱

**請求範例:**
```
GET /api/history/stats?username=user
```

**成功回應 (200 OK):**
```json
{
  "username": "user",
  "total_practices": 45,
  "correct_count": 38,
  "accuracy": 84.44,
  "average_duration_ms": 4250,
  "practice_days": 7
}
```

**欄位說明:**
- `total_practices`: 總練習次數
- `correct_count`: 正確次數
- `accuracy`: 準確率（百分比，保留兩位小數）
- `average_duration_ms`: 平均用時（毫秒）
- `practice_days`: 練習天數（去重計算）

**錯誤回應:**
- `400 Bad Request`: 缺少 username 參數
- `404 Not Found`: 使用者不存在

---

### 健康檢查 API

#### GET /health

健康檢查端點。

**回應格式:**
```json
{
  "status": "ok",
  "words_loaded": 30
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

後端支援以下環境變數（可在 `backend/.env` 檔案中設定）：

#### Flask 伺服器配置
- `PORT`: 伺服器端口（預設：5000）
- `FLASK_ENV`: 環境模式（`development` 啟用除錯模式）

#### PostgreSQL 資料庫配置
- `POSTGRES_HOST`: PostgreSQL 主機位址（預設：localhost）
- `POSTGRES_PORT`: PostgreSQL 端口（預設：5432）
- `POSTGRES_DB`: 資料庫名稱（預設：zhuyin_practice）
- `POSTGRES_USER`: 資料庫使用者名稱（預設：postgres）
- `POSTGRES_PASSWORD`: 資料庫密碼（預設：postgres）

#### 範例 `.env` 檔案

```bash
# Flask 配置
PORT=5000
FLASK_ENV=development

# PostgreSQL 配置（本地）
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=zhuyin_practice
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

#### 使用遠端資料庫

```bash
# PostgreSQL 配置（遠端）
POSTGRES_HOST=10.6.142.157
POSTGRES_PORT=5432
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

範例啟動指令：
```bash
cd backend
uv run python app.py
```

後端會自動讀取 `.env` 檔案中的環境變數。

### 測試
- **前端**: 獨立的 HTML 測試頁面
- **後端**: pytest 單元測試
- **整合**: 手動測試清單

## 未來改進

此專案是 MVP（最小可行產品），未來可以加入：

- 統計功能（速度、準確率）
- 錯誤提示和引導
- 多種難度級別
- 後端認證和進度儲存（目前為前端簡易認證）
- 行動裝置支援
- 更多練習字詞
- 詞組練習（多字詞）
- 文章打字練習

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
A: **不安全**，這是教育用途的簡化實作：
- 帳號密碼明文儲存在前端程式碼中
- 認證狀態儲存在 LocalStorage，使用者可透過開發者工具修改
- 無後端驗證或 session 管理
- 無 session timeout（登入後永久有效直到手動登出）

此實作適合學習和示範，**不適合生產環境**。未來可升級為後端 JWT 認證。

### Q: 如何重設登入狀態？
A: 可以透過以下方式：
1. 點擊「登出」按鈕（推薦）
2. 清除瀏覽器的 LocalStorage（開發者工具 → Application → Local Storage → 刪除 `zhuyin-practice-auth`）
3. 清除瀏覽器快取

## 開發團隊

使用 OpenSpec 工作流程開發
