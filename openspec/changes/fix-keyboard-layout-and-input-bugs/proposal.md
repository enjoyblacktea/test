## Why

手動測試發現了三個關鍵 bug 影響使用者體驗：
1. 虛擬鍵盤排列不符合實體 QWERTY 鍵盤布局，導致使用者難以對應
2. 按 `/` 鍵會觸發瀏覽器的 quick start 功能，而非輸入注音
3. 某些字詞（如「了」）無法正確輸入，按鍵無反應

這些問題必須立即修復以確保基本功能正常運作。

## What Changes

- 修正虛擬鍵盤排列，改為符合實體 QWERTY 鍵盤布局（數字行、QWERTY 行、ASDF 行、ZXCV 行、空格鍵）
- 在輸入處理器中阻止瀏覽器預設行為，避免 `/` 等特殊鍵觸發快捷鍵
- 修正注音映射表中的錯誤，確保所有字詞都能正確輸入
- 驗證 words.json 中的資料正確性，特別是「了」字的注音和按鍵對應

## Capabilities

### New Capabilities
<!-- 無新增能力 -->

### Modified Capabilities
- `zhuyin-keyboard-display`: 修改鍵盤排列順序以符合實體鍵盤布局
- `zhuyin-input-validation`: 新增阻止瀏覽器預設行為，修正輸入驗證邏輯

## Impact

- 修改 `frontend/js/modules/keyboard.js` - 更新 keyboardLayout 陣列
- 修改 `frontend/js/modules/input-handler.js` - 新增 event.preventDefault()
- 修改 `frontend/js/modules/zhuyin-map.js` - 檢查並修正映射表
- 修改 `backend/data/words.json` - 驗證並修正字詞資料
- 可能影響現有測試 - 需要更新測試案例
