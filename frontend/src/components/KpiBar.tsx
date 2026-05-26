import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import clsx from 'clsx';
import { api } from '../lib/api';
import { colorPct, fmtMcap, fmtPct, fmtPrice } from '../lib/format';
import { useActiveEcosystem, useEcosystem } from '../lib/ecosystem';
import ThemeToggle from './ThemeToggle';

interface Props {
  onToggleBrief: () => void;
}

export default function KpiBar({ onToggleBrief }: Props) {
  const { active } = useEcosystem();
  const eco = useActiveEcosystem();
  const qc = useQueryClient();
  const [refreshMsg, setRefreshMsg] = useState<string | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['kpis', active],
    queryFn: () => api.kpis(active),
    refetchInterval: 60_000,
  });

  const refresh = useMutation({
    mutationFn: () => api.refreshEcosystem(active),
    onSuccess: () => {
      setRefreshMsg(null);
      // Invalidate every per-ecosystem query so React Query re-fetches with the warm cache.
      qc.invalidateQueries({ queryKey: ['kpis', active] });
      qc.invalidateQueries({ queryKey: ['grid', active] });
      qc.invalidateQueries({ queryKey: ['news', active] });
      qc.invalidateQueries({ queryKey: ['earnings', active] });
      qc.invalidateQueries({ queryKey: ['ticker'] });
    },
    onError: (e: Error) => {
      setRefreshMsg(e.message);
      setTimeout(() => setRefreshMsg(null), 4000);
    },
  });

  const anchorLabel = eco?.anchor_ticker ?? 'NVDA';
  const titleLabel = eco ? `${eco.name} Tracker` : 'NVIDIA Ecosystem Tracker';

  return (
    <div className="bg-gradient-to-b from-white to-slate-50 dark:from-slate-900 dark:to-slate-950 border-b border-slate-200 dark:border-slate-800">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between mb-3 gap-2">
          <div className="text-xs uppercase tracking-wider text-emerald-700 dark:text-emerald-400 min-w-0 truncate">
            {titleLabel}
          </div>
          <div className="flex items-center gap-2">
            {refreshMsg && (
              <span className="text-xs text-amber-600 dark:text-amber-400 hidden sm:inline">
                {refreshMsg}
              </span>
            )}
            <button
              onClick={() => refresh.mutate()}
              disabled={refresh.isPending}
              title={
                refresh.isPending
                  ? `Refreshing ${eco?.name ?? 'ecosystem'}…`
                  : `Refresh ${eco?.name ?? 'ecosystem'} data`
              }
              aria-label="Refresh ecosystem data"
              className="p-2 rounded-md text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 transition disabled:opacity-60"
            >
              <RefreshIcon spinning={refresh.isPending} />
            </button>
            <button
              onClick={onToggleBrief}
              className="px-3 py-1.5 text-xs rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-200 transition"
            >
              Morning Brief
            </button>
            <ThemeToggle />
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <Stat
            label={anchorLabel}
            value={isLoading ? '…' : fmtPrice(data?.nvda_price)}
            sub={isLoading ? '' : fmtPct(data?.nvda_change_pct)}
            subClass={colorPct(data?.nvda_change_pct)}
          />
          <Stat
            label="Ecosystem mcap"
            value={isLoading ? '…' : fmtMcap(data?.total_market_cap)}
          />
          <Stat
            label="Earnings this week"
            value={isLoading ? '…' : String(data?.earnings_this_week ?? 0)}
          />
          <Stat
            label="Avg daily perf"
            value={isLoading ? '…' : fmtPct(data?.avg_change_pct)}
            valueClass={colorPct(data?.avg_change_pct)}
          />
        </div>
      </div>
    </div>
  );
}

interface StatProps {
  label: string;
  value: string;
  sub?: string;
  valueClass?: string;
  subClass?: string;
}

function Stat({ label, value, sub, valueClass = '', subClass = '' }: StatProps) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">{label}</div>
      <div className={`text-2xl font-semibold text-slate-900 dark:text-slate-100 ${valueClass}`}>{value}</div>
      {sub && <div className={`text-sm ${subClass}`}>{sub}</div>}
    </div>
  );
}

function RefreshIcon({ spinning }: { spinning: boolean }) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden
      className={clsx('transition', spinning && 'animate-spin')}
    >
      <path
        d="M3 10a7 7 0 0 1 12-4.95M17 10a7 7 0 0 1-12 4.95M14 4v3h3M6 16v-3H3"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
