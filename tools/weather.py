import os

import requests
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city using a real weather API."""
    cities = {
        "Tokyo": {
            "latitude": 35.6762,
            "longitude": 139.6503,
        },
        "Paris": {
            "latitude": 48.8566,
            "longitude": 2.3522,
        },
        "London": {
            "latitude": 51.5074,
            "longitude": -0.1278,
        },
    }

    if city not in cities:
        return {
            "error": "City coordinates are not found",
        }

    api_url = os.getenv("WEATHER_API")

    params = {
        "latitude": cities[city]["latitude"],
        "longitude": cities[city]["longitude"],
        "current": "temperature_2m,weather_code",
    }

    max_retries = int(os.getenv("WEATHER_API_MAX_RETRIES", "3"))
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Weather API attempt {attempt}/{max_retries}")
            response = requests.get(
                url=api_url,
                params=params,
                timeout=5,
            )
            response.raise_for_status()

            data = response.json()
            current_weather = data["current"]

            return {
                "weather": {
                    "city": city,
                    "temperature": current_weather["temperature_2m"],
                    "weather_code": current_weather["weather_code"],
                }
            }


        except requests.RequestException as e:
            print(
                f"Weather API failed: {e}"
            )

            if attempt == max_retries:
                return {
                    "success": False,
                    "error": (
                        "Weather service is currently "
                        "unavailable after 3 attempts."
                    ),
                }
    return {
        "weather": None,
        "error": "Weather service unavailable"
    }
