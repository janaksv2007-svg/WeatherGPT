"""
WeatherGPT backend -- SIH hackathon build.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Then open http://localhost:8000 in a browser.
"""
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import CHENNAI, PALLIKARANAI, BBOX
from services import rainviewer, imd_alerts, lightning, weather, news
import notifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(notifier.poll_loop())
    yield
    task.cancel()


app = FastAPI(title="WeatherGPT API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------- meta ---
@app.get("/api/locations")
async def locations():
    return {"chennai": CHENNAI, "pallikaranai": PALLIKARANAI, "bbox": BBOX}


# --------------------------------------------------------------- radar ---
@app.get("/api/radar/rainviewer")
async def rainviewer_frames():
    """Frame list + tile URL templates for the RainViewer rain-risk map."""
    return await rainviewer.get_frames()



# --------------------------------------------------------------- weather ---
@app.get("/api/weather")
async def current_weather(location: str = Query("chennai")):
    return await weather.get_weather(location)


# ---------------------------------------------------------------- news ---
@app.get("/api/news")
async def weather_news():
    return await news.get_news()


# ----------------------------------------------------------- lightning ---
@app.get("/api/lightning")
async def lightning_strikes():
    return await lightning.get_strikes()


# --------------------------------------------------------------- alerts --
@app.get("/api/alerts")
async def disaster_alerts():
    """Cyclone / heavy-rain / flood / thunderstorm warnings (IMD via NDMA SACHET)."""
    return {"alerts": await imd_alerts.get_alerts()}


# ---------------------------------------------------------- websocket ----
@app.websocket("/ws/alerts")
async def ws_alerts(ws: WebSocket):
    await notifier.manager.connect(ws)
    try:
        while True:
            # Keep the connection open; we don't expect inbound messages,
            # but reading keeps disconnects detectable.
            await ws.receive_text()
    except WebSocketDisconnect:
        notifier.manager.disconnect(ws)


# --------------------------------------------------------------- static --
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


@app.get("/")
async def index():
    return FileResponse("../frontend/index.html")
