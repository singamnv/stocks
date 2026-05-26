import clsx from 'clsx';

interface TabOption {
  value: string;
  label: string;
}

interface Props {
  value: string;
  onChange: (value: string) => void;
  options: TabOption[];
}

export default function Tabs({ value, onChange, options }: Props) {
  return (
    <div className="flex border-b border-slate-200 dark:border-slate-800 overflow-x-auto">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={clsx(
            'px-5 py-3 text-sm font-medium border-b-2 transition whitespace-nowrap',
            value === opt.value
              ? 'border-emerald-500 text-emerald-700 dark:text-emerald-400'
              : 'border-transparent text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200',
          )}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
