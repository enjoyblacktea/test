## Why

目前的前端界面過於簡單，使用通用的紫色漸層背景和基本的白色卡片設計，缺乏文化特色和視覺吸引力。作為一個教育類應用，需要更有趣味性和美感的界面來提升學習體驗，讓使用者在練習注音輸入時感受到傳統文化與現代設計的結合。

## What Changes

- 引入**筆墨童趣美學**：結合傳統書法筆觸、水墨漸層與現代互動設計
- 新增**動畫效果系統**：毛筆書寫動畫、墨滴飛濺、鍵盤按下如蓋印章
- 實作**粒子特效系統**：正確輸入時的煙火慶祝效果、水墨渲染動畫
- 新增**學習統計面板**：即時顯示已練習字數、準確率、連續正確次數
- 優化**字體和排版**：使用優雅的宋體/明體，搭配圓潤黑體，提升可讀性
- 改進**色彩設計**：採用暖色調水墨漸層（赭石、朱砂、墨綠）取代通用漸層
- 增強**視覺層次**：添加裝飾性筆觸背景、漸層陰影、進度條水墨渲染效果

## Capabilities

### New Capabilities

- `calligraphy-visual-theme`: 書法筆墨視覺主題設計
  - 水墨風格背景（筆觸、漸層、飛濺效果）
  - 傳統裝飾元素（印章風格、書法筆觸）
  - 暖色調配色方案（赭石、朱砂、墨綠、奶油白）
  - 中文字體系統（宋體、明體、黑體）

- `animated-ui-interactions`: 動畫化界面互動
  - 頁面載入時的交錯顯示動畫（staggered reveals）
  - 標題字元逐字浮現動畫
  - 練習字的毛筆書寫動畫效果
  - 鍵盤按鍵的印章蓋下效果
  - 進度條的水墨渲染動畫

- `particle-effects-system`: 粒子特效系統
  - Canvas 粒子渲染引擎
  - 正確輸入時的煙火慶祝效果
  - 墨滴飛濺粒子動畫
  - 可配置的粒子參數（顏色、速度、數量）

- `learning-stats-panel`: 學習統計面板
  - 即時統計追蹤（已練習字數、準確率、連續正確次數）
  - 統計資料視覺化顯示
  - 本地儲存統計資料（LocalStorage）
  - 統計資料重置功能

### Modified Capabilities

- `zhuyin-keyboard-display`: 更新視覺樣式以符合書法主題
  - 需求變更：鍵盤按鍵採用印章風格設計
  - 需求變更：按鍵高亮效果改為墨色漸變而非單純綠色
  - 需求變更：添加毛筆觸感的視覺反饋

- `zhuyin-input-validation`: 添加視覺反饋
  - 需求變更：正確輸入時觸發粒子特效
  - 需求變更：更新統計面板資料
  - 需求變更：進度條視覺更新

## Impact

**新增檔案**：
- `frontend/index-redesign.html` - 重新設計的主頁面（或覆蓋 index.html）
- `frontend/styles/redesign.css` - 新的主樣式檔案（筆墨主題）
- `frontend/styles/animations.css` - 動畫樣式定義
- `frontend/styles/particles.css` - 粒子效果樣式
- `frontend/js/modules/particle-system.js` - 粒子系統實作
- `frontend/js/modules/stats-tracker.js` - 統計追蹤模組
- `frontend/js/modules/animations.js` - 動畫控制模組
- `frontend/js/main-redesign.js` - 重新設計版本的主入口（或覆蓋 main.js）

**修改檔案**：
- `frontend/js/modules/keyboard.js` - 更新按鍵視覺樣式和動畫
- `frontend/js/modules/input-handler.js` - 添加粒子特效觸發和統計更新
- `frontend/js/modules/practice.js` - 整合統計追蹤

**新增依賴**：
- Google Fonts (Noto Serif TC, Noto Sans TC) - 繁體中文字體
- 可能需要輕量級動畫函式庫（或使用純 CSS/Vanilla JS）
- Canvas API - 粒子系統渲染

**影響的使用者體驗**：
- 視覺風格完全改變，從通用設計變為文化特色設計
- 添加動畫可能影響低效能裝置的流暢度（需要效能優化）
- 新增統計功能提供額外的學習動機
- 載入時間可能因新字體和資源而略微增加

**瀏覽器相容性**：
- 需要支援 CSS 動畫和轉場
- 需要支援 Canvas API（粒子效果）
- 需要支援 LocalStorage（統計資料）
- 維持現有的瀏覽器需求（Chrome 61+、Firefox 60+、Safari 11+）
