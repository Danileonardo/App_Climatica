import re
import requests
from app.config import URL_GEOCODING, URL_CLIMA, DIAS_PRONOSTICO, TIMEOUT_SEGUNDOS, IDIOMA


def validar_ciudad(ciudad):
    ciudad = ciudad.strip()

    if not ciudad:
        return False, "⚠️ Debes ingresar una ciudad o ubicación."

    if ciudad.lower() == "salir":
        return True, ""

    if any(char.isdigit() for char in ciudad):
        return False, "❌ La ciudad no debe contener números."

    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\-\.\,]+$"
    if not re.match(patron, ciudad):
        return False, "❌ La ciudad contiene caracteres no válidos."

    if len(ciudad) < 2:
        return False, "❌ Debes ingresar al menos 2 letras."

    return True, ""


def obtener_coordenadas(ciudad):
    params = {
        "name": ciudad.strip(),
        "count": 1,
        "language": IDIOMA,
        "format": "json",
    }

    try:
        response = requests.get(URL_GEOCODING, params=params, timeout=TIMEOUT_SEGUNDOS)
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
            "timezone": lugar.get("timezone", "auto"),
        }

    except requests.RequestException:
        return {"error": "❌ No se pudo conectar con el servicio de ubicaciones."}


def obtener_clima(ciudad):
    ubicacion = obtener_coordenadas(ciudad)

    if not ubicacion:
        return {"error": "❌ No se encontró la ciudad o ubicación indicada."}

    if "error" in ubicacion:
        return ubicacion

    params = {
        "latitude": ubicacion["latitud"],
        "longitude": ubicacion["longitud"],
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "weather_code",
            "rain",
            "showers",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
        "timezone": ubicacion["timezone"],
        "forecast_days": DIAS_PRONOSTICO,
    }

    try:
        response = requests.get(URL_CLIMA, params=params, timeout=TIMEOUT_SEGUNDOS)
        response.raise_for_status()
        data = response.json()

        actual = data.get("current")
        diario = data.get("daily")

        if not actual or not diario:
            return {"error": "❌ No se pudo obtener la información del clima."}

        pronostico = []
        fechas = diario.get("time", [])
        codigos = diario.get("weather_code", [])
        maximas = diario.get("temperature_2m_max", [])
        minimas = diario.get("temperature_2m_min", [])
        lluvias = diario.get("precipitation_probability_max", [])

        for i in range(min(len(fechas), DIAS_PRONOSTICO)):
            pronostico.append({
                "fecha": fechas[i],
                "codigo_clima": codigos[i] if i < len(codigos) else None,
                "temp_max": maximas[i] if i < len(maximas) else None,
                "temp_min": minimas[i] if i < len(minimas) else None,
                "prob_lluvia": lluvias[i] if i < len(lluvias) else None,
            })

        return {
            "ciudad": ubicacion["nombre"],
            "pais": ubicacion["pais"],
            "temperatura": actual.get("temperature_2m"),
            "viento": actual.get("wind_speed_10m"),
            "codigo_clima": actual.get("weather_code"),
            "lluvia_actual": actual.get("rain"),
            "chubascos_actuales": actual.get("showers"),
            "pronostico": pronostico,
        }

    except requests.RequestException:
        return {"error": "❌ No se pudo conectar con el servicio del clima."}