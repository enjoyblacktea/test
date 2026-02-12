## Context

注音練習網站目前是完全開放存取的單頁應用程式，任何人開啟網頁即可直接進入練習功能。專案使用 Vanilla JavaScript（ES6 modules）+ Flask 後端的架構，前端採用「筆墨童趣」書法主題設計風格。

**現狀**：
- 前端：ES6 modules 組織，無建置工具，純瀏覽器執行
- 後端：Flask API 僅提供練習字詞資料（`/api/words/random`）
- 部署：本地開發環境，前後端分離
- 使用者識別：無

**限制條件**：
- 必須保持 MVP 簡單性（Vanilla JS，無框架）
- 不涉及後端修改（純前端實作）
- 符合現有書法主題視覺風格
- 不需要複雜的使用者管理系統

**利益相關者**：
- 教育使用者（需要簡單易用的登入流程）
- 開發維護者（需要保持程式碼簡潔可維護）

## Goals / Non-Goals

**Goals:**
- 在進入練習功能前要求帳號密碼驗證
- 實現持久化登入狀態（瀏覽器關閉後仍保持登入）
- 提供登出功能讓使用者可以切換帳號
- 登入介面符合現有書法主題設計
- 實作簡單且不需要後端修改

**Non-Goals:**
- ❌ 後端 API 認證或 JWT token 機制
- ❌ 多使用者管理、註冊功能、忘記密碼
- ❌ 安全的密碼儲存（不需要雜湊或加密）
- ❌ Session timeout 或自動登出機制
- ❌ OAuth 或第三方登入整合
- ❌ 後端使用者資料庫
- ❌ 跨裝置登入同步

**重要說明**：這是教育用途的簡單存取控制，不是生產級安全認證系統。

## Decisions

### 1. 使用 LocalStorage 儲存登入狀態

**選擇**：使用 `localStorage.setItem('zhuyin-practice-auth', JSON.stringify({...}))` 儲存認證狀態

**理由**：
- ✅ 持久化：瀏覽器關閉後仍保留（符合需求）
- ✅ 簡單：無需後端 session 管理
- ✅ 同源：同一瀏覽器所有分頁共享狀態

**替代方案**：
- ❌ **sessionStorage**：分頁關閉即清除，不符合持久化需求
- ❌ **Cookie**：需要額外處理過期時間和 HttpOnly 設定，複雜度較高
- ❌ **後端 Session**：需要修改後端和 API 設計，超出範圍

**資料結構**：
```json
{
  "isLoggedIn": true,
  "timestamp": 1707469200000
}
```

### 2. 硬編碼預配置帳號

**選擇**：在 `auth.js` 中使用常數儲存單一帳號資訊

**理由**：
- ✅ MVP 範圍：教育用途的簡單存取控制
- ✅ 無後端依賴：不需要使用者資料庫或 API
- ✅ 易於部署：無需環境變數或配置檔

**替代方案**：
- ❌ **環境變數**：前端無法使用 process.env（無建置工具）
- ❌ **後端 API 驗證**：需要建立使用者資料庫和認證端點
- ❌ **配置檔**：增加部署複雜度

**實作**：
```javascript
const CREDENTIALS = {
    username: 'user',
    password: '1234'
};
```

**安全性說明**：此為明文儲存在前端程式碼，任何人檢查原始碼即可看到。這在教育場景可接受，但不適合生產環境。

### 3. 畫面切換使用 CSS 類別控制可見性

**選擇**：使用 `.hidden` CSS 類別切換 `#login-screen` 和 `#practice-screen`

**理由**：
- ✅ 簡單：符合 Vanilla JS 無框架原則
- ✅ 效能：無需路由或 SPA 框架
- ✅ 可測試：DOM 結構保持一致

**替代方案**：
- ❌ **SPA 路由（History API）**：增加複雜度，超出 MVP 範圍
- ❌ **完全重新渲染 DOM**：效能較差，失去現有狀態
- ❌ **`display: none` inline style**：不夠語意化，難以維護

**實作**：
```javascript
function showLoginScreen() {
    loginScreen.classList.remove('hidden');
    practiceScreen.classList.add('hidden');
}
```

### 4. 純前端驗證（無後端參與）

**選擇**：所有認證邏輯在瀏覽器執行

**理由**：
- ✅ 符合專案限制：不修改後端
- ✅ 降低複雜度：無需處理 API 請求、錯誤處理
- ✅ 快速反饋：即時驗證，無網路延遲

**替代方案**：
- ❌ **後端 API 驗證**：需要建立 `/api/auth/login` 端點和 session 管理

**權衡**：前端驗證不安全（任何人可透過開發者工具修改 LocalStorage），但符合教育場景需求。

### 5. 書法主題一致性

**選擇**：登入畫面使用現有 CSS 變數和設計語言

**理由**：
- ✅ 品牌一致性：統一視覺體驗
- ✅ 重用樣式：減少重複程式碼
- ✅ 維護性：統一管理主題

