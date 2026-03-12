import { useState, useCallback, useRef } from 'react';
import type { WordResponse, KeystrokeEvent } from '../types';
import { isZhuyinKey } from '../utils/zhuyin-map';
import * as practiceApi from '../api/practice';

export function usePractice() {
  const [word, setWord] = useState<WordResponse | null>(null);
  const [inputIndex, setInputIndex] = useState(0);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const keystrokesRef = useRef<KeystrokeEvent[]>([]);
  const startedAtRef = useRef<string>('');

  const loadWord = useCallback(async () => {
    const data = await practiceApi.getWord();
    setWord(data);
    setInputIndex(0);
    setIsCorrect(null);
    keystrokesRef.current = [];
    startedAtRef.current = new Date().toISOString();
  }, []);

  const checkInput = useCallback((key: string) => {
    if (!word || isCorrect !== null) return;
    if (!isZhuyinKey(key)) return;

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
        // Attempt complete - correct
        completeAttempt(true);
      } else {
        setInputIndex(nextIndex);
      }
    } else {
      // Wrong key - mark incorrect and complete
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
    // Auto-load next word after short delay
    setTimeout(() => loadWord(), 800);
  }, [word, loadWord]);

  return { word, inputIndex, isCorrect, loadWord, checkInput };
}
