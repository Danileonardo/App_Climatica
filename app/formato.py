from datetime import datetime


def traducir_clima(codigo):
    mapa = {
        0: "Despejado ☀️",
        1: "Principalmente despejado 🌤️",
        2: "Parcialmente nublado ⛅",
        3: "Nublado ☁️",
        45: "Niebla 🌫️",
        48: "Niebla con escarcha 🌫️",
        51: "Llovizna ligera 🌦️",
        53: "Llovizna moderada 🌦️",
        55: "Llovizna intensa 🌧️",
        61: "Lluvia ligera 🌧️",
        63: "Lluvia moderada 🌧️",
        65: "Lluvia intensa 🌧️",
        71: "Nieve ligera ❄️",
        73: "Nieve moderada ❄️",
        75: "Nieve intensa ❄️",
        80: "Chubascos ligeros 🌦️",
        81: "Chubascos moderados 🌧️",
        82: "Chubascos intensos 🌧️",
        95: "Tormenta ⛈️",
    }
    return mapa.get(codigo, "Clima desconocido")


def formatear_fecha(fecha_iso):
    try:
        fecha = datetime.strptime(fecha_iso, "%Y-%m-%d")
        return fecha.strftime("%d-%m-%Y")
    except ValueError:
        return fecha_iso


def formatear_clima(resultado):
    if not resultado["ok"]:
        return resultado["error"]

    datos = resultado["datos"]
    descripcion_actual = traducir_clima(datos.get("codigo_clima"))

    lineas = [
        "",
        f"📍 {datos.get('ciudad')}, {datos.get('pais')}",
        f"🌡️ Temperatura actual: {datos.get('temperatura')}°C",
        f"🌬️ Viento actual: {datos.get('viento')} km/h",
        f"💧 Humedad actual: {datos.get('humedad')}%",
        f"☁️ Estado actual: {descripcion_actual}",
        "",
        "📅 Pronóstico de los próximos 7 días:"
    ]

    for dia in datos.get("pronostico", []):
        descripcion = traducir_clima(dia.get("codigo_clima"))
        fecha = formatear_fecha(dia.get("fecha"))
        temp_min = dia.get("temp_min")
        temp_max = dia.get("temp_max")
        prob_lluvia = dia.get("prob_lluvia")

        lineas.append(
            f"- {fecha} | {descripcion} | "
            f"Mín: {temp_min}°C | Máx: {temp_max}°C | "
            f"Prob. lluvia: {prob_lluvia}%"
        )

    return "\n".join(lineas)