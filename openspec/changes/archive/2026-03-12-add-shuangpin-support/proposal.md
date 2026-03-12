## Why

目前系統僅支援注音（ㄅㄆㄇ）輸入法練習，無法滿足使用小鶴雙拼等拼音輸入法的使用者需求。加入小鶴雙拼支援，讓系統成為多輸入法練習平台，擴大使用族群。

## What Changes

- 新增小鶴雙拼字庫：前 3000 常用漢字，每字對應一個標準雙拼碼（聲母 + 韻母），存入 `characters` 表（`input_method = 'shuangpin'`）
- 新增對應的 `character_metadata` 記錄：填入 `initial`（聲母）與 `final`（韻母），`tone = NULL`（雙拼不區分聲調）
- 前端新增輸入法切換功能：標頭 Toggle（注音 / 雙拼），選擇儲存於 `localStorage`
- 練習卡片依模式顯示：注音模式顯示注音符號，雙拼模式顯示聲母+韻母拼音（無聲調）
- 虛擬鍵盤依模式切換：雙拼模式顯示 QWERTY 佈局，僅高亮當前按鍵

## Capabilities

### New Capabilities

- `shuangpin-character-data`: 小鶴雙拼字庫的資料模型、seed 腳本與 API 支援
- `input-method-mode-switch`: 前端輸入法模式切換（注音 / 雙拼），含 localStorage 持久化
- `shuangpin-practice-ui`: 雙拼練習卡片顯示（漢字 + 聲韻拼音）與 QWERTY 虛擬鍵盤

### Modified Capabilities

- `zhuyin-keyboard-display`: 虛擬鍵盤需依輸入法模式切換 QWERTY / 注音佈局
- `realtime-input-feedback`: 輸入驗證邏輯需支援雙拼碼（兩個字母）的判斷

## Impact

- **Backend**: `characters` 表新增 shuangpin 字庫資料；`character_metadata` 新增對應聲韻記錄；`GET /api/words/random` 需支援 `input_method` 查詢參數
- **Frontend**: `PracticePage`、`PracticeCard`、`VirtualKeyboard` 元件均需依模式調整；新增 `useInputMethod` hook 管理模式狀態
- **資料**: 需新增 seed 腳本解析 `flypy_self_main.dict.yaml`，批次匯入前 3000 字的雙拼碼
- **無 Breaking Change**：注音模式完全不受影響，兩種模式共存
