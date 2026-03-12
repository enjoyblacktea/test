import { useEffect, useState } from 'react';
import { PracticeCard } from '../components/PracticeCard';
import { VirtualKeyboard } from '../components/VirtualKeyboard';
import { usePractice } from '../hooks/usePractice';
import { useKeyboard } from '../hooks/useKeyboard';
import { useAuth } from '../contexts/AuthContext';

export function PracticePage() {
  const { word, inputIndex, isCorrect, loadWord, checkInput } = usePractice();
  const { logout, user } = useAuth();
  const [activeKey, setActiveKey] = useState<string | null>(null);

  useEffect(() => { loadWord(); }, [loadWord]);

  useKeyboard((key) => {
    setActiveKey(key);
    checkInput(key);
    setTimeout(() => setActiveKey(null), 150);
  });

  return (
    <div className="practice-container">
      <header className="practice-header">
        <span className="user-info">{user?.username}</span>
        <button className="logout-btn" onClick={logout}>登出</button>
      </header>
      <main className="practice-main">
        {word ? (
          <PracticeCard
            character={word.word}
            zhuyin={word.zhuyin}
            inputIndex={inputIndex}
            isCorrect={isCorrect}
          />
        ) : (
          <div className="loading">載入中...</div>
        )}
      </main>
      <VirtualKeyboard activeKey={activeKey} />
    </div>
  );
}
