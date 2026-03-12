import { useEffect, useRef, useState } from 'react';
import { PracticeCard } from '../components/PracticeCard';
import { VirtualKeyboard } from '../components/VirtualKeyboard';
import { usePractice } from '../hooks/usePractice';
import { useKeyboard } from '../hooks/useKeyboard';
import { useGoal } from '../hooks/useGoal';
import { useAuth } from '../contexts/AuthContext';

export function PracticePage() {
  const { word, inputIndex, isCorrect, loadWord, checkInput } = usePractice();
  const { logout, user } = useAuth();
  const { dailyTarget, completedToday, loadGoal, updateGoal, incrementCompleted } = useGoal();
  const [activeKey, setActiveKey] = useState<string | null>(null);
  const [goalInput, setGoalInput] = useState('');
  const [showGoalForm, setShowGoalForm] = useState(false);
  const prevIsCorrect = useRef<boolean | null>(null);

  useEffect(() => { loadWord(); }, [loadWord]);
  useEffect(() => { loadGoal(); }, [loadGoal]);

  // 每次 isCorrect 從 null 變為有值，代表完成一次嘗試
  useEffect(() => {
    if (isCorrect !== null && prevIsCorrect.current === null) {
      incrementCompleted();
    }
    prevIsCorrect.current = isCorrect;
  }, [isCorrect, incrementCompleted]);

  useKeyboard((key) => {
    setActiveKey(key);
    checkInput(key);
    setTimeout(() => setActiveKey(null), 150);
  });

  const handleSetGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    const target = parseInt(goalInput, 10);
    if (!target || target < 1) return;
    await updateGoal(target);
    setGoalInput('');
    setShowGoalForm(false);
  };

  const progressText = dailyTarget === null
    ? '尚未設定目標'
    : `${completedToday} / ${dailyTarget} 題`;

  return (
    <div className="practice-container">
      <header className="practice-header">
        <span className="user-info">{user?.username}</span>
        <div className="goal-area">
          <span className="goal-progress">{progressText}</span>
          <button className="goal-btn" onClick={() => setShowGoalForm((v) => !v)}>
            設定目標
          </button>
        </div>
        <button className="logout-btn" onClick={logout}>登出</button>
      </header>
      {showGoalForm && (
        <form className="goal-form" onSubmit={handleSetGoal}>
          <input
            type="number"
            min={1}
            placeholder="每日目標題數"
            value={goalInput}
            onChange={(e) => setGoalInput(e.target.value)}
            className="goal-input"
          />
          <button type="submit" className="goal-submit-btn">確認</button>
        </form>
      )}
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
