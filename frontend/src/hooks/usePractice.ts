import { useState, useCallback, useRef } from 'react';
import type { WordResponse, KeystrokeEvent } from '../types';
import { isZhuyinKey } from '../utils/zhuyin-map';
import * as practiceApi from '../api/practice';
import type { InputMethod } from './useInputMethod';

export function usePractice() {
  const [word, setWord] = useState<WordResponse | null>(null);
  const [inputIndex, setInputIndex] = useState(0);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const inputMethodRef = useRef<InputMethod>('zhuyin');
  const keystrokesRef = useRef<KeystrokeEvent[]>([]);
  const startedAtRef = useRef<string>('');

  const loadWord = useCallback(async (inputMethod: InputMethod = 'zhuyin') => {
    inputMethodRef.current = inputMethod;
    const apiInputMethod = inputMethod === 'zhuyin' ? 'bopomofo' : 'shuangpin';
    const data = await practiceApi.getWord(apiInputMethod);
    setWord(data);
    setInputIndex(0);
    setIsCorrect(null);
    keystrokesRef.current = [];
    startedAtRef.current = new Date().toISOString();
  }, []);

  const checkInput = useCallback((key: string) => {
    if (!word || isCorrect !== null) return;

    // 雙拼模式：接受字母鍵；注音模式：僅接受注音鍵
    if (inputMethodRef.current === 'shuangpin') {
      if (!/^[a-z]$/.test(key)) return;
    } else {
      if (!isZhuyinKey(key)) return;
    }

    const expectedKey = word.keys[inputIndex];
    const correct = key === expectedKey;

    keystrokesRef.current.push({
      key,
      order: keystrokesRef.current.length,
      typed_at: new Date().toISOString(),
      is_correct: correct,
    });

    if (correct) {
      const nextIndex = inputIndex + 1;
      if (nextIndex >= word.keys.length) {
        completeAttempt(true);
      } else {
        setInputIndex(nextIndex);
      }
    } else {
      completeAttempt(false);
    }
  }, [word, inputIndex, isCorrect]);

  const completeAttempt = useCallback((correct: boolean) => {
    if (!word) return;
    setIsCorrect(correct);
    const endedAt = new Date().toISOString();
    practiceApi.recordAttempt({
      character_id: word.id,
      started_at: startedAtRef.current,
      ended_at: endedAt,
      is_correct: correct,
      keystrokes: [...keystrokesRef.current],
    });
    setTimeout(() => loadWord(inputMethodRef.current), 800);
  }, [word, loadWord]);

  return { word, inputIndex, isCorrect, loadWord, checkInput };
}
