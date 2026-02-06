# 注音輸入法練習網站

一個簡單、可測試的注音輸入法練習工具，專為習慣其他輸入法（如拼音、倉頡）想學習注音的使用者設計。

## 功能特色

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
- Python 3.8+
- uv（Python 套件管理工具）

## 快速開始

### 1. 安裝後端依賴

```bash
cd backend
uv venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt
```

### 2. 啟動後端伺服器

```bash
cd backend
source .venv/bin/activate
python app.py
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

### 4. 開始練習

1. 查看螢幕上顯示的中文字
2. 參考虛擬鍵盤，使用實體鍵盤輸入對應的注音符號
3. 輸入正確時，虛擬鍵盤會高亮顯示
4. 完成一個字後，自動載入下一個字

## 專案結構

```
zhuyin-practice/
├── frontend/                    # 前端檔案
│   ├── index.html              # 主頁面
│   ├── styles/                 # CSS 樣式
│   │   ├── main.css           # 全域樣式
│   │   ├── keyboard.css       # 鍵盤樣式
│   │   └── practice.css       # 練習區樣式
│   └── js/                     # JavaScript 檔案
│       ├── main.js            # 入口點
│       └── modules/           # ES6 模組
│           ├── zhuyin-map.js  # 注音映射表
│           ├── keyboard.js    # 虛擬鍵盤
│           ├── practice.js    # 練習邏輯
│           └── input-handler.js # 輸入處理
│
├── backend/                     # 後端檔案
│   ├── app.py                  # Flask 應用程式
│   ├── requirements.txt        # Python 依賴
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
cd tests/backend
source ../../backend/.venv/bin/activate
python -m pytest test_api.py -v
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
- **flask-cors**: 處理跨域請求
- **靜態 JSON**: 簡單可靠的資料儲存

### 測試
- **前端**: 獨立的 HTML 測試頁面
- **後端**: pytest 單元測試
- **整合**: 手動測試清單

## 未來改進

此專案是 MVP（最小可行產品），未來可以加入：

- 統計功能（速度、準確率）
- 錯誤提示和引導
- 多種難度級別
- 使用者帳號和進度儲存
- 行動裝置支援
- 更多練習字詞
- 詞組練習（多字詞）
- 文章打字練習

## 授權

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 常見問題

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

## 開發團隊

使用 OpenSpec 工作流程開發
