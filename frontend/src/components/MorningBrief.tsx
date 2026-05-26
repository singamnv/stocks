import clsx from 'clsx';
import LiveClock from './morning-brief/LiveClock';
import MacroVitals from './morning-brief/MacroVitals';
import GlobalTape from './morning-brief/GlobalTape';
import PreOpenChecklist from './morning-brief/PreOpenChecklist';
import SectorHeatmap from './morning-brief/SectorHeatmap';

interface Props {
  open: boolean;
  onToggle: () => void;
}

export default function MorningBrief({ open, onToggle }: Props) {
  return (
    <aside
      className={clsx(
        'fixed top-0 left-0 h-full z-40 bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 transition-all duration-200 flex flex-col',
        open ? 'w-full md:w-80' : '-translate-x-full md:translate-x-0 md:w-12',
      )}
    >
      <button
        onClick={onToggle}
        className="border-b border-slate-200 dark:border-slate-800 px-3 py-3 text-left text-xs uppercase tracking-wider text-emerald-700 dark:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-900 flex items-center justify-between"
        aria-label={open ? 'Collapse brief' : 'Expand brief'}
      >
        <span>{open ? 'Morning Brief' : 'B'}</span>
        {open && <span className="text-slate-400">◀</span>}
      </button>
      {open ? (
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          <LiveClock />
          <MacroVitals />
          <GlobalTape />
          <PreOpenChecklist />
          <SectorHeatmap />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <div
            className="text-[10px] uppercase tracking-widest text-slate-400 dark:text-slate-500"
            style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}
          >
            Brief
          </div>
        </div>
      )}
    </aside>
  );
}
