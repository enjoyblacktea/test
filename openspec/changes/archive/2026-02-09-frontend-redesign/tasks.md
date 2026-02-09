## 1. 專案設定與基礎架構

- [x] 1.1 建立新檔案結構目錄（frontend/styles/, frontend/js/modules/）
- [x] 1.2 建立 index-redesign.html 作為重新設計版本的主頁面
- [x] 1.3 建立 main-redesign.js 作為新版本的 JavaScript 入口點
- [x] 1.4 在 HTML <head> 中添加 Google Fonts 預連接（preconnect）
- [x] 1.5 在 HTML <head> 中載入 Noto Serif TC 和 Noto Sans TC 字體

## 2. CSS 主題系統與變數

- [x] 2.1 建立 frontend/styles/redesign.css 主樣式檔案
- [x] 2.2 定義 :root CSS 變數：顏色（墨色、赭石、朱砂、墨綠、奶油白）
- [x] 2.3 定義 :root CSS 變數：字體系統（serif, sans-serif, fallbacks）
- [x] 2.4 定義 :root CSS 變數：間距系統（8px baseline, space-1 到 space-4）
- [x] 2.5 定義 :root CSS 變數：動畫時長（fast, normal, slow）
- [x] 2.6 定義 :root CSS 變數：陰影深度（sm, md, lg with warm tones）
- [x] 2.7 添加備用字體堆疊（Microsoft JhengHei, system fonts）

## 3. 書法筆墨視覺主題實作

- [x] 3.1 建立水墨風格背景：添加裝飾性筆觸 SVG 或 CSS 元素
- [x] 3.2 實作暖色調漸層背景（赭石、朱砂、墨綠）
- [x] 3.3 確保背景透明度 < 0.3，不干擾內容可讀性
- [x] 3.4 建立傳統裝飾元素（header 上下的印章風格裝飾）
- [x] 3.5 使用 CSS 實作裝飾性書法筆觸效果
- [x] 3.6 確保裝飾元素使用主題配色且不遮擋功能性內容
- [x] 3.7 應用主題配色到所有 UI 元素（按鈕、卡片、文字）
- [x] 3.8 驗證所有元素都使用 CSS 變數而非硬編碼顏色
- [x] 3.9 測試字體載入：使用 font-display: swap
- [x] 3.10 測試字體降級：驗證 CDN 失敗時的備用字體顯示

## 4. 動畫樣式定義

- [x] 4.1 建立 frontend/styles/animations.css 動畫樣式檔案
- [x] 4.2 定義 @keyframes fade-in-up（淡入上移動畫）
- [x] 4.3 定義 @keyframes brush-stroke（毛筆書寫動畫）
- [x] 4.4 定義 @keyframes stamp-press（印章蓋下動畫）
- [x] 4.5 定義 @keyframes ink-spread（水墨渲染動畫）
- [x] 4.6 實作標題字元交錯動畫（使用 animation-delay 和 CSS 變數）
- [x] 4.7 添加 @media (prefers-reduced-motion) 支援（duration < 0.01ms）
- [x] 4.8 確保所有動畫使用 transform 和 opacity（GPU 加速）
- [x] 4.9 為互動元素添加 transition 定義（hover, focus states）
- [x] 4.10 測試動畫在目標瀏覽器的流暢度（60fps）

## 5. 粒子特效系統實作

- [x] 5.1 建立 frontend/js/modules/particle-system.js 模組檔案
- [x] 5.2 實作 ParticleSystem class 基礎結構（constructor, canvas, ctx）
- [x] 5.3 建立全螢幕 Canvas overlay（z-index, pointer-events: none）
- [x] 5.4 實作 requestAnimationFrame 渲染循環
- [x] 5.5 實作 Canvas 清除和重繪邏輯
- [x] 5.6 定義 Particle class 或物件結構（position, velocity, color, opacity, lifetime）
- [x] 5.7 實作物件池（Object Pool）：初始化 100 個預分配粒子
- [x] 5.8 實作粒子借用/歸還邏輯（從池中取用和回收）
- [x] 5.9 實作 emitFireworks() 方法：放射狀粒子，重力效果
- [x] 5.10 實作 emitInkDrops() 方法：飛濺效果，墨色粒子
- [x] 5.11 實作粒子物理模擬：速度、加速度、重力
- [x] 5.12 實作粒子淡出：opacity 隨時間減少
- [x] 5.13 實作粒子移除：opacity = 0 時從陣列移除
- [x] 5.14 實作最大粒子數量限制（300 個）
- [x] 5.15 實作可配置參數：color, velocity, count, lifetime
- [x] 5.16 添加 JSDoc 註解說明所有公開方法
- [x] 5.17 建立 frontend/styles/particles.css（Canvas 容器樣式）
- [x] 5.18 測試粒子效果在各瀏覽器的效能（FPS 監控）

