import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../lib/api';
import { useActiveEcosystem, useEcosystem } from '../lib/ecosystem';
import NewsItemRow from './NewsItem';

export default function NewsFeed() {
  const { active } = useEcosystem();
  const eco = useActiveEcosystem();
  const categories = eco ? Object.keys(eco.categories) : [];

  const [filter, setFilter] = useState<string>('all');

  const { data: grid } = useQuery({
    queryKey: ['grid', active],
    queryFn: () => api.tickers(active),
  });

  const { data, isLoading } = useQuery({
    queryKey: ['news', active, filter],
    queryFn: () => {
      if (filter === 'all') return api.news({ ecosystem: active });
      if (filter.startsWith('cat:')) return api.news({ ecosystem: active, category: filter.slice(4) });
      return api.news({ ecosystem: active, ticker: filter });
    },
  });

  return (
    <div>
      <div className="flex items-center gap-3 mb-4 flex-wrap">
        <label className="text-sm text-slate-500 dark:text-slate-400" htmlFor="news-filter">
          Filter:
        </label>
        <select
          id="news-filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-white text-slate-900 border border-slate-300 dark:bg-slate-900 dark:text-slate-100 dark:border-slate-800 rounded-md px-3 py-1.5 text-sm"
        >
          <option value="all">All</option>
          <optgroup label="By category">
            {categories.map((c) => (
              <option key={c} value={`cat:${c}`}>
                {c}
              </option>
            ))}
          </optgroup>
          <optgroup label="By company">
            {grid?.groups.flatMap((g) => g.tickers).map((t) => (
              <option key={t.symbol} value={t.symbol}>
                {t.symbol} — {t.name}
              </option>
            ))}
          </optgroup>
        </select>
      </div>

      {isLoading && <div className="text-slate-500 dark:text-slate-400">Loading news…</div>}
      {data?.warning && (
        <div className="text-amber-600 dark:text-amber-400 text-sm mb-3">⚠ {data.warning}</div>
      )}
      <div className="space-y-2">
        {(data?.items ?? []).map((n) => (
          <NewsItemRow key={n.id} item={n} />
        ))}
      </div>
      {data && !data.warning && data.items.length === 0 && (
        <div className="text-slate-500 dark:text-slate-400 text-sm">No headlines found.</div>
      )}
    </div>
  );
}
