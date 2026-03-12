import { useState, useCallback } from 'react';
import { fetchTodayGoal, setGoal as apiSetGoal } from '../api/goals';

export function useGoal() {
  const [dailyTarget, setDailyTarget] = useState<number | null>(null);
  const [completedToday, setCompletedToday] = useState(0);

  const loadGoal = useCallback(async () => {
    const data = await fetchTodayGoal();
    setDailyTarget(data.daily_target);
    setCompletedToday(data.completed_today);
  }, []);

  const updateGoal = useCallback(async (target: number) => {
    await apiSetGoal(target);
    setDailyTarget(target);
  }, []);

  const incrementCompleted = useCallback(() => {
    setCompletedToday((n) => n + 1);
  }, []);

  return { dailyTarget, completedToday, loadGoal, updateGoal, incrementCompleted };
}
