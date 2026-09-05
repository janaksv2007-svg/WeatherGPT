"""
Lightning / thunderstorm strike feed.

WeatherBug (Earth Networks) lightning data is a commercial product --
there is no free, public, keyless endpoint, and its coverage over India
is limited. This module is written as a pluggable provider so swapping
in real credentials later is a one-line config change:

    export WEATHERBUG_API_KEY="..."
    export WEATHERBUG_ENDPOINT="https://<your-contracted-endpoint>"

Until a key is supplied, a clearly-labelled simulated feed is used so
the map, risk scoring and notification pipeline can be demoed end to
end without a paid contract -- swap `provider` at the bottom to go live.
"""
import random
import time
import httpx
from config import (
    WEATHERBUG_API_KEY,
    WEATHERBUG_ENDPOINT,
    BBOX,
)

_cache = {"strikes": [], "ts": 0, "source": "simulated"}
_CACHE_TTL = 45


async def _fetch_weatherbug() -> list:
    params = {
        "apiKey": WEATHERBUG_API_KEY,
        "minLat": BBOX["min_lat"],
        "maxLat": BBOX["max_lat"],
        "minLon": BBOX["min_lon"],
        "maxLon": BBOX["max_lon"],
    }
    async with httpx.AsyncClient(timeout=8) as client:
        resp = await client.get(WEATHERBUG_ENDPOINT, params=params)
        resp.raise_for_status()
        raw = resp.json()
    # NOTE: reshape this to match your actual WeatherBug/Earth Networks
    # contract response -- field names below are illustrative.
    return [
        {
            "lat": s.get("latitude"),
            "lon": s.get("longitude"),
            "time": s.get("time"),
            "intensity_kA": s.get("amplitude"),
        }
        for s in raw.get("strikes", [])
    ]


def _simulate_strikes() -> list:
    """Random strikes scattered near Chennai/Pallikaranai for demo purposes."""
    n = random.randint(0, 4)
    strikes = []
    for _ in range(n):
        strikes.append(
            {
                "lat": round(random.uniform(BBOX["min_lat"], BBOX["max_lat"]), 4),
                "lon": round(random.uniform(BBOX["min_lon"], BBOX["max_lon"]), 4),
                "time": int(time.time()),
                "intensity_kA": round(random.uniform(5, 60), 1),
            }
        )
    return strikes


async def get_strikes() -> dict:
    now = time.time()
    if _cache["strikes"] is not None and now - _cache["ts"] < _CACHE_TTL and _cache["ts"] != 0:
        pass  # fall through, we still refresh below to keep the feed "live"

    if WEATHERBUG_API_KEY:
        try:
            strikes = await _fetch_weatherbug()
            source = "weatherbug"
        except Exception:
            strikes = _simulate_strikes()
            source = "simulated (weatherbug fetch failed)"
    else:
        strikes = _simulate_strikes()
        source = "simulated (no WEATHERBUG_API_KEY set)"

    _cache.update(strikes=strikes, ts=now, source=source)
    return {"strikes": strikes, "source": source, "generated_at": int(now)}
