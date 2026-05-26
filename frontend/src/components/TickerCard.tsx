import clsx from 'clsx';
import type { TickerQuote } from '../types/api';
import { colorPct, fmtMcap, fmtPct, fmtPe, fmtPrice } from '../lib/format';

interface Props {
  t: TickerQuote;
  onClick: () => void;
}

export default function TickerCard({ t, onClick }: Props) {
  const pos = (t.change_pct ?? 0) >= 0;
  return (
    <button
      onClick={onClick}
      className={clsx(
        'text-left rounded-lg border bg-white dark:bg-slate-900/60 p-4 hover:bg-slate-50 dark:hover:bg-slate-900 transition w-full',
        pos
          ? 'border-emerald-500/40 hover:border-emerald-500/70 dark:border-emerald-500/20 dark:hover:border-emerald-500/50'
          : 'border-rose-500/40 hover:border-rose-500/70 dark:border-rose-500/20 dark:hover:border-rose-500/50',
      )}
    >
      <div className="flex items-baseline justify-between gap-2">
        <div className="min-w-0">
          <div className="font-semibold text-slate-900 dark:text-slate-100">{t.symbol}</div>
          <div className="text-xs text-slate-500 dark:text-slate-400 truncate" title={t.name}>
            {t.name}
          </div>
        </div>
        <div className="text-right">
          <div className="text-lg font-semibold">{fmtPrice(t.price)}</div>
          <div className={clsx('text-sm', colorPct(t.change_pct))}>
            {fmtPct(t.change_pct)}
          </div>
        </div>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
        <Cell label="Mcap" value={fmtMcap(t.market_cap)} />
        <Cell label="P/E" value={fmtPe(t.pe_ratio)} />
        <Cell label="YTD" value={fmtPct(t.ytd_pct)} valueClass={colorPct(t.ytd_pct)} />
        <Cell label="1Y" value={fmtPct(t.one_year_pct)} valueClass={colorPct(t.one_year_pct)} />
      </div>
      {t.error && <div className="mt-2 text-xs text-rose-600 dark:text-rose-400">⚠ {t.error}</div>}
    </button>
  );
}

function Cell({
  label,
  value,
  valueClass = '',
}: {
  label: string;
  value: string;
  valueClass?: string;
}) {
  return (
    <div className="flex justify-between">
      <span className="text-slate-500 dark:text-slate-500">{label}</span>
      <span className={`text-slate-800 dark:text-slate-200 ${valueClass}`}>{value}</span>
    </div>
  );
}
