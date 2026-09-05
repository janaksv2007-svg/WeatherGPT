/* ===================== Tab navigation ===================== */
function showTab(id) {
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.toggle("active", p.id === id));
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.toggle("active", b.dataset.goto === id));
  window.scrollTo({top: 0, behavior: "smooth"});
  setTimeout(() => window.dispatchEvent(new Event("resize")), 100);
}
document.querySelectorAll("[data-goto]").forEach(el => el.addEventListener("click", () => showTab(el.dataset.goto)));

/* ===================== Floating Chat Button ===================== */
const floatingChatBtn = document.getElementById("floatingChatBtn");
if (floatingChatBtn) {
  floatingChatBtn.addEventListener("click", () => showTab("tab-chat"));
}

/* ===================== AI Chatbot Logic ===================== */
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const clearChatBtn = document.getElementById("clearChatBtn");

function parseMarkdown(text) {
  if (!text) return "";
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Bold text **word**
  html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  
  // Headers ### Header
  html = html.replace(/^### (.*$)/gim, "<strong style='display:block;margin:6px 0 2px;color:var(--sky);'>$1</strong>");

  // Bullet items * item or - item
  const lines = html.split("\n");
  let inList = false;
  let result = [];

  for (let line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("* ") || trimmed.startsWith("- ")) {
      if (!inList) {
        inList = true;
        result.push("<ul style='margin:4px 0;padding-left:18px;'>");
      }
      result.push(`<li>${trimmed.slice(2)}</li>`);
    } else {
      if (inList) {
        inList = false;
        result.push("</ul>");
      }
      result.push(line);
    }
  }
  if (inList) result.push("</ul>");

  html = result.join("<br>").replace(/(<br>\s*)+<ul>/g, "<ul>").replace(/<\/ul>\s*(<br>\s*)+/g, "</ul>");
  return html;
}

function speakText(text) {
  if (!("speechSynthesis" in window)) return showToast("Speech synthesis not supported in this browser.", "warn");
  window.speechSynthesis.cancel();
  const cleanText = text.replace(/<[^>]*>/g, "");
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.rate = 1.0;
  utterance.pitch = 1.0;
  window.speechSynthesis.speak(utterance);
}

async function sendChatMessage(promptText) {
  const text = (promptText || chatInput.value).trim();
  if (!text) return;

  // Append user bubble
  appendChatBubble("user", text);
  if (!promptText) chatInput.value = "";

  // Append loading indicator
  const loadingId = "loading-" + Date.now();
  appendChatBubble("ai", "⚡ <em>WeatherGPT is processing query...</em>", loadingId);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: "web-session-001" })
    });
    const data = await res.json();
    document.getElementById(loadingId)?.remove();

    let rawReply = data.response || "Weather information processed.";
    let replyHTML = parseMarkdown(rawReply);
    
    // Format card attachments if risk, simulation or weather is returned
    let extraHTML = "";

    if (data.risk) {
      const r = data.risk;
      const badgeClass = r.risk_level === "HIGH" ? "risk-high" : r.risk_level === "MEDIUM" ? "risk-moderate" : "risk-low";
      extraHTML += `<div style="margin-top:10px;"><span class="risk-badge ${badgeClass}">⚠️ Risk Score: ${r.risk_score}/100 — ${r.risk_level} (${r.primary_risk})</span></div>`;
    }

    if (data.simulation) {
      const s = data.simulation;
      const changeStr = (s.risk_change >= 0 ? "+" : "") + s.risk_change;
      extraHTML += `
        <div style="margin-top:10px;background:#070d19;border:1px solid #334155;padding:12px;border-radius:14px;font-size:0.76rem;">
          <div style="font-weight:800;color:var(--sky);margin-bottom:4px;">🌊 What-If Simulation Engine</div>
          <div>Baseline Risk: <b>${s.baseline_risk}/100</b> ➔ Simulated Risk: <b style="color:var(--warn);">${s.simulated_risk}/100</b> (${changeStr} pts)</div>
          <div style="margin-top:4px;color:var(--muted);">Scenario: ${s.scenario || "Rainfall modification"}</div>
        </div>`;
    }

    if (data.weather) {
      const w = data.weather;
      extraHTML += `
        <div style="margin-top:8px;font-size:0.75rem;color:#cbd5e1;background:#0f172a;border:1px solid #334155;padding:8px 12px;border-radius:12px;display:flex;align-items:center;justify-content:space-between;">
          <span>🌤️ <strong>${w.location || "Chennai"}</strong>: ${w.temperature}°C, ${w.condition || "Cloudy"}</span>
          <span>💧 ${w.humidity}% | 💨 ${w.wind_speed_kmh} km/h</span>
        </div>`;
    }

    appendChatBubble("ai", replyHTML + extraHTML, null, rawReply);
  } catch (err) {
    console.error(err);
    document.getElementById(loadingId)?.remove();
    appendChatBubble("ai", "I'm having trouble connecting to the backend server. Showing offline mode response.");
  }
}

