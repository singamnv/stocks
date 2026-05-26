import type { GridResponse } from '../types/api';
import { useActiveEcosystem } from '../lib/ecosystem';
import TickerCard from './TickerCard';

interface Props {
  data: GridResponse;
  onSelect: (s: string) => void;
}

export default function EcosystemCards({ data, onSelect }: Props) {
  const eco = useActiveEcosystem();
  const descs = eco?.categories ?? {};

  return (
    <div className="space-y-8">
      {data.groups.map((g) => (
        <section key={g.category}>
          <h2 className="text-sm uppercase tracking-wider text-slate-700 dark:text-slate-300">
            {g.category}
          </h2>
          {descs[g.category] && (
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3 mt-0.5">
              {descs[g.category]}
            </p>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {g.tickers.map((t) => (
              <TickerCard key={t.symbol} t={t} onClick={() => onSelect(t.symbol)} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
