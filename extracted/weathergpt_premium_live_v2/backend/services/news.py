import re
import xml.etree.ElementTree as ET
import httpx

FEEDS = [
    ("rain", "Google News · Chennai weather", "https://news.google.com/rss/search?q=Chennai+weather+rain+when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen"),
    ("cyclone", "Google News · Bay of Bengal", "https://news.google.com/rss/search?q=Bay+of+Bengal+cyclone+weather+when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen"),
    ("safety", "Google News · India weather safety", "https://news.google.com/rss/search?q=India+weather+warning+safety+when%3A7d&hl=en-IN&gl=IN%3Aen"),
]

def clean(text):
    return re.sub("<[^>]+>", "", text or "").strip()

async def get_news():
    items = []
    async with httpx.AsyncClient(timeout=10, headers={"User-Agent":"WeatherGPT/1.0"}) as client:
        for category, source, url in FEEDS:
            try:
                r = await client.get(url)
                r.raise_for_status()
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:6]:
                    title = clean(item.findtext("title"))
                    desc = clean(item.findtext("description"))
                    link = (item.findtext("link") or "").strip()
                    pub = clean(item.findtext("pubDate"))
                    if not title:
                        continue
                    icon = "🌧️" if category == "rain" else "🌀" if category == "cyclone" else "🛡️"
                    items.append({
                        "category": category,
                        "icon": icon,
                        "title": title,
                        "summary": desc[:220] if desc else "Latest weather-related update.",
                        "source": source,
                        "published": pub,
                        "link": link,
                    })
            except Exception:
                continue
    return items[:15]
