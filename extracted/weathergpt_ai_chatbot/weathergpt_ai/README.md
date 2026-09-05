# WeatherGPT AI Chatbot 🌦️🤖

An AI-powered chatbot module for **WeatherGPT** that understands natural-language weather queries, detects user intent, extracts locations and time information, supports multilingual conversations, and prepares structured requests for weather, risk, and simulation services.

---

## 🚀 Features

* 🤖 Gemini-powered conversational AI
* 🎯 Weather intent detection
* 📍 Location extraction and resolution
* 🕐 Time and date extraction
* 🌐 Multilingual support

  * English
  * Hindi
  * Tamil
* 💬 Conversation/session memory
* 🌧️ Rain forecast queries
* 🌡️ Temperature queries
* 💨 Wind queries
* 💧 Humidity queries
* 📅 Daily forecasts
* ⏰ Hourly forecast requests
* ⚠️ Weather-risk queries
* ✈️ Travel-weather queries
* 🏃 Outdoor activity queries
* 🔄 Weather comparison
* 🧪 What-if weather scenarios
* 🔌 Standard JSON interface for integration with other modules

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   User Message   │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   WeatherGPT AI     │
                  │      Chatbot        │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Intent Detection  Location       Time
                          Extraction    Extraction
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Structured Analysis │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Weather Module   Risk Module   Simulation
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                  ┌─────────────────────┐
                  │   Gemini Response   │
                  │     Generation      │
                  └──────────┬──────────┘
                             ▼
                    ┌─────────────────┐
                    │  Final Response │
                    └─────────────────┘
```

---

## 📁 Project Structure

```text
weathergpt_ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── gemini.py
│   │   └── response_parser.py
│   │
│   ├── intent/
│   │   ├── __init__.py
│   │   └── local_detector.py
│   │
│   ├── extraction/
│   │
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   └── memory.py
│   │
│   ├── integration/
│   │   └── weather_client.py
│   │
│   ├── location/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── importer.py
│   │   ├── multilingual_database.py
│   │   ├── resolver.py
│   │   └── message_resolver.py
│   │
│   ├── language/
│   │   ├── __init__.py
│   │   ├── supported.py
│   │   └── detector.py
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py
│
├── data/
│   ├── cities1000.zip
│   ├── cities.db
│   ├── multilingual.db
│   └── sample_weather.json
│
├── tests/
│   ├── test_intent.py
│   ├── test_location.py
│   ├── test_chat.py
│   ├── test_local_detector.py
│   ├── test_what_if.py
│   ├── test_comparison.py
│   └── test_response_generation.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🛠️ Technologies

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Python 3.13   | Core development               |
| FastAPI       | REST API                       |
| Pydantic      | Data validation                |
| Google Gemini | AI/Natural Language Processing |
| SQLite        | City/location database         |
| GeoNames      | City/location data             |
| HTTPX         | API communication              |
| python-dotenv | Environment variables          |
| Pytest        | Testing                        |
| Uvicorn       | API server                     |

---

## 📦 Installation

### 1. Clone the project

```bash
git clone <repository-url>
cd weathergpt_ai
```

### 2. Create virtual environment

```bash
py -3.13 -m venv venv
```

### 3. Activate it

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your API key to GitHub.

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the API

Start FastAPI using:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Example:

```json
{
  "status": "ok",
  "service": "WeatherGPT AI Chatbot"
}
```

---

### Chat

```http
POST /chat
```

Request:

```json
{
  "session_id": "session-001",
  "message": "What's the weather in Chennai?"
}
```

Example response:

```json
{
  "analysis": {
    "message": "What's the weather in Chennai?",
    "intent": "CURRENT_WEATHER",
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
    "language": "en",
    "requires_weather_data": true,
    "requires_risk_analysis": false,
    "requires_simulation": false
  },
  "response": "Current weather in Chennai..."
}
```

---

### Analyze

```http
POST /analyze
```

This endpoint returns the structured interpretation of the user's message.

Example:

```json
{
  "session_id": "session-001",
  "message": "Will it rain in Mumbai tomorrow?",
  "analysis": {
    "intent": "RAIN_FORECAST",
    "location": {
      "name": "Mumbai"
    },
    "time": {
      "date": "tomorrow"
    },
    "language": "en",
    "requires_weather_data": true
  }
}
```

---

## 🎯 Supported Intents

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

---

## 🌐 Multilingual Support

The chatbot can detect supported languages and resolve locations written in different languages.

### English

```text
What's the weather in Chennai?
```

### Hindi

```text
मुंबई में आज बारिश होगी?
```

### Tamil

```text
சென்னையில் நாளைக்கு மழை பெய்யுமா?
```

The detected language is stored in the analysis:

```json
{
  "language": "hi"
}
```

or:

```json
{
  "language": "ta"
}
```

The final AI response should be generated in the user's detected language.

---

## 📍 Location Resolution

WeatherGPT uses a local SQLite city database populated using GeoNames data.

