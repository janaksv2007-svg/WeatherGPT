from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator


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
    session_id: str = Field(default="default")
    message: str = Field(..., min_length=1)
    language: str = Field(default="en")


class ChatAnalysis(BaseModel):
    message: Optional[str] = ""
    intent: str = "UNKNOWN"

    # Main location (Optional)
    location: Optional[Location] = None

    # Second location for WEATHER_COMPARISON
    comparison_location: Optional[Location] = None

    time: Optional[TimeInfo] = Field(default_factory=TimeInfo)
    language: str = "en"
    parameters: Optional[Parameters] = Field(default_factory=Parameters)

    requires_weather_data: bool = False
    requires_risk_analysis: bool = False
    requires_simulation: bool = False

    @field_validator("location", "comparison_location", mode="before")
    @classmethod
    def parse_location(cls, v: Any):
        if v is None:
            return None
        if isinstance(v, str):
            return {"name": v}
        return v

    @field_validator("time", mode="before")
    @classmethod
    def parse_time(cls, v: Any):
        if v is None:
            return TimeInfo()
        if isinstance(v, str):
            return {"date": v}
        return v

    @field_validator("parameters", mode="before")
    @classmethod
    def parse_parameters(cls, v: Any):
        if v is None or isinstance(v, (list, str)):
            return Parameters()
        return v


class ChatResponse(BaseModel):
    analysis: ChatAnalysis
    response: str