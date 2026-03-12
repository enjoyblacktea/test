## ADDED Requirements

### Requirement: React + TypeScript + Vite 建置

系統 SHALL 使用 React 18 + TypeScript + Vite 作為前端技術棧，取代 Vanilla JavaScript ES6 模組。

#### Scenario: 開發模式啟動
- **WHEN** 執行 `npm run dev`
- **THEN** Vite 啟動開發伺服器，支援 HMR（Hot Module Replacement）

#### Scenario: 生產建置
- **WHEN** 執行 `npm run build`
- **THEN** Vite 產生最佳化的靜態檔案至 `dist/` 目錄，包含 tree-shaking 與 code splitting

#### Scenario: TypeScript 型別檢查
- **WHEN** 執行 `npm run build` 或 IDE 開啟專案
- **THEN** TypeScript 編譯器對所有 `.ts` / `.tsx` 檔案執行型別檢查，未定義 props 或 API 欄位即報錯

---

### Requirement: 元件化架構

系統 SHALL 將 UI 拆分為獨立 React 元件，每個元件有明確的單一職責。

#### Scenario: PracticeCard 顯示
- **WHEN** PracticePage 載入
- **THEN** PracticeCard 元件顯示當前字符，並接受 `character`、`inputProgress` props 控制顯示狀態

#### Scenario: VirtualKeyboard 渲染
- **WHEN** PracticePage 載入
- **THEN** VirtualKeyboard 元件根據 zhuyin-map 渲染按鍵，並以 props 接收 `activeKeys` 高亮顯示

---

### Requirement: 自訂 hooks 封裝業務邏輯

系統 SHALL 使用自訂 React hooks 封裝練習流程與認證邏輯，元件不直接存取 API 或 localStorage。

#### Scenario: usePractice hook 管理練習狀態
- **WHEN** PracticePage 掛載
- **THEN** `usePractice` hook 自動載入隨機字符，提供 `checkInput`、`completeAttempt` 方法，並累積 keystroke 事件

#### Scenario: useAuth hook 管理認證狀態
- **WHEN** 任何頁面需要確認登入狀態
- **THEN** `useAuth` hook 提供 `user`、`isAuthenticated`、`login`、`logout` 介面，從 localStorage 讀取 token

---

### Requirement: TypeScript 型別覆蓋所有 API 介面

系統 SHALL 在 `src/types/index.ts` 定義所有 API request / response 的 TypeScript interface，API client 函式使用泛型確保型別安全。

#### Scenario: API response 型別
- **WHEN** 呼叫 `api.practice.getWord()`
- **THEN** 回傳值型別為 `WordResponse`，包含 `character`、`zhuyin`、`keys` 欄位，IDE 可自動補全

#### Scenario: 錯誤型別
- **WHEN** API 呼叫失敗
- **THEN** 拋出型別為 `ApiError` 的 error，包含 `status`、`message` 欄位

---

### Requirement: axios JWT interceptor 自動刷新 token

系統 SHALL 使用 axios interceptor 攔截 401 回應，自動執行 token refresh，並重試原始請求，與現有後端邏輯相容。

#### Scenario: token 過期自動刷新
- **WHEN** API 回傳 401 且 localStorage 有 refresh_token
- **THEN** interceptor 自動呼叫 POST /api/auth/refresh，更新 access_token，並重試原始請求

#### Scenario: refresh 失敗導向登入
- **WHEN** refresh token 也已過期（refresh API 回傳 401）
- **THEN** 清除 localStorage 的 token，跳轉至登入頁面

---

### Requirement: 深色主題保留

系統 SHALL 保留現有深色主題設計風格（純黑底色、cyan 強調色、green 成功色）。

#### Scenario: 主題顏色一致
- **WHEN** React 前端在瀏覽器顯示
- **THEN** 視覺風格與現有 Vanilla JS 前端一致，使用相同 CSS 變數定義（--bg-primary: #0a0a0a、--accent-cyan: #00d9ff）
