## Context（脈絡）

注音輸入練習網站目前使用「筆墨童趣」視覺主題的重新設計版本，具備以下特點：
- **模組化架構**：ES6 模組組織，使用相依注入模式
- **多重回饋機制**：鍵盤高亮、墨滴粒子效果、煙火慶祝、進度條、學習統計
- **狀態管理**：`practice.js` 模組維護當前字詞狀態（包含 `word`, `zhuyin`, `keys`, `currentIndex`）
- **輸入處理流程**：`input-handler-redesign.js` 協調輸入驗證與各種回饋效果

**現有問題：**
使用者雖然能透過進度條看到整體進度（例如 33%、66%、100%），但無法看到自己實際輸入了哪些注音符號。這對學習者造成困擾，特別是在輸入較長的注音組合時（如 ㄓㄨㄤˋ），使用者只能透過記憶判斷自己輸入到哪裡。

**基礎設施已就緒：**
- HTML 已有 `<div id="zhuyin-display">` 元素（位於 `index-redesign.html` 第 73 行）
- CSS 已有 `.zhuyin-display` 樣式定義（位於 `styles/redesign.css` 第 225-231 行）
- 只需新增 JavaScript 邏輯來更新此元素

## Goals / Non-Goals（目標與非目標）

**Goals（目標）:**
1. 在練習字下方即時顯示已正確輸入的注音符號
2. 隨著使用者輸入逐步累加顯示（ㄓ → ㄓㄨ → ㄓㄨˋ）
3. 完成字詞後保持顯示完整注音，直到載入下一個字才清空
4. 整合現有架構，無需引入新相依套件或重構現有模組
5. 最小化程式碼變更（約 15 行新增程式碼）

**Non-Goals（非目標）:**
- ❌ 不修改 CSS 樣式或調整視覺設計（使用現有樣式即可）
- ❌ 不顯示錯誤輸入或提供錯誤提示（符合現有「靜默忽略錯誤」的設計原則）
- ❌ 不顯示「剩餘待輸入」的注音符號（僅顯示已輸入部分）
- ❌ 不新增動畫效果（使用現有 CSS 轉場即可）
- ❌ 不改變現有輸入驗證邏輯（`practice.checkInput()` 保持不變）

## Decisions（設計決策）

### 決策 1：使用 `practice.getState()` 取得輸入進度

**選項 A（採用）：** 每次更新顯示時呼叫 `practice.getState()` 取得當前狀態
**選項 B：** 在 `input-handler-redesign.js` 中維護獨立的顯示狀態

**理由：**
- `practice.js` 已經是單一真相來源（Single Source of Truth）
- 避免狀態重複與同步問題
- 符合現有架構的相依注入模式
- 程式碼更簡潔，無需額外的狀態管理

**實作方式：**
```javascript
function updateZhuyinDisplay() {
    if (!zhuyinDisplayElement) return;

    const state = practice.getState();
    const typedZhuyin = state.zhuyin.slice(0, state.currentIndex);
    zhuyinDisplayElement.textContent = typedZhuyin.join('');
}
```

---

### 決策 2：在 `handleKeyDown()` 正確輸入後更新顯示

**選項 A（採用）：** 在 `if (result.correct)` 區塊中，統計更新後呼叫 `updateZhuyinDisplay()`
**選項 B：** 修改 `practice.checkInput()` 回傳結果，讓其包含已輸入的注音陣列
**選項 C：** 在 `loadWord()` 中註冊回呼函式來監聽狀態變化

**理由：**
- 選項 A 符合現有程式碼結構，其他回饋（粒子、統計）也在此處觸發
- 統一的觸發點便於維護和理解程式碼流程
- 選項 B 違反關注點分離原則（`practice.js` 不應關心顯示邏輯）
- 選項 C 過度設計，引入不必要的複雜性

**插入位置：**
```javascript
// 在 handleKeyDown() 中，第 72 行附近
if (statsTracker) {
    statsTracker.recordCorrectInput();
    updateStatsDisplay();
}

// 新增以下這一行
updateZhuyinDisplay();

// 更新進度條
updateProgressBar(result.progress);
```

---

### 決策 3：在 `loadNextWord()` 中清空顯示

**選項 A（採用）：** 在 `loadNextWord()` 開頭、重置進度條之後清空顯示
**選項 B：** 在 `practice.loadWord()` 中清空顯示
**選項 C：** 在字詞完成時立即清空（與載入下一個字同時進行）

**理由：**
- 選項 A 保持關注點分離（`practice.js` 負責狀態，`input-handler` 負責 UI）
- 清空時機與重置進度條一致，符合使用者預期
- 選項 B 違反模組職責劃分
- 選項 C 會讓使用者無法看到完成字詞的完整注音（違反需求）

**實作方式：**
```javascript
async function loadNextWord() {
    try {
        // 重置進度條
        resetProgressBar();

        // 清空注音顯示
        if (zhuyinDisplayElement) {
            zhuyinDisplayElement.textContent = '';
        }

        // 載入新字詞
        const wordData = await practice.fetchNextWord();
        practice.loadWord(wordData);
        // ...
    }
}
```

