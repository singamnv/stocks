import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import clsx from 'clsx';
import { api } from '../lib/api';
import { useEcosystem } from '../lib/ecosystem';
import EcosystemCards from './EcosystemCards';
import EcosystemTable from './EcosystemTable';

interface Props {
  onSelect: (s: string) => void;
}

type View = 'cards' | 'table';
const VIEW_KEY = 'overview:view';

function getInitialView(): View {
  try {
    const v = localStorage.getItem(VIEW_KEY);
    if (v === 'table' || v === 'cards') return v;
  } catch {}
  return 'cards';
}

export default function EcosystemGrid({ onSelect }: Props) {
  const { active } = useEcosystem();
  const [view, setViewState] = useState<View>(getInitialView);
  const setView = (v: View) => {
    setViewState(v);
    try { localStorage.setItem(VIEW_KEY, v); } catch {}
  };

  const { data, isLoading, error } = useQuery({
    queryKey: ['grid', active],
    queryFn: () => api.tickers(active),
    refetchInterval: 60_000,
  });

  if (isLoading) return <div className="text-slate-500 dark:text-slate-400">Loading ecosystem…</div>;
  if (error) return <div className="text-rose-600 dark:text-rose-400">Failed to load: {String(error)}</div>;
  if (!data) return null;

  return (
    <div>
      <div className="flex justify-end mb-4">
        <div className="inline-flex rounded-md border border-slate-200 dark:border-slate-800 overflow-hidden">
          <ViewBtn current={view} target="cards" onClick={setView} label="Cards" />
          <ViewBtn current={view} target="table" onClick={setView} label="Table" />
        </div>
      </div>
      {view === 'cards' ? (
        <EcosystemCards data={data} onSelect={onSelect} />
      ) : (
        <EcosystemTable data={data} onSelect={onSelect} />
      )}
    </div>
  );
}

function ViewBtn({
  current,
  target,
  onClick,
  label,
}: {
  current: View;
  target: View;
  onClick: (v: View) => void;
  label: string;
}) {
  const active = current === target;
  return (
    <button
      onClick={() => onClick(target)}
      className={clsx(
        'px-3 py-1 text-xs transition',
        active
          ? 'bg-slate-100 text-slate-900 dark:bg-slate-700 dark:text-white'
          : 'bg-white text-slate-600 hover:bg-slate-50 dark:bg-slate-950 dark:text-slate-400 dark:hover:bg-slate-900',
      )}
    >
      {label}
    </button>
  );
}
