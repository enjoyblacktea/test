## ADDED Requirements

### Requirement: 每日目標設定
系統 SHALL 允許已登入使用者設定每日練習目標題數，每次設定產生一筆新記錄（保留歷史），並以 `effective_date` 標記生效日期。

#### Scenario: 設定新目標
- **WHEN** 使用者提交 `daily_target`（正整數）
- **THEN** 系統建立一筆 `user_goals` 記錄，`effective_date` 設為當日，回傳 201

#### Scenario: 目標值不合法
- **WHEN** 使用者提交 `daily_target` 小於 1 或非整數
- **THEN** 系統回傳 422 並說明錯誤原因

### Requirement: 查詢今日有效目標與進度
系統 SHALL 提供端點，回傳當前使用者今日有效目標題數，以及今日已完成的嘗試次數。

#### Scenario: 有目標記錄
- **WHEN** 使用者查詢今日目標
- **THEN** 系統取 `effective_date <= 今日` 中最新一筆的 `daily_target`，並計算今日 `typing_attempts` 筆數，一併回傳

#### Scenario: 尚未設定目標
- **WHEN** 使用者從未設定目標
- **THEN** 系統回傳 `daily_target: null`，`completed_today: 0`

### Requirement: 目標歷史不可刪除或覆蓋
系統 SHALL NOT 允許刪除或修改既有的 `user_goals` 記錄；若使用者修改目標，SHALL 新增一筆記錄。

#### Scenario: 同日多次設定
- **WHEN** 使用者在同一天內多次設定目標
- **THEN** 系統允許多筆相同 `effective_date` 的記錄，查詢時取最後一筆（依 `id` 最大值）

### Requirement: 前端顯示今日進度
系統 SHALL 在練習頁面顯示今日已完成題數與目標題數（格式：`N / M 題`），並提供入口供使用者更新目標。

#### Scenario: 顯示進度
- **WHEN** 使用者進入練習頁面
- **THEN** 頁面呼叫今日目標 API，顯示目前進度

#### Scenario: 未設定目標時的顯示
- **WHEN** 使用者尚未設定目標
- **THEN** 頁面顯示「尚未設定目標」並引導設定
