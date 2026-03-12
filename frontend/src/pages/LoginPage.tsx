import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export function LoginPage() {
  const { login, register } = useAuth();
  const [tab, setTab] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (tab === 'login') {
        await login(username, password);
      } else {
        await register(username, password);
      }
    } catch {
      setError(tab === 'login' ? '帳號或密碼錯誤' : '註冊失敗，請換個帳號');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">注音練習</h1>
        <div className="login-tabs">
          <button
            className={`tab-btn${tab === 'login' ? ' active' : ''}`}
            onClick={() => setTab('login')}
          >
            登入
          </button>
          <button
            className={`tab-btn${tab === 'register' ? ' active' : ''}`}
            onClick={() => setTab('register')}
          >
            註冊
          </button>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            className="login-input"
            type="text"
            placeholder="帳號"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            className="login-input"
            type="password"
            placeholder="密碼"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="login-error">{error}</p>}
          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? '處理中...' : tab === 'login' ? '登入' : '註冊'}
          </button>
        </form>
      </div>
    </div>
  );
}
