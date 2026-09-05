"""
Member 3 Risk Engine Service
Calculates 0-100 risk score, risk level (LOW, MEDIUM, HIGH), primary risk factor,
and individual hazard factor weights based on weather conditions.
"""
from typing import Dict, Any, Optional


def calculate_risk(
    temperature: float = 28.0,
    humidity: float = 70.0,
    rainfall_mm: float = 0.0,
    rain_probability: float = 0.0,
    wind_speed_kmh: float = 10.0,
    condition: str = "Clear",
    lightning_count: int = 0
) -> Dict[str, Any]:
    """
    Compute comprehensive weather risk score (0-100).
    
    Risk Levels:
      0 - 39: LOW
     40 - 69: MEDIUM
     70 - 100: HIGH
    """
    # 1. Rainfall Score (Max 50 points)
    rain_score = min(50.0, (rainfall_mm / 60.0) * 50.0)
    if rain_probability > 0:
        rain_score += min(10.0, (rain_probability / 100.0) * 10.0)
    rain_score = min(50.0, rain_score)

    # 2. Wind Score (Max 25 points)
    wind_score = min(25.0, (wind_speed_kmh / 50.0) * 25.0)

    # 3. Temperature / Heat Score (Max 15 points)
    temp_score = 0.0
    if temperature > 35.0:
        temp_score = min(15.0, (temperature - 35.0) * 3.0)
    elif temperature < 10.0:
        temp_score = min(15.0, (10.0 - temperature) * 2.0)

    # 4. Lightning / Condition Bonus Score (Max 10 points)
    condition_lower = condition.lower()
    lightning_score = min(10.0, lightning_count * 2.0)
    if "thunder" in condition_lower or "lightning" in condition_lower or "storm" in condition_lower:
        lightning_score = max(lightning_score, 8.0)
    elif "heavy rain" in condition_lower or "torrential" in condition_lower:
        lightning_score = max(lightning_score, 6.0)

    # Total Raw Score
    total_score = round(min(100.0, rain_score + wind_score + temp_score + lightning_score))

    # Determine Risk Level
    if total_score >= 70:
        risk_level = "HIGH"
    elif total_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Identify Primary Risk
    factors = {
        "rainfall": round(min(100.0, (rain_score / 50.0) * 100.0)),
        "wind": round(min(100.0, (wind_score / 25.0) * 100.0)),
        "temperature": round(min(100.0, (temp_score / 15.0) * 100.0)),
        "lightning": round(min(100.0, (lightning_score / 10.0) * 100.0))
    }

    max_factor = max(factors.items(), key=lambda x: x[1])
    factor_name_map = {
        "rainfall": "Flooding & Heavy Inundation",
        "wind": "High Winds & Structural Hazards",
        "temperature": "Extreme Temperature / Heatwave",
        "lightning": "Severe Lightning & Thunderstorm"
    }

    primary_risk = factor_name_map.get(max_factor[0], "General Weather Hazard")
    if total_score < 25:
        primary_risk = "None (Minimal Hazard)"

    return {
        "risk_score": total_score,
        "risk_level": risk_level,
        "primary_risk": primary_risk,
        "factors": factors
    }
