## 1. Authentication Module Setup

- [x] 1.1 建立 `frontend/js/modules/auth.js` 檔案
- [x] 1.2 定義 CREDENTIALS 常數（username: 'user', password: '1234'）
- [x] 1.3 實作 `checkAuth()` 函式，讀取 LocalStorage 並返回 boolean
- [x] 1.4 實作 `login(username, password)` 函式，驗證帳密並儲存狀態
- [x] 1.5 實作 `logout()` 函式，清除 LocalStorage 認證資料
- [x] 1.6 加入程式碼註解說明這是教育用途的簡化實作
- [x] 1.7 驗證 auth.js 模組可正確匯出 3 個函式

## 2. HTML Structure Modifications

- [x] 2.1 在 `index-redesign.html` 新增 `#login-screen` 容器（初始不包含 .hidden）
- [x] 2.2 在 `#login-screen` 中建立登入表單（id="login-form"）
- [x] 2.3 新增帳號輸入欄位（id="username", type="text", required, autofocus）
- [x] 2.4 新增密碼輸入欄位（id="password", type="password", required）
- [x] 2.5 新增登入按鈕（type="submit", 文字「登入」）
- [x] 2.6 新增錯誤訊息容器（id="login-error", 初始隱藏）
- [x] 2.7 在 `#practice-screen` 容器加入初始 `.hidden` 類別
- [x] 2.8 在練習畫面頭部新增登出按鈕（id="logout-button", 文字「登出」）
- [x] 2.9 驗證 HTML 結構符合規格要求

## 3. CSS Styling for Login Screen

- [x] 3.1 建立 `frontend/styles/login.css` 檔案
- [x] 3.2 在 `index-redesign.html` 中引入 `login.css`
- [x] 3.3 定義 `.hidden` 類別（display: none）
- [x] 3.4 設計 `#login-screen` 佈局（垂直居中、最大寬度 400px）
- [x] 3.5 設計登入表單樣式，使用書法主題色彩變數（--color-ink-*, --color-paper-*）
- [x] 3.6 設計輸入框樣式（筆觸風格邊框 3px solid, 圓角, padding）
- [x] 3.7 設計登入按鈕樣式（書法風格，手繪感圓角和陰影）
- [x] 3.8 設計按鈕 hover 效果（顏色加深，transition 平滑過渡）
- [x] 3.9 設計錯誤訊息樣式（紅色文字，fade-in/fade-out 動畫）
- [x] 3.10 設計登出按鈕樣式（明顯可見，與主題一致）
- [x] 3.11 驗證所有樣式符合「筆墨童趣」書法主題

## 4. Main Application Integration

- [x] 4.1 在 `main-redesign.js` 頂部匯入 auth 模組（`import * as auth from './modules/auth.js'`）
- [x] 4.2 取得 DOM 元素參考（login-screen, practice-screen, login-form, logout-button, login-error）
- [x] 4.3 實作 `showLoginScreen()` 函式（移除 login-screen 的 .hidden，加入 practice-screen 的 .hidden）
- [x] 4.4 實作 `showPracticeScreen()` 函式（移除 practice-screen 的 .hidden，加入 login-screen 的 .hidden）
- [x] 4.5 實作 `initPracticeApp()` 函式（初始化所有練習功能模組）
- [x] 4.6 在 DOMContentLoaded 中加入認證檢查邏輯（調用 auth.checkAuth()）
- [x] 4.7 如果已認證，執行 showPracticeScreen() 和 initPracticeApp()
- [x] 4.8 如果未認證，執行 showLoginScreen() 並綁定登入事件
- [x] 4.9 實作登入表單 submit 事件處理（preventDefault, 取得輸入值, 調用 auth.login()）
- [x] 4.10 登入成功時執行 showPracticeScreen() 和 initPracticeApp()
- [x] 4.11 登入失敗時顯示錯誤訊息並清空密碼欄位
- [x] 4.12 實作錯誤訊息顯示函式（fade-in 顯示，3 秒後 fade-out）
- [x] 4.13 實作登出按鈕 click 事件處理（調用 auth.logout(), 執行 showLoginScreen()）
- [x] 4.14 確保練習功能僅在認證後初始化

## 5. Error Handling and Edge Cases

- [x] 5.1 處理 LocalStorage 不可用情況（try-catch 包裹，降級或顯示警告）
- [x] 5.2 處理 LocalStorage 資料損壞情況（JSON.parse 錯誤時視為未認證）
- [x] 5.3 確保空白輸入透過 HTML5 required 屬性阻止提交
- [x] 5.4 確保密碼欄位使用 type="password" 遮蔽輸入
- [x] 5.5 確保 Enter 鍵可觸發表單提交

