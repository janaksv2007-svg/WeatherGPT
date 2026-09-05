# WeatherGPT – Module Integration Contract

## 1. Purpose

This document defines the standard interface between the **AI/Chatbot module** and the other WeatherGPT modules.

The AI module is responsible for:

* Understanding the user's message
* Detecting intent
* Extracting location
* Extracting date/time
* Detecting language
* Extracting scenario parameters
* Maintaining conversation context
* Preparing structured requests

The AI module does **not** calculate weather risk or simulation results.

---

# 2. Overall Integration Flow

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │   AI CHATBOT  │
              └───────┬───────┘
                      │
              Structured Request
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   WEATHER API    RISK ENGINE   SIMULATION
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                AI RESPONSE
                      │
                      ▼
                    USER
```

---

# 3. Standard AI Analysis Object

Every user message should first be converted into this structure:

```json
{
  "session_id": "session-001",
  "message": "Will it rain in Chennai tomorrow?",
  "intent": "RAIN_FORECAST",

  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "comparison_location": null,

  "time": {
    "date": "tomorrow",
    "time_period": null,
    "exact_time": null
  },

  "language": "en",

  "parameters": {
    "rainfall_change_mm": null,
    "wind_speed_kmh": null,
    "target_rainfall_mm": null
  },

  "requires_weather_data": true,
  "requires_risk_analysis": false,
  "requires_simulation": false
}
```

---

# 4. Intent Values

The AI module can return one of these intents:

```text
CURRENT_WEATHER
HOURLY_FORECAST
DAILY_FORECAST
RAIN_FORECAST
TEMPERATURE
WIND
HUMIDITY
WEATHER_ALERT
WEATHER_EXPLANATION
WEATHER_COMPARISON
TRAVEL_WEATHER
OUTDOOR_ACTIVITY
WEATHER_RISK
WHAT_IF_SCENARIO
GENERAL_WEATHER_CHAT
UNKNOWN
```

Other modules should use these values to determine what operation is required.

---

# 5. Location Object

```json
{
  "name": "Chennai",
  "latitude": 13.08784,
  "longitude": 80.27847
}
```

If the user does not provide a location:

```json
{
  "name": null,
  "latitude": null,
  "longitude": null
}
```

### Important

The AI module must **never hallucinate a location**.

If the location is missing, the downstream module should either:

1. Use the user's configured current location, or
2. Ask the user for a location.

---

# 6. Time Object

Supported examples:

```text
today
tomorrow
tonight
morning
afternoon
evening
night
weekend
next week
weekdays
in 3 hours
after 6 PM
```

Example:

```json
{
  "date": "tomorrow",
  "time_period": null,
  "exact_time": null
}
```

Example:

```json
{
  "date": "today",
  "time_period": "evening",
  "exact_time": "18:00"
}
```

If no time is specified:

```json
{
  "date": null,
  "time_period": null,
  "exact_time": null
}
```

---

# 7. Language

The AI module detects the user's language.

Current supported languages:

```text
en = English
hi = Hindi
ta = Tamil
```

Example:

```json
{
  "language": "hi"
}
```

The final chatbot response should preferably be returned in the same language.

---

# 8. Weather API Integration

## Request

The AI module sends the following information to the Weather API module:

```json
{
  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "intent": "RAIN_FORECAST",

  "time": {
    "date": "tomorrow",
    "time_period": null,
    "exact_time": null
  }
}
```

The Weather API module should use:

* Latitude
* Longitude
* Intent
* Date
* Time period
* Exact time

to obtain the appropriate weather data.

---

# 9. Weather API Response

Recommended standard response:

```json
{
  "location": "Chennai",
  "forecast_type": "daily",

  "forecast": {
    "date": "2026-09-05",
    "temperature": 29,
    "feels_like": 32,
    "humidity": 80,
    "rainfall_mm": 20,
    "rain_probability": 70,
    "wind_speed_kmh": 18,
    "condition": "Light Rain"
  }
}
```

For current weather:

```json
{
  "location": "Chennai",
  "forecast_type": "current",

  "forecast": {
    "temperature": 29,
    "feels_like": 32,
    "humidity": 82,
    "rainfall_mm": 45,
    "rain_probability": 80,
    "wind_speed_kmh": 22,
    "condition": "Heavy Rain"
  }
}
```

---

# 10. Hourly Forecast Response

For:

```text
Give me the hourly forecast for Chennai.
```

The Weather API should return:

```json
{
  "location": "Chennai",
  "forecast_type": "hourly",

  "forecast": [
    {
      "time": "18:00",
      "temperature": 29,
      "rain_probability": 70,
      "rainfall_mm": 5,
      "wind_speed_kmh": 18,
      "condition": "Rain"
    },
    {
      "time": "19:00",
      "temperature": 28,
      "rain_probability": 75,
      "rainfall_mm": 7,
      "wind_speed_kmh": 20,
      "condition": "Rain"
    }
  ]
}
```

---

# 11. Weather Comparison

For:

```text
Compare Chennai and Mumbai.
```

AI output:

```json
{
  "intent": "WEATHER_COMPARISON",

  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "comparison_location": {
    "name": "Mumbai",
    "latitude": 19.07283,
    "longitude": 72.88261
  },

  "time": {
    "date": null,
    "time_period": null,
    "exact_time": null
  },

  "requires_weather_data": true
}
```

Weather API should return data for **both locations**.

```json
{
  "primary": {
    "location": "Chennai",
    "temperature": 29,
    "humidity": 82,
    "rain_probability": 70,
    "wind_speed_kmh": 22
  },

  "comparison": {
    "location": "Mumbai",
    "temperature": 27,
    "humidity": 86,
    "rain_probability": 80,
    "wind_speed_kmh": 25
  }
}
```

---

# 12. Risk Engine Integration

For:

```text
What is the weather risk in Chennai?
```

AI output:

```json
{
  "intent": "WEATHER_RISK",

  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "time": {
    "date": null,
    "time_period": null,
    "exact_time": null
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true,
  "requires_simulation": false
}
```

Weather data is first obtained:

```text
AI
 ↓
Weather API
 ↓
Weather Data
 ↓
Risk Engine
```

Risk Engine can then calculate:

```json
{
  "risk_score": 72,
  "risk_level": "HIGH",
  "primary_risk": "Flooding"
}
```

---

# 13. What-If Simulation Integration

For:

```text
What if rainfall increases to 100 mm in Chennai?
```

AI output:

```json
{
  "intent": "WHAT_IF_SCENARIO",

  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "parameters": {
    "rainfall_change_mm": null,
    "wind_speed_kmh": null,
    "target_rainfall_mm": 100
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true,
  "requires_simulation": true
}
```

The AI module does **not** calculate the simulated risk.

Instead:

```text
AI
 │
 ├── Location
 ├── Current Weather
 └── Scenario Parameters
          │
          ▼
   Simulation Engine
          │
          ▼
    Simulated Result
```

Example simulation response:

```json
{
  "scenario": {
    "type": "rainfall",
    "target_rainfall_mm": 100
  },

  "baseline_risk": 45,
  "simulated_risk": 72,
  "risk_change": 27,
  "risk_level": "HIGH"
}
```

---

# 14. Wind What-If

User:

```text
What if wind speed increases to 60 km/h in Chennai?
```

AI:

```json
{
  "intent": "WHAT_IF_SCENARIO",

  "location": {
    "name": "Chennai"
  },

  "parameters": {
    "rainfall_change_mm": null,
    "wind_speed_kmh": 60,
    "target_rainfall_mm": null
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true,
  "requires_simulation": true
}
```

The simulation module performs the actual calculation.

---

# 15. Travel Weather

For:

```text
Is Chennai safe for travel this weekend?
```

AI:

```json
{
  "intent": "TRAVEL_WEATHER",

  "location": {
    "name": "Chennai"
  },

  "time": {
    "date": "weekend"
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true
}
```

The Risk Engine can determine travel safety based on weather conditions.

---

# 16. Outdoor Activity

For:

```text
Is it good to go outside in Chennai today?
```

AI:

```json
{
  "intent": "OUTDOOR_ACTIVITY",

  "location": {
    "name": "Chennai"
  },

  "time": {
    "date": "today"
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true
}
```

---

# 17. Final AI Response Input

After the other modules return their results, they should send the information back to the AI module.

Example:

```json
{
  "user_message": "Is Chennai safe for travel this weekend?",

  "analysis": {
    "intent": "TRAVEL_WEATHER",
    "language": "en"
  },

  "weather_data": {
    "location": "Chennai",
    "temperature": 29,
    "rain_probability": 80,
    "rainfall_mm": 45,
    "wind_speed_kmh": 22,
    "condition": "Heavy Rain"
  },

  "risk_data": {
    "risk_score": 72,
    "risk_level": "HIGH",
    "primary_risk": "Flooding"
  }
}
```

Gemini then converts this structured data into a natural-language answer.

---

# 18. Final Response

Example:

```text
Chennai has a high weather risk this weekend, mainly due to heavy rainfall and potential flooding. If you're planning to travel, consider checking conditions before leaving and avoid flood-prone areas.
```

---

# 19. Error Response Standard

Every module should return errors using a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "WEATHER_DATA_UNAVAILABLE",
    "message": "Weather data could not be retrieved for Chennai."
  }
}
```

Recommended error codes:

```text
INVALID_LOCATION
LOCATION_NOT_FOUND
WEATHER_DATA_UNAVAILABLE
FORECAST_UNAVAILABLE
RISK_ANALYSIS_FAILED
SIMULATION_FAILED
INVALID_SCENARIO
AI_SERVICE_UNAVAILABLE
INVALID_REQUEST
```

---

# 20. Success Response Standard

Successful responses should follow:

```json
{
  "success": true,
  "data": {}
}
```

Example:

```json
{
  "success": true,
  "data": {
    "location": "Chennai",
    "temperature": 29
  }
}
```

---

# 21. Important Integration Rules

### Rule 1 — AI does not calculate weather

The AI module only interprets the user's request.

### Rule 2 — AI does not calculate risk

Risk calculations belong to the Risk Engine.

### Rule 3 — AI does not calculate simulations

What-if calculations belong to the Simulation Engine.

### Rule 4 — Weather API owns weather data

Current, hourly, daily and alert data should come from the Weather API module.

### Rule 5 — Explicit location has priority

If the user says:

```text
What's the temperature in Mumbai?
```

the system must use Mumbai even if the previous conversation was about Chennai.

### Rule 6 — Explicit time has priority

If the user says:

```text
What's the weather in Chennai tomorrow?
```

the Weather API must return tomorrow's forecast, not current weather.

### Rule 7 — Never hallucinate

Missing weather data should result in an error/unavailable response, not fabricated data.

### Rule 8 — Preserve session ID

Every request should carry:

```json
{
  "session_id": "session-001"
}
```

This allows conversational context to be maintained.

---

# 22. Recommended API Communication

The modules can communicate through REST APIs.

Example:

```text
POST /weather
POST /risk/analyze
POST /simulation/run
POST /chat
```

### Weather

```http
POST /weather
```

### Risk

```http
POST /risk/analyze
```

### Simulation

```http
POST /simulation/run
```

### AI

```http
POST /chat
```

---

# 23. Responsibility Table

| Module            | Responsibility                                 |
| ----------------- | ---------------------------------------------- |
| AI/Chatbot        | Intent, language, location, time, conversation |
| Weather API       | Current/hourly/daily weather                   |
| Risk Engine       | Risk score and classification                  |
| Simulation Engine | What-if calculations                           |
| Flutter/UI        | User interface                                 |
| Risk Map/Alerts   | Maps, alerts and visualization                 |

---

# 24. Integration Checklist

Before integration, every team member should confirm:

### AI/Chatbot

* [ ] `/chat` endpoint working
* [ ] `/analyze` endpoint working
* [ ] Intent detection working
* [ ] Location extraction working
* [ ] Time extraction working
* [ ] Language detection working
* [ ] Session ID working
* [ ] JSON contract finalized

### Weather API

* [ ] `/weather` endpoint working
* [ ] Current weather
* [ ] Hourly forecast
* [ ] Daily forecast
* [ ] Rain probability
* [ ] Temperature
* [ ] Wind
* [ ] Humidity
* [ ] Alerts
* [ ] Error handling

### Risk Engine

* [ ] `/risk/analyze`
* [ ] Risk score
* [ ] Risk level
* [ ] Primary risk
* [ ] Weather input contract

### Simulation Engine

* [ ] `/simulation/run`
* [ ] Rainfall scenario
* [ ] Wind scenario
* [ ] Baseline risk
* [ ] Simulated risk
* [ ] Risk change

### Flutter

* [ ] Chat UI
* [ ] API integration
* [ ] JSON parsing
* [ ] Weather cards
* [ ] Risk display
* [ ] Simulation display
* [ ] Multilingual UI

---

# 25. One Complete Example

### User

```text
What if rainfall increases to 100 mm in Chennai tomorrow?
```

### Step 1 — AI

```json
{
  "session_id": "session-001",
  "intent": "WHAT_IF_SCENARIO",

  "location": {
    "name": "Chennai",
    "latitude": 13.08784,
    "longitude": 80.27847
  },

  "time": {
    "date": "tomorrow",
    "time_period": null,
    "exact_time": null
  },

  "parameters": {
    "rainfall_change_mm": null,
    "wind_speed_kmh": null,
    "target_rainfall_mm": 100
  },

  "requires_weather_data": true,
  "requires_risk_analysis": true,
  "requires_simulation": true
}
```

### Step 2 — Weather API

```text
Get tomorrow's Chennai weather
```

↓

```json
{
  "temperature": 28,
  "rainfall_mm": 60,
  "rain_probability": 75,
  "wind_speed_kmh": 20
}
```

### Step 3 — Risk Engine

```text
Weather Data
      +
Location
      ↓
Risk Calculation
```

↓

```json
{
  "risk_score": 55,
  "risk_level": "MEDIUM"
}
```

### Step 4 — Simulation Engine

```text
Baseline rainfall = 60 mm
Scenario rainfall = 100 mm
```

↓

```json
{
  "baseline_risk": 55,
  "simulated_risk": 78,
  "risk_change": 23,
  "risk_level": "HIGH"
}
```

### Step 5 — AI

Gemini receives the results and generates:

```text
If rainfall increases to 100 mm in Chennai tomorrow, the estimated weather risk could rise from MEDIUM to HIGH. The main concern would be flooding due to the significantly higher rainfall.
```

### Step 6 — Flutter

The UI displays:

```text
🌧️ Rainfall Scenario
━━━━━━━━━━━━━━━━━━━━
Tomorrow: Chennai

Normal rainfall: 60 mm
Scenario rainfall: 100 mm

Risk:
MEDIUM → HIGH

Risk increase: +23

⚠️ Primary concern:
Flooding
```

---

# 26. Golden Rule

```text
AI interprets.
Weather API provides weather.
Risk Engine calculates risk.
Simulation Engine calculates scenarios.
Flutter displays everything.
```

This separation should be maintained throughout integration.