## 6. 學習統計面板實作

- [x] 6.1 建立 frontend/js/modules/stats-tracker.js 模組檔案
- [x] 6.2 實作 StatsTracker class 基礎結構
- [x] 6.3 定義統計資料結構：totalWords, correctInputs, totalInputs, currentStreak, longestStreak
- [x] 6.4 實作 load() 方法：從 LocalStorage 讀取資料
- [x] 6.5 實作 save() 方法：寫入資料到 LocalStorage（key: 'zhuyin-practice-stats'）
- [x] 6.6 實作 getDefaultStats() 方法：回傳初始統計物件（全為 0）
- [x] 6.7 實作 recordCorrectInput() 方法：增加計數器、更新連擊
- [x] 6.8 實作 recordIncorrectInput() 方法：增加總輸入、重置連擊
- [x] 6.9 實作 incrementWordCount() 方法：完成字數 +1
- [x] 6.10 實作 getAccuracy() 方法：計算準確率百分比
- [x] 6.11 實作 reset() 方法：重置所有統計為 0
- [x] 6.12 添加 timestamp 欄位：lastPracticeDate, sessionStart
- [x] 6.13 建立 HTML 統計面板結構（在 index-redesign.html）
- [x] 6.14 建立 frontend/styles/stats-panel.css 樣式檔案
- [x] 6.15 使用 BEM 命名：.stats-panel, .stats-panel__item, .stats-panel__value
- [x] 6.16 添加統計圖示：📖 (words), ✨ (accuracy), 🔥 (streak)
- [x] 6.17 添加統計標籤：「已練習」、「準確率」、「連續正確」
- [x] 6.18 應用主題配色到統計面板
- [x] 6.19 實作統計數值的即時更新（DOM 操作）
- [x] 6.20 建立重置按鈕 UI 和確認對話框
- [x] 6.21 整合重置功能到 StatsTracker
- [x] 6.22 添加 JSDoc 註解說明所有公開方法

## 7. 動畫控制模組實作

- [x] 7.1 建立 frontend/js/modules/animations.js 模組檔案
- [x] 7.2 實作頁面載入動畫控制器（觸發標題字元交錯動畫）
- [x] 7.3 實作練習字書寫動畫控制（添加/移除 CSS class）
- [x] 7.4 實作進度條水墨渲染動畫（更新寬度 %，添加 transition）
- [x] 7.5 實作按鍵印章動畫觸發器（添加/移除 .stamp-press class）
- [x] 7.6 實作動畫序列管理（確保動畫按正確順序播放）
- [x] 7.7 添加 JSDoc 註解說明所有公開方法

## 8. 鍵盤顯示模組修改（印章風格）

- [x] 8.1 建立 frontend/styles/keyboard-redesign.css 樣式檔案
- [x] 8.2 更新 keyboard.js：添加印章風格 CSS class 應用邏輯
- [x] 8.3 實作印章視覺設計：圓角、暖色調陰影、邊框效果
- [x] 8.4 實作按鍵深度效果：box-shadow 使用暖色調（非純灰色）
- [x] 8.5 修改按鍵高亮樣式：墨色漸變（移除綠色 #4CAF50）
- [x] 8.6 實作高亮時的漸變背景（jade/rust 色調）
- [x] 8.7 實作按鍵文字顏色轉換（高亮時變為 cream/white）
- [x] 8.8 實作印章按下動畫：scale transform (1.0 → 1.05)
- [x] 8.9 實作陰影深度增加動畫（按下時）
- [x] 8.10 實作按鍵釋放動畫：回到預設狀態
- [x] 8.11 確保動畫時長 200-300ms，使用 ease-out timing
- [x] 8.12 測試按鍵視覺效果在各瀏覽器的一致性

