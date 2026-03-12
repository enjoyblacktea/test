## ADDED Requirements

### Requirement: Store shuangpin characters in existing characters table
系統必須（SHALL）將小鶴雙拼字庫存入現有的 `characters` 表，`input_method` 欄位設為 `'shuangpin'`，每字對應一筆記錄。

#### Scenario: Shuangpin character record structure
- **WHEN** 系統匯入雙拼字庫
- **THEN** 每筆記錄的 `word` 欄位儲存單一漢字
- **THEN** `input_code` 欄位儲存兩字母的小鶴雙拼碼（如 `ni`）
- **THEN** `input_method` 欄位值為 `'shuangpin'`

#### Scenario: Coverage
- **WHEN** 種子腳本執行完畢
- **THEN** 系統包含前 3000 常用漢字中有對應小鶴雙拼碼的所有字
- **THEN** 無對應碼的字被跳過並記錄於腳本輸出

### Requirement: Store shuangpin phonetic breakdown in character_metadata
系統必須（SHALL）為每筆雙拼字庫記錄在 `character_metadata` 表新增對應的聲韻資料。

#### Scenario: Metadata record structure
- **WHEN** 系統為雙拼字符建立 metadata
- **THEN** `initial` 欄位儲存聲母字母（如 `n`），允許為 NULL（零聲母）
- **THEN** `final` 欄位儲存韻母字母（如 `i`）
- **THEN** `tone` 欄位設為 NULL（雙拼不區分聲調）
- **THEN** `character_id` 指向對應的 `characters` 記錄

### Requirement: Idempotent seed script
系統必須（SHALL）提供可重複執行的種子腳本 `backend/scripts/seed_shuangpin.py`，不產生重複資料。

#### Scenario: First run
- **WHEN** 種子腳本首次在空資料庫執行
- **THEN** 系統匯入所有有效的雙拼字庫記錄
- **THEN** 腳本輸出匯入數量與跳過數量

#### Scenario: Subsequent run
- **WHEN** 種子腳本在已有資料的情況下再次執行
- **THEN** 系統不建立重複記錄（ON CONFLICT DO NOTHING）
- **THEN** 腳本正常結束不報錯

### Requirement: API supports input_method query parameter
系統必須（SHALL）讓 `GET /api/words/random` 端點支援 `input_method` 查詢參數。

#### Scenario: Request shuangpin word
- **WHEN** 客戶端發送 `GET /api/words/random?input_method=shuangpin`
- **THEN** 系統從 `input_method = 'shuangpin'` 的記錄中隨機取一字
- **THEN** response 包含 `word`、`zhuyin`（值為 `initial + final`）、`input_code`

#### Scenario: Default behavior preserved
- **WHEN** 客戶端發送 `GET /api/words/random`（無參數）
- **THEN** 系統行為與現有注音模式相同
- **THEN** 注音字庫不受影響
