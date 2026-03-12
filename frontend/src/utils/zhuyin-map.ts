export const keyToZhuyin: Record<string, string> = {
  '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
  '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
  'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
  'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
  '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
  'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
  'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
  '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
  '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
  '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
  '-': 'ㄦ',
  // 聲調：空白鍵 = 一聲（以 ˉ 顯示），其他聲調
  ' ': 'ˉ', '6': 'ˊ', '3': 'ˇ', '4': 'ˋ', '7': '˙',
};

export const zhuyinToKey: Record<string, string> = Object.fromEntries(
  Object.entries(keyToZhuyin).filter(([, v]) => v).map(([k, v]) => [v, k])
);

export function isZhuyinKey(key: string): boolean {
  return key in keyToZhuyin;
}

export function getZhuyin(key: string): string | null {
  return keyToZhuyin[key] ?? null;
}

export function getKey(zhuyin: string): string | null {
  return zhuyinToKey[zhuyin] ?? null;
}