function appendChatBubble(role, htmlContent, id = null, speakableText = null) {
  const container = document.createElement("div");
  container.className = `chat-bubble ${role}`;
  if (id) container.id = id;

  const avatar = document.createElement("div");
  avatar.className = "chat-avatar";
  avatar.textContent = role === "user" ? "👤" : "🤖";

  const textDiv = document.createElement("div");
  textDiv.className = "chat-text";
  textDiv.innerHTML = htmlContent;

  if (role === "ai" && speakableText && !id) {
    const speakBtn = document.createElement("button");
    speakBtn.innerHTML = "🔊";
    speakBtn.title = "Read response aloud";
    speakBtn.style.cssText = "background:none;border:none;cursor:pointer;font-size:0.9rem;margin-top:6px;padding:2px;display:block;opacity:0.8;";
    speakBtn.addEventListener("click", () => speakText(speakableText));
    textDiv.appendChild(speakBtn);
  }

  container.appendChild(avatar);
  container.appendChild(textDiv);
  chatMessages.appendChild(container);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

if (chatForm) {
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendChatMessage();
  });
}

if (clearChatBtn) {
  clearChatBtn.addEventListener("click", () => {
    chatMessages.innerHTML = `
      <div class="chat-bubble ai">
        <div class="chat-avatar">🤖</div>
        <div class="chat-text">
          <strong>Chat cleared! 👋</strong><br>
          Ask me anything about weather, storm risks, or What-If scenarios.
        </div>
      </div>`;
    showToast("Chat conversation cleared.", "info");
  });
}

document.querySelectorAll(".chat-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    sendChatMessage(chip.dataset.ask);
  });
});


/* ===================== Toasts + Notifications ===================== */
function showToast(message, level = "info") {
  const root = document.getElementById("toastRoot");
  const el = document.createElement("div");
  el.className = `toast ${level}`;
  el.textContent = message;
  root.appendChild(el);
  setTimeout(() => el.remove(), 6000);
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification("WeatherGPT Alert", { body: message });
  }
}
const notifBtn = document.getElementById("notifBtn");
const locations = {
  chennai: {name:"Chennai", lat:13.0827, lon:80.2707},
  pallikaranai: {name:"Pallikaranai", lat:12.9345, lon:80.2145}
};
let selectedLocation = localStorage.getItem("weathergpt_location") || "chennai";
function applyLocation(loc){
  selectedLocation=loc; localStorage.setItem("weathergpt_location",loc);
  const l=locations[loc];
  document.getElementById("locationSelect").value=loc;
  document.getElementById("settingsLocation").value=loc;
  document.querySelector(".hero-card h1").textContent=l.name;
  loadWeather(); loadLightning(); loadAlerts();
}

function refreshNotifBtn() {
  if ("Notification" in window && Notification.permission === "granted") {
    notifBtn.textContent = "🔔 Alerts On";
    notifBtn.classList.add("enabled");
  }
}
if (notifBtn) {
  notifBtn.addEventListener("click", async () => {
    if (!("Notification" in window)) return showToast("Browser notifications are not supported.", "warn");
    const perm = await Notification.requestPermission();
    if (perm === "granted") showToast("Notifications enabled — important weather alerts will appear here.", "info");
    refreshNotifBtn();
  });
}
refreshNotifBtn();

