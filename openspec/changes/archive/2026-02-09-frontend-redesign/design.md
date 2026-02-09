## Context

### 當前狀態

專案目前使用 Vanilla JavaScript with ES6 modules 架構，無框架、無建置工具的 MVP 設計：
- **架構**：模組化前端（`zhuyin-map.js`, `keyboard.js`, `practice.js`, `input-handler.js`, `main.js`）
- **樣式**：分離的 CSS 檔案（`main.css`, `keyboard.css`, `practice.css`）
- **視覺設計**：通用紫色漸層背景 + 白色卡片，Material Design 風格
- **瀏覽器需求**：Chrome 61+, Firefox 60+, Safari 11+

### 設計約束

1. **保持 MVP 精神**：無框架、無建置工具、直接在瀏覽器運行
2. **模組化架構**：維持現有的 ES6 modules 結構，新功能作為獨立模組
3. **向後相容**：不破壞現有功能，支援相同的瀏覽器版本
4. **效能第一**：60fps 動畫、快速載入、低記憶體佔用
5. **漸進式增強**：核心功能在低端裝置仍可用，特效可優雅降級

### 利害關係人

- **學習者**：需要美觀、有趣、流暢的學習體驗
- **開發團隊**：需要可維護、可測試、易於擴展的程式碼
- **教育機構**：需要文化特色、專業外觀的教學工具

---

## Goals / Non-Goals

### Goals

1. **創造獨特的視覺識別**：筆墨童趣美學，結合傳統與現代
2. **提升學習參與度**：通過動畫、特效、統計提供即時反饋
3. **保持技術簡潔性**：純 CSS + Vanilla JS，無需複雜建置流程
4. **確保跨裝置體驗**：響應式設計，效能優化
5. **可測試性**：每個新模組都可獨立測試

### Non-Goals

1. **引入框架**：不使用 React/Vue/Angular
2. **複雜建置工具**：不需要 Webpack/Vite/Rollup
3. **行動裝置專屬優化**：桌面優先，行動端基本可用即可
4. **多語言支援**：僅支援繁體中文
5. **後端修改**：純前端改進，不改變 API
6. **完整遊戲化**：不做成就系統、排行榜等複雜功能

---

## Decisions

### 決策 1：漸進式替換策略（Parallel Development）

**選擇**：建立平行的重新設計版本，保留原始檔案

**理由**：
- ✅ 安全：原始版本保持不變，可隨時回退
- ✅ 比較：可以同時維護兩個版本進行 A/B 測試
- ✅ 學習：保留原始程式碼作為參考
- ❌ 重複：需要維護兩套檔案

**實作**：
- 新增 `index-redesign.html`（不覆蓋 `index.html`）
- 新增 `styles/redesign.css`, `styles/animations.css`, `styles/particles.css`
- 新增 `js/main-redesign.js`
- 共用現有模組：`zhuyin-map.js`（資料層不變）
- 擴展模組：`keyboard.js`, `input-handler.js`, `practice.js` 添加新功能但保持向後相容

**替代方案**：
- ❌ **直接覆蓋**：風險高，難以回退
- ❌ **特性開關（Feature Flags）**：增加複雜度，不符合 MVP 精神

---

### 決策 2：CSS-First 動畫策略

**選擇**：優先使用 CSS animations/transitions，僅在必要時使用 JavaScript

**理由**：
- ✅ 效能：CSS 動畫由瀏覽器原生優化，GPU 加速
- ✅ 簡潔：聲明式語法，易於維護
- ✅ 降級：不支援的瀏覽器自動忽略，不影響功能
- ✅ 無依賴：不需要動畫函式庫

**實作**：
```css
/* CSS 動畫定義 */
@keyframes brush-stroke {
  from { stroke-dashoffset: 1000; }
  to { stroke-dashoffset: 0; }
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 交錯動畫使用 animation-delay */
.title-char {
  animation: fade-in-up 0.6s ease-out backwards;
  animation-delay: calc(var(--char-index) * 0.1s);
}
```

**JavaScript 控制**：僅用於：
- 動態添加/移除 CSS class（觸發動畫）
- Canvas 粒子系統（CSS 無法實現）
- 複雜的狀態機動畫序列

**替代方案**：
- ❌ **GSAP/Anime.js**：功能強大但增加 ~100KB 依賴，違反 MVP 原則
- ❌ **Web Animations API**：瀏覽器支援不一致，需要 polyfill

---

### 決策 3：Vanilla Canvas 粒子系統

**選擇**：自行實作輕量級 Canvas 粒子系統

**理由**：
- ✅ 客製化：完全符合筆墨美學（墨滴、煙火形狀）
- ✅ 輕量：約 200 行程式碼，無外部依賴
- ✅ 學習：保持專案的教育價值
- ❌ 開發時間：需要從零實作