## 9. 輸入驗證模組修改（整合特效和統計）

- [x] 9.1 修改 input-handler.js：匯入 ParticleSystem 和 StatsTracker
- [x] 9.2 初始化粒子系統實例和統計追蹤器實例
- [x] 9.3 修改正確輸入處理：呼叫 particleSystem.emitInkDrops()
- [x] 9.4 修改正確輸入處理：呼叫 statsTracker.recordCorrectInput()
- [x] 9.5 修改正確輸入處理：更新進度條視覺（計算百分比）
- [x] 9.6 修改錯誤輸入處理：呼叫 statsTracker.recordIncorrectInput()
- [x] 9.7 修改字完成處理：呼叫 particleSystem.emitFireworks()
- [x] 9.8 修改字完成處理：呼叫 statsTracker.incrementWordCount()
- [x] 9.9 實作進度條動畫：平滑填充（0.3-0.5s duration, ease-out）
- [x] 9.10 實作進度條重置：新字載入時淡出並重置為 0%
- [x] 9.11 實作進度條主題樣式：ink-gradient fill, jade/rust 色調
- [x] 9.12 測試所有整合功能的協同運作

## 10. 練習邏輯模組修改（統計整合）

- [x] 10.1 修改 practice.js：匯入 StatsTracker
- [x] 10.2 整合統計追蹤器到練習流程
- [x] 10.3 確保字完成時更新統計面板 UI
- [x] 10.4 實作統計數值的即時 DOM 更新
- [x] 10.5 測試統計資料的持久化（重新整理頁面後恢復）

## 11. HTML 結構更新

- [x] 11.1 更新 index-redesign.html：添加水墨背景裝飾元素
- [x] 11.2 添加筆觸 SVG 或 CSS 裝飾性元素（.ink-bg, .stroke）
- [x] 11.3 添加 Canvas 元素（#particles-canvas）
- [x] 11.4 更新 header 結構：添加裝飾線（.header-decoration）
- [x] 11.5 更新標題：使用 .title-char span 包裹每個字元（交錯動畫）
- [x] 11.6 更新練習區域：添加墨色飛濺裝飾（.ink-splash）
- [x] 11.7 添加進度條元素（.progress-bar, .progress-fill, .progress-ink）
- [x] 11.8 添加統計面板 HTML 結構（.stats-panel）
- [x] 11.9 添加統計項目（.stat-item × 3: words, accuracy, streak）
- [x] 11.10 添加鍵盤提示文字更新（包含煙火特效說明）
- [x] 11.11 添加 footer 詩意文字（「用心練習，字字生花」）
- [x] 11.12 驗證語意化 HTML 和無障礙屬性（ARIA labels）

## 12. JavaScript 主入口整合

- [x] 12.1 更新 main-redesign.js：匯入所有新模組
- [x] 12.2 初始化粒子系統（建立 Canvas，啟動渲染循環）
- [x] 12.3 初始化統計追蹤器（載入 LocalStorage 資料）
- [x] 12.4 初始化動畫控制器（觸發頁面載入動畫）
- [x] 12.5 整合現有模組：zhuyin-map, keyboard, practice, input-handler
- [x] 12.6 設定模組間的通訊和事件傳遞
- [x] 12.7 實作重置按鈕事件監聽（統計重置）
- [x] 12.8 實作確認對話框邏輯（重置前詢問）
- [x] 12.9 測試所有模組的初始化順序和依賴關係

## 13. 響應式設計調整

- [x] 13.1 添加 viewport meta tag（已存在，驗證設定）
- [x] 13.2 實作響應式鍵盤佈局（手機、平板、桌面）
- [x] 13.3 實作響應式統計面板（螢幕寬度 < 768px 時調整排列）
- [x] 13.4 實作響應式字體大小（使用 clamp() 或媒體查詢）
- [x] 13.5 測試在不同螢幕尺寸的顯示效果

## 14. 效能優化

