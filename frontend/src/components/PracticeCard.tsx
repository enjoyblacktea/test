import { ProgressBar } from './ProgressBar';
import type { InputMethod } from '../hooks/useInputMethod';

interface Props {
  character: string;
  zhuyin: string[];
  inputIndex: number;
  isCorrect: boolean | null;
  inputMethod?: InputMethod;
}

export function PracticeCard({ character, zhuyin, inputIndex, isCorrect }: Props) {
  const statusClass = isCorrect === true ? 'correct' : isCorrect === false ? 'incorrect' : '';

  return (
    <div className={`practice-card ${statusClass}`}>
      <div className="character-display">{character}</div>
      <div className="zhuyin-display">
        {zhuyin.map((sym, i) => (
          <span
            key={i}
            className={`zhuyin-sym${i < inputIndex ? ' typed' : i === inputIndex ? ' current' : ''}`}
          >
            {sym || 'ˉ'}
          </span>
        ))}
      </div>
      <ProgressBar current={inputIndex} total={zhuyin.length} />
    </div>
  );
}
