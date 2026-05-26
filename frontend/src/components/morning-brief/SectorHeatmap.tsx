import { useQuery } from '@tanstack/react-query';
import { api } from '../../lib/api';

function tileBg(pct: number | null): string {
  if (pct == null) return 'bg-slate-100 dark:bg-slate-800';
  const mag = Math.min(Math.abs(pct), 3) / 3;
  if (pct >= 0) {
    if (mag > 0.66) return 'bg-emerald-500/70 dark:bg-emerald-500/60';
    if (mag > 0.33) return 'bg-emerald-500/40 dark:bg-emerald-500/30';
    return 'bg-emerald-500/20 dark:bg-emerald-500/15';
  }
  if (mag > 0.66) return 'bg-rose-500/70 dark:bg-rose-500/60';
  if (mag > 0.33) return 'bg-rose-500/40 dark:bg-rose-500/30';
  return 'bg-rose-500/20 dark:bg-rose-500/15';
}

export default function SectorHeatmap() {
  const { data } = useQuery({ queryKey: ['brief'], queryFn: api.brief, refetchInterval: 60_000 });
  const rows = data?.sectors ?? [];

  return (
    <div className="space-y-2">
      <div className="text-xs uppercase tracking-widest text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 pb-1">
        Sector Heatmap
      </div>
      <div className="text-[10px] text-slate-400 dark:text-slate-500">S&amp;P 500 by sector</div>
      <div className="grid grid-cols-3 gap-1">
        {rows.map((s) => (
          <div
            key={s.symbol}
            className={`rounded p-2 ${tileBg(s.change_pct)}`}
            title={s.name}
          >
            <div className="font-mono text-xs font-semibold text-slate-900 dark:text-slate-100">
              {s.symbol}
            </div>
            <div className="font-mono text-[11px] text-slate-700 dark:text-slate-200">
              {s.change_pct != null
                ? `${s.change_pct >= 0 ? '+' : ''}${s.change_pct.toFixed(2)}%`
                : '—'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
