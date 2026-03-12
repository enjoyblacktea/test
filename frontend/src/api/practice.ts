import client from './client';
import type { WordResponse, AttemptRequest, AttemptResponse } from '../types';

export async function getWord(): Promise<WordResponse> {
  const { data } = await client.get<WordResponse>('/words/random');
  return data;
}

export async function recordAttempt(attempt: AttemptRequest): Promise<void> {
  await client.post<AttemptResponse>('/attempts', attempt);
}
