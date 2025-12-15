import os
import json
import urllib.request
import urllib.parse
from typing import Tuple

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("pk.eyJ1Ijoia2xpbmVyZXN0IiwiYSI6ImNtajZlajk3MzFpcmUzZHB1OHd0azA5NWgifQ.U39wEN6nBNZYuW2Sb-LB_Q")
MBTA_API_KEY = os.getenv("pk.eyJ1Ijoia2xpbmVyZXN0IiwiYSI6ImNtajZlajk3MzFpcmUzZHB1OHd0azA5NWgifQ.U39wEN6nBNZYuW2Sb-LB_Q")


# Base URLs
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)


def build_mapbox_url(place_name: str) -> str:
    """Build a Mapbox forward-geocoding URL for a place name."""
    query = urllib.parse.quote(place_name)
    # Use the Mapbox geocoding endpoint
    return f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&limit=1"


def get_lat_lng(place_name: str) -> Tuple[str, str]:
    url = build_mapbox_url(place_name)
    data = get_json(url)

    features = data.get("features") or []
    if not features:
        raise ValueError("No geocoding results for place: %s" % place_name)

    feature = features[0]
    lng, lat = feature["geometry"]["coordinates"]

    return str(lat), str(lng)


def get_nearest_station(latitude: str, longitude: str) -> Tuple[str, bool]:
    url = (
        f"{MBTA_BASE_URL}"
        f"?api_key={MBTA_API_KEY}"
        f"&filter[latitude]={latitude}"
        f"&filter[longitude]={longitude}"
        f"&sort=distance"
    )

    data = get_json(url)
    stops = data.get("data") or []
    if not stops:
        raise ValueError("No MBTA stops found near the provided coordinates.")

    stop = stops[0]
    name = stop["attributes"].get("name")
    wheelchair = stop["attributes"].get("wheelchair_boarding") == 1

    return name, wheelchair


def find_stop_near(place_name: str) -> Tuple[str, bool]:
    lat, lng = get_lat_lng(place_name)
    return get_nearest_station(lat, lng)
