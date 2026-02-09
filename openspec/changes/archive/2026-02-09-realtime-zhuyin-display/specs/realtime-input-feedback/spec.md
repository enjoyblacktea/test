## ADDED Requirements

### Requirement: Display typed zhuyin symbols progressively
系統必須（SHALL）在使用者每次正確輸入注音符號後，在注音顯示區域即時更新已輸入的符號，讓使用者能夠視覺確認自己的輸入進度。

#### Scenario: User types correct zhuyin symbol
- **WHEN** 使用者按下正確的注音按鍵
- **THEN** 系統在注音顯示區域附加該注音符號
- **THEN** 顯示內容逐步累加（例如：ㄓ → ㄓㄨ → ㄓㄨˋ）
- **THEN** 使用現有的 `.zhuyin-display` CSS 樣式

#### Scenario: User types incorrect zhuyin symbol
- **WHEN** 使用者按下不正確的注音按鍵
- **THEN** 系統不更新注音顯示
- **THEN** 顯示內容保持不變

#### Scenario: User completes entire word
- **WHEN** 使用者輸入最後一個正確的注音符號完成整個字
- **THEN** 系統顯示完整的注音組合
- **THEN** 顯示保持可見直到載入下一個練習字

#### Scenario: User types first tone with space key
- **WHEN** 使用者按下空白鍵輸入第一聲
- **THEN** 系統在注音顯示中加入空格字元
- **THEN** 空格字元在視覺上可能不明顯但被正確處理
- **THEN** CSS 的 `letter-spacing` 提供適當的間距效果

### Requirement: Clear display when loading new word
系統必須（SHALL）在載入新的練習字時清空注音顯示區域，為下一個字的輸入準備乾淨的顯示狀態。

#### Scenario: New practice word loads
- **WHEN** 系統載入下一個練習字
- **THEN** 系統清空注音顯示區域的內容
- **THEN** 顯示區域變為空白狀態
- **THEN** 清空時機在重置進度條之後、載入新字資料之前

#### Scenario: Auto-advance to next word
- **WHEN** 使用者在第一聲位置直接輸入下一個字的開頭（自動前進）
- **THEN** 系統清空注音顯示
- **THEN** 系統載入下一個練習字
- **THEN** 系統顯示新字的第一個正確輸入符號

### Requirement: Use existing practice state as data source
系統必須（SHALL）從 `practice` 模組的狀態取得當前輸入進度資訊，而非維護獨立的顯示狀態。

#### Scenario: Reading current input progress
- **WHEN** 系統需要更新注音顯示
- **THEN** 系統呼叫 `practice.getState()` 取得當前狀態
- **THEN** 系統從狀態中讀取 `zhuyin` 陣列和 `currentIndex`
- **THEN** 系統使用 `zhuyin.slice(0, currentIndex)` 取得已輸入的符號
- **THEN** 系統使用 `join('')` 將符號陣列轉換為顯示字串

#### Scenario: State synchronization
- **WHEN** 使用者輸入正確符號後 `practice` 模組更新 `currentIndex`
- **THEN** 下次查詢 `getState()` 時會反映最新進度
- **THEN** 注音顯示自動與練習狀態保持同步
- **THEN** 無需額外的狀態同步機制

### Requirement: Integrate with existing input handling flow
系統必須（SHALL）在現有的輸入處理流程中整合注音顯示更新，與其他回饋機制（粒子效果、統計、進度條）協調運作。

#### Scenario: Update display after correct input
- **WHEN** 系統在 `handleKeyDown()` 中檢測到正確輸入
- **THEN** 系統依序執行：粒子效果 → 統計更新 → 注音顯示更新 → 進度條更新
- **THEN** 注音顯示更新在統計更新之後、進度條更新之前執行
- **THEN** 所有回饋機制保持協調一致

#### Scenario: Initialize display element on startup
- **WHEN** 輸入處理模組在 `init()` 函式中初始化
- **THEN** 系統取得 `zhuyin-display` DOM 元素的引用
- **THEN** 元素引用儲存在模組層級變數中
- **THEN** 後續更新操作直接使用此引用而無需重複查詢 DOM
