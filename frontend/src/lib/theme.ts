import { useEffect, useState } from 'react';

export type Theme = 'light' | 'dark';

const KEY = 'theme';
const EVENT = 'themechange';

export function getCurrentTheme(): Theme {
  return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
}

export function setTheme(t: Theme): void {
  try {
    localStorage.setItem(KEY, t);
  } catch {}
  document.documentElement.classList.toggle('dark', t === 'dark');
  window.dispatchEvent(new CustomEvent(EVENT, { detail: t }));
}

export function toggleTheme(): void {
  setTheme(getCurrentTheme() === 'dark' ? 'light' : 'dark');
}

export function useTheme(): Theme {
  const [theme, set] = useState<Theme>(getCurrentTheme);
  useEffect(() => {
    const onChange = (e: Event) => set((e as CustomEvent).detail as Theme);
    window.addEventListener(EVENT, onChange);
    return () => window.removeEventListener(EVENT, onChange);
  }, []);
  return theme;
}
