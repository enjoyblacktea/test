## ADDED Requirements

### Requirement: Login screen display on unauthenticated access

系統 SHALL 在使用者未認證時顯示登入畫面，阻止直接存取練習功能。

登入畫面 MUST 包含以下元素：
- 帳號輸入欄位（username input field）
- 密碼輸入欄位（password input field, type="password"）
- 登入按鈕（login button）
- 錯誤訊息顯示區域（error message container）

#### Scenario: First-time visitor sees login screen

- **WHEN** 使用者首次開啟應用程式
- **THEN** 系統顯示登入畫面
- **AND** 練習畫面被隱藏

#### Scenario: Unauthenticated user cannot access practice screen

- **WHEN** 使用者未登入且嘗試存取應用程式
- **THEN** 系統阻止練習功能載入
- **AND** 顯示登入畫面要求認證

#### Scenario: Login screen contains all required form elements

- **WHEN** 登入畫面顯示
- **THEN** 使用者看到帳號輸入欄位
- **AND** 使用者看到密碼輸入欄位（遮蔽輸入）
- **AND** 使用者看到登入按鈕

### Requirement: Credential validation

系統 SHALL 驗證使用者輸入的帳號密碼是否符合預配置的認證資訊。

預配置帳號：
- 帳號（username）: `user`
- 密碼（password）: `1234`

驗證邏輯 MUST 為完全比對（exact match），區分大小寫。

#### Scenario: Successful login with correct credentials

- **WHEN** 使用者輸入帳號 `user` 和密碼 `1234`
- **AND** 按下登入按鈕
- **THEN** 系統驗證成功
- **AND** 系統儲存認證狀態到 LocalStorage
- **AND** 系統顯示練習畫面

#### Scenario: Login failure with incorrect username

- **WHEN** 使用者輸入錯誤的帳號（非 `user`）
- **AND** 按下登入按鈕
- **THEN** 系統驗證失敗
- **AND** 系統顯示錯誤訊息「帳號或密碼錯誤」
- **AND** 系統保持在登入畫面

#### Scenario: Login failure with incorrect password

- **WHEN** 使用者輸入正確帳號 `user` 但錯誤密碼（非 `1234`）
- **AND** 按下登入按鈕
- **THEN** 系統驗證失敗
- **AND** 系統顯示錯誤訊息「帳號或密碼錯誤」
- **AND** 系統清空密碼欄位

#### Scenario: Login failure with empty credentials

- **WHEN** 使用者未填寫帳號或密碼
- **AND** 嘗試按下登入按鈕
- **THEN** 系統阻止表單提交
- **AND** 瀏覽器顯示原生驗證提示（HTML5 required 屬性）

### Requirement: Authentication state persistence

系統 SHALL 將登入狀態儲存於 LocalStorage，實現跨 session 的持久化認證。

LocalStorage 鍵名 MUST 為 `zhuyin-practice-auth`。

資料結構 MUST 包含：
- `isLoggedIn` (boolean): 登入狀態標記
- `timestamp` (number): 登入時間戳記（milliseconds since epoch）

#### Scenario: Login state persists after page refresh

- **WHEN** 使用者成功登入
- **AND** 重新整理頁面
- **THEN** 系統讀取 LocalStorage 認證資料
- **AND** 系統維持登入狀態
- **AND** 顯示練習畫面而非登入畫面

#### Scenario: Login state persists after browser restart

- **WHEN** 使用者成功登入
- **AND** 關閉瀏覽器後重新開啟
- **THEN** 系統讀取 LocalStorage 認證資料
- **AND** 系統維持登入狀態
- **AND** 直接顯示練習畫面

#### Scenario: Login state shared across same-origin tabs

- **WHEN** 使用者在第一個分頁成功登入
- **AND** 在同一瀏覽器開啟第二個分頁
- **THEN** 第二個分頁讀取共享的 LocalStorage 狀態
- **AND** 第二個分頁直接顯示練習畫面（無需重新登入）

#### Scenario: LocalStorage data structure validation

- **WHEN** 系統儲存認證狀態
- **THEN** LocalStorage 包含鍵 `zhuyin-practice-auth`
- **AND** 值為 JSON 格式字串
- **AND** JSON 物件包含 `isLoggedIn: true`
- **AND** JSON 物件包含 `timestamp` 欄位（數字型別）

### Requirement: Authentication check on application initialization

