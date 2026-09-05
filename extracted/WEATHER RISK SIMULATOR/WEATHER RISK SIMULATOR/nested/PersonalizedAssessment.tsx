import React, { useState, useMemo } from 'react';
import { WeatherInput, RiskCalculationResponse, UserContext, UserActivityType } from '../types';
import { personalizeAssessment } from '../engine/clientRiskEngine';
import { UserCheck, Compass, Clock, MapPin, AlertTriangle, ShieldCheck } from 'lucide-react';

interface Props {
  weather: WeatherInput;
  riskResult: RiskCalculationResponse;
}

export const PersonalizedAssessment: React.FC<Props> = ({ weather, riskResult }) => {
  const [activity, setActivity] = useState<UserActivityType>('travel');
  const [travelTime, setTravelTime] = useState<string>('08:30 AM');
  const [destination, setDestination] = useState<string>('City University Campus');

  const assessment = useMemo(() => {
    const ctx: UserContext = {
      activity,
      travel_time: travelTime,
      destination_type: destination,
    };
    return personalizeAssessment(weather, riskResult, ctx);
  }, [weather, riskResult, activity, travelTime, destination]);

  return (
    <div id="personalized-assessment-card" className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
            Personalized Impact Assessment
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Tailor risk intelligence for specific user roles, schedules, and operations
          </p>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-600 bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full uppercase tracking-wider">
          <UserCheck className="w-3.5 h-3.5 text-blue-600" />
          <span>Role Context</span>
        </div>
      </div>

      {/* Activity selector chips */}
      <div className="flex flex-wrap gap-2">
        {[
          { id: 'travel', label: 'Commute / Travel' },
          { id: 'delivery', label: 'Delivery Fleet' },
          { id: 'farming', label: 'Agriculture & Farming' },
          { id: 'outdoor_activity', label: 'Outdoor Labor / Sports' },
          { id: 'event', label: 'Public Event / Venue' },
          { id: 'general', label: 'General Public' },
        ].map((act) => (
          <button
            key={act.id}
            onClick={() => setActivity(act.id as UserActivityType)}
            className={`text-xs px-3 py-1.5 rounded-lg border transition-all cursor-pointer font-medium ${
              activity === act.id
                ? 'bg-blue-600 text-white border-blue-600 font-semibold shadow-2xs'
                : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
            }`}
          >
            {act.label}
          </button>
        ))}
      </div>

      {/* Contextual Input Fields */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs">
        <div>
          <label className="block text-slate-600 mb-1 font-semibold text-[11px] uppercase tracking-wider">Destination / Area Type</label>
          <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-lg px-2.5 py-1.5">
            <MapPin className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="e.g. University campus, low-lying farm"
              className="w-full bg-transparent outline-none text-slate-800 text-xs"
            />
          </div>
        </div>

        <div>
          <label className="block text-slate-600 mb-1 font-semibold text-[11px] uppercase tracking-wider">Scheduled Time Window</label>
          <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-lg px-2.5 py-1.5">
            <Clock className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            <input
              type="text"
              value={travelTime}
              onChange={(e) => setTravelTime(e.target.value)}
              placeholder="e.g. 08:30 AM, Evening rush hour"
              className="w-full bg-transparent outline-none text-slate-800 text-xs"
            />
          </div>
        </div>
      </div>

      {/* Tailored Explanation Output */}
      <div className="p-4 rounded-xl border border-blue-200 bg-blue-50/40">
        <h4 className="text-[10px] font-bold uppercase tracking-widest text-blue-700 mb-1.5">
          Contextual Advisory
        </h4>
        <p className="text-xs text-slate-700 leading-relaxed font-sans">
          {assessment.tailored_explanation}
        </p>
      </div>

      {/* Priority Action Alerts */}
      {assessment.priority_alerts.length > 0 && (
        <div className="space-y-2">
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 block">
            Priority Action Checklist
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {assessment.priority_alerts.map((alert, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2 p-3 rounded-lg bg-white border border-slate-200 shadow-2xs text-xs text-slate-700"
              >
                <ShieldCheck className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                <span>{alert}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
