import { useEffect, useRef, useState } from 'react';
import clsx from 'clsx';
import type { EcosystemMeta } from '../types/api';
import { useEcosystem, useEcosystemsList } from '../lib/ecosystem';

// Group order in the dropdown. Anything not in this list falls under "Other".
const GROUP_ORDER = ['AI', 'Tech', 'Finance', 'Healthcare', 'Other'];

export default function EcosystemMenu() {
  const ecos = useEcosystemsList();
  const { active, set } = useEcosystem();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  const activeEco = ecos.find((e) => e.key === active);

  // Close on outside click / escape.
  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  if (ecos.length === 0) return null;

  // Bucket ecosystems by group, preserving declaration order within each group.
  const byGroup = new Map<string, EcosystemMeta[]>();
  for (const e of ecos) {
    const g = e.group || 'Other';
    if (!byGroup.has(g)) byGroup.set(g, []);
    byGroup.get(g)!.push(e);
  }
  const orderedGroups = [
    ...GROUP_ORDER.filter((g) => byGroup.has(g)),
    ...[...byGroup.keys()].filter((g) => !GROUP_ORDER.includes(g)),
  ];

  return (
    <div
      ref={rootRef}
      className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 relative"
    >
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-3">
        <button
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          aria-haspopup="menu"
          className={clsx(
            'inline-flex items-center gap-2 px-3 py-1.5 rounded-md border text-sm font-medium transition',
            open
              ? 'border-emerald-500 text-emerald-700 bg-white dark:bg-slate-900 dark:text-emerald-400'
              : 'border-slate-300 text-slate-700 bg-white hover:border-slate-400 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-slate-600',
          )}
        >
          <Burger />
          <span className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Ecosystem
          </span>
          <span className="text-slate-900 dark:text-slate-100">
            {activeEco?.name ?? '…'}
          </span>
          <Chevron open={open} />
        </button>
        {activeEco?.description && (
          <span className="hidden lg:block text-xs text-slate-500 dark:text-slate-400 truncate">
            {activeEco.description}
          </span>
        )}
      </div>

      {open && (
        <div
          role="menu"
          className="absolute left-0 right-0 top-full z-30 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 shadow-lg"
        >
          <div className="max-w-7xl mx-auto px-4 py-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {orderedGroups.map((group) => (
              <section key={group}>
                <div className="text-[10px] uppercase tracking-widest text-emerald-700 dark:text-emerald-400 mb-2">
                  {group}
                </div>
                <ul className="space-y-1">
                  {byGroup.get(group)!.map((e) => (
                    <li key={e.key}>
                      <button
                        role="menuitem"
                        onClick={() => {
                          set(e.key);
                          setOpen(false);
                        }}
                        className={clsx(
                          'w-full text-left p-2 rounded-md transition',
                          active === e.key
                            ? 'bg-emerald-50 dark:bg-emerald-500/10'
                            : 'hover:bg-slate-100 dark:hover:bg-slate-800',
                        )}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span
                            className={clsx(
                              'text-sm font-medium',
                              active === e.key
                                ? 'text-emerald-700 dark:text-emerald-400'
                                : 'text-slate-900 dark:text-slate-100',
                            )}
                          >
                            {e.name}
                          </span>
                          <span className="font-mono text-[10px] text-slate-400 dark:text-slate-500">
                            {e.anchor_ticker}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-500 dark:text-slate-400 leading-snug mt-0.5">
                          {e.description}
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Burger() {
  return (
    <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden>
      <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
    </svg>
  );
}

function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      width="12"
      height="12"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden
      className={clsx('transition-transform', open ? 'rotate-180' : '')}
    >
      <path d="M5 7l5 5 5-5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