**架構**：
```javascript
// frontend/js/modules/particle-system.js
export class ParticleSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
  }

  // 墨滴粒子
  emitInkDrops(x, y, count = 10) {
    // 黑色/墨綠色粒子，向外飛濺，逐漸淡出
  }

  // 煙火粒子
  emitFireworks(x, y, color = '#d97706') {
    // 放射狀粒子，拋物線運動，重力效果
  }

  update(deltaTime) {
    // 更新所有粒子位置、透明度、移除死亡粒子
  }

  render() {
    // 清除畫布，繪製所有活躍粒子
  }
}
```

**效能優化**：
- 使用物件池（Object Pool）避免頻繁記憶體分配
- 限制最大粒子數量（300 個）
- 使用 `requestAnimationFrame` 確保流暢渲染
- 粒子超出畫布時立即移除

**替代方案**：
- ❌ **particles.js**：50KB，功能過多且不符合筆墨美學
- ❌ **Three.js/PixiJS**：3D/遊戲引擎級別，過重

---

### 決策 4：CSS Variables 主題系統

**選擇**：使用 CSS Custom Properties 實作筆墨主題

**理由**：
- ✅ 集中管理：所有顏色、間距、字體定義在一處
- ✅ 動態切換：JavaScript 可修改 CSS 變數（未來可擴展多主題）
- ✅ 原生支援：所有目標瀏覽器都支援
- ✅ 可維護：修改主題只需改變變數值

**實作**：
```css
:root {
  /* 筆墨配色 */
  --color-ink-dark: #1a1a1a;
  --color-ink-medium: #4a5568;
  --color-rust: #d97706;        /* 赭石 */
  --color-vermillion: #dc2626;  /* 朱砂 */
  --color-jade: #059669;        /* 墨綠 */
  --color-cream: #fffbeb;       /* 奶油白 */

  /* 字體系統 */
  --font-serif: 'Noto Serif TC', serif;
  --font-sans: 'Noto Sans TC', sans-serif;

  /* 間距系統（8px baseline） */
  --space-1: 0.5rem;   /* 8px */
  --space-2: 1rem;     /* 16px */
  --space-3: 1.5rem;   /* 24px */
  --space-4: 2rem;     /* 32px */

  /* 動畫時長 */
  --duration-fast: 0.2s;
  --duration-normal: 0.4s;
  --duration-slow: 0.8s;

  /* 陰影深度 */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 8px rgba(0,0,0,0.15);
  --shadow-lg: 0 8px 16px rgba(0,0,0,0.2);
}
```

**替代方案**：
- ❌ **SASS/LESS 變數**：需要建置工具
- ❌ **硬編碼顏色**：難以維護，無法動態切換

---

### 決策 5：LocalStorage 統計持久化

**選擇**：使用 LocalStorage 儲存學習統計，單一 JSON 物件

**理由**：
- ✅ 簡單：無需後端修改，純前端實作
- ✅ 即時：無網路延遲，立即讀寫
- ✅ 持久：跨 session 保留資料
- ❌ 限制：僅限單一瀏覽器，無跨裝置同步

**資料結構**：
```javascript
{
  "stats": {
    "totalWords": 42,              // 總練習字數
    "correctInputs": 156,          // 正確輸入次數
    "totalInputs": 162,            // 總輸入次數
    "currentStreak": 8,            // 當前連續正確
    "longestStreak": 15,           // 最長連續正確
    "lastPracticeDate": "2026-02-09",
    "sessionStart": "2026-02-09T10:30:00Z"
  }
}
```

**實作模組**：
```javascript
// frontend/js/modules/stats-tracker.js
export class StatsTracker {
  constructor() {
    this.load();
  }

  load() {
    const data = localStorage.getItem('zhuyin-practice-stats');
    this.stats = data ? JSON.parse(data) : this.getDefaultStats();
  }

  save() {
    localStorage.setItem('zhuyin-practice-stats', JSON.stringify(this.stats));
  }

  recordCorrectInput() {
    this.stats.correctInputs++;
    this.stats.totalInputs++;
    this.stats.currentStreak++;
    this.stats.longestStreak = Math.max(
      this.stats.longestStreak,
      this.stats.currentStreak
    );
    this.save();
  }

  recordIncorrectInput() {
    this.stats.totalInputs++;
    this.stats.currentStreak = 0;
    this.save();
  }

  getAccuracy() {
    if (this.stats.totalInputs === 0) return 100;
    return Math.round(
      (this.stats.correctInputs / this.stats.totalInputs) * 100
    );
  }
}
```

**替代方案**：
- ❌ **後端 API**：需要改動後端，增加複雜度
- ❌ **IndexedDB**：過度設計，LocalStorage 已足夠
- ❌ **Cookies**：大小限制（4KB），不適合