**設計元素**：
- 使用現有 `--color-ink-*` 顏色變數
- 筆觸風格邊框（`border: 3px solid var(--color-ink-medium)`）
- 毛筆字型（與現有練習字體一致）
- 手繪感按鈕（hover 效果）

### 6. ES6 模組化架構

**選擇**：建立獨立的 `auth.js` 模組並在 `main-redesign.js` 匯入

**理由**：
- ✅ 關注點分離：認證邏輯獨立於應用程式初始化
- ✅ 可測試性：易於單元測試
- ✅ 可重用性：未來可在其他頁面使用

**模組介面**：
```javascript
// auth.js
export function checkAuth()
export function login(username, password)
export function logout()
```

## Architecture

### 應用程式流程

```
使用者開啟頁面
    ↓
DOMContentLoaded 事件觸發
    ↓
檢查 auth.checkAuth()
    ↓
┌─────────────┬─────────────┐
│  已登入     │  未登入     │
└─────────────┴─────────────┘
      ↓              ↓
顯示練習畫面    顯示登入畫面
初始化練習功能   綁定登入表單
      ↓              ↓
使用者按登出    使用者輸入帳密
      ↓              ↓
auth.logout()   auth.login()
      ↓              ↓
返回登入畫面    驗證成功 → 顯示練習畫面
                驗證失敗 → 顯示錯誤訊息
```

### 檔案結構

```
frontend/
├── index-redesign.html (修改)
│   ├── #login-screen (新增)
│   │   ├── 登入表單
│   │   └── 錯誤訊息容器
│   └── #practice-screen (修改)
│       ├── 登出按鈕 (新增)
│       └── 現有練習介面
├── js/
│   ├── main-redesign.js (修改)
│   │   ├── 認證檢查邏輯
│   │   ├── 畫面切換函式
│   │   └── 登入/登出事件處理
│   └── modules/
│       └── auth.js (新增)
│           ├── CREDENTIALS 常數
│           ├── checkAuth()
│           ├── login()
│           └── logout()
└── styles/
    └── login.css (新增)
        ├── 登入畫面佈局
        ├── 表單樣式
        └── 書法主題適配
```

### 資料流

```
使用者輸入帳密
    ↓
表單 submit 事件
    ↓
auth.login(username, password)
    ↓
比對 CREDENTIALS
    ↓
┌──────────┬──────────┐
│  正確    │  錯誤    │
└──────────┴──────────┘
     ↓           ↓
寫入 LocalStorage  返回 false
     ↓           ↓
返回 true    顯示錯誤訊息
     ↓
切換到練習畫面
     ↓
初始化練習功能
```

## Error Handling

### 登入驗證錯誤

**情境**：使用者輸入錯誤帳號或密碼

**處理**：
1. `auth.login()` 返回 `false`
2. 顯示錯誤訊息：「帳號或密碼錯誤」
3. 清空密碼欄位
4. 使用 fade-in 動畫顯示錯誤

**實作**：
```javascript
function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.add('show');
    setTimeout(() => errorElement.classList.remove('show'), 3000);
}
```

### LocalStorage 不可用

**情境**：瀏覽器隱私模式或禁用 LocalStorage

**處理**：
- 簡化方案：直接降級到 sessionStorage
- 或顯示警告：「請啟用瀏覽器儲存功能」

**偵測**：
```javascript
function isLocalStorageAvailable() {
    try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
        return true;
    } catch {
        return false;
    }
}
```

### 空白輸入

**情境**：使用者未填寫帳號或密碼

**處理**：
- HTML5 表單驗證：`<input required>`
- 瀏覽器原生提示訊息

## Risks / Trade-offs

### [風險] 前端儲存的帳密完全不安全

**影響**：任何人檢查原始碼即可看到帳號密碼

**緩解措施**：
- 📝 在 README 中明確標示這是教育用途，不適合生產環境
- 📝 使用簡單密碼 `1234`，不造成真實帳號外洩風險
- 📝 未來可升級為後端驗證時，架構易於擴展

**接受理由**：這是教育場景的 MVP，主要目的是練習功能的存取控制，不是安全性防護。

### [風險] LocalStorage 可被使用者手動修改

**影響**：使用者可透過開發者工具修改 `isLoggedIn: true` 繞過驗證

**緩解措施**：
- ⚠️ 目前無緩解措施（前端無法防止）
- 🔮 未來：後端 session validation

**接受理由**：教育用途不需防範惡意使用者，只需基本存取控制。

### [風險] 無 session timeout

**影響**：使用者登入後永久保持登入狀態

**緩解措施**：
- 提供明顯的登出按鈕
- 可檢查 `timestamp` 實作簡單的過期機制（未來增強）

**接受理由**：教育場景不需要嚴格的 session 管理。

### [風險] 跨瀏覽器相容性

**影響**：舊版瀏覽器可能不支援 LocalStorage 或 ES6 modules

**緩解措施**：
- 目標瀏覽器：現代瀏覽器（Chrome 61+, Firefox 60+, Safari 11+）
- LocalStorage 支援度：IE 8+ 以上均支援

