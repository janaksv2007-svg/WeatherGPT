"""
Member 3 Simulation Engine Service
Executes counterfactual what-if weather scenarios, computing simulated risk scores,
impact category transitions, emerging hazards, and mandatory risk disclaimers.
"""
from typing import Dict, Any, Optional
from app.services.risk_engine import calculate_risk


def simulate_scenario(
    baseline_weather: Dict[str, Any],
    scenario: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Simulates a counterfactual weather scenario against baseline conditions.
    
    scenario dictionary can contain:
      - target_rainfall_mm: float
      - rainfall_change_mm: float
      - rainfall_change_percent: float
      - wind_speed_change_percent: float
      - additional_rainfall_hours: float
      - temperature_change_celsius: float
    """
    b_temp = float(baseline_weather.get("temperature", 28.0))
    b_rain = float(baseline_weather.get("rainfall_mm", 10.0))
    b_wind = float(baseline_weather.get("wind_speed_kmh", 15.0))
    b_humidity = float(baseline_weather.get("humidity", 70.0))
    b_condition = str(baseline_weather.get("condition", "Cloudy"))
    b_lightning = int(baseline_weather.get("lightning_count", 0))

    # Compute baseline risk
    baseline_risk = calculate_risk(
        temperature=b_temp,
        humidity=b_humidity,
        rainfall_mm=b_rain,
        wind_speed_kmh=b_wind,
        condition=b_condition,
        lightning_count=b_lightning
    )

    # Compute simulated weather values
    s_rain = b_rain
    if scenario.get("target_rainfall_mm") is not None:
        s_rain = float(scenario["target_rainfall_mm"])
    elif scenario.get("rainfall_change_mm") is not None:
        s_rain = max(0.0, b_rain + float(scenario["rainfall_change_mm"]))
    elif scenario.get("rainfall_change_percent") is not None:
        s_rain = max(0.0, b_rain * (1.0 + float(scenario["rainfall_change_percent"]) / 100.0))

    s_hours = float(scenario.get("additional_rainfall_hours", 0.0))
    if s_hours > 0:
        s_rain += s_hours * 8.0  # Accumulate 8mm/hr for additional continuous rain

    s_wind = b_wind
    if scenario.get("target_wind_speed_kmh") is not None:
        s_wind = float(scenario["target_wind_speed_kmh"])
    elif scenario.get("wind_speed_change_percent") is not None:
        s_wind = max(0.0, b_wind * (1.0 + float(scenario["wind_speed_change_percent"]) / 100.0))

    s_temp = b_temp
    if scenario.get("temperature_change_celsius") is not None:
        s_temp = b_temp + float(scenario["temperature_change_celsius"])

    s_condition = b_condition
    if s_rain >= 50.0:
        s_condition = "Torrential Heavy Rain & Storm"
    elif s_rain >= 25.0:
        s_condition = "Heavy Rain"
    elif s_wind >= 40.0:
        s_condition = "High Wind Storm"

    # Compute simulated risk
    simulated_risk = calculate_risk(
        temperature=s_temp,
        humidity=b_humidity,
        rainfall_mm=s_rain,
        wind_speed_kmh=s_wind,
        condition=s_condition,
        lightning_count=b_lightning
    )

    b_score = baseline_risk["risk_score"]
    s_score = simulated_risk["risk_score"]
    score_diff = s_score - b_score
    pct_change = round((score_diff / max(1, b_score)) * 100.0, 1)

    # Sector impact comparisons
    impact_comparisons = [
        {
            "category": "Road Drainage & Transport",
            "baseline": "Moderate Waterlogging" if b_rain > 15 else "Normal Flow",
            "simulated": "Severe Inundation & Traffic Stoppage" if s_rain > 40 else "Minor Waterlogging",
            "delta": 2 if s_rain > 40 else 0,
            "shifted": s_rain > 40 and b_rain <= 40,
            "transition_note": "Risk escalated to High Alert" if (s_rain > 40 and b_rain <= 40) else "Conditions remain stable"
        },
        {
            "category": "Power & Utility Grid",
            "baseline": "Low Disruption Risk",
            "simulated": "High Pole Damage & Power Outage" if s_wind > 35 else "Stable Grid",
            "delta": 2 if s_wind > 35 else 0,
            "shifted": s_wind > 35 and b_wind <= 35,
            "transition_note": "High wind load detected on cables" if (s_wind > 35 and b_wind <= 35) else "Normal electrical stability"
        },
        {
            "category": "Public Safety & Shelter",
            "baseline": "Safe Outdoor Movement" if b_score < 40 else "Caution Advised",
            "simulated": "Evacuation & Stay Indoors Mandatory" if s_score >= 70 else "Proceed with Caution",
            "delta": s_score - b_score,
            "shifted": s_score >= 70 and b_score < 70,
            "transition_note": "Severe threat to low-lying residential areas" if (s_score >= 70 and b_score < 70) else "Standard risk monitoring"
        }
    ]

    # Emerging hazards list
    emerging = []
    if s_rain >= 50.0:
        emerging.append("Flash Flooding in low-lying urban sectors")
    if s_wind >= 40.0:
        emerging.append("Tree uprooting and sign-board collapse")
    if s_temp >= 38.0:
        emerging.append("Heatwave advisory & dehydration hazard")

    disclaimer = (
        "Simulation models counterfactual weather scenarios based on parametric inputs. "
        "Calculated risk changes reflect hypothetical estimates for emergency planning."
    )

    return {
        "scenario": scenario,
        "baseline": {
            "risk_score": b_score,
            "risk_level": baseline_risk["risk_level"],
            "rainfall_mm": round(b_rain, 1),
            "wind_speed_kmh": round(b_wind, 1),
            "temperature": round(b_temp, 1)
        },
        "simulated": {
            "risk_score": s_score,
            "risk_level": simulated_risk["risk_level"],
            "rainfall_mm": round(s_rain, 1),
            "wind_speed_kmh": round(s_wind, 1),
            "temperature": round(s_temp, 1)
        },
        "change": {
            "risk_score_change": score_diff,
            "percentage_change": pct_change
        },
        "baseline_risk": b_score,
        "simulated_risk": s_score,
        "risk_change": score_diff,
        "risk_level": simulated_risk["risk_level"],
        "impact_comparisons": impact_comparisons,
        "emerging_impacts": emerging,
        "simulation_disclaimer": disclaimer
    }