/* ===================== Live alert websocket ===================== */
function connectWS() {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${proto}://${location.host}/ws/alerts`);
  ws.onmessage = evt => {
    const msg = JSON.parse(evt.data);
    if (msg.type === "disaster_alert") {
      const sev = (msg.severity || "").toLowerCase();
      const level = sev.includes("severe") || sev.includes("extreme") ? "danger" : "warn";
      showToast(`⚠️ ${msg.title}`, level);
      loadAlerts(); computeRisk(); updatePrecautions();
      setHomeStrip(`⚠️ ${msg.title}`, level);
    } else if (msg.type === "lightning_alert") {
      showToast(`⚡ ${msg.message}`, "warn");
      loadLightning(); computeRisk(); updatePrecautions();
    }
  };
  ws.onclose = () => setTimeout(connectWS, 4000);
}
connectWS();

function setHomeStrip(text, level) {
  const strip = document.getElementById("latestAlertStrip");
  if (!strip) return;
  strip.textContent = text;
  strip.className = `alert-strip ${level === "danger" ? "danger" : ""}`;
  strip.classList.remove("hidden");
}

/* ===================== Weather ===================== */
const weatherCode = {
  0:["☀️","Clear sky"],1:["🌤️","Mainly clear"],2:["⛅","Partly cloudy"],3:["☁️","Overcast"],
  45:["🌫️","Fog"],48:["🌫️","Rime fog"],51:["🌦️","Light drizzle"],53:["🌦️","Drizzle"],55:["🌧️","Heavy drizzle"],
  61:["🌦️","Light rain"],63:["🌧️","Rain"],65:["🌧️","Heavy rain"],71:["🌨️","Light snow"],73:["🌨️","Snow"],75:["❄️","Heavy snow"],
  80:["🌦️","Rain showers"],81:["🌧️","Rain showers"],82:["⛈️","Heavy showers"],95:["⛈️","Thunderstorm"],96:["⛈️","Thunderstorm + hail"],99:["⛈️","Severe thunderstorm"]
};
function codeInfo(code){ return weatherCode[code] || ["🌤️","Weather"] }

async function loadWeather() {
  try {
    const d = await fetch(`/api/weather?location=${selectedLocation}`).then(r => r.json());
    const c = codeInfo(d.current.weather_code);
    document.getElementById("heroTemp").textContent = `${Math.round(d.current.temperature_2m)}°`;
    document.getElementById("heroCondition").textContent = c[1];
    document.getElementById("heroWeatherIcon").textContent = c[0];
    document.getElementById("heroHumidity").textContent = Math.round(d.current.relative_humidity_2m);
    document.getElementById("heroWind").textContent = Math.round(d.current.wind_speed_10m);
    document.getElementById("heroRain").textContent = Math.round(d.current.precipitation_probability ?? 0);

    document.getElementById("weatherIcon").textContent = c[0];
    document.getElementById("weatherTemp").textContent = `${Math.round(d.current.temperature_2m)}°C`;
    document.getElementById("weatherLabel").textContent = c[1];
    document.getElementById("weatherHumidity").textContent = `${Math.round(d.current.relative_humidity_2m)}%`;
    document.getElementById("weatherWind").textContent = `${Math.round(d.current.wind_speed_10m)} km/h`;
    document.getElementById("weatherPrecip").textContent = `${Math.round(d.current.precipitation_probability ?? 0)}%`;
    document.getElementById("weatherUV").textContent = d.current.uv_index == null ? "--" : d.current.uv_index.toFixed(1);
    document.getElementById("homeUV").textContent = d.current.uv_index == null ? "--" : d.current.uv_index.toFixed(1);
    const uv=d.current.uv_index ?? 0; document.getElementById("homeUVLabel").textContent = uv>=8?"Very high":uv>=6?"High":uv>=3?"Moderate":"Low";
    if(d.air_quality){ document.getElementById("aqiValue").textContent=d.air_quality.aqi ?? "--"; document.getElementById("homeAQI").textContent=d.air_quality.aqi ?? "--"; document.getElementById("aqiText").textContent=d.air_quality.label; document.getElementById("homeAQILabel").textContent=d.air_quality.label; }

    const hourly = d.hourly || [];
    document.getElementById("hourlyForecast").innerHTML = hourly.slice(0, 12).map(h => {
      const hc = codeInfo(h.weather_code);
      return `<div class="hour-card"><b>${h.time}</b><span>${hc[0]}</span><strong>${Math.round(h.temperature_2m)}°</strong><small>🌧️ ${Math.round(h.precipitation_probability ?? 0)}%</small></div>`;
    }).join("");

    document.getElementById("dailyForecast").innerHTML = (d.daily || []).map(day => {
      const dc = codeInfo(day.weather_code);
      return `<div class="day-card"><b>${day.date}</b><span>${dc[0]}</span><strong>${Math.round(day.temp_max)}° / ${Math.round(day.temp_min)}°</strong><small>${dc[1]} · 🌧️ ${Math.round(day.rain_probability ?? 0)}%</small></div>`;
    }).join("");

    document.getElementById("lastUpdated").textContent = `Updated ${new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})}`;
  } catch(e) {
    console.error(e);
    document.getElementById("heroCondition").textContent = "Weather unavailable";
  }
}

