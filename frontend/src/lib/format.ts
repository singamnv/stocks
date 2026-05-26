export const fmtPrice = (n: number | null | undefined): string =>
  n == null ? '—' : `$${n.toFixed(2)}`;

export const fmtPct = (n: number | null | undefined, withSign = true): string => {
  if (n == null) return '—';
  const s = n.toFixed(2);
  return withSign && n >= 0 ? `+${s}%` : `${s}%`;
};

export const fmtMcap = (n: number | null | undefined): string => {
  if (n == null || n === 0) return '—';
  if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
  return `$${n.toLocaleString()}`;
};

export const fmtPe = (n: number | null | undefined): string =>
  n == null ? '—' : n.toFixed(1);

export const colorPct = (n: number | null | undefined): string =>
  n == null
    ? 'text-slate-500 dark:text-slate-400'
    : n >= 0
      ? 'text-emerald-600 dark:text-emerald-400'
      : 'text-rose-600 dark:text-rose-400';

export const fmtTime = (unixSec: number): string => {
  const d = new Date(unixSec * 1000);
  return d.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
};

export const fmtDate = (iso: string): string => {
  const d = new Date(`${iso}T00:00:00`);
  return d.toLocaleDateString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });
};

export const fmtRevenue = (n: number | null | undefined): string => {
  if (n == null) return '—';
  if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  return `$${n.toLocaleString()}`;
};

export const fmtMargin = (n: number | null | undefined): string => {
  if (n == null) return '—';
  return `${(n * 100).toFixed(1)}%`;
};
