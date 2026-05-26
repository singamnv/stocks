import clsx from 'clsx';
import type { Range } from '../types/api';

const RANGES: Range[] = ['1D', '1W', '1M', '1Y', '5Y'];

interface Props {
  value: Range;
  onChange: (r: Range) => void;
}

export default function RangeToggle({ value, onChange }: Props) {
  return (
    <div className="inline-flex rounded-lg bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-1">
      {RANGES.map((r) => (
        <button
          key={r}
          onClick={() => onChange(r)}
          className={clsx(
            'px-3 py-1 text-xs rounded-md transition',
            value === r
              ? 'bg-white text-slate-900 shadow-sm dark:bg-slate-700 dark:text-white'
              : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200',
          )}
        >
          {r}
        </button>
      ))}
    </div>
  );
}
