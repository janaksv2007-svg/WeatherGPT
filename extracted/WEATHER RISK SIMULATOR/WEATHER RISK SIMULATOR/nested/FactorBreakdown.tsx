import React from 'react';
import { RiskFactorItem } from '../types';
import { getRiskColor } from './RiskScoreGauge';

interface Props {
  factors: RiskFactorItem[];
}

export const FactorBreakdown: React.FC<Props> = ({ factors }) => {
  return (
    <div id="factor-breakdown-card" className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
            Risk Factor Attribution & Contribution
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Weighted decomposition showing exact point contributions toward the composite 0–100 score
          </p>
        </div>
        <div className="text-[11px] text-slate-500 font-mono bg-slate-50 border border-slate-200 px-2.5 py-1 rounded">
          Formula: ∑(subscore × weight)
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-50 border-y border-slate-200 text-slate-500 font-bold uppercase tracking-wider text-[10px]">
              <th className="py-2.5 px-3">Hazard Factor</th>
              <th className="py-2.5 px-3">Observed / Raw Value</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Sub-Score</th>
              <th className="py-2.5 px-3">Weight</th>
              <th className="py-2.5 px-3 text-right">Points Contributed</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-sans">
            {factors.map((f, idx) => {
              const colors = getRiskColor(f.severity);
              return (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-3 font-semibold text-slate-800">
                    {f.factor}
                  </td>
                  <td className="py-3 px-3 font-mono font-medium text-slate-700">
                    {f.raw_value}
                  </td>
                  <td className="py-3 px-3">
                    <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider ${colors.badgeBg} ${colors.badgeText} ${colors.border}`}>
                      {f.severity}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-700 font-mono">
                    {f.normalized_subscore} / 100
                  </td>
                  <td className="py-3 px-3 text-slate-500 font-mono">
                    {(f.weight * 100).toFixed(0)}%
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">
                    +{f.contribution.toFixed(1)} pts
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
        <span>Total normalized risk points: <strong className="text-slate-800 font-mono font-bold">{factors.reduce((acc, curr) => acc + curr.contribution, 0).toFixed(1)}</strong></span>
        <span className="text-[11px]">Deterministic formula ensures 100% auditable results without AI hallucinations</span>
      </div>
    </div>
  );
};
