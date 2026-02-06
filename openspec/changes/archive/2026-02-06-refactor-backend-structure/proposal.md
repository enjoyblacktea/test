## Why

目前 Backend 所有代碼集中在單一的 `app.py` 檔案（49 行），隨著專案發展，缺乏模組化結構會降低程式碼可維護性和可測試性。需要建立清晰的模組結構，將路由、業務邏輯和配置分離，為未來擴展奠定良好基礎，同時保持 MVP 的簡潔性。

## What Changes

- 將單一 `app.py` 重構為模組化結構：`routes/`, `services/`, `config.py`
- 建立 `routes/words.py` 和 `routes/health.py` 處理 API 端點
- 建立 `services/word_service.py` 封裝字詞資料載入和管理邏輯
- 建立 `config.py` 集中管理配置（檔案路徑、端口等）
- 簡化 `app.py` 為應用程式入口點（~15 行）
- **保證**：API 端點、回應格式、行為保持 100% 不變（零破壞性變更）

## Capabilities

### New Capabilities

- `backend-modular-structure`: Backend 模組化架構，定義 routes、services、config 層的職責和互動方式

### Modified Capabilities

無。這是內部重構，不改變任何對外 API 的需求或行為。

## Impact

**受影響的檔案：**

- **重構檔案**：
  - `backend/app.py` - 簡化為應用程式入口（從 49 行減少到 ~15 行）

- **新增檔案**：
  - `backend/config.py` - 配置管理
  - `backend/routes/__init__.py` - 路由模組初始化
  - `backend/routes/words.py` - 字詞相關 API 端點
  - `backend/routes/health.py` - 健康檢查端點
  - `backend/services/__init__.py` - 服務層初始化
  - `backend/services/word_service.py` - 字詞業務邏輯

- **不變的檔案**：
  - `backend/data/words.json` - 保持不變
  - `backend/pyproject.toml` - 保持不變
  - `frontend/*` - 完全不受影響

**API 相容性：**

- ✅ `GET /api/words/random` - 完全相同的端點和回應格式
- ✅ `GET /health` - 完全相同的端點和回應格式
- ✅ 錯誤處理邏輯保持一致
- ✅ CORS 配置保持一致

**測試影響：**

- 現有的 `tests/backend/test_api.py` 應該無需修改即可通過
- 可以添加新的單元測試來測試各個模組（services, routes）

**開發流程影響：**

- 開發者需要了解新的模組結構
- import 路徑會改變（但對外 API 不變）
- 更容易進行單元測試和 mock

**風險：**

- 重構過程中可能引入 bug（緩解：確保所有測試通過）
- 開發者需要適應新結構（緩解：提供清晰的文件說明）
