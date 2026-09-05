import React, { useState, useMemo } from 'react';
import { WeatherInput, ScenarioModification, SimulationResponse } from '../types';
import { simulateScenario } from '../engine/clientRiskEngine';
import { getRiskColor } from './RiskScoreGauge';
import {
  Sliders,
  Play,
  RotateCcw,
  TrendingUp,
  TrendingDown,
  ArrowRight,
  AlertTriangle,
  Info,
  CloudRain,
  Wind,
  Clock,
  Thermometer,
  ShieldCheck
} from 'lucide-react';

interface Props {
  baselineWeather: WeatherInput;
}

export const WhatIfSimulator: React.FC<Props> = ({ baselineWeather }) => {
  const [rainDeltaPct, setRainDeltaPct] = useState<number>(40);
  const [windDeltaPct, setWindDeltaPct] = useState<number>(0);
  const [additionalHours, setAdditionalHours] = useState<number>(0);
  const [tempShift, setTempShift] = useState<number>(0);
  const [activePreset, setActivePreset] = useState<string>('scenario_a');

  // Compute simulation on the fly
  const simulationResult: SimulationResponse = useMemo(() => {
    const scenario: ScenarioModification = {
      rainfall_change_percent: rainDeltaPct !== 0 ? rainDeltaPct : undefined,
      wind_speed_change_percent: windDeltaPct !== 0 ? windDeltaPct : undefined,
      additional_rainfall_hours: additionalHours > 0 ? additionalHours : undefined,
      temperature_change_celsius: tempShift !== 0 ? tempShift : undefined,
    };
    return simulateScenario(baselineWeather, scenario);
  }, [baselineWeather, rainDeltaPct, windDeltaPct, additionalHours, tempShift]);

  const applyPreset = (preset: string) => {
    setActivePreset(preset);
    switch (preset) {
      case 'scenario_a': // Rainfall +40%
        setRainDeltaPct(40);
        setWindDeltaPct(0);
        setAdditionalHours(0);
        setTempShift(0);
        break;
      case 'scenario_a_50': // Rainfall +50%
        setRainDeltaPct(50);
        setWindDeltaPct(0);
        setAdditionalHours(0);
        setTempShift(0);
        break;
      case 'scenario_b': // Wind +20%
        setRainDeltaPct(0);
        setWindDeltaPct(20);
        setAdditionalHours(0);
        setTempShift(0);
        break;
      case 'scenario_c_6h': // Rain continues +6 hrs
        setRainDeltaPct(0);
        setWindDeltaPct(0);
        setAdditionalHours(6);
        setTempShift(0);
        break;
      case 'scenario_c_2h': // Rain continues +2 hrs
        setRainDeltaPct(0);
        setWindDeltaPct(0);
        setAdditionalHours(2);
        setTempShift(0);
        break;
      case 'scenario_d': // Temp +3°C
        setRainDeltaPct(0);
        setWindDeltaPct(0);
        setAdditionalHours(0);
        setTempShift(3);
        break;
      case 'scenario_e': // Rainfall -30%
        setRainDeltaPct(-30);
        setWindDeltaPct(0);
        setAdditionalHours(0);
        setTempShift(0);
        break;
      case 'scenario_f': // Combined Rain +40% & Wind +20%
        setRainDeltaPct(40);
        setWindDeltaPct(20);
        setAdditionalHours(0);
        setTempShift(0);
        break;
      case 'reset':
        setRainDeltaPct(0);
        setWindDeltaPct(0);
        setAdditionalHours(0);
        setTempShift(0);
        break;
    }
  };

  const bColors = getRiskColor(simulationResult.baseline.risk_level);
  const sColors = getRiskColor(simulationResult.simulated.risk_level);
  const isUp = simulationResult.change.risk_score_change > 0;
  const isDown = simulationResult.change.risk_score_change < 0;

  return (
    <div id="weather-impact-simulator-section" className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-100">
              <Sliders className="w-4 h-4" />
            </span>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              Weather Impact Simulator
            </h3>
            <span className="text-[10px] px-2.5 py-0.5 rounded-full font-bold bg-blue-50 text-blue-700 border border-blue-200 uppercase tracking-wider">
              Main Innovation
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            "What could happen if the weather conditions become worse or change?" – Counterfactual scenario modeling
          </p>
        </div>

        {/* Reset button */}
        <button
          onClick={() => applyPreset('reset')}
          className="self-start lg:self-auto flex items-center gap-1.5 text-xs font-medium text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 border border-slate-200 px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5 text-slate-500" />
          <span>Reset to Baseline</span>
        </button>
      </div>

      {/* Preset Scenario Selector */}
      <div>
        <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 block mb-2">
          1-Click Benchmark Scenarios
        </span>
        <div className="flex flex-wrap gap-2">
          {[
            { id: 'scenario_a', label: 'Scenario A: Rain +40%' },
            { id: 'scenario_a_50', label: 'Scenario A: Rain +50%' },
            { id: 'scenario_b', label: 'Scenario B: Wind +20%' },
            { id: 'scenario_c_2h', label: 'Scenario C: Rain +2 Hours' },
            { id: 'scenario_c_6h', label: 'Scenario C: Rain +6 Hours' },
            { id: 'scenario_d', label: 'Scenario D: Temp +3°C' },
            { id: 'scenario_e', label: 'Scenario E: Rain -30%' },
            { id: 'scenario_f', label: 'Scenario F: Combined (+40% Rain, +20% Wind)' },
          ].map((p) => (
            <button
              key={p.id}
              onClick={() => applyPreset(p.id)}
              className={`text-xs px-3 py-1.5 rounded-lg border transition-all cursor-pointer font-medium ${
                activePreset === p.id
                  ? 'bg-blue-600 text-white border-blue-600 shadow-sm font-semibold'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Interactive Controls & Sliders */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
        {/* Rain Slider */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="flex items-center gap-1 font-semibold text-slate-700">
              <CloudRain className="w-3.5 h-3.5 text-blue-600" /> Rainfall Shift
            </span>
            <span className="font-mono font-bold text-slate-900">
              {rainDeltaPct > 0 ? `+${rainDeltaPct}%` : `${rainDeltaPct}%`}
            </span>
          </div>
          <input
            type="range"
            min="-50"
            max="150"
            step="5"
            value={rainDeltaPct}
            onChange={(e) => {
              setRainDeltaPct(Number(e.target.value));
              setActivePreset('custom');
            }}
            className="w-full accent-blue-600 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>-50%</span>
            <span>0%</span>
            <span>+150%</span>
          </div>
        </div>

        {/* Wind Slider */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="flex items-center gap-1 font-semibold text-slate-700">
              <Wind className="w-3.5 h-3.5 text-cyan-600" /> Wind Shift
            </span>
            <span className="font-mono font-bold text-slate-900">
              {windDeltaPct > 0 ? `+${windDeltaPct}%` : `${windDeltaPct}%`}
            </span>
          </div>
          <input
            type="range"
            min="-40"
            max="100"
            step="5"
            value={windDeltaPct}
            onChange={(e) => {
              setWindDeltaPct(Number(e.target.value));
              setActivePreset('custom');
            }}
            className="w-full accent-blue-600 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>-40%</span>
            <span>0%</span>
            <span>+100%</span>
          </div>
        </div>

        {/* Additional Hours Slider */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="flex items-center gap-1 font-semibold text-slate-700">
              <Clock className="w-3.5 h-3.5 text-purple-600" /> Continuous Rain
            </span>
            <span className="font-mono font-bold text-slate-900">
              +{additionalHours} hrs
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="24"
            step="1"
            value={additionalHours}
            onChange={(e) => {
              setAdditionalHours(Number(e.target.value));
              setActivePreset('custom');
            }}
            className="w-full accent-blue-600 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>0h (current)</span>
            <span>+12h</span>
            <span>+24h</span>
          </div>
        </div>

        {/* Temperature Delta Slider */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="flex items-center gap-1 font-semibold text-slate-700">
              <Thermometer className="w-3.5 h-3.5 text-rose-500" /> Temp Delta
            </span>
            <span className="font-mono font-bold text-slate-900">
              {tempShift > 0 ? `+${tempShift}°C` : `${tempShift}°C`}
            </span>
          </div>
          <input
            type="range"
            min="-10"
            max="10"
            step="0.5"
            value={tempShift}
            onChange={(e) => {
              setTempShift(Number(e.target.value));
              setActivePreset('custom');
            }}
            className="w-full accent-blue-600 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>-10°C</span>
            <span>0°C</span>
            <span>+10°C</span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Current vs Simulated Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        {/* Baseline Card */}
        <div className="md:col-span-5 p-5 rounded-xl border border-slate-200 bg-white shadow-2xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
              CURRENT BASELINE
            </span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${bColors.badgeBg} ${bColors.badgeText} ${bColors.border}`}>
              {simulationResult.baseline.risk_level}
            </span>
          </div>
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-3xl font-bold font-mono tracking-tight text-slate-900">
              {simulationResult.baseline.risk_score}
            </span>
            <span className="text-xs text-slate-400 font-mono">/ 100 Risk</span>
          </div>
          <div className="space-y-1 text-xs text-slate-600 font-mono border-t border-slate-100 pt-2.5">
            <div>Rainfall: <strong className="text-slate-800">{simulationResult.baseline.rainfall_mm} mm</strong></div>
            <div>Wind Speed: <strong className="text-slate-800">{simulationResult.baseline.wind_speed_kmh} km/h</strong></div>
            <div>Temperature: <strong className="text-slate-800">{simulationResult.baseline.temperature} °C</strong></div>
          </div>
        </div>

        {/* Arrow & Delta Indicator */}
        <div className="md:col-span-2 flex flex-col items-center justify-center text-center py-2">
          <div className="p-2 rounded-full bg-slate-100 text-slate-600 mb-1 border border-slate-200">
            <ArrowRight className="w-5 h-5 hidden md:block" />
            <TrendingUp className="w-5 h-5 md:hidden" />
          </div>
          <div className={`text-xs font-bold font-mono px-2 py-0.5 rounded border ${
            isUp
              ? 'text-rose-700 bg-rose-50 border-rose-200'
              : isDown
              ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
              : 'text-slate-700 bg-slate-100 border-slate-200'
          }`}>
            {simulationResult.change.risk_score_change > 0 ? `+${simulationResult.change.risk_score_change}` : simulationResult.change.risk_score_change} pts
          </div>
          <span className="text-[10px] text-slate-400 font-mono mt-0.5">
            {simulationResult.change.percentage_change > 0 ? `+${simulationResult.change.percentage_change}%` : `${simulationResult.change.percentage_change}%`}
          </span>
        </div>

        {/* Simulated Scenario Card */}
        <div className="md:col-span-5 p-5 rounded-xl border-2 border-blue-400/80 bg-blue-50/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest text-blue-700">
              SIMULATED SCENARIO
            </span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${sColors.badgeBg} ${sColors.badgeText} ${sColors.border}`}>
              {simulationResult.simulated.risk_level}
            </span>
          </div>
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-3xl font-bold font-mono tracking-tight text-slate-900">
              {simulationResult.simulated.risk_score}
            </span>
            <span className="text-xs text-slate-400 font-mono">/ 100 Risk</span>
          </div>
          <div className="space-y-1 text-xs text-slate-700 font-mono border-t border-blue-200/60 pt-2.5">
            <div>Rainfall: <strong className="text-slate-900">{simulationResult.simulated.rainfall_mm} mm</strong></div>
            <div>Wind Speed: <strong className="text-slate-900">{simulationResult.simulated.wind_speed_kmh} km/h</strong></div>
            <div>Temperature: <strong className="text-slate-900">{simulationResult.simulated.temperature} °C</strong></div>
          </div>
        </div>
      </div>

      {/* Impact Transitions Table */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">
          Sector Impact Category Transitions
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 text-xs">
          {simulationResult.impact_comparisons.map((c, i) => (
            <div
              key={i}
              className={`p-2.5 rounded-lg border ${
                c.shifted
                  ? 'border-amber-200 bg-amber-50/70'
                  : 'border-slate-200 bg-slate-50/50'
              }`}
            >
              <div className="flex items-center justify-between font-semibold text-slate-800 mb-1">
                <span>{c.category}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                  c.delta > 0 ? 'text-rose-700 bg-rose-50 border border-rose-200 font-bold' : 'text-slate-500'
                }`}>
                  {c.delta > 0 ? `+${c.delta}` : c.delta}
                </span>
              </div>
              <div className="text-[11px] text-slate-600 font-mono">
                {c.transition_note}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Emerging Hazards Alert */}
      {simulationResult.emerging_impacts.length > 0 && (
        <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200">
          <div className="flex items-center gap-2 text-xs font-bold text-amber-900 mb-1">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            <span>Emerging Hazards in this Scenario</span>
          </div>
          <ul className="list-disc list-inside text-xs text-amber-800 space-y-0.5">
            {simulationResult.emerging_impacts.map((h, i) => (
              <li key={i}>{h}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Mandatory Disclaimer Box */}
      <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-start gap-2.5 text-xs text-slate-600">
        <Info className="w-4 h-4 text-slate-500 mt-0.5 shrink-0" />
        <p className="leading-relaxed">
          <strong className="text-slate-800">Mandatory Simulation Disclaimer:</strong> {simulationResult.simulation_disclaimer}
        </p>
      </div>
    </div>
  );
};
