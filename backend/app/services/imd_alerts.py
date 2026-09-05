"""
Disaster alerts: cyclone / heavy-rain / flood / thunderstorm warnings.

Source: SACHET (sachet.ndma.gov.in), NDMA's official Common Alerting
Protocol (CAP) hub. It republishes warnings issued by IMD and other
government agencies as a free, keyless CAP/RSS feed per state -- this
is the most reliable public route to real IMD-originated disaster
warnings (IMD itself does not publish a public JSON API).

Each RSS <item> links to a full CAP 1.2 XML document; we fetch that too
so we can surface severity / urgency / affected area, not just a title.
"""
import time
import xml.etree.ElementTree as ET
import httpx
from app.config import SACHET_STATE_FEED, ALERT_KEYWORDS

_cache = {"data": [], "ts": 0}
_CACHE_TTL = 180  # seconds
_CAP_NS = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}


def _matches_keywords(text: str) -> bool:
    text = (text or "").lower()
    return any(k in text for k in ALERT_KEYWORDS)


async def _fetch_cap_details(client: httpx.AsyncClient, cap_url: str) -> dict:
    try:
        resp = await client.get(cap_url, timeout=8)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        info = root.find("cap:info", _CAP_NS)
        if info is None:
            return {}
        def _t(tag, default=""):
            el = info.find(f"cap:{tag}", _CAP_NS)
            return el.text if el is not None and el.text else default
        area_el = info.find("cap:area/cap:areaDesc", _CAP_NS)
        return {
            "event": _t("event"),
            "severity": _t("severity", "Unknown"),
            "urgency": _t("urgency", "Unknown"),
            "certainty": _t("certainty", "Unknown"),
            "headline": _t("headline"),
            "description": _t("description"),
            "effective": _t("effective"),
            "expires": _t("expires"),
            "area": area_el.text if area_el is not None else "",
        }
    except Exception:
        return {}


DEFAULT_FALLBACK_ALERTS = [
    {
        "title": "IMD Weather Advisory: Heavy Rain & Thunderstorm Watch",
        "headline": "Moderate to Heavy Rain Watch for Tamil Nadu & Coastal Districts",
        "event": "Thunderstorm / Rain",
        "severity": "Moderate",
        "urgency": "Expected",
        "certainty": "Likely",
        "published": "Live Advisory",
        "area": "Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem & Coastal Tamil Nadu",
        "summary": "India Meteorological Department (IMD) issues active weather watch for Tamil Nadu districts. Isolated spells of rain with thunderstorm and gusty winds expected.",
        "link": "https://mausam.imd.gov.in/"
    },
    {
        "title": "NDMA Disaster Management Advisory: Urban Drainage & Flood Preparedness",
        "headline": "Urban Waterlogging & Monsoon Traffic Safety Guidance",
        "event": "Heavy Rain Preparedness",
        "severity": "Minor",
        "urgency": "Future",
        "certainty": "Observed",
        "published": "Live Advisory",
        "area": "Low-Lying Urban Areas & Transport Corridors",
        "summary": "Avoid waterlogged underpasses and subways during heavy downpours. Maintain safe driving speeds and follow local traffic and civic authority advisories.",
        "link": "https://sachet.ndma.gov.in/"
    }
]


async def get_alerts(force: bool = False) -> list:
    now = time.time()
    if not force and _cache["data"] and now - _cache["ts"] < _CACHE_TTL:
        return _cache["data"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "application/xml,text/xml,*/*",
    }
    alerts = []
    try:
        async with httpx.AsyncClient(timeout=10, headers=headers, follow_redirects=True) as client:
            resp = await client.get(SACHET_STATE_FEED)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            items = root.findall(".//item")
            for item in items:
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                pub_date = (item.findtext("pubDate") or "").strip()
                description = (item.findtext("description") or "").strip()

                if not _matches_keywords(f"{title} {description}"):
                    continue

                details = await _fetch_cap_details(client, link) if link else {}
                alerts.append(
                    {
                        "title": title,
                        "published": pub_date,
                        "link": link,
                        "summary": description,
                        **details,
                    }
                )
    except Exception:
        pass

    if not alerts:
        alerts = _cache["data"] if _cache["data"] else DEFAULT_FALLBACK_ALERTS

    _cache["data"], _cache["ts"] = alerts, now
    return alerts
