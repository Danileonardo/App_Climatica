import requests
from app.config import URL_GEOCODING, URL_CLIMA


def obtener_coordenadas(ciudad):
    params = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json",
    }

    try:
        response = requests.get(URL_GEOCODING, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        resultados = data.get("results")
        if not resultados:
            return None

        lugar = resultados[0]

        return {
            "nombre": lugar.get("name"),
            "pais": lugar.get("country"),
            "latitud": lugar.get("latitude"),
            "longitud": lugar.get("longitude"),
        }

    except Exception as e:
        print("❌ Error al obtener coordenadas:", e)
        return None


def obtener_clima(ciudad):
    ubicacion = obtener_coordenadas(ciudad)

    if not ubicacion:
        return None

    params = {
        "latitude": ubicacion["latitud"],
        "longitude": ubicacion["longitud"],
        "current_weather": "true",
    }

    try:
        response = requests.get(URL_CLIMA, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        clima_actual = data.get("current_weather")
        if not clima_actual:
            return None

        return {
            "ciudad": ubicacion["nombre"],
            "pais": ubicacion["pais"],
            "temperatura": clima_actual.get("temperature"),
            "viento": clima_actual.get("windspeed"),
            "codigo_clima": clima_actual.get("weathercode"),
        }

    except Exception as e:
        print("❌ Error al obtener clima:", e)
        return None