---

### 決策 6：Google Fonts 字體載入策略

**選擇**：使用 Google Fonts CDN，`font-display: swap`

**理由**：
- ✅ CDN 優勢：全球 CDN，快速載入，可能已快取
- ✅ 字型品質：Noto Serif TC 專為繁中優化，涵蓋完整字集
- ✅ 降級優雅：`font-display: swap` 確保文字立即顯示

**實作**：
```html
<!-- 在 <head> 中預先連接 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 載入字體 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
```

**備用字體堆疊**：
```css
--font-serif: 'Noto Serif TC', 'Microsoft JhengHei', '微軟正黑體', serif;
--font-sans: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**替代方案**：
- ❌ **自行託管字體**：增加伺服器負擔，無 CDN 優勢
- ❌ **系統字體**：無法保證中文顯示品質

---

### 決策 7：模組化 CSS 架構

**選擇**：按功能分離 CSS 檔案，使用 BEM 命名慣例

**理由**：
- ✅ 可維護：每個功能模組獨立樣式檔案
- ✅ 可重用：BEM 避免樣式衝突
- ✅ 載入彈性：可選擇性載入樣式檔案

**檔案結構**：
```
frontend/styles/
├── redesign.css          # 主題變數、全域樣式、佈局
├── animations.css        # 所有動畫定義（@keyframes）
├── particles.css         # Canvas 容器樣式
├── keyboard-redesign.css # 鍵盤印章風格樣式
└── stats-panel.css       # 統計面板樣式
```

**BEM 範例**：
```css
/* Block */
.stats-panel { }

/* Block__Element */
.stats-panel__item { }
.stats-panel__value { }
.stats-panel__label { }

/* Block--Modifier */
.stats-panel--compact { }

