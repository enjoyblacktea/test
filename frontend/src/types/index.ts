export interface User {
  id: number;
  username: string;
  created_at: string;
}

export interface WordResponse {
  id: number;
  word: string;
  zhuyin: string[];
  keys: string[];
}

export interface KeystrokeEvent {
  key: string;
  order: number;
  typed_at: string;
  is_correct: boolean;
}

export interface AttemptRequest {
  character_id: number;
  started_at: string;
  ended_at: string;
  is_correct: boolean;
  keystrokes?: KeystrokeEvent[];
}

export interface AttemptResponse {
  message: string;
  attempt_id: number | null;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface AccessTokenResponse {
  access_token: string;
}

export interface ApiError {
  status: number;
  message: string;
}
