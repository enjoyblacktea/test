import { useState, useCallback } from 'react';

export type InputMethod = 'zhuyin' | 'shuangpin';

const STORAGE_KEY = 'inputMethod';

function getInitialMethod(): InputMethod {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored === 'shuangpin' ? 'shuangpin' : 'zhuyin';
}

export function useInputMethod() {
  const [inputMethod, setInputMethodState] = useState<InputMethod>(getInitialMethod);

  const setInputMethod = useCallback((method: InputMethod) => {
    localStorage.setItem(STORAGE_KEY, method);
    setInputMethodState(method);
  }, []);

  return { inputMethod, setInputMethod };
}
