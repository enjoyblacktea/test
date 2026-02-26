/**
 * Authentication Module
 *
 * 提供簡單的前端認證功能，使用 LocalStorage 儲存登入狀態。
 *
 * ⚠️ 重要：這是教育用途的簡化實作，不適合生產環境使用。
 * - 帳號密碼明文儲存於前端程式碼
 * - LocalStorage 資料可被使用者手動修改
 * - 無後端驗證或安全性保護
 * - 無 session timeout（登入後永久有效直到手動登出）
 *
 * 🔮 未來增強建議：
 * - 使用 timestamp 實作 session 過期機制
 * - 整合後端 API 進行真實的身份驗證
 * - 使用 JWT 或 session token
 */

// 預配置帳號資訊（教育用途）
const CREDENTIALS = {
  username: 'user',
  password: '1234'
};

// LocalStorage 鍵名
const AUTH_STORAGE_KEY = 'zhuyin-practice-auth';

/**
 * 檢查使用者是否已登入
 *
 * 從 LocalStorage 讀取認證狀態並驗證。如果 LocalStorage 不可用或資料損壞，
 * 會安全地返回 false（視為未登入）。
 *
 * @returns {boolean} 如果已登入返回 true，否則返回 false
 * @example
 * // 檢查使用者是否已登入
 * if (checkAuth()) {
 *     console.log('User is logged in');
 *     showDashboard();
 * } else {
 *     showLoginScreen();
 * }
 */
export function checkAuth() {
  try {
    const authData = localStorage.getItem(AUTH_STORAGE_KEY);

    if (!authData) {
      return false;
    }

    const parsed = JSON.parse(authData);
    // 檢查 isLoggedIn 和 username 都存在（向後相容性：舊資料沒有 username 會被視為未登入）
    return parsed.isLoggedIn === true && parsed.username;

  } catch (error) {
    // LocalStorage 不可用或資料損壞，視為未登入
    console.warn('Failed to check auth status:', error);
    return false;
  }
}

/**
 * 執行登入驗證
 *
 * 驗證使用者提供的帳號密碼是否與預配置的憑證相符。驗證成功後會將認證狀態
 * 儲存到 LocalStorage，包含登入標記和時間戳記。帳號密碼驗證區分大小寫。
 *
 * ⚠️ 安全性限制：
 * - 帳號密碼比對在前端進行，無後端驗證
 * - LocalStorage 資料可被使用者手動修改
 * - 適合教育用途，不適合生產環境
 *
 * @param {string} username - 使用者名稱（預設為 'user'）
 * @param {string} password - 密碼（預設為 '1234'）
 * @returns {boolean} 如果帳密正確且成功儲存狀態返回 true，否則返回 false
 * @example
 * // 嘗試登入
 * const success = login('user', '1234');
 * if (success) {
 *     console.log('Login successful');
 * } else {
 *     console.log('Invalid credentials');
 * }
 */
export function login(username, password) {
  // 驗證帳號密碼（完全比對，區分大小寫）
  if (username === CREDENTIALS.username && password === CREDENTIALS.password) {
    try {
      // 儲存認證狀態到 LocalStorage（包含 username 以便歷史記錄使用）
      const authData = {
        isLoggedIn: true,
        username: username,  // 儲存 username 用於練習歷史記錄
        timestamp: Date.now()  // 記錄登入時間（未來可用於實作 session 過期）
      };

      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(authData));
      return true;

    } catch (error) {
      // LocalStorage 寫入失敗
      console.error('Failed to save auth state:', error);
      return false;
    }
  }

  return false;
}

/**
 * 登出並清除認證狀態
 *
 * 從 LocalStorage 移除認證資料，使用者需要重新登入才能存取應用程式。
 * 如果 LocalStorage 操作失敗會記錄錯誤但不會拋出例外。
 *
 * @example
 * // 使用者點擊登出按鈕
 * logout();
 * showLoginScreen();
 */
export function logout() {
  try {
    localStorage.removeItem(AUTH_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear auth state:', error);
  }
}

/**
 * 取得當前登入的使用者名稱
 *
 * 從 LocalStorage 讀取已登入使用者的 username。用於歷史記錄 API 呼叫。
 * 如果使用者未登入或資料損壞，返回 null。
 *
 * @returns {string|null} 使用者名稱，如果未登入或讀取失敗返回 null
 * @example
 * // 取得當前使用者名稱用於記錄練習歷史
 * const username = getCurrentUsername();
 * if (username) {
 *     recordPractice({ username, word: '你', isCorrect: true, ... });
 * } else {
 *     console.warn('User not logged in, cannot record history');
 * }
 */
export function getCurrentUsername() {
  try {
    const authData = localStorage.getItem(AUTH_STORAGE_KEY);

    if (!authData) {
      return null;
    }

    const parsed = JSON.parse(authData);

    // 確認使用者已登入且有 username
    if (parsed.isLoggedIn && parsed.username) {
      return parsed.username;
    }

    return null;

  } catch (error) {
    // LocalStorage 不可用或 JSON 解析失敗
    console.warn('Failed to get current username:', error);
    return null;
  }
}
