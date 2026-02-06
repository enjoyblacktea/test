## Context

專案目前使用單一的 `backend/app.py` 檔案（49 行）處理所有 Backend 邏輯，包括：
- Flask 應用程式初始化和 CORS 配置
- words.json 資料載入和錯誤處理
- 兩個 API 端點：`GET /api/words/random` 和 `GET /health`
- 應用程式啟動邏輯

這是典型的 MVP 快速開發模式，適合初期驗證。專案已完成 MVP，現在需要建立更清晰的模組結構以支援未來維護和擴展。

**當前技術棧：**
- Python 3.10+ with uv 套件管理
- Flask 3.1.0 + flask-cors 5.0.0
- 靜態 JSON 資料（30 個練習字）
- pytest 測試框架

**關鍵約束：**
- 必須保持 API 100% 向後相容（前端不能受影響）
- 保持 MVP 的簡潔性，不過度設計
- 現有測試必須全部通過

## Goals / Non-Goals

**Goals:**

1. **關注點分離**：將路由、業務邏輯、配置清晰分離
2. **提高可維護性**：每個模組職責單一，易於理解和修改
3. **改善可測試性**：各層可獨立測試，支援 mock 和 unit test
4. **保持簡潔**：適合當前 MVP 規模，避免過度工程
5. **零破壞性變更**：API 行為和回應格式完全不變

**Non-Goals:**

1. **不引入新功能**：純粹重構，不添加新 API 或功能
2. **不改變資料存儲**：繼續使用 words.json，不引入資料庫
3. **不使用複雜框架**：不引入 Blueprint 以外的 Flask 擴展
4. **不改變部署方式**：gunicorn 啟動方式保持不變
5. **不重寫測試**：現有整合測試應無需修改

## Decisions

### 決策 1：採用三層架構（Routes → Services → Data）

**選擇**：將程式碼組織為 routes（路由層）、services（業務邏輯層）、config（配置層）

**理由**：
- 清晰的職責劃分：routes 處理 HTTP，services 處理邏輯
- 易於測試：可以獨立測試 service 邏輯而不啟動 Flask
- 適合 MVP 規模：不需要更複雜的 DDD 或 Clean Architecture
- 易於理解：新開發者可快速掌握結構

**替代方案考量**：
- **單檔案**（現狀）：簡單但不利擴展
- **Blueprint 模組化**：過於複雜，當前只有 2 個端點
- **完整 Clean Architecture**：過度設計，違反 YAGNI 原則

### 決策 2：使用 Flask Blueprint 組織路由

**選擇**：建立 `words_bp` 和 `health_bp` 兩個 Blueprint

**理由**：
- Flask 官方推薦的模組化方式
- 支援 URL prefix（`/api/words`）的優雅管理
- 易於添加新功能模組
- 不破壞現有 URL 結構

**實作細節**：
```python
# routes/words.py
from flask import Blueprint, jsonify
words_bp = Blueprint('words', __name__)

@words_bp.route('/random', methods=['GET'])
def get_random_word():
    # 實作邏輯
```

**替代方案考量**：
- **直接 @app.route**：需要在 app.py 中集中管理，不利分離
- **Flask MethodView**：過於複雜，當前不需要類別化路由

### 決策 3：Service 層使用模組級單例模式

**選擇**：`word_service.py` 在 import 時載入 words.json，儲存在模組變數

**理由**：
- 簡單有效：不需要複雜的單例實作
- 效能優良：應用程式啟動時載入一次，後續請求無 I/O
- 符合 Python 慣例：模組本身就是單例
- 易於測試：可以 mock 模組變數

