import { useEffect } from 'react';

export function useKeyboard(onKey: (key: string) => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Prevent default for zhuyin keys to avoid browser shortcuts
      const key = e.key === ' ' ? ' ' : e.key;
      onKey(key);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onKey]);
}
