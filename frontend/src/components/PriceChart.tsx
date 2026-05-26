import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { PricePoint } from '../types/api';
import { useTheme } from '../lib/theme';

interface Props {
  points: PricePoint[];
}

export default function PriceChart({ points }: Props) {
  const theme = useTheme();
  if (!points.length) {
    return (
      <div className="h-full flex items-center justify-center text-slate-500 dark:text-slate-400 text-sm">
        Loading chart…
      </div>
    );
  }
  const first = points[0].c;
  const last = points[points.length - 1].c;
  const positive = last >= first;
  const color = positive ? '#10b981' : '#f43f5e';
  const axisColor = theme === 'dark' ? '#475569' : '#94a3b8';
  const tooltipBg = theme === 'dark' ? '#0f172a' : '#ffffff';
  const tooltipBorder = theme === 'dark' ? '#1e293b' : '#e2e8f0';
  const tooltipText = theme === 'dark' ? '#f1f5f9' : '#0f172a';

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={points} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <defs>
          <linearGradient id="priceFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.35} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis
          dataKey="t"
          tickFormatter={(t) =>
            new Date(t).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
          }
          stroke={axisColor}
          fontSize={11}
          minTickGap={48}
        />
        <YAxis
          domain={['auto', 'auto']}
          tickFormatter={(v) => `$${Number(v).toFixed(0)}`}
          stroke={axisColor}
          fontSize={11}
          width={48}
        />
        <Tooltip
          contentStyle={{
            background: tooltipBg,
            border: `1px solid ${tooltipBorder}`,
            borderRadius: 8,
            color: tooltipText,
          }}
          labelFormatter={(t) => new Date(t as number).toLocaleString()}
          formatter={(v: number) => [`$${v.toFixed(2)}`, 'Close']}
        />
        <Area
          type="monotone"
          dataKey="c"
          stroke={color}
          strokeWidth={2}
          fill="url(#priceFill)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
