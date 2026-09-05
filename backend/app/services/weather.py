import httpx

LAT, LON = 13.0827, 80.2707

async def get_weather(location="chennai"):
    loc_key = (location or "chennai").strip().lower()
    coords = {
        "chennai": (13.0827, 80.2707),
        "coimbatore": (11.0168, 76.9558),
        "madurai": (9.9252, 78.1198),
        "trichy": (10.7905, 78.7047),
        "tiruchirappalli": (10.7905, 78.7047),
        "salem": (11.6643, 78.1460),
        "tirunelveli": (8.7139, 77.7567),
        "pallikaranai": (12.9345, 80.2145),
        "vellore": (12.9165, 79.1325),
        "thanjavur": (10.7870, 79.1378),
        "kanyakumari": (8.0883, 77.5385),
        "bengaluru": (12.9716, 77.5946),
        "bangalore": (12.9716, 77.5946),
        "mumbai": (19.0760, 72.8777),
        "delhi": (28.6139, 77.2090),
    }

    if loc_key in coords:
        lat, lon = coords[loc_key]
    else:
        try:
            from app.location.resolver import resolve_city
            res = resolve_city(loc_key)
            if res and "latitude" in res and "longitude" in res:
                lat, lon = res["latitude"], res["longitude"]
            else:
                lat, lon = coords["chennai"]
        except Exception:
            lat, lon = coords["chennai"]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,uv_index",
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "Asia/Kolkata",
        "forecast_days": 7,
    }
    raw = {}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            raw = r.json()
    except Exception as err:
        print(f"[Weather API Service Warning] {err}. Using fallback baseline.")
        raw = {
            "current": {"temperature_2m": 29.0, "relative_humidity_2m": 80, "precipitation": 5.0, "weather_code": 63, "wind_speed_10m": 18.0, "uv_index": 5.0},
            "hourly": {"time": [f"2026-09-05T{h:02d}:00" for h in range(24)], "temperature_2m": [28.0]*24, "precipitation_probability": [60]*24, "weather_code": [63]*24},
            "daily": {"time": ["2026-09-05", "2026-09-06", "2026-09-07"], "temperature_2m_max": [31.0, 30.0, 32.0], "temperature_2m_min": [25.0, 24.0, 26.0], "precipitation_probability_max": [70, 80, 40], "weather_code": [63, 65, 3]}
        }

    current = raw.get("current", {})
    hourly_raw = raw.get("hourly", {})
    daily_raw = raw.get("daily", {})

    hourly = []
    times = hourly_raw.get("time", [])
    for i, t in enumerate(times[:24]):
        hourly.append({
            "time": t[11:16],
            "temperature_2m": hourly_raw.get("temperature_2m", [0]*len(times))[i],
            "precipitation_probability": hourly_raw.get("precipitation_probability", [0]*len(times))[i],
            "weather_code": hourly_raw.get("weather_code", [0]*len(times))[i],
        })

    daily = []
    dates = daily_raw.get("time", [])
    for i, d in enumerate(dates):
        daily.append({
            "date": d,
            "temp_max": daily_raw.get("temperature_2m_max", [0]*len(dates))[i],
            "temp_min": daily_raw.get("temperature_2m_min", [0]*len(dates))[i],
            "rain_probability": daily_raw.get("precipitation_probability_max", [0]*len(dates))[i],
            "weather_code": daily_raw.get("weather_code", [0]*len(dates))[i],
        })
    # Air quality is from the same Open-Meteo ecosystem and requires no API key.
    air = {"aqi": 42, "label": "Good"}
    try:
        aq_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        aq_params = {"latitude":lat,"longitude":lon,"current":"us_aqi,pm2_5,pm10","timezone":"Asia/Kolkata"}
        async with httpx.AsyncClient(timeout=10) as client:
            ar = await client.get(aq_url, params=aq_params); ar.raise_for_status(); aq=ar.json().get("current",{})
        value=aq.get("us_aqi"); label="Good" if value is not None and value<=50 else "Moderate" if value is not None and value<=100 else "Unhealthy" if value is not None else "Unavailable"
        air={"aqi":value,"label":label,"pm2_5":aq.get("pm2_5"),"pm10":aq.get("pm10")}
    except Exception:
        pass
    return {"current": current, "hourly": hourly, "daily": daily, "air_quality": air}

