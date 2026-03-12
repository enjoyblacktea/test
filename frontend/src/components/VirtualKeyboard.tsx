import { keyToZhuyin } from '../utils/zhuyin-map';
import type { InputMethod } from '../hooks/useInputMethod';

// 注音 QWERTY 佈局（現有）
const ZHUYIN_LAYOUT = [
  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
  ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
  [' '],
];

// 小鶴雙拼鍵位對應（官方方案）
// initial = 聲母注音，final = 韻母注音（可為 null 表示無此功能）
// 若同一鍵同時是聲母鍵與韻母鍵，兩者均顯示
const XIAOHE_MAP: Record<string, { initial?: string; final?: string }> = {
  a: { final: 'ㄚ' },
  b: { initial: 'ㄅ', final: 'ㄧㄣ' },
  c: { initial: 'ㄘ', final: 'ㄠ' },
  d: { initial: 'ㄉ', final: 'ㄞ' },
  e: { initial: 'ㄍ', final: 'ㄜ' },
  f: { initial: 'ㄈ', final: 'ㄣ' },
  g: { initial: 'ㄍ', final: 'ㄥ' },
  h: { initial: 'ㄏ', final: 'ㄤ' },
  i: { initial: 'ㄔ', final: 'ㄧ' },
  j: { initial: 'ㄐ', final: 'ㄢ' },
  k: { initial: 'ㄎ', final: 'ㄧㄥ/ㄨㄞ' },
  l: { initial: 'ㄌ', final: 'ㄧㄤ/ㄨㄤ' },
  m: { initial: 'ㄇ', final: 'ㄧㄢ' },
  n: { initial: 'ㄋ', final: 'ㄧㄠ' },
  o: { final: 'ㄛ/ㄨㄛ' },
  p: { initial: 'ㄆ', final: 'ㄧㄝ' },
  q: { initial: 'ㄑ', final: 'ㄧㄡ' },
  r: { initial: 'ㄖ', final: 'ㄨㄢ' },
  s: { initial: 'ㄙ', final: 'ㄨㄥ/ㄩㄥ' },
  t: { initial: 'ㄊ', final: 'ㄩㄝ' },
  u: { initial: 'ㄕ', final: 'ㄨ' },
  v: { initial: 'ㄓ', final: 'ㄨㄟ' },
  w: { final: 'ㄟ' },
  x: { initial: 'ㄒ', final: 'ㄨㄚ/ㄧㄚ' },
  y: { final: 'ㄨㄣ' },
  z: { initial: 'ㄗ', final: 'ㄡ' },
};

const SHUANGPIN_LAYOUT = [
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
  ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
];

interface Props {
  activeKey?: string | null;
  layout?: InputMethod;
}

export function VirtualKeyboard({ activeKey, layout = 'zhuyin' }: Props) {
  if (layout === 'shuangpin') {
    return (
      <div className="keyboard keyboard-shuangpin">
        {SHUANGPIN_LAYOUT.map((row, i) => (
          <div key={i} className="keyboard-row">
            {row.map((key) => {
              const map = XIAOHE_MAP[key];
              // 顯示：聲母 / 韻母（若兩者都有則用 / 分隔）
              const parts: string[] = [];
              if (map?.initial) parts.push(map.initial);
              if (map?.final && map.final !== map?.initial) parts.push(map.final);
              const sublabel = parts.join('/');
              return (
                <div
                  key={key}
                  className={`key shuangpin-key${activeKey === key ? ' highlighted' : ''}`}
                  data-key={key}
                >
                  <span className="letter">{key.toUpperCase()}</span>
                  {sublabel && <span className="zhuyin sublabel">{sublabel}</span>}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="keyboard">
      {ZHUYIN_LAYOUT.map((row, i) => (
        <div key={i} className="keyboard-row">
          {row.map((key) => (
            <div
              key={key}
              className={`key${key === ' ' ? ' spacebar' : ''}${activeKey === key ? ' highlighted' : ''}`}
              data-key={key}
            >
              <span className="zhuyin">
                {key === ' ' ? 'ˉ' : keyToZhuyin[key] || ''}
              </span>
              <span className="letter">{key === ' ' ? 'Space' : key}</span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
