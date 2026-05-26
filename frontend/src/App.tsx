import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import DetailDrawer from './components/DetailDrawer';
import MorningBrief from './components/MorningBrief';
import EcosystemMenu from './components/EcosystemMenu';
import { EcosystemProvider } from './lib/ecosystem';
import { getBriefPinned, setBriefPinned } from './lib/brief';

export default function App() {
  const [activeSymbol, setActiveSymbol] = useState<string | null>(null);
  const [briefOpen, setBriefOpenState] = useState<boolean>(() => getBriefPinned());
  const setBriefOpen = (b: boolean) => {
    setBriefOpenState(b);
    setBriefPinned(b);
  };

  return (
    <EcosystemProvider>
      <div className="min-h-screen bg-white text-slate-900 dark:bg-slate-950 dark:text-slate-100">
        <MorningBrief open={briefOpen} onToggle={() => setBriefOpen(!briefOpen)} />
        <div className={briefOpen ? 'md:ml-80 transition-all' : 'md:ml-12 transition-all'}>
          <EcosystemMenu />
          <Dashboard onSelect={setActiveSymbol} onToggleBrief={() => setBriefOpen(!briefOpen)} />
        </div>
        {activeSymbol && (
          <DetailDrawer symbol={activeSymbol} onClose={() => setActiveSymbol(null)} />
        )}
      </div>
    </EcosystemProvider>
  );
}
