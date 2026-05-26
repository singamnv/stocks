import type {
  AiBriefResponse,
  BriefResponse,
  EarningsResponse,
  EcosystemsResponse,
  GridResponse,
  HistoryResponse,
  KpiResponse,
  NewsResponse,
  Range,
  TickerDetail,
} from '../types/api';

async function get<T>(url: string): Promise<T> {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json() as Promise<T>;
}

async function post<T>(url: string): Promise<T> {
  const r = await fetch(url, { method: 'POST' });
  if (!r.ok) {
    let detail = `${r.status} ${r.statusText}`;
    try {
      const body = await r.json();
      if (body?.detail) detail = body.detail;
    } catch {}
    const err = new Error(detail) as Error & { status?: number };
    err.status = r.status;
    throw err;
  }
  return r.json() as Promise<T>;
}

const ecoQS = (eco: string) => `ecosystem=${encodeURIComponent(eco)}`;

export const api = {
  ecosystems: () => get<EcosystemsResponse>('/api/ecosystems'),
  kpis: (eco: string) => get<KpiResponse>(`/api/kpis?${ecoQS(eco)}`),
  tickers: (eco: string) => get<GridResponse>(`/api/tickers?${ecoQS(eco)}`),
  ticker: (symbol: string, eco?: string) =>
    get<TickerDetail>(`/api/tickers/${symbol}${eco ? `?${ecoQS(eco)}` : ''}`),
  history: (symbol: string, range: Range) =>
    get<HistoryResponse>(`/api/tickers/${symbol}/history?range=${range}`),
  news: (filters?: { ecosystem?: string; ticker?: string; category?: string }) => {
    const q = new URLSearchParams();
    if (filters?.ecosystem) q.set('ecosystem', filters.ecosystem);
    if (filters?.ticker) q.set('ticker', filters.ticker);
    if (filters?.category) q.set('category', filters.category);
    const qs = q.toString();
    return get<NewsResponse>(`/api/news${qs ? `?${qs}` : ''}`);
  },
  earnings: (eco: string) => get<EarningsResponse>(`/api/earnings?${ecoQS(eco)}`),
  brief: () => get<BriefResponse>('/api/brief'),
  aiBrief: () => get<AiBriefResponse>('/api/ai-brief'),
  refreshEcosystem: (eco: string) =>
    post<{ status: string; key: string; cleared: number }>(
      `/api/ecosystems/${encodeURIComponent(eco)}/refresh`,
    ),
};
