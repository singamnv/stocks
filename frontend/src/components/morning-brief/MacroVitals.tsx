import { useQuery } from '@tanstack/react-query';
import { api } from '../../lib/api';
import { colorPct, fmtPct, fmtPrice } from '../../lib/format';
import type { MarketRow, RatesRow, VixData } from '../../types/api';

export default function MacroVitals() {
  const { data, isLoading } = useQuery({
    queryKey: ['brief'],
    queryFn: api.brief,
    refetchInterval: 60_000,
  });

  if (isLoading || !data) return <Skeleton />;
  const v = data.vitals;

  return (
    <div className="space-y-4">
      <SectionHeading>Macro Vitals</SectionHeading>
      <Block title="US Futures" rows={v.futures} />
      <Block title="FX / Commodities" rows={v.fx_commodities} />
      <Rates rates={v.rates} />
      <Vix vix={v.vix} />
    </div>
  );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-xs uppercase tracking-widest text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 pb-1">
      {children}
    </div>
  );
}

function Block({ title, rows }: { title: string; rows: MarketRow[] }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wider text-slate-500 dark:text-slate-500 mb-1">
        {title}
      </div>
      <div className="space-y-0.5">
        {rows.map((r) => <Row key={r.symbol} label={r.name} value={fmtPrice(r.price)} sub={fmtPct(r.change_pct)} subClass={colorPct(r.change_pct)} />)}
      </div>
    </div>
  );
}

function Row({ label, value, sub, subClass }: { label: string; value: string; sub: string; subClass: string }) {
  return (
    <div className="flex items-baseline justify-between text-xs">
      <span className="text-slate-700 dark:text-slate-300">{label}</span>
      <span className="flex items-baseline gap-2">
        <span className="font-mono text-slate-900 dark:text-slate-100">{value}</span>
        <span className={`font-mono w-14 text-right ${subClass}`}>{sub}</span>
      </span>
    </div>
  );
}

function Rates({ rates }: { rates: RatesRow[] }) {
  const r = rates[0];
  if (!r) return null;
  const bps = r.bps_change;
  const col =
    bps == null ? 'text-slate-500 dark:text-slate-400'
      : bps >= 0 ? 'text-emerald-600 dark:text-emerald-400'
        : 'text-rose-600 dark:text-rose-400';
  const sign = bps != null && bps >= 0 ? '+' : '';
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wider text-slate-500 dark:text-slate-500 mb-1">Rates</div>
      <div className="flex items-baseline justify-between text-xs">
        <span className="text-slate-700 dark:text-slate-300">{r.label}</span>
        <span className="flex items-baseline gap-2">
          <span className="font-mono text-slate-900 dark:text-slate-100">
            {r.yield_pct != null ? `${r.yield_pct.toFixed(2)}%` : '—'}
          </span>
          <span className={`font-mono w-14 text-right ${col}`}>
            {bps != null ? `${sign}${bps.toFixed(1)} bp` : '—'}
          </span>
        </span>
      </div>
      <div className="text-[10px] text-slate-400 dark:text-slate-500 mt-1">
        2Y unavailable from yfinance; 2s10s requires FRED.
      </div>
    </div>
  );
}

function Vix({ vix }: { vix: VixData }) {
  const ratio = vix.term_ratio;
  const note = ratio == null ? '' : ratio >= 1 ? ' (backwardation)' : ' (contango)';
  const col =
    ratio == null ? 'text-slate-500 dark:text-slate-400'
      : ratio >= 1 ? 'text-rose-600 dark:text-rose-400'
        : 'text-emerald-600 dark:text-emerald-400';
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wider text-slate-500 dark:text-slate-500 mb-1">Volatility</div>
      <div className="space-y-0.5 text-xs">
        <Row label="VIX (front)" value={vix.spot != null ? vix.spot.toFixed(2) : '—'} sub="" subClass="" />
        <Row label="VIX3M" value={vix.three_month != null ? vix.three_month.toFixed(2) : '—'} sub="" subClass="" />
        <div className="flex items-baseline justify-between">
          <span className="text-slate-700 dark:text-slate-300">Term ratio</span>
          <span className={`font-mono ${col}`}>
            {ratio != null ? ratio.toFixed(3) + note : '—'}
          </span>
        </div>
      </div>
    </div>
  );
}

function Skeleton() {
  return (
    <div className="space-y-2 text-xs text-slate-400 dark:text-slate-500">Loading vitals…</div>
  );
}