/* ===================== Risk + precautions ===================== */
let latestAlerts = [];
let latestLightning = [];
async function computeRisk() {
  try {
    const [alertsRes, lightningRes] = await Promise.all([
      fetch("/api/alerts").then(r => r.json()),
      fetch(`/api/lightning?location=${selectedLocation}`).then(r => r.json())
    ]);
    latestAlerts = alertsRes.alerts || [];
    latestLightning = lightningRes.strikes || [];
    const alertCount = latestAlerts.length, strikeCount = latestLightning.length;
    const badge = document.getElementById("riskBadge");
    if (alertCount > 0 || strikeCount >= 3) {
      badge.textContent = "⚠ High risk — active weather warnings nearby";
      badge.className = "risk-badge risk-high";
    } else if (strikeCount > 0) {
      badge.textContent = "◐ Moderate risk — lightning detected nearby";
      badge.className = "risk-badge risk-moderate";
    } else {
      badge.textContent = "✓ Low risk right now";
      badge.className = "risk-badge risk-low";
    }
    updatePrecautions();
  } catch(e){ console.error(e); }
}
function updatePrecautions(){
  const severe = latestAlerts.some(a => /severe|extreme/i.test(a.severity || ""));
  const lightning = latestLightning.length > 0;
  const rain = latestAlerts.some(a => /rain|flood|storm/i.test(`${a.title} ${a.event} ${a.summary}`));
  const banner = document.getElementById("precautionBanner");
  if(!banner) return;
  if (severe) {
    banner.className = "precaution-banner danger";
    banner.innerHTML = `<span>🚨</span><div><b>Take extra care</b><small>Official severe weather warnings are active. Follow local authority instructions.</small></div>`;
  } else if (lightning || rain) {
    banner.className = "precaution-banner warn";
    banner.innerHTML = `<span>🛡️</span><div><b>Be weather-ready</b><small>${lightning ? "Lightning is active nearby. " : ""}${rain ? "Rain/flood conditions may develop. " : ""}Limit unnecessary outdoor travel.</small></div>`;
  } else {
    banner.className = "precaution-banner safe";
    banner.innerHTML = `<span>✅</span><div><b>No major active warning detected</b><small>Continue checking official alerts as conditions can change quickly.</small></div>`;
  }
}

/* ===================== Windy map controls ===================== */
function setWindyOverlay(overlay){
  const frame = document.getElementById("windyRadarFrame");
  if(!frame) return;
  const base = "https://embed.windy.com/embed2.html?lat=13.0827&lon=80.2707&detailLat=13.0827&detailLon=80.2707&width=100%&height=100%&zoom=9&level=surface&product=ecmwf&menu=&message=true&marker=true&calendar=now&type=map&location=coordinates";
  frame.src = `${base}&overlay=${overlay}`;
  document.querySelectorAll(".map-switch").forEach(b => b.classList.toggle("active", b.dataset.windyOverlay === overlay));
}
document.querySelectorAll(".map-switch").forEach(btn => btn.addEventListener("click", () => setWindyOverlay(btn.dataset.windyOverlay)));

