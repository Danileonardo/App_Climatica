import os

URL_GEOCODING = os.getenv(
    "OPENMETEO_GEOCODING_URL",
    "https://geocoding-api.open-meteo.com/v1/search"
)

URL_CLIMA = os.getenv(
    "OPENMETEO_BASE_URL",
    "https://api.open-meteo.com/v1/forecast"
)

TIMEOUT = 10
DIAS_PRONOSTICO = 7
IDIOMA = "es"