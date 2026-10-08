import os

import requests
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city using a real weather API."""

    geocoding_url = os.getenv("WEATHER_API", "https://geocoding-api.open-meteo.com/v1/search")
    forecast_url = os.getenv("WEATHER_FORECAST_API", "https://api.open-meteo.com/v1/forecast")

    max_retries = int(os.getenv("WEATHER_API_MAX_RETRIES", "3"))
    for attempt in range(1, max_retries + 1):
        try:
            geo_response = requests.get(
                url=geocoding_url,
                params={"name": city, "count": 1},
                timeout=5,
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            results = geo_data.get("results")
            if not results:
                return {
                    "weather": None,
                    "error": f"City '{city}' not found."
                }

            lat = results[0]["latitude"]
            lon = results[0]["longitude"]

            weather_response = requests.get(
                url=forecast_url,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,weather_code",
                },
                timeout=5,
            )
            weather_response.raise_for_status()

            weather_data = weather_response.json()
            current_weather = weather_data.get("current", {})

            return {
                "weather": {
                    "city": city,
                    "temperature": current_weather.get("temperature_2m"),
                    "weather_code": current_weather.get("weather_code"),
                }
            }

        except Exception as e:
            print(f"Weather API failed (attempt {attempt}): {e}")

            if attempt == max_retries:
                return {
                    "weather": None,
                    "error": "Weather service is currently unavailable after retries."
                }

    return {
        "weather": None,
        "error": "Weather service unavailable"
    }