/* ===================== RainViewer map ===================== */
let rainMap, rainLayer, rainFrames = [], rainFrameIdx = 0, playing = false, playTimer;
function initRainMap() {
  const el = document.getElementById("rainMap");
  if(!el) return;
  rainMap = L.map("rainMap").setView([13.0827, 80.2707], 10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution:"&copy; OpenStreetMap contributors"}).addTo(rainMap);
  L.marker([13.0827,80.2707]).addTo(rainMap).bindPopup("Chennai");
  L.marker([12.9345,80.2145]).addTo(rainMap).bindPopup("Pallikaranai");
}
async function loadRainFrames() {
  try {
    const data = await fetch("/api/radar/rainviewer").then(r => r.json());
    rainFrames = [...data.past_frames, ...data.forecast_frames];
    const slider = document.getElementById("frameSlider");
    if (!slider) return;
    slider.max = Math.max(0, rainFrames.length - 1);
    slider.value = Math.max(0, data.past_frames.length - 1);
    rainFrameIdx = parseInt(slider.value,10);
    renderRainFrame();
  } catch(e){ console.error(e); }
}
function renderRainFrame(){
  if(!rainFrames.length || !rainMap) return;
  const frame = rainFrames[rainFrameIdx];
  if(rainLayer) rainMap.removeLayer(rainLayer);
  rainLayer = L.tileLayer(frame.tile_url_template,{opacity:.7}).addTo(rainMap);
  const d = new Date(frame.time*1000);
  const timeEl = document.getElementById("frameTime");
  if(timeEl) timeEl.textContent = d.toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"});
}
const sliderEl = document.getElementById("frameSlider");
if(sliderEl) sliderEl.addEventListener("input",e=>{rainFrameIdx=parseInt(e.target.value,10);renderRainFrame();});
const playBtnEl = document.getElementById("playBtn");
if(playBtnEl) playBtnEl.addEventListener("click",()=>{
  playing=!playing;
  playBtnEl.textContent=playing?"⏸ Pause":"▶ Play";
  if(playing) playTimer=setInterval(()=>{if(!rainFrames.length)return;rainFrameIdx=(rainFrameIdx+1)%rainFrames.length;sliderEl.value=rainFrameIdx;renderRainFrame();},700);
  else clearInterval(playTimer);
});

/* ===================== Lightning ===================== */
let lightningMap, lightningMarkers=[];
function initLightningMap(){
  const el = document.getElementById("lightningMap");
  if(!el) return;
  lightningMap=L.map("lightningMap").setView([13.0827,80.2707],10);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap contributors"}).addTo(lightningMap);
}
async function loadLightning(){
  try{
    const data=await fetch("/api/lightning").then(r=>r.json());
    document.getElementById("lightningSource").textContent=`Live strike feed: ${data.source}`;
    document.getElementById("strikeCount").textContent=data.strikes.length;
    document.getElementById("lightningRisk").textContent=data.strikes.length>=3?"High":data.strikes.length?"Moderate":"Low";
    if (!lightningMap) return;
    lightningMarkers.forEach(m=>lightningMap.removeLayer(m)); lightningMarkers=[];
    data.strikes.forEach(s=>{
      const marker=L.circleMarker([s.lat,s.lon],{radius:8,color:"#f59e0b",fillColor:"#fde047",fillOpacity:.9}).addTo(lightningMap);
      marker.bindPopup(`⚡ ${s.intensity_kA} kA<br>${new Date(s.time*1000).toLocaleTimeString()}`);
      lightningMarkers.push(marker);
    });
  }catch(e){console.error(e);}
}