The location pipeline is:

```text
User Message
     ↓
Location Extraction
     ↓
Normalization
     ↓
Alias Resolution
     ↓
City Database
     ↓
Latitude + Longitude
```

Example:

```text
சென்னை
```

is resolved to:

```json
{
  "name": "Chennai",
  "latitude": 13.08784,
  "longitude": 80.27847
}
```

---

## 🧠 Conversation Memory

Each conversation uses a `session_id`.

Example:

```text
User:
What's the weather in Chennai?

Bot:
Current weather in Chennai...

User:
What about tomorrow?

Bot:
Tomorrow's weather in Chennai...
```

The chatbot can use the previous session context when the user asks follow-up questions.

Explicitly provided locations should always take priority over previous session context.

---

## 🔄 Weather Comparison

Example:

```text
Compare the weather in Chennai and Mumbai.
```

The chatbot extracts:

```json
{
  "intent": "WEATHER_COMPARISON",
  "location": {
    "name": "Chennai"
  },
  "comparison_location": {
    "name": "Mumbai"
  }
}
```

Both locations can then be sent to the Weather API module.

---

## 🧪 What-If Scenarios

Example:

```text
What if rainfall increases to 100 mm in Chennai?
```

The chatbot extracts the scenario:

```json
{
  "intent": "WHAT_IF_SCENARIO",
  "location": {
    "name": "Chennai"
  },
  "parameters": {
    "target_rainfall_mm": 100
  },
  "requires_weather_data": true,
  "requires_risk_analysis": true,
  "requires_simulation": true
}
```

The AI module **does not calculate the final risk score**.

The structured scenario is passed to the Risk/Simulation module.

---

## 🔗 Module Integration

WeatherGPT AI acts as the intelligent interpretation layer.

```text
Flutter UI
    ↓
AI Chatbot
    ↓
Intent + Location + Time
    ↓
Weather API
    ↓
Risk Engine
    ↓
Simulation Engine
    ↓
AI Explanation
    ↓
Flutter UI
```

### Responsibilities

**AI/Chatbot module:**

* Understand user messages
* Detect intent
* Extract location
* Extract time
* Detect language
* Maintain conversation context
* Generate natural-language responses
* Prepare structured requests

**Weather API module:**

* Current weather
* Hourly forecast
* Daily forecast
* Rain
* Temperature
* Wind
* Humidity
* Alerts

**Risk module:**

* Risk score
* Risk classification
* Weather impact

**Simulation module:**

* What-if calculations
* Scenario comparison

---

## 🧪 Testing

Run all tests:

```bash
pytest -q
```

Run a specific test file:

```bash
pytest tests/test_intent.py -q
```

Run location tests:

```bash
pytest tests/test_location.py -q
```

Run comparison tests:

```bash
pytest tests/test_comparison.py -q
```

Run What-If tests:

```bash
pytest tests/test_what_if.py -q
```

---

## 📋 Example Queries

### Current Weather

```text
What's the weather in Chennai?
```

### Temperature

```text
What is the temperature in Delhi?
```

### Rain

```text
Will it rain in Mumbai today?
```

### Forecast

```text
What's the weather in Chennai tomorrow?
```

### Hourly

```text
Give me the hourly forecast for Chennai.
```

### Wind

```text
What is the wind speed in Chennai?
```

### Humidity

```text
What is the humidity in Chennai?
```

### Comparison

```text
Compare the weather in Chennai and Mumbai.
```

### Travel

```text
Is Chennai safe for travel this weekend?
```

### Outdoor Activity

```text
Is it good to go outside in Chennai today?
```

### Risk

```text
What is the weather risk in Chennai?
```

### What-If

```text
What if rainfall increases to 100 mm in Chennai?
```

### Multilingual

```text
मुंबई में आज बारिश होगी?
```

```text
சென்னையில் நாளைக்கு மழை பெய்யுமா?
```

---

## ⚠️ Important Design Rules

The chatbot must:

* Never hallucinate a location.
* Never invent weather information.
* Never pretend mock data is real-time weather.
* Preserve explicit user locations over conversation memory.
* Preserve explicit time information.
* Return structured data for other WeatherGPT modules.
* Avoid performing risk calculations inside the AI module.
* Keep API keys private.
* Use `session_id` for conversation context.

---

## 🔮 Future Improvements

* Complete real-time Weather API integration
* More Indian-language support
* Automatic language switching
* Voice input/output
* Advanced conversational memory
* Better ambiguity resolution
* Weather alert explanations
* Personalized weather recommendations
* Streaming Gemini responses
* Improved automated test coverage
* Production deployment

---

## 👨‍💻 Module

**WeatherGPT – AI/Chatbot Module**

Responsible for:

> **Natural Language Understanding + Intent Detection + Location/Time Extraction + Conversation + AI Response Generation**

---

## 📄 License

This project is developed as part of an internal hackathon project.

---
