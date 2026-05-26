import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import clsx from 'clsx';
import { api } from '../../lib/api';
import { colorPct, fmtPct, fmtPrice } from '../../lib/format';

type Region = 'asia' | 'europe' | 'us';
const REGIONS: { value: Region; label: string }[] = [
  { value: 'asia', label: 'Asia' },
  { value: 'europe', label: 'Europe' },
  { value: 'us', label: 'US' },
];

export default function GlobalTape() {
  const [region, setRegion] = useState<Region>('us');
  const { data } = useQuery({ queryKey: ['brief'], queryFn: api.brief, refetchInterval: 60_000 });
  const rows = data?.tape[region] ?? [];

  return (
    <div className="space-y-2">
      <div className="text-xs uppercase tracking-widest text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 pb-1">
        Global Tape
      </div>
      <div className="flex gap-1">
        {REGIONS.map((r) => (
          <button
            key={r.value}
            onClick={() => setRegion(r.value)}
            className={clsx(
              'px-2 py-0.5 text-[10px] uppercase tracking-wider rounded transition',
              region === r.value
                ? 'bg-slate-900 text-white dark:bg-slate-700'
                : 'text-slate-500 hover:text-slate-900 dark:hover:text-slate-200',
            )}
          >
            {r.label}
          </button>
        ))}
      </div>
      <div className="space-y-0.5">
        {rows.map((r) => (
          <div key={r.symbol} className="flex items-baseline justify-between text-xs">
            <span className="text-slate-700 dark:text-slate-300">{r.name}</span>
            <span className="flex items-baseline gap-2">
              <span className="font-mono text-slate-900 dark:text-slate-100">{fmtPrice(r.price)}</span>
              <span className={`font-mono w-14 text-right ${colorPct(r.change_pct)}`}>
                {fmtPct(r.change_pct)}
              </span>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
