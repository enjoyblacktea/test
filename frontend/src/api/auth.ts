import client from './client';
import type { TokenResponse } from '../types';

export async function login(username: string, password: string): Promise<TokenResponse> {
  const { data } = await client.post<TokenResponse>('/auth/login', { username, password });
  return data;
}

export async function register(username: string, password: string) {
  const { data } = await client.post('/auth/register', { username, password });
  return data;
}