---

### 決策 4：第一聲（空白鍵）的處理方式

**決策：** 使用 `zhuyin.join('')` 自然處理，不需特殊邏輯

**理由：**
- `practice.js` 中的 `state.zhuyin` 陣列若包含第一聲會儲存為 `' '`（空格字元）
- JavaScript 的 `Array.join('')` 會自動保留空格
- 例如：`['ㄓ', 'ㄨ', 'ㄥ', ' ']` → `'ㄓㄨㄥ '`（視覺上可能不明顯但正確）
- 與 CSS 的 `letter-spacing: 0.5em` 配合，空格會有合適的間距

**無需特殊處理：**
- ❌ 不需檢查 `' '` 並替換為 `'(一聲)'` 等文字說明
- ❌ 不需過濾掉空格字元
- ✅ 保持簡單，信任現有資料格式

---

### 決策 5：錯誤輸入不顯示

**決策：** 只在 `result.correct === true` 時更新顯示，錯誤輸入不做任何處理

**理由：**
- 符合現有設計哲學：靜默忽略錯誤輸入（無錯誤提示、無錯誤音效）
- 使用者只看到正確進度，不會因錯誤輸入而困惑
- 進度條也是相同邏輯（只在正確輸入時前進）
- 保持一致的使用者體驗

## Risks / Trade-offs（風險與權衡）

### 風險 1：第一聲空格可能不明顯

**描述：** 第一聲使用空格字元 `' '`，在視覺上可能不夠明顯，使用者可能無法清楚看到已輸入第一聲。

**緩解措施：**
- 現有 CSS 的 `letter-spacing: 0.5em` 提供足夠間距，空格會有視覺效果
- 如果未來有使用者回饋指出此問題，可考慮：
  - 選項 1：在 `updateZhuyinDisplay()` 中檢測空格並替換為特殊符號（如 `˙` 或 `○`）
  - 選項 2：調整 CSS 為空格字元新增底線樣式
- **目前決策：** 先觀察使用者反應，不提前過度設計

---

### 權衡 1：每次輸入都呼叫 `getState()` 的效能

**權衡：** 每次正確輸入都會呼叫 `practice.getState()` 並進行陣列切片操作。

**評估：**
- `getState()` 回傳淺拷貝物件，效能影響極小（單字最多 4-5 個注音符號）
- 陣列 `slice()` 操作在小型陣列上效能優異（< 10 元素）
- 使用者輸入頻率低（人類打字速度約每秒 1-3 個按鍵）
- **結論：** 效能影響可忽略不計，程式碼簡潔性更重要

---

### 權衡 2：不實作動畫效果

**權衡：** 新增注音符號時無淡入動畫或打字機效果。

**評估：**
- 符合非目標：保持最小變更
- 現有設計已有足夠的視覺回饋（墨滴粒子、進度條動畫）
- 文字立即出現更直接、回饋更即時
- 如需新增動畫，可透過 CSS 的 `::after` 偽元素和 `@keyframes` 實作
- **結論：** MVP 不包含動畫，可作為未來增強項目

---

### 風險 2：自動前進邏輯的顯示清空時機

**描述：** 當第一聲位置使用者直接輸入下一個字的開頭時（自動前進），顯示清空時機需要正確處理。

**現有邏輯分析：**
```javascript
if (result.autoAdvance && result.nextKey) {
    await loadNextWord();  // 這裡會清空顯示
    const nextEvent = new KeyboardEvent('keydown', { key: result.nextKey });
    await handleKeyDown(nextEvent);  // 新字的第一個輸入
}
```

**評估：**
- `loadNextWord()` 會清空顯示（符合預期）
- 遞迴呼叫 `handleKeyDown()` 會觸發新字的第一個正確輸入並更新顯示
- 時序正確：清空 → 載入新字 → 顯示新字的第一個注音
- **結論：** 無需特殊處理，現有流程已正確

---

## 實作摘要

**修改檔案：** `frontend/js/modules/input-handler-redesign.js`（單一檔案）

**新增內容：**
1. 模組層級變數：`let zhuyinDisplayElement = null;`
2. `init()` 函式：新增一行初始化 `zhuyinDisplayElement`
3. `updateZhuyinDisplay()` 函式：約 6 行程式碼
4. `handleKeyDown()`：新增一行呼叫 `updateZhuyinDisplay()`
5. `loadNextWord()`：新增 3 行清空顯示邏輯

**總計：約 15 行新增程式碼**

**測試驗證點：**
1. ✓ 輸入正確注音時，注音符號逐步出現
2. ✓ 輸入錯誤注音時，顯示不變（靜默忽略）
3. ✓ 完成字詞後，完整注音持續顯示
4. ✓ 載入下一個字時，顯示清空
5. ✓ 第一聲（空白鍵）正確處理
6. ✓ 自動前進功能正常運作
