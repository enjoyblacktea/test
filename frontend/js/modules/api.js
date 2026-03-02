/**
 * API Client Module
 * Centralized API wrapper with JWT token management
 */

const API_BASE_URL = 'http://localhost:5000/api';
const TOKEN_STORAGE_KEY = 'zhuyin-practice-tokens';

/**
 * Get tokens from localStorage
 * @returns {Object|null} - {access_token, refresh_token} or null
 */
export function getTokens() {
  try {
    const tokensJson = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!tokensJson) return null;
    return JSON.parse(tokensJson);
  } catch (error) {
    console.error('Error reading tokens from localStorage:', error);
    return null;
  }
}

/**
 * Get access token from localStorage
 * @returns {string|null} - Access token or null
 */
export function getToken() {
  const tokens = getTokens();
  return tokens ? tokens.access_token : null;
}

/**
 * Save tokens to localStorage
 * @param {string} accessToken - JWT access token
 * @param {string} refreshToken - JWT refresh token
 */
export function saveTokens(accessToken, refreshToken) {
  const tokens = {
    access_token: accessToken,
    refresh_token: refreshToken
  };
  localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokens));
}

/**
 * Clear tokens from localStorage (logout)
 */
export function clearTokens() {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
}

/**
 * Check if access token is expired
 * @param {string} token - JWT token
 * @returns {boolean} - True if expired
 */
function isTokenExpired(token) {
  if (!token) return true;

  try {
    // Decode JWT payload (base64)
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiryTime = payload.exp * 1000; // Convert to milliseconds
    return Date.now() >= expiryTime;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true;
  }
}

/**
 * Refresh access token using refresh token
 * @returns {Promise<string|null>} - New access token or null if failed
 */
async function refreshAccessToken() {
  const tokens = getTokens();
  if (!tokens || !tokens.refresh_token) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        refresh_token: tokens.refresh_token
      })
    });

    if (response.ok) {
      const data = await response.json();
      // Update access token (keep same refresh token)
      saveTokens(data.access_token, tokens.refresh_token);
      return data.access_token;
    } else {
      // Refresh token expired or invalid - clear tokens
      clearTokens();
      return null;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    return null;
  }
}

/**
 * Authenticated fetch wrapper that automatically adds Authorization header
 * and handles token refresh on 401 errors
 * @param {string} url - API endpoint URL (relative to API_BASE_URL)
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} - Fetch response
 */
export async function authFetch(url, options = {}) {
  // Get access token
  let accessToken = getToken();

  // Check if token is expired and refresh if needed
  if (accessToken && isTokenExpired(accessToken)) {
    console.log('Access token expired, refreshing...');
    accessToken = await refreshAccessToken();

    if (!accessToken) {
      // Redirect to login if refresh failed
      console.warn('Token refresh failed, redirecting to login');
      window.location.href = '/frontend/login.html';
      throw new Error('Authentication required');
    }
  }

  // Add Authorization header
  const headers = {
    ...options.headers,
  };

  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`;
  }

  // Make request
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers
  });

  // Handle 401 Unauthorized - try to refresh token once
  if (response.status === 401) {
    console.log('Received 401, attempting token refresh');
    accessToken = await refreshAccessToken();

    if (!accessToken) {
      // Redirect to login if refresh failed
      console.warn('Token refresh failed, redirecting to login');
      window.location.href = '/frontend/login.html';
      throw new Error('Authentication required');
    }

    // Retry request with new token
    headers['Authorization'] = `Bearer ${accessToken}`;
    return fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers
    });
  }

  return response;
}

/**
 * Convenience method for GET requests
 * @param {string} url - API endpoint URL
 * @returns {Promise<any>} - Parsed JSON response
 */
export async function apiGet(url) {
  const response = await authFetch(url, {
    method: 'GET'
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Convenience method for POST requests
 * @param {string} url - API endpoint URL
 * @param {Object} data - Request body data
 * @returns {Promise<any>} - Parsed JSON response
 */
export async function apiPost(url, data) {
  const response = await authFetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Convenience method for PUT requests
 * @param {string} url - API endpoint URL
 * @param {Object} data - Request body data
 * @returns {Promise<any>} - Parsed JSON response
 */
export async function apiPut(url, data) {
  const response = await authFetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Convenience method for DELETE requests
 * @param {string} url - API endpoint URL
 * @returns {Promise<any>} - Parsed JSON response
 */
export async function apiDelete(url) {
  const response = await authFetch(url, {
    method: 'DELETE'
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}
