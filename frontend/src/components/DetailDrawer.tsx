import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../lib/api';
import PriceChart from './PriceChart';
import RangeToggle from './RangeToggle';
import NewsItemRow from './NewsItem';
import { useActiveEcosystem, useEcosystem } from '../lib/ecosystem';
import {
  colorPct,
  fmtMargin,
  fmtMcap,
  fmtPct,
  fmtPe,
  fmtPrice,
  fmtRevenue,
} from '../lib/format';
import type { Range } from '../types/api';

interface Props {
  symbol: string;
  onClose: () => void;
}

export default function DetailDrawer({ symbol, onClose }: Props) {
  const { active } = useEcosystem();
  const eco = useActiveEcosystem();
  const [range, setRange] = useState<Range>('1M');

  const { data: detail } = useQuery({
    queryKey: ['ticker', symbol, active],
    queryFn: () => api.ticker(symbol, active),
  });
  const { data: hist } = useQuery({
    queryKey: ['history', symbol, range],
    queryFn: () => api.history(symbol, range),
  });
  const { data: news } = useQuery({
    queryKey: ['news', active, { ticker: symbol }],
    queryFn: () => api.news({ ecosystem: active, ticker: symbol }),
  });

  const categoryDesc = detail?.category
    ? (eco?.categories?.[detail.category] ?? null)
    : null;

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="flex-1 bg-black/60" onClick={onClose} />
      <div className="w-full md:w-[640px] bg-white dark:bg-slate-950 border-l border-slate-200 dark:border-slate-800 overflow-y-auto">
        <div className="sticky top-0 bg-white/95 dark:bg-slate-950/95 backdrop-blur border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex items-start justify-between">
          <div>
            <div className="text-xl font-semibold text-slate-900 dark:text-slate-100">{detail?.symbol ?? symbol}</div>
            <div className="text-sm text-slate-500 dark:text-slate-400">{detail?.name}</div>
            <div className="mt-1 flex items-baseline gap-3">
              <span className="text-2xl font-semibold">{fmtPrice(detail?.price)}</span>
              <span className={colorPct(detail?.change_pct)}>
                {fmtPct(detail?.change_pct)}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 text-3xl leading-none px-2"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div className="px-6 py-5 space-y-6">
          <div>
            <RangeToggle value={range} onChange={setRange} />
            <div className="mt-3 h-64">
              <PriceChart points={hist?.points ?? []} />
            </div>
          </div>

          {detail?.category && (
            <div className="text-xs text-slate-500 dark:text-slate-400">
              <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 mr-2">
                {detail.category}
              </span>
              {categoryDesc}
            </div>
          )}

          {detail?.role && (
            <div>
              <div className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">
                Role in {eco?.name ?? 'ecosystem'}
              </div>
              <p className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed">{detail.role}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-sm">
            <KV label="Sector" value={detail?.sector ?? '—'} />
            <KV label="Industry" value={detail?.industry ?? '—'} />
            <KV label="Market cap" value={fmtMcap(detail?.market_cap)} />
            <KV label="P/E" value={fmtPe(detail?.pe_ratio)} />
            <KV label="Revenue (TTM)" value={fmtRevenue(detail?.revenue)} />
            <KV label="Gross margin" value={fmtMargin(detail?.gross_margins)} />
            <KV label="Free cash flow" value={fmtRevenue(detail?.free_cashflow)} />
            <KV
              label="52W range"
              value={`${fmtPrice(detail?.fifty_two_week_low)} – ${fmtPrice(detail?.fifty_two_week_high)}`}
            />
          </div>

          {detail?.website && (
            <a
              href={detail.website}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-emerald-700 dark:text-emerald-400 hover:underline inline-block"
            >
              Visit website →
            </a>
          )}

          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
              Recent news
            </div>
            <div className="space-y-2">
              {(news?.items ?? []).slice(0, 8).map((n) => (
                <NewsItemRow key={n.id} item={n} />
              ))}
              {news?.warning && (
                <div className="text-xs text-amber-600 dark:text-amber-400">{news.warning}</div>
              )}
              {news && !news.warning && news.items.length === 0 && (
                <div className="text-xs text-slate-500 dark:text-slate-400">No recent headlines.</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function KV({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <div className="flex justify-between border-b border-slate-200 dark:border-slate-800/50 pb-1">
      <span className="text-slate-500 dark:text-slate-500">{label}</span>
      <span className="text-slate-200 dark:text-slate-200">{value ?? '—'}</span>
    </div>
  );
}
