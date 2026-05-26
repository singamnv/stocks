import { useEffect, useState } from 'react';

function formatET(d: Date) {
  const time = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(d);
  const date = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(d);
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    weekday: 'short',
  }).formatToParts(d);
  const hour = parseInt(parts.find((p) => p.type === 'hour')?.value ?? '0', 10);
  const minute = parseInt(parts.find((p) => p.type === 'minute')?.value ?? '0', 10);
  const weekday = parts.find((p) => p.type === 'weekday')?.value ?? '';
  const minutes = hour * 60 + minute;
  const isWeekend = weekday === 'Sat' || weekday === 'Sun';
  let session = 'Closed';
  if (!isWeekend) {
    if (minutes >= 4 * 60 && minutes < 9 * 60 + 30) session = 'Pre-Market';
    else if (minutes >= 9 * 60 + 30 && minutes < 16 * 60) session = 'Regular';
    else if (minutes >= 16 * 60 && minutes < 20 * 60) session = 'After Hours';
  }
  return { time, date, session };
}

export default function LiveClock() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const { time, date, session } = formatET(now);
  return (
    <div>
      <div className="text-[10px] uppercase tracking-widest text-emerald-700 dark:text-emerald-400">
        Pre-Open Reconnaissance · Vitals First
      </div>
      <div className="mt-1 text-sm text-slate-500 dark:text-slate-400">{date}</div>
      <div className="mt-0.5 font-mono text-2xl text-slate-900 dark:text-slate-100">
        {time} <span className="text-sm text-slate-500 dark:text-slate-400">ET</span>
      </div>
      <div className="mt-1 inline-block text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
        {session}
      </div>
    </div>
  );
}