系統 SHALL 在應用程式載入時（DOMContentLoaded）檢查認證狀態，決定顯示登入畫面或練習畫面。

認證檢查流程：
1. 讀取 LocalStorage 的 `zhuyin-practice-auth` 鍵
2. 驗證資料完整性（JSON 格式、包含 `isLoggedIn` 欄位）
3. 根據 `isLoggedIn` 值決定畫面切換

#### Scenario: Authenticated user bypasses login screen

- **WHEN** 應用程式初始化
- **AND** LocalStorage 存在有效的認證資料（`isLoggedIn: true`）
- **THEN** 系統跳過登入畫面
- **AND** 直接顯示練習畫面
- **AND** 初始化練習功能模組

#### Scenario: Unauthenticated user sees login screen

- **WHEN** 應用程式初始化
- **AND** LocalStorage 不存在認證資料或 `isLoggedIn: false`
- **THEN** 系統顯示登入畫面
- **AND** 不初始化練習功能模組

#### Scenario: Corrupted auth data treated as unauthenticated

- **WHEN** 應用程式初始化
- **AND** LocalStorage 認證資料格式錯誤（無效 JSON 或缺少 `isLoggedIn` 欄位）
- **THEN** 系統視為未認證
- **AND** 顯示登入畫面

### Requirement: Screen visibility control

系統 SHALL 使用 CSS 類別控制登入畫面和練習畫面的可見性，同時只顯示一個畫面。

畫面切換 MUST 透過新增/移除 `.hidden` CSS 類別實現。

#### Scenario: Only login screen visible before authentication

- **WHEN** 使用者未認證
- **THEN** `#login-screen` 元素不包含 `.hidden` 類別
- **AND** `#practice-screen` 元素包含 `.hidden` 類別

#### Scenario: Only practice screen visible after authentication

- **WHEN** 使用者成功登入
- **THEN** `#login-screen` 元素包含 `.hidden` 類別
- **AND** `#practice-screen` 元素不包含 `.hidden` 類別

#### Scenario: Screen switch maintains DOM structure

- **WHEN** 系統在登入和練習畫面之間切換
- **THEN** 兩個畫面的 DOM 結構保持存在
- **AND** 僅透過 CSS 控制顯示/隱藏
- **AND** 不進行 DOM 移除或重建

### Requirement: Login error feedback

系統 SHALL 在登入失敗時顯示清楚的錯誤訊息，並在 3 秒後自動消失。

錯誤訊息 MUST 使用淡入淡出（fade-in/fade-out）動畫效果。

#### Scenario: Error message displays on login failure

- **WHEN** 使用者輸入錯誤的帳號或密碼
- **AND** 提交登入表單
- **THEN** 系統顯示錯誤訊息「帳號或密碼錯誤」
- **AND** 錯誤訊息使用 fade-in 動畫出現

#### Scenario: Error message auto-dismisses after 3 seconds

- **WHEN** 錯誤訊息顯示
- **THEN** 3 秒後錯誤訊息自動使用 fade-out 動畫消失

#### Scenario: Password field clears on login failure

- **WHEN** 登入驗證失敗
- **THEN** 密碼輸入欄位內容被清空
- **AND** 帳號輸入欄位內容保留

### Requirement: Logout functionality

系統 SHALL 提供登出功能，允許使用者結束當前 session 並返回登入畫面。

登出按鈕 MUST 顯示於練習畫面的明顯位置。

#### Scenario: Logout button visible in practice screen

- **WHEN** 使用者已登入並在練習畫面
- **THEN** 系統顯示登出按鈕
- **AND** 登出按鈕文字為「登出」或明確的登出圖示

#### Scenario: Logout clears authentication state

- **WHEN** 使用者點擊登出按鈕
- **THEN** 系統從 LocalStorage 移除 `zhuyin-practice-auth` 鍵
- **AND** 系統清除記憶體中的認證狀態

#### Scenario: Logout redirects to login screen

- **WHEN** 使用者點擊登出按鈕
- **AND** 認證狀態已清除
- **THEN** 系統切換顯示登入畫面
- **AND** 隱藏練習畫面

#### Scenario: Post-logout state prevents unauthorized access

- **WHEN** 使用者登出後
- **AND** 重新整理頁面
- **THEN** 系統顯示登入畫面
- **AND** 要求重新輸入帳號密碼

