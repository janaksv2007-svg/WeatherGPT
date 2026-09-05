# WeatherGPT — Risk Maps & Alerts (SIH Hackathon)

A FastAPI backend + lightweight web frontend (installable as a mobile
app shell / PWA-style shell) that shows **Chennai / Pallikaranai**
rain risk, IMD radar, lightning strikes, and disaster alerts, with
real-time in-app + browser notifications.

## Features
| Feature | Data source | Status |
|---|---|---|
| Rain risk map | **RainViewer** public tile API | ✅ Live, free, no key |
| IMD Doppler radar (Chennai) | mausam.imd.gov.in image proxy | ✅ Live (best-effort — see note) |
| Disaster alerts (cyclone/rain/flood/thunderstorm) | **SACHET (NDMA)** CAP/RSS feed, which republishes IMD warnings | ✅ Live, free, no key |
| Lightning / thunderstorm strikes | WeatherBug (Earth Networks) | ⚠️ Requires a paid API key — ships with a clearly-labelled simulated feed until you add one |
| Real-time notifications | WebSocket + browser Notification API | ✅ Live |

### Honest notes on data sources
- **IMD has no documented public JSON API.** The radar image and the
  disaster-alert list are the two most reliable free, public routes
  into IMD data: the radar page IMD's own website/app use, and the
  SACHET portal (run by NDMA), which redistributes IMD's cyclone /
  heavy-rain / flood warnings as an open CAP feed. If IMD changes a
  URL, only `backend/config.py` needs updating.
- **WeatherBug's lightning API is commercial** (Earth Networks) and
  has limited India coverage. `backend/services/lightning.py` is
  written as a pluggable provider — set `WEATHERBUG_API_KEY` and
  `WEATHERBUG_ENDPOINT` (from your contract) once you have access.
  Until then, the app runs on a clearly-labelled simulated strike feed
  so the whole pipeline (map, risk badge, notifications) can be demoed
  end-to-end at the hackathon.
- **Notifications** use a WebSocket + the browser's Notification API
  rather than a full Web Push/VAPID server. This is simpler to run for
  a hackathon demo and delivers instantly while the app/browser is
  open; true background push (app closed) would need a VAPID key pair
  + `pywebpush` — a natural "next step" to mention in your pitch.

## Project structure
```
weathergpt/
  backend/
    main.py            FastAPI app: REST + WebSocket routes
    config.py           Locations, URLs, keys, poll interval
    notifier.py          WebSocket broadcast + background polling
    services/
      rainviewer.py       RainViewer frame list
      imd_radar.py        IMD radar image proxy
      imd_alerts.py       SACHET CAP/RSS alert parser
      lightning.py        WeatherBug adapter + simulated fallback
    requirements.txt
  frontend/
    index.html            Mobile-style app shell (bottom nav, 5 tabs)
    static/style.css       Bright, card-based UI
    static/app.js           Tabs, Leaflet maps, WebSocket client, toasts
```

## Run it
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Open **http://localhost:8000**.

Optional (real lightning data):
```bash
export WEATHERBUG_API_KEY="your-key"
export WEATHERBUG_ENDPOINT="https://your-contracted-endpoint"
```

## API reference
- `GET /api/locations` — Chennai/Pallikaranai coordinates + bounding box
- `GET /api/radar/imd` — proxied IMD Chennai radar image (binary)
- `GET /api/radar/rainviewer` — RainViewer frame timestamps + tile URL templates
- `GET /api/lightning` — recent strikes near Chennai (GeoJSON-ish list)
- `GET /api/alerts` — active cyclone/rain/flood/thunderstorm warnings
- `WS /ws/alerts` — pushes `{type: "disaster_alert" | "lightning_alert", ...}` the moment something new appears

## Next steps for the full pitch
- Swap the simulated lightning feed for a real provider once you have
  a key (WeatherBug, or a free alternative like Blitzortung.org, which
  needs its own strike-decoding client).
- Add a VAPID/Web Push backend (`pywebpush`) so alerts reach users even
  when the app is fully closed, not just backgrounded.
- Package the frontend as a PWA (manifest.json + service worker with
  offline caching) so it installs like a native mobile app.


## Updated UI
- Replaced the IMD radar screen with an embedded Windy radar interface.
- Replaced the WeatherBug-facing lightning UI with a Windy lightning interface while retaining the existing local strike/risk pipeline for demo/alert scoring.
- Added a Windy satellite/cloud interface.
- Added a bright Weather Dashboard with current conditions, hourly outlook and 7-day cards.
- Added Weather News with Rain / Cyclone / Safety filters.
- Added a dedicated Alerts dashboard with severity summary.
- Added a Safety & Precautions interface with thunderstorm, rain, wind, flood, heat and emergency guidance.
- Existing RainViewer timeline, official SACHET alerts, WebSocket alerts and bottom navigation remain in place.

### New backend endpoints
- `/api/weather` — Open-Meteo forecast data for Chennai.
- `/api/news` — recent weather news RSS aggregation.