/* Block__Element--Modifier */
.stats-panel__value--highlighted { }
```

**替代方案**：
- ❌ **單一巨大 CSS 檔案**：難以維護
- ❌ **CSS-in-JS**：需要建置工具，違反 MVP 原則
- ❌ **Tailwind CSS**：需要建置工具

---

## Risks / Trade-offs

### 風險 1：效能影響（低端裝置）

**風險**：大量動畫和粒子效果可能導致低端裝置卡頓

**緩解措施**：
- 使用 `will-change` CSS 屬性預先優化動畫元素
- 粒子系統限制最大數量（300 個）
- 使用 `requestAnimationFrame` 而非 `setInterval`
- 提供 "reduced motion" 媒體查詢支援：
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
- 檢測裝置效能，動態調整粒子密度

---

### 風險 2：字體載入延遲（FOUT/FOIT）

**風險**：Google Fonts 載入時可能出現文字閃爍或不可見

**緩解措施**：
- 使用 `font-display: swap` 確保文字立即顯示
- 提供完整的備用字體堆疊
- 使用 `<link rel="preconnect">` 預先建立連接
- 考慮使用 Font Loading API 顯示載入狀態：
  ```javascript
  document.fonts.ready.then(() => {
    document.body.classList.add('fonts-loaded');
  });
  ```

---

### 風險 3：LocalStorage 資料遺失

**風險**：使用者清除瀏覽器資料會遺失統計

**緩解措施**：
- 在統計面板提示使用者資料僅存於本地
- 提供匯出統計功能（下載 JSON）
- 提供匯入統計功能（上傳 JSON）
- 未來可考慮後端同步（非本次範圍）

---

### 風險 4：CSS 複雜度增加

**風險**：大量自訂動畫和樣式可能難以維護

**緩解措施**：
- 使用 CSS 變數集中管理主題
- 詳細註解每個動畫的用途
- 使用 BEM 命名避免衝突
- 建立樣式指南文件（Style Guide）

---

### 風險 5：瀏覽器相容性

**風險**：CSS Grid、CSS 變數、Canvas API 可能在舊版瀏覽器不支援

**緩解測試**：
- Chrome 61+：✅ 完整支援
- Firefox 60+：✅ 完整支援
- Safari 11+：✅ 完整支援
- 不支援 IE11：✅ 符合需求（IE 已淘汰）

**降級策略**：
- 使用 `@supports` 特性查詢：
  ```css
  @supports (display: grid) {
    .container { display: grid; }
  }

  @supports not (display: grid) {
    .container { display: flex; }
  }
  ```

---

### 風險 6：專案複雜度增加

**風險**：新增多個模組和檔案可能讓專案變得難以理解

**緩解措施**：
- 維持現有 README 並新增設計文件
- 每個新模組都有清楚的 JSDoc 註解
- 提供架構圖說明模組關係
- 保持模組單一職責原則（SRP）

---

## Migration Plan

### 階段 1：建立基礎（不影響現有版本）

1. 建立新檔案結構：
   ```bash
   frontend/
   ├── index-redesign.html         # 新增
   ├── styles/
   │   ├── redesign.css            # 新增
   │   ├── animations.css          # 新增
   │   ├── particles.css           # 新增
   │   ├── keyboard-redesign.css   # 新增
   │   └── stats-panel.css         # 新增
   └── js/
       ├── modules/
       │   ├── particle-system.js  # 新增
       │   ├── stats-tracker.js    # 新增
       │   └── animations.js       # 新增
       └── main-redesign.js        # 新增
   ```

2. 實作 CSS 主題系統（變數定義）
3. 實作基礎動畫（fade-in, slide-up）

### 階段 2：實作核心模組

1. 實作粒子系統模組（Canvas）
2. 實作統計追蹤模組（LocalStorage）
3. 實作動畫控制模組

### 階段 3：整合現有模組

1. 擴展 `keyboard.js`：添加印章風格樣式邏輯
2. 擴展 `input-handler.js`：整合粒子特效觸發
3. 擴展 `practice.js`：整合統計追蹤

### 階段 4：視覺設計實作

1. HTML 結構調整（新增裝飾元素、統計面板）
2. 筆墨主題 CSS 實作
3. 響應式調整

### 階段 5：測試與優化

1. 跨瀏覽器測試
2. 效能測試（FPS、記憶體）
3. 無障礙測試（鍵盤導航、螢幕閱讀器）

### 回退策略

- 保留原始 `index.html`，隨時可回退
- 使用 Git 分支管理（`feature/frontend-redesign`）
- 部署時可透過 URL 參數切換版本：
  - `?version=classic` → `index.html`
  - `?version=redesign` → `index-redesign.html`

---

## Open Questions

1. **動畫觸發時機**：
   - Q: 每次輸入都觸發粒子效果，還是只有完成整個字時？
   - A: (待決定) 建議每次正確輸入都觸發小型粒子，完成字時觸發大型煙火

2. **統計資料重置**：
   - Q: 是否提供「重置統計」按鈕？放在哪裡？
   - A: (待決定) 建議放在統計面板右上角，需要確認對話框

3. **筆觸背景動畫**：
   - Q: 筆觸背景是靜態 SVG 還是動畫 SVG？
   - A: (待決定) 建議頁面載入時播放一次書寫動畫，之後保持靜態

4. **印章效果細節**：
   - Q: 鍵盤按鍵的印章效果是圖片還是 CSS？
   - A: (待決定) 建議使用 CSS（box-shadow, border-radius）模擬，保持輕量

5. **進度條顯示**：
   - Q: 進度條顯示當前字的輸入進度，還是整體練習進度？
   - A: (待決定) 建議顯示當前字的輸入進度（X / Y 個注音符號）

6. **錯誤輸入視覺反饋**：
   - Q: 錯誤輸入時是否需要視覺提示（除了不高亮鍵盤）？
   - A: (待決定) 建議添加微妙的抖動動畫（shake animation）

---

## 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                   index-redesign.html                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CSS: redesign.css, animations.css, particles.css    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────────┐
        │      main-redesign.js (Entry)         │
        └───────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 粒子系統模組  │   │ 統計追蹤模組  │   │ 動畫控制模組  │
│ particle-    │   │ stats-       │   │ animations.js│
│ system.js    │   │ tracker.js   │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │         現有模組（共用/擴展）           │
        ├───────────────────────────────────────┤
        │  zhuyin-map.js     (共用，不修改)      │
        │  keyboard.js       (擴展，印章樣式)     │
        │  practice.js       (擴展，統計整合)     │
        │  input-handler.js  (擴展，特效觸發)     │
        └───────────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────────┐
        │      Flask Backend API (不變)          │
        │      GET /api/words/random            │
        └───────────────────────────────────────┘
```

---

## 總結

這個設計保持了專案的 MVP 精神（無框架、無建置工具），同時引入了視覺上令人印象深刻的筆墨童趣美學。通過 CSS-first 動畫策略、輕量級粒子系統、模組化架構，我們可以在不犧牲效能和可維護性的前提下，創造出獨特且引人入勝的學習體驗。

關鍵優勢：
- ✅ **技術簡潔**：純 CSS + Vanilla JS
- ✅ **效能優先**：GPU 加速動畫、物件池優化
- ✅ **可維護**：模組化、BEM 命名、詳細註解
- ✅ **安全遷移**：平行開發、保留原版、可回退
- ✅ **文化特色**：獨特的書法筆墨美學

主要權衡：
- ❌ 開發時間較長（自行實作粒子系統）
- ❌ 需要細心的效能調校
- ❌ 統計資料僅限本地（未來可擴展後端同步）
