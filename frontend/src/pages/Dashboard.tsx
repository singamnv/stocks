import { useState } from 'react';
import KpiBar from '../components/KpiBar';
import EcosystemGrid from '../components/EcosystemGrid';
import NewsFeed from '../components/NewsFeed';
import EarningsCalendar from '../components/EarningsCalendar';
import Tabs from '../components/Tabs';

type Tab = 'overview' | 'news' | 'earnings';

interface Props {
  onSelect: (symbol: string) => void;
  onToggleBrief: () => void;
}

export default function Dashboard({ onSelect, onToggleBrief }: Props) {
  const [tab, setTab] = useState<Tab>('overview');

  return (
    <div className="min-h-screen">
      <KpiBar onToggleBrief={onToggleBrief} />
      <div className="max-w-7xl mx-auto px-4 py-4">
        <Tabs
          value={tab}
          onChange={(v) => setTab(v as Tab)}
          options={[
            { value: 'overview', label: 'Overview' },
            { value: 'news', label: 'News' },
            { value: 'earnings', label: 'Earnings' },
          ]}
        />
        <div className="mt-6">
          {tab === 'overview' && <EcosystemGrid onSelect={onSelect} />}
          {tab === 'news' && <NewsFeed />}
          {tab === 'earnings' && <EarningsCalendar />}
        </div>
      </div>
    </div>
  );
}
