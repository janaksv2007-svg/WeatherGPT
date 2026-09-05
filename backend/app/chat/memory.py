from typing import Dict, Any, Optional

_sessions: Dict[str, Dict[str, Any]] = {}


def get_session(session_id: str) -> Dict[str, Any]:
    return _sessions.setdefault(
        session_id,
        {
            "location": None,
            "time": {
                "date": None,
                "time_period": None,
            },
            "language": "en",
        },
    )


def update_session(
    session_id: str,
    location: Optional[str] = None,
    time: Optional[Dict[str, Any]] = None,
    language: Optional[str] = None,
):
    session = get_session(session_id)

    if location:
        session["location"] = location

    if time:
        old_time = session.get("time") or {}

        if time.get("date") is not None:
            old_time["date"] = time["date"]

        if time.get("time_period") is not None:
            old_time["time_period"] = time["time_period"]

        session["time"] = old_time

    if language:
        session["language"] = language

    return session


def has_context(session_id: str) -> bool:
    session = get_session(session_id)
    return session.get("location") is not None


def get_location(session_id: str) -> Optional[str]:
    return get_session(session_id).get("location")


def get_time(session_id: str) -> Dict[str, Any]:
    return get_session(session_id).get("time") or {
        "date": None,
        "time_period": None,
    }


def clear_session(session_id: str):
    _sessions.pop(session_id, None)