- [x] 14.1 添加 will-change CSS 屬性到動畫元素
- [x] 14.2 驗證所有動畫使用 GPU 加速屬性（transform, opacity）
- [x] 14.3 實作粒子系統效能監控（FPS counter for testing）
- [x] 14.4 測試低端裝置效能，必要時降低粒子密度
- [x] 14.5 優化字體載入：使用 font-display: swap
- [x] 14.6 測試 LocalStorage 讀寫效能
- [x] 14.7 優化 Canvas 渲染：使用 off-screen canvas（如需要）
- [x] 14.8 實作效能降級策略（偵測 FPS < 30，減少粒子）

## 15. 瀏覽器相容性測試

- [x] 15.1 測試 Chrome 61+：所有功能正常運作
- [x] 15.2 測試 Firefox 60+：所有功能正常運作
- [x] 15.3 測試 Safari 11+：所有功能正常運作
- [x] 15.4 測試 CSS Grid 降級策略（@supports）
- [x] 15.5 測試 CSS 變數降級策略
- [x] 15.6 測試 Canvas API 可用性檢查
- [x] 15.7 測試 LocalStorage 可用性檢查和錯誤處理
- [x] 15.8 驗證 Google Fonts CDN 失敗時的備用字體顯示

## 16. 無障礙功能

- [x] 16.1 確保所有互動元素可用鍵盤導航（Tab, Enter）
- [x] 16.2 添加適當的 ARIA labels 到統計面板
- [x] 16.3 添加 alt text 到裝飾性圖示
- [x] 16.4 確保顏色對比度符合 WCAG AA 標準（文字 vs 背景）
- [x] 16.5 測試螢幕閱讀器相容性（NVDA/VoiceOver）
- [x] 16.6 確保 focus indicators 清晰可見
- [x] 16.7 實作 skip to content link（如需要）

## 17. 測試撰寫

- [x] 17.1 更新 frontend/test.html：添加新模組測試
- [x] 17.2 撰寫粒子系統單元測試（emitFireworks, emitInkDrops, 物件池）
- [x] 17.3 撰寫統計追蹤器單元測試（計數器、準確率計算、持久化）
- [x] 17.4 撰寫動畫控制器單元測試（動畫觸發、CSS class 管理）
- [x] 17.5 更新鍵盤模組測試（印章風格、主題色高亮）
- [x] 17.6 更新輸入處理器測試（特效觸發、統計整合）
- [x] 17.7 撰寫整合測試：完整使用者流程（載入 → 輸入 → 完成字 → 統計更新）
- [x] 17.8 驗證所有測試通過（frontend 單元測試）

## 18. 視覺品質檢查

- [x] 18.1 驗證所有顏色使用主題配色（無硬編碼顏色）
- [x] 18.2 驗證所有字體使用定義的字體變數
- [x] 18.3 檢查視覺一致性（間距、圓角、陰影）
- [x] 18.4 檢查動畫流暢度和時序（無卡頓、無閃爍）
- [x] 18.5 檢查粒子效果美觀性（顏色、軌跡、數量）
- [x] 18.6 檢查統計面板排版和對齊
- [x] 18.7 檢查按鍵印章效果的視覺品質
- [x] 18.8 檢查水墨背景和裝飾元素的美感

## 19. 文檔撰寫

- [x] 19.1 更新 README.md：新增重新設計版本說明
- [x] 19.2 撰寫新模組的 JSDoc 註解（已在各任務中完成）
- [x] 19.3 撰寫 CSS 註解：說明主題變數用途
- [x] 19.4 撰寫使用指南：如何在兩個版本間切換
- [x] 19.5 記錄已知問題和限制（如：僅限桌面優化）
- [x] 19.6 更新瀏覽器需求說明

## 20. 最終整合與驗收

- [x] 20.1 執行完整使用者流程測試：開啟頁面 → 練習 10 個字 → 檢查統計
- [x] 20.2 驗證所有 89 個規格場景都能通過
- [x] 20.3 執行效能基準測試：FPS、記憶體使用、載入時間
- [x] 20.4 比較原版和重新設計版本的差異
- [x] 20.5 確認所有檔案都已提交到 Git
- [x] 20.6 準備 demo 或截圖展示新設計
- [x] 20.7 準備向 main 分支合併的 Pull Request
