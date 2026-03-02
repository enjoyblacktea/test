/**
 * Backend Authentication Module
 * Handles user authentication with backend API and JWT tokens
 * Replaces the frontend-only auth.js module
 */

import * as api from './api.js';

const API_BASE_URL = 'http://localhost:5000/api';
const USER_STORAGE_KEY = 'zhuyin-practice-user';

/**
 * Register a new user account
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} - {success: boolean, user: Object|null, error: string|null}
 */
export async function register(username, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
      return {
        success: true,
        user: data.user,
        error: null
      };
    } else {
      return {
        success: false,
        user: null,
        error: data.error || 'Registration failed'
      };
    }
  } catch (error) {
    console.error('Registration error:', error);
    return {
      success: false,
      user: null,
      error: 'Network error or server unavailable'
    };
  }
}

/**
 * Log in with username and password
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} - {success: boolean, user: Object|null, error: string|null}
 */
export async function login(username, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
      // Save tokens using api module
      api.saveTokens(data.access_token, data.refresh_token);

      // Save user info to localStorage
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(data.user));

      console.log('Login successful:', data.user.username);
      return {
        success: true,
        user: data.user,
        error: null
      };
    } else {
      return {
        success: false,
        user: null,
        error: data.error || 'Login failed'
      };
    }
  } catch (error) {
    console.error('Login error:', error);
    return {
      success: false,
      user: null,
      error: 'Network error or server unavailable'
    };
  }
}

/**
 * Log out the current user
 * Clears tokens and user info from localStorage and redirects to login
 */
export function logout() {
  // Clear tokens
  api.clearTokens();

  // Clear user info
  localStorage.removeItem(USER_STORAGE_KEY);

  console.log('Logged out');

  // Redirect to login page
  window.location.href = '/frontend/login.html';
}

/**
 * Check if user is authenticated
 * @returns {boolean} - True if user has valid tokens
 */
export function isAuthenticated() {
  const token = api.getToken();

  if (!token) {
    return false;
  }

  // Check if token is expired
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiryTime = payload.exp * 1000;
    return Date.now() < expiryTime;
  } catch (error) {
    console.error('Error checking token expiry:', error);
    return false;
  }
}

/**
 * Get current user info from localStorage
 * @returns {Object|null} - User object or null if not logged in
 */
export function getCurrentUser() {
  try {
    const userJson = localStorage.getItem(USER_STORAGE_KEY);
    if (!userJson) return null;
    return JSON.parse(userJson);
  } catch (error) {
    console.error('Error reading user from localStorage:', error);
    return null;
  }
}

/**
 * Require authentication - redirect to login if not authenticated
 * Call this at the start of pages that require authentication
 */
export function requireAuth() {
  if (!isAuthenticated()) {
    console.warn('Authentication required, redirecting to login');
    window.location.href = '/frontend/login.html';
  }
}
