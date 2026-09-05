"""
Real-time notification layer.

- ConnectionManager fans messages out to every connected browser over
  WebSocket (/ws/alerts). The frontend turns each message into an
  in-app toast AND a browser Notification (if the user granted
  permission) -- that combo works even if the tab is in the background,
  without needing a full Web Push/VAPID server for a hackathon MVP.
- `poll_loop` runs forever in the background, checking disaster alerts
  and lightning strikes every POLL_INTERVAL_SECONDS, and only pushes a
  notification when something NEW shows up (so users aren't spammed on
  every refresh).
"""
import asyncio
import json
import logging
from typing import Set

from fastapi import WebSocket

from config import POLL_INTERVAL_SECONDS
from services import imd_alerts, lightning

log = logging.getLogger("weathergpt.notifier")


class ConnectionManager:
    def __init__(self):
        self.active: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)

    def disconnect(self, ws: WebSocket):
        self.active.discard(ws)

    async def broadcast(self, payload: dict):
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(json.dumps(payload))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()

_seen_alert_links: Set[str] = set()
_LIGHTNING_STRIKE_THRESHOLD = 1  # notify if any strikes land in the bbox


async def poll_loop():
    while True:
        try:
            await _check_alerts()
            await _check_lightning()
        except Exception as exc:  # never let the background loop die
            log.exception("poll_loop error: %s", exc)
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def _check_alerts():
    alerts = await imd_alerts.get_alerts(force=True)
    for alert in alerts:
        key = alert.get("link") or alert.get("title")
        if key and key not in _seen_alert_links:
            _seen_alert_links.add(key)
            await manager.broadcast(
                {
                    "type": "disaster_alert",
                    "severity": alert.get("severity", "Unknown"),
                    "title": alert.get("headline") or alert.get("title"),
                    "area": alert.get("area", ""),
                    "summary": alert.get("summary", "")[:280],
                    "link": alert.get("link", ""),
                }
            )


async def _check_lightning():
    result = await lightning.get_strikes()
    strikes = result["strikes"]
    if len(strikes) >= _LIGHTNING_STRIKE_THRESHOLD:
        await manager.broadcast(
            {
                "type": "lightning_alert",
                "count": len(strikes),
                "source": result["source"],
                "message": f"{len(strikes)} lightning strike(s) detected near Chennai / Pallikaranai",
            }
        )
