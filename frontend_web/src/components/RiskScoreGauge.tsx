import React from 'react';
import { RiskLevel, SubScoreBreakdown } from '../types';
import { ShieldCheck, AlertTriangle, CloudRain, Wind, Thermometer, Eye, Bell, MapPin } from 'lucide-react';

interface Props {
  score: number;
  level: RiskLevel;
  location: string;
  explanation: string;
  subScores: SubScoreBreakdown;
}

export const getRiskColor = (level: RiskLevel) => {
  switch (level) {
    case 'LOW':
      return {
        badgeBg: 'bg-emerald-100',
        badgeText: 'text-emerald-800',
        border: 'border-emerald-300',
        stroke: '#10b981',
        text: 'text-emerald-700'
      };
    case 'MODERATE':
      return {
        badgeBg: 'bg-amber-100',
        badgeText: 'text-amber-800',
        border: 'border-amber-300',
        stroke: '#f59e0b',
        text: 'text-amber-700'
      };
    case 'HIGH':
      return {
        badgeBg: 'bg-orange-100',
        badgeText: 'text-orange-700',
        border: 'border-orange-300',
        stroke: '#f97316',
        text: 'text-orange-700'
      };
    case 'VERY HIGH':
      return {
        badgeBg: 'bg-rose-100',
        badgeText: 'text-rose-700',
        border: 'border-rose-300',
        stroke: '#ef4444',
        text: 'text-rose-700'
      };
    case 'EXTREME':
      return {
        badgeBg: 'bg-purple-100',
        badgeText: 'text-purple-700',
        border: 'border-purple-300',
        stroke: '#a855f7',
        text: 'text-purple-700'
      };
  }
};

export const RiskScoreGauge: React.FC<Props> = ({ score, level, location, explanation, subScores }) => {
  const colors = getRiskColor(level);
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div id="risk-gauge-card" className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2 text-slate-800">
          <MapPin className="w-4 h-4 text-blue-600" />
          <span className="font-bold text-base text-slate-800">{location}</span>
          <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 uppercase tracking-wider">
            Observation Point
          </span>
        </div>
        <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full border uppercase tracking-wider ${colors.badgeBg} ${colors.badgeText} ${colors.border}`}>
          {level} RISK
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        {/* Radial Gauge */}
        <div className="md:col-span-4 flex flex-col items-center justify-center relative">
          <svg className="w-40 h-40 transform -rotate-90" viewBox="0 0 160 160">
            <circle
              cx="80"
              cy="80"
              r={radius}
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              className="text-slate-100"
            />
            <circle
              cx="80"
              cy="80"
              r={radius}
              stroke={colors.stroke}
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-700 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none">
            <span className="text-4xl font-bold font-mono tracking-tight text-slate-800">
              {score}
            </span>
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
              out of 100
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-2 font-mono uppercase tracking-wider">Normalized Index</p>
        </div>

        {/* Narrative & Sub-scores */}
        <div className="md:col-span-8 space-y-4">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">
              Deterministic Attribution
            </h4>
            <p className="text-sm text-slate-700 leading-relaxed font-sans">
              {explanation}
            </p>
          </div>

          {/* Subscore mini bars */}
          <div className="pt-3 border-t border-slate-100">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2.5">
              Normalized Sub-Score Drivers (0–100)
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 text-xs">
              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><CloudRain className="w-3.5 h-3.5 text-blue-500" /> Rain</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.rainfall_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-500 h-full rounded-full" style={{ width: `${subScores.rainfall_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><Wind className="w-3.5 h-3.5 text-cyan-600" /> Wind</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.wind_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-cyan-500 h-full rounded-full" style={{ width: `${subScores.wind_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><Bell className="w-3.5 h-3.5 text-amber-500" /> Warning</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.warning_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full rounded-full" style={{ width: `${subScores.warning_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><Thermometer className="w-3.5 h-3.5 text-red-500" /> Temp</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.temperature_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-red-500 h-full rounded-full" style={{ width: `${subScores.temperature_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><Eye className="w-3.5 h-3.5 text-blue-600" /> Visibility</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.visibility_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-600 h-full rounded-full" style={{ width: `${subScores.visibility_score}%` }} />
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <div className="flex items-center justify-between text-slate-600 mb-1">
                  <span className="flex items-center gap-1 font-medium"><ShieldCheck className="w-3.5 h-3.5 text-teal-600" /> Terrain</span>
                  <span className="font-mono font-bold text-slate-800">{subScores.historical_score}</span>
                </div>
                <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-teal-500 h-full rounded-full" style={{ width: `${subScores.historical_score}%` }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
