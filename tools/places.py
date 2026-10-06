from langchain_core.tools import tool


@tool
def search_places(city: str) -> dict:
    """Find recommended places to visit in a city."""

    places = {
        "Tokyo": [
            "Senso-ji Temple",
            "Meiji Shrine",
            "Shibuya Crossing",
            "Tokyo Skytree",
        ]
    }

    return {
        "places": places.get(city, [])
    }
