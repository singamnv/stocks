import { createContext, useContext, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from './api';
import type { EcosystemMeta } from '../types/api';

const KEY = 'ecosystem:active';
const DEFAULT = 'nvidia';

interface Ctx {
  active: string;
  set: (key: string) => void;
}

const EcosystemContext = createContext<Ctx>({ active: DEFAULT, set: () => {} });

export function EcosystemProvider({ children }: { children: React.ReactNode }) {
  const [active, setActiveState] = useState<string>(() => {
    try {
      return localStorage.getItem(KEY) || DEFAULT;
    } catch {
      return DEFAULT;
    }
  });
  const set = (k: string) => {
    setActiveState(k);
    try { localStorage.setItem(KEY, k); } catch {}
  };
  return (
    <EcosystemContext.Provider value={{ active, set }}>{children}</EcosystemContext.Provider>
  );
}

export const useEcosystem = () => useContext(EcosystemContext);

// Cached forever — ecosystems list is static config baked into the backend.
export function useEcosystemsList(): EcosystemMeta[] {
  const { data } = useQuery({
    queryKey: ['ecosystems'],
    queryFn: api.ecosystems,
    staleTime: Infinity,
  });
  return data?.ecosystems ?? [];
}

export function useActiveEcosystem(): EcosystemMeta | undefined {
  const { active } = useEcosystem();
  return useEcosystemsList().find((e) => e.key === active);
}