**實作結構**：
```python
# services/word_service.py
import json
from config import Config

# 模組級變數（單例）
_words_data = []

def _load_words():
    """啟動時載入 words.json"""
    global _words_data
    try:
        with open(Config.WORDS_DATA_PATH, 'r', encoding='utf-8') as f:
            _words_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading words: {e}")
        _words_data = []

# 啟動時執行
_load_words()

def get_random_word():
    """回傳隨機字詞或 None"""
    if not _words_data:
        return None
    return random.choice(_words_data)

def get_words_count():
    """回傳已載入字詞數量"""
    return len(_words_data)
```

**替代方案考量**：
- **類別單例**：過度設計，無狀態服務不需要類別
- **每次請求讀檔**：效能差，不必要的 I/O
- **全域變數在 app.py**：違反關注點分離

### 決策 4：集中配置管理（config.py）

**選擇**：建立 `config.py` 使用 Config 類別管理所有配置

**理由**：
- 單一真相來源：所有路徑、端口等配置集中管理
- 易於修改：不需要在多處改配置
- 支援環境變數：未來可輕鬆擴展多環境配置
- 符合 12-factor app 原則

**實作結構**：
```python
# config.py
import os

class Config:
    # 路徑配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WORDS_DATA_PATH = os.path.join(BASE_DIR, 'data', 'words.json')

    # 伺服器配置
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # CORS 配置（未來可擴展）
    CORS_ORIGINS = '*'
```

**替代方案考量**：
- **硬編碼在各檔案**：難以維護
- **.env 檔案 + python-dotenv**：目前不需要，配置簡單
- **多環境 Config 類別**：過度設計，當前只有開發環境

### 決策 5：保持 app.py 為輕量入口點

**選擇**：app.py 只負責創建 Flask app 和註冊 blueprints（~15 行）

**理由**：
- 清晰的入口點：一眼看出應用程式結構
- 易於擴展：未來添加新 blueprint 只需一行
- 符合 Flask 最佳實踐
- gunicorn 啟動不受影響

**實作結構**：
```python
# app.py
from flask import Flask
from flask_cors import CORS
from routes.words import words_bp
from routes.health import health_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(words_bp, url_prefix='/api/words')
    app.register_blueprint(health_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**替代方案考量**：
- **Application Factory 完整模式**：過度設計，不需要多實例
- **保持所有邏輯在 app.py**：違反重構目標

### 決策 6：錯誤處理策略

**選擇**：Service 層處理資料錯誤，Route 層處理 HTTP 錯誤

**職責劃分**：
- **Service 層**：捕獲 I/O 和資料錯誤，回傳 None 或錯誤資訊
- **Route 層**：將 None 轉換為適當的 HTTP 狀態碼（500）
- **一致性**：保持與現有實作相同的錯誤回應格式

**理由**：
- 關注點分離：Service 不關心 HTTP，Route 不關心檔案系統
- 易於測試：可獨立測試錯誤情境
- 保持向後相容：錯誤回應格式不變

## Risks / Trade-offs

### Risk 1: 重構過程中引入 Bug

**風險**：移動程式碼可能導致邏輯錯誤或遺漏某些邊界情況

**緩解措施**：
- ✅ 先執行所有現有測試，確認通過
- ✅ 逐步重構，每次改動後立即測試
- ✅ 保持 git 提交小而頻繁，方便回溯
- ✅ 重構完成後再次執行完整測試套件

### Risk 2: Import 路徑改變可能導致循環引用

**風險**：模組間相互 import 可能造成 circular import

**緩解措施**：
- ✅ 遵守依賴方向：routes → services → config（單向）
- ✅ 避免 services 引用 routes
- ✅ Config 不引用任何專案模組，只使用標準庫
- ✅ 如果遇到循環引用，考慮延遲 import（在函式內 import）

**依賴圖**：
```
app.py
  ↓
