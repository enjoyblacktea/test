## ADDED Requirements

### Requirement: 字符元數據儲存
系統 SHALL 為每個 `characters` 表中的字符維護一筆對應的元數據記錄，包含聲母、韻母、聲調、難度等級與常用字頻率排名。

#### Scenario: 元數據完整性
- **WHEN** 查詢任一 `character_id` 的元數據
- **THEN** 系統回傳包含 `initial`（聲母，可為 NULL）、`final`（韻母）、`tone`（1–5）、`difficulty`（1–3）、`frequency_rank`（可為 NULL）的記錄

#### Scenario: 聲母為空的字符
- **WHEN** 字符無聲母（例如純韻母字）
- **THEN** `initial` 欄位儲存為 NULL，其他欄位正常填入

### Requirement: 元數據初始化腳本
系統 SHALL 提供一個一次性初始化腳本，從 `characters.input_code` 自動解析注音成分並批次填入 `character_metadata`。

#### Scenario: 從 input_code 解析
- **WHEN** 執行初始化腳本
- **THEN** 腳本解析每筆 `input_code`，將聲母、韻母、聲調分別寫入對應欄位，已存在的記錄跳過（不覆蓋）

#### Scenario: 重複執行安全性
- **WHEN** 腳本重複執行
- **THEN** 不產生重複記錄，不拋出錯誤

### Requirement: 元數據不透過應用程式 API 修改
系統 SHALL NOT 提供讓前端使用者新增或修改 `character_metadata` 的 API 端點；元數據僅由初始化腳本或資料庫管理員維護。

#### Scenario: 前端無修改路由
- **WHEN** 前端發送任何對 character_metadata 的寫入請求
- **THEN** 系統回傳 404 或 405
