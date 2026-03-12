## Context

系統目前支援注音輸入法練習，資料庫的 `characters` 表已有 `input_method` 欄位，`character_metadata` 表已有 `initial`、`final`、`tone` 欄位，架構天然支援多輸入法擴充。

小鶴雙拼（Xiaohe Shuangpin）是以 QWERTY 鍵盤將中文音節拆為聲母鍵 + 韻母鍵的兩鍵輸入法，無聲調資訊。字庫來源為 `rime-flypyquick5/flypy_self_main.dict.yaml`，格式為 `漢字\t兩字母碼`。

## Goals / Non-Goals

**Goals:**
- 新增前 3000 常用漢字的雙拼字庫（`input_method = 'shuangpin'`）
- API 支援依 `input_method` 隨機取字
- 前端支援注音 / 雙拼模式切換，練習卡片與虛擬鍵盤依模式渲染

**Non-Goals:**
- 不支援其他雙拼方案（自然碼、搜狗等）
- 不記錄輸入法偏好至後端（localStorage 即可）
- 不修改注音模式的任何邏輯

## Decisions

### 1. 字庫儲存：沿用現有表結構，不新增表

`characters` 表新增一批 `input_method = 'shuangpin'` 的記錄；`character_metadata` 補上對應的聲韻資料（`initial`、`final`，`tone = NULL`）。

**捨棄方案**：新增 `shuangpin_characters` 獨立表。
**原因**：現有 `characters + character_metadata` 結構已滿足需求，兩表共存讓 dbt Star Schema 可直接 JOIN，無需額外處理。

### 2. 聲韻顯示：取 `character_metadata.initial + final`，不另存欄位

練習卡片的「注音顯示」在雙拼模式下顯示 `initial + final`（如 `nǐ` 顯示為 `ni`），直接從 `character_metadata` 取得，無需新增欄位。

**原因**：資料唯一來源，避免冗餘。

### 3. 模式狀態：`localStorage` 儲存，React Context 管理

新增 `useInputMethod` hook，讀寫 `localStorage` 的 `inputMethod` 鍵（值為 `'zhuyin' | 'shuangpin'`），並透過 Context 向下傳遞給 `PracticeCard`、`VirtualKeyboard`。

**捨棄方案**：後端記錄使用者偏好。
**原因**：模式偏好為 UI 狀態，無需持久化至 DB，localStorage 足夠且無 API round-trip。

### 4. 虛擬鍵盤：複用現有元件，依模式切換佈局資料

`VirtualKeyboard` 接受 `layout` prop，注音模式傳注音佈局，雙拼模式傳 QWERTY 26 鍵佈局。

雙拼模式下每個按鍵同時顯示兩層標籤：
- **主標籤**：英文字母（如 `Q`）
- **副標籤**：該鍵對應的注音符號（聲母或韻母），使用注音符號（ㄅㄆㄇ），不使用拼音字母。例如：Q → `ㄧㄡ`、W → `ㄟ`、N → `ㄋ / ㄧㄠ`（若同時為聲母和韻母則兩者都顯示）

鍵盤只高亮當前按下的鍵，不顯示「正確/錯誤」顏色。

### 5. 字庫 Seed：Python 腳本解析 YAML，批次匯入

新增 `backend/scripts/seed_shuangpin.py`，讀取 `rime-flypyquick5/flypy_self_main.dict.yaml`，過濾前 3000 常用字清單後批次 INSERT（`ON CONFLICT DO NOTHING`）。

常用字清單以硬編碼 Python list 儲存於腳本中（手動整理 3000 字），無需外部依賴。

### 6. API：`input_method` 查詢參數

`GET /api/words/random?input_method=shuangpin` 傳回該模式的隨機字，response 結構不變（`word`、`zhuyin`、`input_code`），`zhuyin` 欄位在雙拼模式下值為 `initial + final`（無聲調符號）。

## Risks / Trade-offs

- **字庫覆蓋率**：`flypy_self_main.dict.yaml` 可能不包含所有 3000 常用字中的部分罕見字 → 跳過無對應碼的字，seed 腳本記錄跳過數量
- **`zhuyin` 欄位語意模糊**：API response 的 `zhuyin` 在雙拼模式下不是真正的注音 → 前端依 `input_method` 決定如何顯示，欄位本身改名為 `display_phonetic` 會是 breaking change，故暫不修改
- **前 3000 字清單維護**：硬編碼清單難以更新 → 接受此限制，清單穩定後不需頻繁變動

## Migration Plan

1. 執行 `seed_shuangpin.py` 匯入雙拼字庫（冪等，可重複執行）
2. 無 schema 變更，不需要 Alembic migration
3. 前端新功能為加法，不影響現有注音流程
4. 回滾：刪除 `input_method = 'shuangpin'` 的 characters 記錄即可

## Open Questions

- 無
