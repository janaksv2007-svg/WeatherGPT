from fastapi import FastAPI
from pydantic import BaseModel

from app.chat.chatbot import chat_response


app = FastAPI(
    title="WeatherGPT AI Chatbot",
    description="AI chatbot and intent analysis module for WeatherGPT",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    language: str = "en"


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "WeatherGPT AI Chatbot"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    result = chat_response(
        message=request.message,
        session_id=request.session_id,
        language=request.language,
    )

    return result


@app.post("/analyze")
def analyze(request: ChatRequest):

    result = chat_response(
        message=request.message,
        session_id=request.session_id,
        language=request.language,
    )

    return {
        "session_id": request.session_id,
        "message": request.message,
        "analysis": result.get("analysis"),
    }