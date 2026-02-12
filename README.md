# 注音輸入法練習網站

一個簡單、可測試的注音輸入法練習工具，專為習慣其他輸入法（如拼音、倉頡）想學習注音的使用者設計。

## 功能特色

- ✅ **使用者認證** - 簡單的登入系統，需要帳號密碼才能使用練習功能
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

#### 安裝 uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 快速開始

### 1. 安裝後端依賴

```bash
cd backend
uv sync
```

這會自動建立虛擬環境（`.venv`）並安裝所有依賴，包括開發工具。

### 2. 啟動後端伺服器

```bash
cd backend
uv run python app.py
```

伺服器會在 http://localhost:5000 啟動。

### 3. 開啟前端網頁

**方法 A: 使用 HTTP 伺服器（推薦）**

```bash
cd frontend
python3 -m http.server 8000
```

然後在瀏覽器開啟 http://localhost:8000

**方法 B: 直接開啟檔案**

直接用瀏覽器開啟 `frontend/index.html` 檔案。

> **注意**: 部分瀏覽器可能因為 CORS 政策限制，直接開啟檔案時無法正常呼叫 API。建議使用方法 A。

### 4. 登入系統

首次開啟應用程式時，會顯示登入畫面。請使用以下憑證登入：

- **帳號**: `user`
- **密碼**: `1234`

> ⚠️ **注意**：這是教育用途的簡化實作，帳號密碼儲存在前端程式碼中，不適合生產環境使用。

### 5. 開始練習

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
│   ├── routes/                 # API 路由層
│   │   ├── words.py           # 字詞 API 端點
│   │   └── health.py          # 健康檢查端點
│   ├── services/               # 業務邏輯層
│   │   └── word_service.py    # 字詞資料管理
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
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──────┐    ┌────▼────────┐
│  routes/ │    │  services/  │
│ (HTTP層) │───>│ (業務邏輯層)│
└──────────┘    └─────┬───────┘
                      │
                ┌─────▼──────┐
                │  config.py  │
                │  (配置層)   │
                └─────────────┘
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

## API 文件

### GET /api/words/random

返回一個隨機的練習字詞。

**回應格式:**
```json
{
  "word": "你",
  "zhuyin": ["ㄋ", "ㄧ", "ˇ"],
  "keys": ["s", "u", "3"]
}
```

- `word`: 中文字
- `zhuyin`: 注音符號陣列
- `keys`: 對應的鍵盤按鍵陣列

### GET /health

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

後端支援以下環境變數：

- `PORT`: 伺服器端口（預設：5000）
- `FLASK_ENV`: 環境模式（`development` 啟用除錯模式）

範例：
```bash
PORT=8000 FLASK_ENV=development python app.py
```

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