### Requirement: Visual theme consistency

登入畫面的視覺設計 SHALL 符合應用程式現有的「筆墨童趣」書法主題風格。

設計元素包含：
- 使用現有 CSS 變數（`--color-ink-*` 系列）
- 筆觸風格的邊框和裝飾
- 與練習畫面一致的字型選擇
- 手繪感的按鈕和互動效果

#### Scenario: Login screen uses consistent color palette

- **WHEN** 登入畫面顯示
- **THEN** 背景色使用 `--color-paper-*` 變數
- **AND** 文字色使用 `--color-ink-*` 變數
- **AND** 色彩與練習畫面協調一致

#### Scenario: Form elements match calligraphy theme

- **WHEN** 登入畫面顯示
- **THEN** 輸入框使用筆觸風格邊框（3px solid）
- **AND** 按鈕具有手繪感的圓角和陰影
- **AND** 字型與練習畫面保持一致

#### Scenario: Interactive elements have hover effects

- **WHEN** 使用者滑鼠移至登入按鈕
- **THEN** 按鈕顯示 hover 狀態變化（顏色加深或陰影增強）
- **AND** 過渡效果使用 CSS transition 平滑呈現

### Requirement: Form validation and user experience

系統 SHALL 提供良好的使用者體驗，包含表單驗證、焦點管理、Enter 鍵提交等功能。

#### Scenario: Enter key submits login form

- **WHEN** 使用者在帳號或密碼欄位按下 Enter 鍵
- **THEN** 系統觸發登入表單提交
- **AND** 執行認證驗證流程

#### Scenario: Input fields support autofocus

- **WHEN** 登入畫面顯示
- **THEN** 帳號輸入欄位自動獲得焦點（autofocus）
- **AND** 使用者可立即開始輸入

#### Scenario: Password input is masked

- **WHEN** 使用者在密碼欄位輸入
- **THEN** 輸入的字元顯示為圓點或星號（type="password"）
- **AND** 實際密碼內容不可見

#### Scenario: Required fields prevent empty submission

- **WHEN** 使用者未填寫帳號欄位
- **AND** 嘗試提交表單
- **THEN** 瀏覽器顯示「請填寫此欄位」提示
- **AND** 表單不被提交

### Requirement: Module architecture and integration

認證系統 SHALL 實作為獨立的 ES6 模組（`auth.js`），提供清晰的介面供主應用程式使用。

模組 MUST 導出以下函式：
- `checkAuth()`: 檢查當前認證狀態，返回 boolean
- `login(username, password)`: 執行登入驗證，返回 boolean
- `logout()`: 清除認證狀態，無返回值

#### Scenario: Auth module exports required functions

- **WHEN** 其他模組匯入 `auth.js`
- **THEN** 可存取 `checkAuth` 函式
- **AND** 可存取 `login` 函式
- **AND** 可存取 `logout` 函式

#### Scenario: checkAuth returns boolean based on state

- **WHEN** 調用 `checkAuth()`
- **THEN** 如果已認證，返回 `true`
- **OR** 如果未認證，返回 `false`

#### Scenario: login returns boolean based on validation result

- **WHEN** 調用 `login(username, password)`
- **THEN** 如果帳密正確，儲存認證狀態並返回 `true`
- **OR** 如果帳密錯誤，不儲存狀態並返回 `false`

#### Scenario: logout clears state without return value

- **WHEN** 調用 `logout()`
- **THEN** 系統清除 LocalStorage 認證資料
- **AND** 函式不返回值（void）

### Requirement: Security considerations and limitations

系統 MUST 在文件中明確標示此為教育用途的存取控制，非生產級安全認證系統。

已知限制包含：
- 帳號密碼明文儲存於前端程式碼
- LocalStorage 資料可被使用者手動修改
- 無後端驗證機制
- 無 session timeout 或自動登出

#### Scenario: Security disclaimer in documentation

- **WHEN** 開發者閱讀專案文件
- **THEN** 文件明確說明這是教育用途的實作
- **AND** 文件列出已知的安全限制
- **AND** 文件警告不適合生產環境使用

#### Scenario: Code comments indicate hardcoded credentials

- **WHEN** 開發者檢視 `auth.js` 原始碼
- **THEN** 程式碼註解標示 CREDENTIALS 為硬編碼
- **AND** 註解說明此為 MVP 簡化方案
