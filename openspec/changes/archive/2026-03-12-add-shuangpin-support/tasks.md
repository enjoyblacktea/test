## 1. 後端：字庫資料與 Seed 腳本

- [x] 1.1 建立 `backend/scripts/seed_shuangpin.py`：讀取 `rime-flypyquick5/flypy_self_main.dict.yaml`，解析每字的兩字母雙拼碼
- [x] 1.2 在腳本中定義前 3000 常用漢字清單（硬編碼 Python list）
- [x] 1.3 腳本過濾出在字庫中有對應碼的字，批次 INSERT 至 `characters`（`input_method='shuangpin'`），使用 `ON CONFLICT DO NOTHING`
- [x] 1.4 腳本同步 INSERT 對應的 `character_metadata` 記錄（`initial`、`final`、`tone=NULL`）
- [x] 1.5 執行腳本並確認資料正確匯入

## 2. 後端：API 更新

- [x] 2.1 修改 `GET /api/words/random` 端點，支援 `input_method` 查詢參數（預設 `'zhuyin'`）
- [x] 2.2 雙拼模式的 response 中，`zhuyin` 欄位值回傳 `character_metadata.initial + final`

## 3. 前端：useInputMethod Hook

- [x] 3.1 新增 `frontend/src/hooks/useInputMethod.ts`：讀寫 `localStorage['inputMethod']`，預設值為 `'zhuyin'`
- [x] 3.2 Hook 回傳 `inputMethod`（`'zhuyin' | 'shuangpin'`）與 `setInputMethod` 函式

## 4. 前端：模式切換 UI

- [x] 4.1 在 `PracticePage` 標頭新增「注音」/「雙拼」兩個切換按鈕
- [x] 4.2 當前模式按鈕顯示高亮樣式，切換時更新 `inputMethod` 狀態
- [x] 4.3 切換模式時重新呼叫 `loadWord(inputMethod)` 載入對應模式的練習字

## 5. 前端：usePractice Hook 更新

- [x] 5.1 `loadWord` 接受 `inputMethod` 參數，呼叫 `GET /api/words/random?input_method=...`
- [x] 5.2 雙拼模式下 `checkInput` 驗證兩鍵輸入（`inputIndex` 0→1→完成）

## 6. 前端：PracticeCard 元件更新

- [x] 6.1 `PracticeCard` 接受 `inputMethod` prop
- [x] 6.2 注音模式顯示注音符號（現有行為）；雙拼模式顯示 `initial + final` 字母（無聲調）
- [x] 6.3 雙拼模式下顯示兩個目標按鍵提示，已輸入的鍵以高亮顯示

## 7. 前端：VirtualKeyboard 元件更新

- [x] 7.1 `VirtualKeyboard` 接受 `layout` prop（`'zhuyin' | 'shuangpin'`）
- [x] 7.2 新增小鶴雙拼 QWERTY 佈局資料常數（26 鍵，每鍵含主標籤英文字母與副標籤注音符號聲韻）
- [x] 7.3 雙拼模式下每鍵同時顯示英文字母（主）與對應注音符號聲韻（副，字體較小）
- [x] 7.4 注音符號副標籤：同一鍵若同時對應聲母與韻母，兩者均顯示（以 `/` 分隔）
- [x] 7.5 `activeKey` 高亮邏輯在雙拼模式下對應 QWERTY 鍵位

## 8. 前端：PracticePage 整合

- [x] 8.1 將 `inputMethod` 傳入 `PracticeCard` 與 `VirtualKeyboard`
- [x] 8.2 確認模式切換後練習流程（載字、輸入、完成）全程正常運作

## 9. 測試與驗收

- [x] 9.1 注音模式功能完全不受影響（迴歸測試）
- [x] 9.2 雙拼模式：隨機字載入、兩鍵輸入驗證、自動前進正常
- [x] 9.3 模式切換後 localStorage 持久化正確（重新整理後保留選擇）
- [x] 9.4 虛擬鍵盤雙拼佈局：注音副標籤正確對應小鶴雙拼鍵位
