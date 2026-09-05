"""
WeatherGPT - central configuration.
All tunables (locations, refresh intervals, provider keys) live here so the
rest of the codebase never hardcodes a magic number.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# ---- Area of interest -------------------------------------------------

CHENNAI = {"lat": 13.0827, "lon": 80.2707, "name": "Chennai"}
PALLIKARANAI = {"lat": 12.9345, "lon": 80.2145, "name": "Pallikaranai"}

# Bounding box used to filter lightning strikes / radar crops to the
# Chennai + Pallikaranai marsh belt (south Chennai).
BBOX = {
    "min_lat": 12.75,
    "max_lat": 13.25,
    "min_lon": 80.05,
    "max_lon": 80.35,
}

# ---- IMD (India Meteorological Department) -----------------------------
# IMD does not publish a documented public JSON API. The station radar
# pages below are the same images the public mausam.imd.gov.in site and
# the official "Mausam" app use. If IMD changes the URL pattern, update
# IMD_RADAR_STATIONS only -- nothing else needs to change.
IMD_RADAR_STATIONS = {
    "chennai": "https://mausam.imd.gov.in/responsive/radar.php?id=Chennai",
}
IMD_RADAR_IMAGE_FALLBACK = (
    "https://mausam.imd.gov.in/Radar/caz_chn.gif"  # best-effort static frame
)

# ---- Disaster alerts (cyclone / rain / flood warnings) -----------------
# SACHET is NDMA's official Common Alerting Protocol (CAP) hub. It
# redistributes IMD (and other agency) warnings as a public CAP/RSS feed
# per state -- this is the closest thing to a stable public "IMD alerts
# API" that exists today, no API key required.
SACHET_STATE_FEED = "https://sachet.ndma.gov.in/cap_public_website/rss/rss_Tamil%20Nadu.xml"
ALERT_KEYWORDS = ["cyclone", "rain", "flood", "thunderstorm", "lightning", "storm", "wind"]

# ---- RainViewer (free public radar/precipitation tiles) -----------------
RAINVIEWER_API = "https://api.rainviewer.com/public/weather-maps.json"

# ---- Lightning ----------------------------------------------------------
# WeatherBug / Earth Networks lightning data requires a commercial API
# key and contract -- there is no free public endpoint. Set
# WEATHERBUG_API_KEY to switch the app over to it; otherwise a clearly
# labelled simulated feed is used so the UI/notification pipeline can
# still be demoed end-to-end.
WEATHERBUG_API_KEY = os.getenv("WEATHERBUG_API_KEY", "")
WEATHERBUG_ENDPOINT = os.getenv(
    "WEATHERBUG_ENDPOINT",
    "https://api.weatherbug.com/v1/lightning/strikes",  # adjust to your contract's real path
)

# ---- Polling ------------------------------------------------------------
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "120"))
RADAR_CACHE_SECONDS = 60
