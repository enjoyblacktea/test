import client from './client';

export interface TodayGoal {
  daily_target: number | null;
  completed_today: number;
}

export async function fetchTodayGoal(): Promise<TodayGoal> {
  const { data } = await client.get<TodayGoal>('/goals/today');
  return data;
}

export async function setGoal(daily_target: number): Promise<void> {
  await client.post('/goals', { daily_target });
}
