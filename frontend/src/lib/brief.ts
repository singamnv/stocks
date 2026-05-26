// Date in America/New_York as YYYY-MM-DD.
export function getETDate(): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
}

const CHECKLIST_PREFIX = 'brief:checklist:';

export function getChecklist(): Set<number> {
  const today = getETDate();
  try {
    // Prune stale checklist keys from other days.
    const stale: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith(CHECKLIST_PREFIX) && k !== CHECKLIST_PREFIX + today) {
        stale.push(k);
      }
    }
    stale.forEach((k) => localStorage.removeItem(k));

    const raw = localStorage.getItem(CHECKLIST_PREFIX + today);
    if (!raw) return new Set();
    return new Set(JSON.parse(raw));
  } catch {
    return new Set();
  }
}

export function setChecklist(ids: Set<number>): void {
  try {
    localStorage.setItem(CHECKLIST_PREFIX + getETDate(), JSON.stringify([...ids]));
  } catch {}
}

const PIN_KEY = 'brief:pinned';

export function getBriefPinned(): boolean {
  try {
    return localStorage.getItem(PIN_KEY) === '1';
  } catch {
    return false;
  }
}

export function setBriefPinned(pinned: boolean): void {
  try {
    localStorage.setItem(PIN_KEY, pinned ? '1' : '0');
  } catch {}
}
