import { useMemo, useState } from 'react';
import clsx from 'clsx';
import type { GridResponse, TickerQuote } from '../types/api';
import { useActiveEcosystem } from '../lib/ecosystem';
import { colorPct, fmtMcap, fmtPct, fmtPe, fmtPrice } from '../lib/format';

type SortKey =
  | 'symbol' | 'name' | 'category' | 'price'
  | 'change_pct' | 'market_cap' | 'pe_ratio' | 'ytd_pct' | 'one_year_pct';

interface Props {
  data: GridResponse;
  onSelect: (s: string) => void;
}

export default function EcosystemTable({ data, onSelect }: Props) {
  const eco = useActiveEcosystem();
  const descs = eco?.categories ?? {};

  const [sort, setSort] = useState<{ key: SortKey; dir: 'asc' | 'desc' }>({
    key: 'category',
    dir: 'asc',
  });

  const rows = useMemo(() => {
    const all = data.groups.flatMap((g) => g.tickers);
    const sorted = [...all].sort((a, b) => compare(a, b, sort.key));
    return sort.dir === 'desc' ? sorted.reverse() : sorted;
  }, [data, sort]);

  const setKey = (k: SortKey) => {
    setSort((s) => (s.key === k ? { key: k, dir: s.dir === 'asc' ? 'desc' : 'asc' } : { key: k, dir: 'asc' }));
  };

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 dark:bg-slate-900 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
          <tr>
            <Th label="Ticker" k="symbol" sort={sort} onClick={setKey} />
            <Th label="Name" k="name" sort={sort} onClick={setKey} />
            <Th label="Category" k="category" sort={sort} onClick={setKey} />
            <Th label="Price" k="price" sort={sort} onClick={setKey} right />
            <Th label="%Chg" k="change_pct" sort={sort} onClick={setKey} right />
            <Th label="Mcap" k="market_cap" sort={sort} onClick={setKey} right />
            <Th label="P/E" k="pe_ratio" sort={sort} onClick={setKey} right />
            <Th label="YTD" k="ytd_pct" sort={sort} onClick={setKey} right />
            <Th label="1Y" k="one_year_pct" sort={sort} onClick={setKey} right />
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
          {rows.map((t) => (
            <tr
              key={t.symbol}
              onClick={() => onSelect(t.symbol)}
              className="hover:bg-slate-50 dark:hover:bg-slate-900/60 cursor-pointer"
            >
              <td className="px-3 py-2 font-semibold text-slate-900 dark:text-slate-100">{t.symbol}</td>
              <td className="px-3 py-2 text-slate-700 dark:text-slate-300 truncate max-w-[14rem]">{t.name}</td>
              <td className="px-3 py-2 text-xs text-slate-500 dark:text-slate-400" title={descs[t.category]}>
                {t.category}
              </td>
              <td className="px-3 py-2 text-right font-mono text-slate-800 dark:text-slate-200">{fmtPrice(t.price)}</td>
              <td className={`px-3 py-2 text-right font-mono ${colorPct(t.change_pct)}`}>{fmtPct(t.change_pct)}</td>
              <td className="px-3 py-2 text-right font-mono text-slate-800 dark:text-slate-200">{fmtMcap(t.market_cap)}</td>
              <td className="px-3 py-2 text-right font-mono text-slate-800 dark:text-slate-200">{fmtPe(t.pe_ratio)}</td>
              <td className={`px-3 py-2 text-right font-mono ${colorPct(t.ytd_pct)}`}>{fmtPct(t.ytd_pct)}</td>
              <td className={`px-3 py-2 text-right font-mono ${colorPct(t.one_year_pct)}`}>{fmtPct(t.one_year_pct)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Th({
  label,
  k,
  sort,
  onClick,
  right = false,
}: {
  label: string;
  k: SortKey;
  sort: { key: SortKey; dir: 'asc' | 'desc' };
  onClick: (k: SortKey) => void;
  right?: boolean;
}) {
  const active = sort.key === k;
  const arrow = active ? (sort.dir === 'asc' ? ' ▲' : ' ▼') : '';
  return (
    <th
      onClick={() => onClick(k)}
      className={clsx(
        'px-3 py-2 cursor-pointer select-none whitespace-nowrap',
        right ? 'text-right' : 'text-left',
        active && 'text-slate-900 dark:text-slate-100',
      )}
    >
      {label}{arrow}
    </th>
  );
}

function compare(a: TickerQuote, b: TickerQuote, key: SortKey): number {
  const av = a[key];
  const bv = b[key];
  if (av == null && bv == null) return 0;
  if (av == null) return 1;
  if (bv == null) return -1;
  if (typeof av === 'number' && typeof bv === 'number') return av - bv;
  return String(av).localeCompare(String(bv));
}
