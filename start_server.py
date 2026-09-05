"""
WeatherGPT 1-Click Server Launcher
Starts the Unified FastAPI Backend Engine on http://localhost:8000
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

import uvicorn

if __name__ == "__main__":
    print("=" * 65)
    print(" [WeatherGPT] Launching WeatherGPT Unified API Engine v2.0.0")
    print(" [Server URL] http://localhost:8000")
    print(" [API Docs]   http://localhost:8000/docs")
    print(" [Mobile App] Connect Flutter to http://127.0.0.1:8000")
    print("=" * 65)

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
