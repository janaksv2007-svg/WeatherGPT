"""
RainViewer integration.
RainViewer's `weather-maps.json` endpoint is free, keyless and public.
It returns a list of recent + forecast radar/satellite frame timestamps;
each frame is served as XYZ map tiles the frontend loads directly into
Leaflet, e.g.:

    https://tilecache.rainviewer.com/v2/radar/{time}/256/{z}/{x}/{y}/2/1_1.png

We only need the backend to fetch the frame list (so the frontend
doesn't hit RainViewer directly and we can cache / rate-limit it).
"""
import time
import httpx
from app.config import RAINVIEWER_API

_cache = {"data": None, "ts": 0}
_CACHE_TTL = 60  # seconds


async def get_frames():
    now = time.time()
    if _cache["data"] and now - _cache["ts"] < _CACHE_TTL:
        return _cache["data"]

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(RAINVIEWER_API)
            resp.raise_for_status()
            raw = resp.json()
    except Exception:
        # RainViewer unreachable -- serve the last good frame list (or
        # an empty one on first run) instead of a 500.
        return _cache["data"] or {
            "host": "",
            "generated_at": int(now),
            "past_frames": [],
            "forecast_frames": [],
        }

    host = raw.get("host", "https://tilecache.rainviewer.com")
    past = raw.get("radar", {}).get("past", [])
    forecast = raw.get("radar", {}).get("nowcast", [])

    def frame_url(frame):
        return f"{host}{frame['path']}/256/{{z}}/{{x}}/{{y}}/2/1_1.png"

    data = {
        "host": host,
        "generated_at": raw.get("generated", int(now)),
        "past_frames": [
            {"time": f["time"], "tile_url_template": frame_url(f)} for f in past
        ],
        "forecast_frames": [
            {"time": f["time"], "tile_url_template": frame_url(f)} for f in forecast
        ],
    }
    _cache["data"], _cache["ts"] = data, now
    return data