/* ===================== Alerts ===================== */
async function loadAlerts(){
  const container=document.getElementById("alertsList");
  if(!container) return;
  try{
    const data=await fetch("/api/alerts").then(r=>r.json());
    latestAlerts=data.alerts||[];
    const severe=latestAlerts.filter(a=>/severe|extreme/i.test(a.severity||"")).length;
    document.getElementById("alertSummary").innerHTML=`
      <div class="summary-chip"><b>${latestAlerts.length}</b><span>Active</span></div>
      <div class="summary-chip danger-chip"><b>${severe}</b><span>Severe</span></div>
      <div class="summary-chip"><b>IMD</b><span>Source</span></div>`;
    if(!latestAlerts.length){
      container.innerHTML=`<div class="empty-state">No active cyclone / flood / rain warnings returned for Tamil Nadu right now.</div>`;
    }else{
      container.innerHTML=latestAlerts.map(a=>{
        const sevClass="sev-"+(a.severity||"unknown").toLowerCase();
        return `<div class="alert-card ${sevClass}">
          <div class="alert-icon">${/cyclone/i.test(a.title||a.event)?"🌀":/flood/i.test(a.title||a.event)?"🌊":/thunder|lightning/i.test(a.title||a.event)?"⚡":"🌧️"}</div>
          <div class="alert-content"><div class="alert-title">${a.headline||a.title}</div>
          <div class="alert-meta">${a.severity||"Unknown"} severity • ${a.area||"Tamil Nadu"} • ${a.published||""}</div>
          <div class="alert-summary">${(a.summary||a.description||"").slice(0,300)}</div>
          ${a.link?`<a href="${a.link}" target="_blank" rel="noopener" class="alert-link">View official alert ↗</a>`:""}</div>
        </div>`;
      }).join("");
    }
    updatePrecautions();
  }catch(e){container.innerHTML=`<div class="empty-state">Unable to load official alerts right now.</div>`;}
}
const refreshAlertsEl = document.getElementById("refreshAlerts");
if(refreshAlertsEl) refreshAlertsEl.addEventListener("click",()=>{loadAlerts();showToast("Refreshing official alerts…")});

/* ===================== News ===================== */
let newsItems=[];
function renderNews(filter="all"){
  const list=document.getElementById("newsList");
  if(!list) return;
  const items=filter==="all"?newsItems:newsItems.filter(n=>n.category===filter);
  if(!items.length){list.innerHTML=`<div class="empty-state">No stories in this category right now.</div>`;return;}
  list.innerHTML=items.map(n=>`
    <article class="news-card">
      <div class="news-icon">${n.icon||"📰"}</div>
      <div class="news-body"><span class="news-tag">${n.category}</span><h3>${n.title}</h3><p>${n.summary}</p>
      <div class="news-meta">${n.source} · ${n.published||""}</div>
      ${n.link?`<a href="${n.link}" target="_blank" rel="noopener" class="news-link">Read update ↗</a>`:""}</div>
    </article>`).join("");
}
async function loadNews(){
  try{
    newsItems=await fetch("/api/news").then(r=>r.json());
    const activeFilter = document.querySelector(".news-filter.active")?.dataset.newsFilter || "all";
    renderNews(activeFilter);
  } catch(e){
    const list = document.getElementById("newsList");
    if(list) list.innerHTML=`<div class="empty-state">News is temporarily unavailable.</div>`;
  }
}
document.querySelectorAll(".news-filter").forEach(btn=>btn.addEventListener("click",()=>{
  document.querySelectorAll(".news-filter").forEach(b=>b.classList.remove("active"));btn.classList.add("active");renderNews(btn.dataset.newsFilter);
}));
const refreshNewsEl = document.getElementById("refreshNews");
if(refreshNewsEl) refreshNewsEl.addEventListener("click",()=>{loadNews();showToast("Refreshing weather news…")});

const locSelect = document.getElementById("locationSelect");
if(locSelect) locSelect.addEventListener("change",e=>applyLocation(e.target.value));
const setLocSelect = document.getElementById("settingsLocation");
if(setLocSelect) setLocSelect.addEventListener("change",e=>{applyLocation(e.target.value);showToast(`Location changed to ${locations[e.target.value].name}`)});
const setNotifBtn = document.getElementById("settingsNotif");
if(setNotifBtn) setNotifBtn.addEventListener("click",()=>notifBtn.click());

/* ===================== Boot ===================== */
window.addEventListener("load",()=>{
  if(locSelect) locSelect.value=selectedLocation;
  if(setLocSelect) setLocSelect.value=selectedLocation;
  applyLocation(selectedLocation);
  initRainMap(); initLightningMap();
  loadWeather(); loadRainFrames(); loadLightning(); loadAlerts(); loadNews(); computeRisk();
  setInterval(loadWeather, 10*60*1000);
  setInterval(loadLightning, 45*1000);
  setInterval(loadAlerts, 180*1000);
  setInterval(loadNews, 10*60*1000);
  setInterval(computeRisk, 60*1000);
});