## 6. Functionality Testing

- [x] 6.1 測試首次訪問顯示登入畫面
- [x] 6.2 測試輸入正確帳密（user/1234）可成功登入
- [x] 6.3 測試輸入錯誤帳號顯示錯誤訊息
- [x] 6.4 測試輸入錯誤密碼顯示錯誤訊息並清空密碼欄位
- [x] 6.5 測試錯誤訊息 3 秒後自動消失
- [x] 6.6 測試空白欄位觸發 HTML5 驗證提示
- [x] 6.7 測試登入後重新整理頁面仍保持登入狀態
- [x] 6.8 測試關閉瀏覽器重新開啟仍保持登入狀態
- [x] 6.9 測試同源分頁共享登入狀態
- [x] 6.10 測試登出按鈕清除認證狀態並返回登入畫面
- [x] 6.11 測試登出後重新整理頁面顯示登入畫面
- [x] 6.12 測試練習功能在登入後正常運作

## 7. UI/UX Validation

- [x] 7.1 驗證登入畫面符合書法主題（色彩、字型、筆觸風格）
- [x] 7.2 驗證輸入框有明顯的 focus 效果
- [x] 7.3 驗證登入按鈕有 hover 效果（顏色變化、transition）
- [x] 7.4 驗證錯誤訊息有 fade-in/fade-out 動畫
- [x] 7.5 驗證登出按鈕在練習畫面明顯可見
- [x] 7.6 驗證帳號輸入欄位自動獲得 autofocus
- [x] 7.7 驗證密碼輸入顯示為遮蔽符號（圓點或星號）
- [x] 7.8 驗證畫面切換流暢無閃爍
- [x] 7.9 驗證表單佈局在不同螢幕尺寸下正常顯示

## 8. LocalStorage Data Validation

- [x] 8.1 驗證登入成功後 LocalStorage 包含 `zhuyin-practice-auth` 鍵
- [x] 8.2 驗證儲存的資料為 JSON 格式字串
- [x] 8.3 驗證 JSON 物件包含 `isLoggedIn: true`
- [x] 8.4 驗證 JSON 物件包含 `timestamp` 欄位（數字型別）
- [x] 8.5 驗證登出後 LocalStorage 的 `zhuyin-practice-auth` 鍵被移除

## 9. Code Quality and Documentation

- [x] 9.1 在 auth.js 加入 JSDoc 註解說明每個函式的用途和參數
- [x] 9.2 在 design.md 標示的限制和風險處加入程式碼註解
- [x] 9.3 確保所有變數和函式命名清晰有意義
- [x] 9.4 確保程式碼符合專案現有的編碼風格
- [x] 9.5 檢查 console.log 除錯訊息是否已移除或保留必要的
- [x] 9.6 在 README 中加入登入功能說明（帳號: user, 密碼: 1234）

## 10. Integration and Regression Testing

- [x] 10.1 驗證現有練習功能不受認證系統影響
- [x] 10.2 驗證虛擬鍵盤在登入後正常顯示和互動
- [x] 10.3 驗證注音輸入驗證在登入後正常運作
- [x] 10.4 驗證練習字詞 API 調用正常
- [x] 10.5 驗證統計追蹤（若已實作）在登入後正常
- [x] 10.6 驗證粒子效果（若已實作）在登入後正常
- [x] 10.7 開啟瀏覽器開發者工具檢查無錯誤或警告訊息

## 11. Cross-Browser Compatibility (Optional)

- [x] 11.1 在 Chrome 測試所有功能正常
- [ ] 11.2 在 Firefox 測試所有功能正常
- [ ] 11.3 在 Safari 測試所有功能正常（如可用）
- [x] 11.4 驗證 LocalStorage 在所有測試瀏覽器均可用

## 12. Final Review and Documentation

- [x] 12.1 檢視 proposal.md 確認所有 What Changes 項目已實作
- [x] 12.2 檢視 specs/user-authentication/spec.md 確認所有需求已滿足
- [x] 12.3 檢視 design.md 確認所有設計決策已實現
- [x] 12.4 確認約 280 行程式碼的估算範圍合理（auth.js ~60, main.js +90, HTML +50, CSS ~80）
- [x] 12.5 更新專案文件標示新增的認證功能
- [x] 12.6 準備 commit 訊息總結此次變更
