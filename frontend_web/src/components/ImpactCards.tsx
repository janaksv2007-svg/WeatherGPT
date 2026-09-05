import React from 'react';
import { WeatherImpactSummary, SingleImpactCategory } from '../types';
import { getRiskColor } from './RiskScoreGauge';
import { Car, Droplets, Waves, Trees, Zap, Sprout, AlertCircle, ShieldAlert } from 'lucide-react';

interface Props {
  impacts: WeatherImpactSummary;
}

export const ImpactCards: React.FC<Props> = ({ impacts }) => {
  const categories: {
    key: keyof WeatherImpactSummary;
    title: string;
    icon: React.ComponentType<{ className?: string }>;
    data: SingleImpactCategory;
  }[] = [
    {
      key: 'travel_risk',
      title: 'Travel & Commute Risk',
      icon: Car,
      data: impacts.travel_risk
    },
    {
      key: 'waterlogging_risk',
      title: 'Urban Waterlogging Risk',
      icon: Droplets,
      data: impacts.waterlogging_risk
    },
    {
      key: 'flood_risk',
      title: 'Flood & Inundation Risk',
      icon: Waves,
      data: impacts.flood_risk
    },
    {
      key: 'outdoor_activity_risk',
      title: 'Outdoor Activity & Labor',
      icon: Trees,
      data: impacts.outdoor_activity_risk
    },
    {
      key: 'infrastructure_risk',
      title: 'Infrastructure & Utilities',
      icon: Zap,
      data: impacts.infrastructure_risk
    },
    {
      key: 'agriculture_risk',
      title: 'Agriculture & Crop Health',
      icon: Sprout,
      data: impacts.agriculture_risk
    }
  ];

  return (
    <div id="impact-cards-section" className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
            6-Category Domain Impact Estimates
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Probabilistic decision-support assessments tailored across critical sectors
          </p>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200 uppercase tracking-wider">
          <AlertCircle className="w-3.5 h-3.5 text-blue-600" />
          <span>Probabilistic Impact Advisory (potential / may / could)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {categories.map((c) => {
          const colors = getRiskColor(c.data.level);
          const Icon = c.icon;
          return (
            <div
              key={c.key}
              id={`impact-card-${c.key}`}
              className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col justify-between hover:border-slate-300 hover:shadow transition-all"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
                      <Icon className="w-4 h-4 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-800">
                        {c.title}
                      </h4>
                      <span className="text-[11px] font-mono font-semibold text-slate-500">Score {c.data.score}/100</span>
                    </div>
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${colors.badgeBg} ${colors.badgeText} ${colors.border}`}>
                    {c.data.level}
                  </span>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed mb-3 font-sans">
                  {c.data.reason}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100">
                <div className="flex items-start gap-1.5 text-[11px] text-slate-600">
                  <ShieldAlert className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
                  <span><strong className="text-slate-700">Action:</strong> {c.data.actionable_guidance}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
