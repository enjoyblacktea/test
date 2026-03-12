import { keyToZhuyin } from '../utils/zhuyin-map';

const KEYBOARD_LAYOUT = [
  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
  ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
  [' '],
];

interface Props {
  activeKey?: string | null;
}

export function VirtualKeyboard({ activeKey }: Props) {
  return (
    <div className="keyboard">
      {KEYBOARD_LAYOUT.map((row, i) => (
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
