from typing import Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TimeInfo(BaseModel):
    date: Optional[str] = None
    time_period: Optional[str] = None
    exact_time: Optional[str] = None


class Parameters(BaseModel):
    rainfall_change_mm: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    target_rainfall_mm: Optional[float] = None


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatAnalysis(BaseModel):
    message: str
    intent: str

    # Main location
    location: Location

    # Second location for WEATHER_COMPARISON
    comparison_location: Optional[Location] = None

    time: TimeInfo
    language: str = "en"
    parameters: Parameters = Field(default_factory=Parameters)

    requires_weather_data: bool = False
    requires_risk_analysis: bool = False
    requires_simulation: bool = False


class ChatResponse(BaseModel):
    analysis: ChatAnalysis
    response: str