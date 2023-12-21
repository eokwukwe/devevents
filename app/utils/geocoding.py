import googlemaps
from typing import Dict

from app.utils.config import settings

gmaps = googlemaps.Client(key=settings.google_api_key)


def get_latlng(address: str) -> Dict[str, float]:
    geocode_result = gmaps.geocode(address)
    return geocode_result[0]['geometry']['location']
