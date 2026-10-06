import os

import requests
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city using a real weather API."""

    api_url = os.getenv("WEATHER_API")

    params = {
        "name": city,
        "count": 1
    }

    max_retries = int(os.getenv("WEATHER_API_MAX_RETRIES", "3"))
    for attempt in range(1, max_retries + 1):
        try:
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
