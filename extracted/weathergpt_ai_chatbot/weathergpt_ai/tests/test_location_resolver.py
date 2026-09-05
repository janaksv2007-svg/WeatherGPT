from app.location.message_resolver import (
    extract_city_candidates,
    resolve_location_from_message,
)


def test_extract_city():
    candidates = extract_city_candidates(
        "What's the weather in Tokyo tomorrow?"
    )

    assert "Tokyo" in candidates


def test_resolve_tokyo():
    city = resolve_location_from_message(
        "What's the weather in Tokyo tomorrow?"
    )

    assert city is not None
    assert city["name"] == "Tokyo"
    assert city["country_code"] == "JP"


def test_resolve_london():
    city = resolve_location_from_message(
        "Will it rain in London?"
    )

    assert city is not None
    assert city["name"] == "London"
    assert city["country_code"] == "GB"


def test_resolve_coimbatore():
    city = resolve_location_from_message(
        "Weather in Coimbatore"
    )

    assert city is not None
    assert city["name"] == "Coimbatore"
    assert city["country_code"] == "IN"