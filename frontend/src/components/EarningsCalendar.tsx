import { useQuery } from '@tanstack/react-query';
import clsx from 'clsx';
import { api } from '../lib/api';
import { useEcosystem } from '../lib/ecosystem';
import { fmtDate, fmtRevenue } from '../lib/format';
import type { EarningsItem } from '../types/api';

export default function EarningsCalendar() {
  const { active } = useEcosystem();
  const { data, isLoading } = useQuery({
    queryKey: ['earnings', active],
    queryFn: () => api.earnings(active),
  });

  if (isLoading) return <div className="text-slate-500 dark:text-slate-400">Loading earnings…</div>;
  if (data?.warning)
    return <div className="text-amber-600 dark:text-amber-400 text-sm">⚠ {data.warning}</div>;

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const weekEnd = new Date(today);
  weekEnd.setDate(today.getDate() + 7);

  const byDate = new Map<string, EarningsItem[]>();
  for (const it of data?.items ?? []) {
    if (!it.date) continue;
    if (!byDate.has(it.date)) byDate.set(it.date, []);
    byDate.get(it.date)!.push(it);
  }
  const dates = Array.from(byDate.keys()).sort();

  if (dates.length === 0)
    return (
      <div className="text-slate-500 dark:text-slate-400 text-sm">No upcoming earnings in window.</div>
    );

  return (
    <div className="space-y-4">
      {dates.map((d) => {
        const dDate = new Date(`${d}T00:00:00`);
        const isThisWeek = dDate >= today && dDate <= weekEnd;
        return (
          <div
            key={d}
            className={clsx(
              'rounded-lg border p-4',
              isThisWeek
                ? 'border-amber-500/40 bg-amber-50 dark:bg-amber-500/5'
                : 'border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900/40',
            )}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="font-semibold text-slate-900 dark:text-slate-100">{fmtDate(d)}</div>
              {isThisWeek && (
                <span className="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-800 dark:text-amber-300">
                  This week
                </span>
              )}
            </div>
            <div className="space-y-2">
              {byDate.get(d)!.map((it) => (
                <Row key={`${it.date}-${it.ticker}`} it={it} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function Row({ it }: { it: EarningsItem }) {
  return (
    <div className="grid grid-cols-12 gap-2 text-sm items-baseline">
      <div className="col-span-3 sm:col-span-2 font-medium text-slate-900 dark:text-slate-100">{it.ticker}</div>
      <div className="col-span-5 text-slate-500 dark:text-slate-400 truncate">{it.name}</div>
      <div className="col-span-1 text-xs text-slate-500 dark:text-slate-500 uppercase">
        {it.hour ?? ''}
      </div>
      <div className="col-span-2 text-right text-slate-800 dark:text-slate-200">
        {it.eps_estimate != null ? it.eps_estimate.toFixed(2) : '—'}
      </div>
      <div className="col-span-1 sm:col-span-2 text-right text-slate-800 dark:text-slate-200">
        {fmtRevenue(it.revenue_estimate)}
      </div>
    </div>
  );
}
