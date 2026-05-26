import type { NewsItem } from '../types/api';
import { fmtTime } from '../lib/format';

interface Props {
  item: NewsItem;
}

export default function NewsItemRow({ item }: Props) {
  return (
    <a
      href={item.url}
      target="_blank"
      rel="noreferrer"
      className="block rounded-md border border-slate-200 bg-white hover:bg-slate-50 dark:border-slate-800 dark:bg-slate-900/40 dark:hover:bg-slate-900 p-3 transition"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="text-sm text-slate-900 dark:text-slate-100 leading-snug">{item.title}</div>
          <div className="mt-1 text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2 flex-wrap">
            <span>{item.source}</span>
            <span>·</span>
            <span>{fmtTime(item.timestamp)}</span>
          </div>
        </div>
        <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 whitespace-nowrap">
          {item.ticker}
        </span>
      </div>
    </a>
  );
}