**接受理由**：專案已使用 ES6 modules，瀏覽器需求一致。

### [權衡] 簡單性 vs 安全性

**選擇**：優先簡單性

**理由**：
- ✅ MVP 快速驗證概念
- ✅ 教育場景無敏感資料
- ✅ 未來易於升級為安全方案

**代價**：
- ❌ 不適合生產環境
- ❌ 無法防止惡意存取

### [權衡] 單一帳號 vs 多使用者

**選擇**：單一預配置帳號

**理由**：
- ✅ 實作簡單（無需資料庫）
- ✅ 符合教育用途（共用帳號）

**代價**：
- ❌ 無法追蹤個人學習進度
- ❌ 無法實作個人化功能

## Testing Strategy

### 功能測試清單

**登入流程**：
- [ ] 首次開啟網站顯示登入畫面
- [ ] 輸入正確帳號密碼（user/1234）可成功登入
- [ ] 輸入錯誤帳號或密碼顯示錯誤訊息
- [ ] 錯誤訊息 3 秒後自動消失
- [ ] 空白欄位觸發 HTML5 驗證

**登入狀態持久化**：
- [ ] 登入後重新整理頁面仍保持登入狀態
- [ ] 關閉瀏覽器重新開啟仍保持登入狀態
- [ ] 不同分頁共享登入狀態

**登出流程**：
- [ ] 點擊登出按鈕返回登入畫面
- [ ] 登出後 LocalStorage 清除認證資料
- [ ] 登出後重新整理頁面顯示登入畫面

**UI/UX**：
- [ ] 登入畫面符合書法主題風格
- [ ] 表單輸入框有 focus 效果
- [ ] 登入按鈕有 hover 效果
- [ ] 錯誤訊息有 fade-in/out 動畫
- [ ] 登出按鈕明顯可見

**整合**：
- [ ] 登入後練習功能正常運作
- [ ] 練習功能不受認證模組影響
- [ ] Console 無錯誤訊息

### 手動測試步驟

1. **首次訪問測試**
   - 清除 LocalStorage
   - 開啟 `index-redesign.html`
   - 確認顯示登入畫面

2. **登入失敗測試**
   - 輸入 `wrong` / `wrong`
   - 確認顯示「帳號或密碼錯誤」
   - 確認密碼欄位被清空

3. **登入成功測試**
   - 輸入 `user` / `1234`
   - 確認切換到練習畫面
   - 確認練習功能正常

4. **持久化測試**
   - 重新整理頁面
   - 確認仍在練習畫面
   - 檢查 LocalStorage 存在 `zhuyin-practice-auth` 鍵

5. **登出測試**
   - 點擊登出按鈕
   - 確認返回登入畫面
   - 確認 LocalStorage 已清除

## Migration Plan

### 部署步驟

此為純前端變更，無需資料庫遷移或 API 版本管理。

**步驟**：
1. 建立新檔案：`auth.js`, `login.css`
2. 修改現有檔案：`index-redesign.html`, `main-redesign.js`
3. 本地測試通過後，部署到伺服器
4. 通知使用者：首次訪問需要使用帳號 `user` 密碼 `1234` 登入

**向後相容性**：
- ✅ 不影響後端 API
- ✅ 現有練習功能完全不變
- ⚠️ 新增存取門檻（需要登入）

### Rollback 策略

**情境**：登入功能有重大問題需要緊急回退

**步驟**：
1. Git revert 相關 commits
2. 重新部署舊版本（無認證版本）
3. 通知使用者恢復開放存取

**影響**：
- 使用者 LocalStorage 殘留資料無害（下次更新時會覆寫）
- 無資料庫變更，回退無風險

## Open Questions

### Q1: 是否需要「記住我」選項？

**目前設計**：預設永久記住登入狀態

**替代方案**：提供 checkbox 讓使用者選擇是否記住

**決策**：暫不實作，保持簡單。未來若有需求可輕鬆新增。

### Q2: 是否需要更換帳號密碼的機制？

**目前設計**：硬編碼在程式碼中

**替代方案**：管理員介面修改帳密

**決策**：超出 MVP 範圍，標記為未來增強項目。

### Q3: 是否需要限制登入嘗試次數？

**目前設計**：無限制

**風險**：可能被暴力破解（但前端驗證本質上可繞過）

**決策**：暫不實作。若未來升級為後端驗證時再加入 rate limiting。

## Future Enhancements

超出此次變更範圍，但已考慮架構擴展性：

1. **後端驗證整合**
   - 新增 `/api/auth/login` 端點
   - `auth.js` 修改為 async API 呼叫
   - 使用 JWT token 替代 LocalStorage flag

2. **多使用者支援**
   - 後端使用者資料庫
   - 註冊、忘記密碼功能
   - 個人學習進度追蹤

3. **Session timeout**
   - 檢查 `timestamp` 實作過期邏輯
   - 自動登出提示

4. **安全性增強**
   - HTTPS only
   - CSRF token
   - 密碼雜湊（後端）
