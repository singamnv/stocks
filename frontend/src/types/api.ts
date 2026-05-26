export interface TickerQuote {
  symbol: string;
  name: string;
  category: string;
  price: number | null;
  change_pct: number | null;
  market_cap: number | null;
  pe_ratio: number | null;
  ytd_pct: number | null;
  one_year_pct: number | null;
  error: string | null;
}

export interface TickerGroup {
  category: string;
  tickers: TickerQuote[];
}

export interface GridResponse {
  groups: TickerGroup[];
}

export interface KpiResponse {
  nvda_price: number | null;
  nvda_change_pct: number | null;
  total_market_cap: number | null;
  earnings_this_week: number;
  avg_change_pct: number | null;
}

export interface TickerDetail {
  symbol: string;
  name: string;
  category: string;
  role: string;
  price: number | null;
  change_pct: number | null;
  market_cap: number | null;
  pe_ratio: number | null;
  revenue: number | null;
  gross_margins: number | null;
  free_cashflow: number | null;
  fifty_two_week_high: number | null;
  fifty_two_week_low: number | null;
  sector: string | null;
  industry: string | null;
  website: string | null;
}

export interface PricePoint {
  t: number;
  c: number;
}

export interface HistoryResponse {
  symbol: string;
  range: string;
  points: PricePoint[];
}

export type Range = '1D' | '1W' | '1M' | '1Y' | '5Y';

export interface NewsItem {
  id: string;
  title: string;
  source: string;
  url: string;
  timestamp: number;
  ticker: string;
  category: string;
  image: string | null;
  summary: string | null;
}

export interface NewsResponse {
  items: NewsItem[];
  warning: string | null;
}

export interface EarningsItem {
  date: string;
  ticker: string;
  name: string;
  category: string;
  hour: string | null;
  eps_estimate: number | null;
  revenue_estimate: number | null;
}

export interface EarningsResponse {
  items: EarningsItem[];
  warning: string | null;
}

export interface MarketRow {
  symbol: string;
  name: string;
  price: number | null;
  change_pct: number | null;
}

export interface RatesRow {
  label: string;
  yield_pct: number | null;
  bps_change: number | null;
}

export interface VixData {
  spot: number | null;
  three_month: number | null;
  term_ratio: number | null;
}

export interface BriefVitals {
  futures: MarketRow[];
  fx_commodities: MarketRow[];
  rates: RatesRow[];
  vix: VixData;
}

export interface BriefTape {
  asia: MarketRow[];
  europe: MarketRow[];
  us: MarketRow[];
}

export interface BriefResponse {
  vitals: BriefVitals;
  tape: BriefTape;
  sectors: MarketRow[];
}

export interface AiBriefBullet {
  title: string;
  body: string;
  tickers: string[];
}

export interface AiBriefWatchItem {
  label: string;
  when: string | null;
}

export interface AiBriefResponse {
  date: string;
  headline: string;
  bullets: AiBriefBullet[];
  watch_today: AiBriefWatchItem[];
  model: string;
  generated_at: number;
}

export interface EcosystemMeta {
  key: string;
  name: string;
  group: string;
  description: string;
  anchor_ticker: string;
  categories: Record<string, string>; // category name -> description
}

export interface EcosystemsResponse {
  ecosystems: EcosystemMeta[];
  default_key: string;
}
