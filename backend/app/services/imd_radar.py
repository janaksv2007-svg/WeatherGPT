"""
IMD Doppler radar (Chennai station) image proxy.

IMD does not expose radar imagery through a documented public API --
the official "Mausam" app and mausam.imd.gov.in website simply embed a
refreshing image. We proxy that image server-side so the frontend can
show it without hitting CORS/hotlink restrictions, and so we control
caching.

If IMD reorganizes their URLs this is the ONLY place that needs updating.
"""
import time
import httpx
from app.config import IMD_RADAR_IMAGE_FALLBACK, RADAR_CACHE_SECONDS

_cache = {"bytes": None, "content_type": "image/gif", "ts": 0, "ok": False}


async def get_radar_image() -> dict:
    now = time.time()
    if _cache["bytes"] and now - _cache["ts"] < RADAR_CACHE_SECONDS:
        return _cache

    headers = {"User-Agent": "Mozilla/5.0 (WeatherGPT-SIH-Hackathon)"}
    try:
        async with httpx.AsyncClient(timeout=8, headers=headers) as client:
            resp = await client.get(IMD_RADAR_IMAGE_FALLBACK)
            resp.raise_for_status()
            _cache.update(
                bytes=resp.content,
                content_type=resp.headers.get("content-type", "image/gif"),
                ts=now,
                ok=True,
            )
    except Exception:
        # Keep serving the last good frame (if any) instead of breaking the UI.
        _cache["ok"] = False
    return _cache
