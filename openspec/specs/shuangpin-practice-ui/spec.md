## ADDED Requirements

### Requirement: Practice card displays shuangpin phonetic in shuangpin mode
系統必須（SHALL）在雙拼模式下，練習卡片的注音提示區域顯示聲母 + 韻母的羅馬字拼音（無聲調），取代注音符號。

#### Scenario: Shuangpin mode card display
- **WHEN** 系統處於雙拼模式且載入練習字
- **THEN** 練習卡片顯示漢字
- **THEN** 提示區域顯示 `initial + final` 的拼音字母（如 `ni`）
- **THEN** 不顯示聲調符號或聲調數字

#### Scenario: Zhuyin mode card display unchanged
- **WHEN** 系統處於注音模式且載入練習字
- **THEN** 練習卡片顯示邏輯與現有注音模式完全相同
- **THEN** 注音符號正常顯示

### Requirement: Practice card shows shuangpin input code as hint
系統必須（SHALL）在雙拼模式下，練習卡片同時顯示對應的雙拼按鍵提示（兩個字母，如 `n` + `i`）。

#### Scenario: Key hint display
- **WHEN** 系統處於雙拼模式且載入練習字
- **THEN** 練習卡片顯示兩個目標按鍵（聲母鍵與韻母鍵）分開展示
- **THEN** 已輸入的鍵以高亮顏色標示
- **THEN** 尚未輸入的鍵以正常顏色顯示

### Requirement: Virtual keyboard shows both QWERTY letters and shuangpin phonetic labels in shuangpin mode
系統必須（SHALL）在雙拼模式下，虛擬鍵盤的每個按鍵同時顯示英文字母（主標籤）與對應的小鶴雙拼聲母/韻母標注（副標籤）。

#### Scenario: Dual-label QWERTY layout rendered
- **WHEN** 系統切換至雙拼模式
- **THEN** 虛擬鍵盤顯示標準 QWERTY 字母排列（三行：qwertyuiop / asdfghjkl / zxcvbnm）
- **THEN** 每個鍵顯示大寫英文字母作為主標籤
- **THEN** 每個鍵的副標籤顯示該鍵在小鶴雙拼中對應的聲母或韻母（如 Q 鍵顯示「iu」、W 鍵顯示「ei」）
- **THEN** 主標籤（英文字母）字體較大，副標籤（聲韻）字體較小

#### Scenario: Active key highlight
- **WHEN** 使用者在雙拼模式下按下字母鍵
- **THEN** 對應的 QWERTY 鍵以高亮顏色（cyan #00d9ff）標示
- **THEN** 高亮持續至少 150ms 後消失
- **THEN** 不顯示正確/錯誤顏色區分（僅高亮按下的鍵）

#### Scenario: Zhuyin keyboard layout preserved
- **WHEN** 系統處於注音模式
- **THEN** 虛擬鍵盤顯示原有注音符號佈局
- **THEN** 注音鍵盤行為與現有實作完全相同

### Requirement: Input validation handles two-key shuangpin input
系統必須（SHALL）在雙拼模式下，按順序驗證使用者輸入的兩個字母鍵是否符合目標雙拼碼。

#### Scenario: First key correct
- **WHEN** 使用者在雙拼模式下按下聲母鍵（第一鍵）且正確
- **THEN** 系統接受輸入，`inputIndex` 推進至 1
- **THEN** 畫面更新以顯示第一鍵已輸入

#### Scenario: Second key correct (word complete)
- **WHEN** 使用者按下韻母鍵（第二鍵）且正確
- **THEN** 系統標記本字完成（`isCorrect = true`）
- **THEN** 系統自動載入下一個練習字

#### Scenario: Wrong key input
- **WHEN** 使用者按下錯誤的鍵
- **THEN** 系統標記輸入錯誤（`isCorrect = false`）
- **THEN** 系統顯示錯誤回饋後重設當前字