routes/* → services/* → config.py
```

### Risk 3: 開發者需要適應新結構

**權衡**：短期學習成本 vs. 長期可維護性

**緩解措施**：
- ✅ 在 README.md 添加架構說明
- ✅ 每個模組添加清晰的 docstring
- ✅ 提供架構圖和資料流程圖
- ✅ Code review 時確保理解新結構

### Risk 4: 測試覆蓋可能不足

**風險**：現有整合測試可能未覆蓋所有邊界情況

**緩解措施**：
- ✅ 添加 service 層單元測試
- ✅ 測試錯誤情境（檔案不存在、JSON 錯誤）
- ✅ 使用 pytest-cov 檢查覆蓋率
- ✅ 確保關鍵路徑（資料載入、隨機選擇）有測試

### Trade-off: 檔案數量增加

**權衡**：1 個檔案（49 行）→ 7 個檔案（~120 行總計）

**理由**：
- 雖然檔案數量增加，但每個檔案職責更清晰
- 總行數增加主要來自模組結構（`__init__.py`、import 語句）
- 長期來看，模組化更易於維護和測試
- 未來添加功能時不會讓單一檔案膨脹

## Migration Plan

### 階段 1：準備和驗證（5 分鐘）

1. **確認當前狀態**
   ```bash
   cd backend
   pytest tests/backend/  # 確認所有測試通過
   ```

2. **建立 git 分支**
   ```bash
   git checkout -b refactor/backend-modular-structure
   ```

### 階段 2：建立新結構（15 分鐘）

3. **建立目錄結構**
   ```bash
   mkdir -p routes services
   touch routes/__init__.py services/__init__.py
   ```

4. **建立 config.py**
   - 移動配置邏輯
   - 定義 Config 類別

5. **建立 services/word_service.py**
   - 移動資料載入邏輯
   - 實作 `get_random_word()` 和 `get_words_count()`

6. **建立 routes/words.py**
   - 建立 words_bp Blueprint
   - 實作 `/random` 端點
   - 呼叫 word_service

7. **建立 routes/health.py**
   - 建立 health_bp Blueprint
   - 實作 `/health` 端點

8. **重構 app.py**
   - 簡化為入口點
   - 註冊 blueprints

### 階段 3：測試和驗證（10 分鐘）

9. **執行測試**
   ```bash
   pytest tests/backend/ -v
   # 所有測試必須通過
   ```

10. **手動測試 API**
    ```bash
    python app.py
    # 另一個終端：
    curl http://localhost:5000/api/words/random
    curl http://localhost:5000/health
    ```

11. **檢查錯誤情境**
    - 暫時重命名 words.json，確認錯誤處理正常
    - 恢復 words.json

### 階段 4：添加新測試（選擇性，10 分鐘）

12. **建立 tests/backend/test_word_service.py**
    - 測試 service 層邏輯
    - 測試錯誤處理

### 階段 5：文件和提交（5 分鐘）

13. **更新 README.md**
    - 添加架構說明
    - 更新開發指南

14. **提交變更**
    ```bash
    git add .
    git commit -m "Refactor: Modularize backend structure into routes/services/config"
    ```

### Rollback 策略

如果重構後發現問題：

**立即回滾**：
```bash
git checkout main
git branch -D refactor/backend-modular-structure
```

**漸進式回滾**（如果已合併）：
1. 保留新結構，修正發現的 bug
2. 如果 bug 嚴重，可 `git revert` 合併提交
3. 舊的 `app.py` 可從 git history 恢復

## Open Questions

1. **是否需要添加日誌記錄？**
   - 目前使用 `print()`，是否升級為 `logging` 模組？
   - 建議：暫時保持 print()，未來可獨立添加 logging

2. **是否需要型別提示（Type Hints）？**
   - 可提高程式碼可讀性和 IDE 支援
   - 建議：重構完成後再添加，避免混合太多變更

3. **Service 層是否需要介面/抽象類別？**
   - 有助於未來替換實作（如改用資料庫）
   - 建議：暫時不需要，YAGNI 原則

4. **是否需要 API 版本管理（/api/v1/words）？**
   - 有助於未來 API 演進
   - 建議：當前不需要，只有兩個端點且穩定
