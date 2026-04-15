import requests
import unicodedata
from app.config import URL_GEOCODING, URL_CLIMA, TIMEOUT, DIAS_PRONOSTICO, IDIOMA


def normalizar_texto(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(char for char in texto if unicodedata.category(char) != "Mn")
    return " ".join(texto.split())


def buscar_coincidencias_ciudad(ciudad):
    params = {
        "name": ciudad,
        "count": 10,
        "language": IDIOMA,
        "format": "json",
    }

    try:
        response = requests.get(URL_GEOCODING, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        resultados = data.get("results")
        if not resultados:
            return {
                "ok": False,
                "error": "❌ No se encontró la ciudad indicada."
            }

        coincidencias = []
        vistos = set()

        for lugar in resultados:
            nombre = (lugar.get("name") or "").strip()
            pais = (lugar.get("country") or "").strip()

            clave = (
                normalizar_texto(nombre),
                normalizar_texto(pais)
            )

            if clave in vistos:
                continue

            vistos.add(clave)

            coincidencias.append({
                "nombre": nombre,
                "pais": pais,
                "latitud": lugar.get("latitude"),
                "longitud": lugar.get("longitude"),
                "timezone": lugar.get("timezone", "auto"),
            })

        return {
            "ok": True,
            "coincidencias": coincidencias
        }

    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "error": "❌ El servicio de ubicaciones tardó demasiado en responder."
        }

    except requests.exceptions.ConnectionError:
        return {
            "ok": False,
            "error": "❌ No se pudo conectar con el servicio de ubicaciones."
        }

    except requests.exceptions.HTTPError:
        return {
            "ok": False,
            "error": "❌ El servicio de ubicaciones devolvió un error."
        }

    except requests.exceptions.RequestException:
        return {
            "ok": False,
            "error": "❌ Ocurrió un problema al consultar la ubicación."
        }


def obtener_coordenadas(ciudad):
    resultado_busqueda = buscar_coincidencias_ciudad(ciudad)

    if not resultado_busqueda["ok"]:
        return resultado_busqueda

    coincidencias = resultado_busqueda["coincidencias"]

    if len(coincidencias) == 1:
        return {
            "ok": True,
            "datos": coincidencias[0]
        }

    ciudad_usuario = normalizar_texto(ciudad)

    coincidencias_filtradas = []
    for opcion in coincidencias:
        nombre_normalizado = normalizar_texto(opcion["nombre"])
        pais_normalizado = normalizar_texto(opcion["pais"] or "")

        if (
            ciudad_usuario == nombre_normalizado
            or ciudad_usuario in nombre_normalizado
            or ciudad_usuario in f"{nombre_normalizado} {pais_normalizado}"
        ):
            coincidencias_filtradas.append(opcion)

    if len(coincidencias_filtradas) == 1:
        return {
            "ok": True,
            "datos": coincidencias_filtradas[0]
        }

    if len(coincidencias_filtradas) > 1:
        return {
            "ok": True,
            "seleccion_requerida": True,
            "coincidencias": coincidencias_filtradas
        }

    return {
        "ok": True,
        "seleccion_requerida": True,
        "coincidencias": coincidencias
    }


def obtener_clima_por_ubicacion(ubicacion):
    params = {
        "latitude": ubicacion["latitud"],
        "longitude": ubicacion["longitud"],
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "weather_code",
            "relative_humidity_2m",
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
        response = requests.get(URL_CLIMA, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        actual = data.get("current")
        diario = data.get("daily")

        if not actual or not diario:
            return {
                "ok": False,
                "error": "❌ No se pudo obtener la información del clima."
            }

        pronostico = []
        fechas = diario.get("time", [])
        codigos = diario.get("weather_code", [])
        maximas = diario.get("temperature_2m_max", [])
        minimas = diario.get("temperature_2m_min", [])
        lluvias = diario.get("precipitation_probability_max", [])

        total_dias = min(len(fechas), DIAS_PRONOSTICO)

        for i in range(total_dias):
            pronostico.append({
                "fecha": fechas[i],
                "codigo_clima": codigos[i] if i < len(codigos) else None,
                "temp_max": maximas[i] if i < len(maximas) else None,
                "temp_min": minimas[i] if i < len(minimas) else None,
                "prob_lluvia": lluvias[i] if i < len(lluvias) else None,
            })

        return {
            "ok": True,
            "datos": {
                "ciudad": ubicacion["nombre"],
                "pais": ubicacion["pais"],
                "temperatura": actual.get("temperature_2m"),
                "viento": actual.get("wind_speed_10m"),
                "codigo_clima": actual.get("weather_code"),
                "humedad": actual.get("relative_humidity_2m"),
                "pronostico": pronostico,
            }
        }

    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "error": "❌ El servicio del clima tardó demasiado en responder."
        }

    except requests.exceptions.ConnectionError:
        return {
            "ok": False,
            "error": "❌ No se pudo conectar con el servicio del clima."
        }

    except requests.exceptions.HTTPError:
        return {
            "ok": False,
            "error": "❌ El servicio del clima devolvió un error."
        }

    except requests.exceptions.RequestException:
        return {
            "ok": False,
            "error": "❌ Ocurrió un problema al consultar el clima."
        }


def obtener_clima(ciudad):
    resultado_ubicacion = obtener_coordenadas(ciudad)

    if not resultado_ubicacion["ok"]:
        return resultado_ubicacion

    if resultado_ubicacion.get("seleccion_requerida"):
        return resultado_ubicacion

    ubicacion = resultado_ubicacion["datos"]
    return obtener_clima_por_ubicacion(ubicacion)