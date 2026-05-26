import { useEffect, useState } from 'react';
import clsx from 'clsx';
import { getChecklist, setChecklist } from '../../lib/brief';

const ITEMS = [
  'Scan US futures: ES, NQ, YM, RTY direction and magnitude',
  'Check overnight Asia close and where Europe is trading',
  '10Y yield and 2s10s curve, anything above 4 bps move?',
  'DXY direction, oil, gold for commodity tape',
  'VIX level and curve shape (front month vs M3)',
  "Today's economic data releases and timing",
  'Pre-market earnings reports and post-close from yesterday',
  'Top pre-market gainers and losers, identify catalysts',
  'Sector tape: which XL_ ETFs are leading and lagging',
  'Check own watchlist for overnight gaps',
];

export default function PreOpenChecklist() {
  const [checked, setChecked] = useState<Set<number>>(new Set());

  useEffect(() => {
    setChecked(getChecklist());
  }, []);

  const toggle = (i: number) => {
    const next = new Set(checked);
    if (next.has(i)) next.delete(i);
    else next.add(i);
    setChecked(next);
    setChecklist(next);
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-1">
        <div className="text-xs uppercase tracking-widest text-slate-500 dark:text-slate-400">
          Pre-Open Checklist
        </div>
        <div className="text-[10px] font-mono text-slate-400 dark:text-slate-500">
          {checked.size}/{ITEMS.length}
        </div>
      </div>
      <div className="text-[10px] text-slate-400 dark:text-slate-500">
        Tap to mark · resets daily at midnight ET
      </div>
      <ul className="space-y-1">
        {ITEMS.map((text, i) => {
          const on = checked.has(i);
          return (
            <li key={i}>
              <button
                onClick={() => toggle(i)}
                className={clsx(
                  'w-full text-left text-xs flex items-start gap-2 p-2 rounded transition',
                  on
                    ? 'bg-emerald-50 dark:bg-emerald-500/10 text-slate-400 dark:text-slate-500 line-through'
                    : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200',
                )}
              >
                <span className="font-mono text-[10px] text-slate-400 dark:text-slate-500 mt-0.5 shrink-0">
                  {String(i + 1).padStart(2, '0')}
                </span>
                <span className="flex-1 leading-snug">{text}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
