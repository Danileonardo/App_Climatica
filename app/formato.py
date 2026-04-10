def traducir_clima(codigo):
    mapa = {
        0: "Despejado ☀️",
        1: "Principalmente despejado 🌤️",
        2: "Parcialmente nublado ⛅",
        3: "Nublado ☁️",
        45: "Niebla 🌫️",
        48: "Niebla con escarcha 🌫️",
        51: "Llovizna ligera 🌦️",
        61: "Lluvia ligera 🌧️",
        63: "Lluvia moderada 🌧️",
        65: "Lluvia intensa 🌧️",
        71: "Nieve ligera ❄️",
        95: "Tormenta ⛈️",
    }
    return mapa.get(codigo, "Clima desconocido")


def formatear_clima(datos):
    if not datos:
        return "❌ No se pudo obtener información del clima."

    descripcion = traducir_clima(datos.get("codigo_clima"))

    return (
        f"\n📍 {datos.get('ciudad')}, {datos.get('pais')}\n"
        f"🌡️ Temperatura: {datos.get('temperatura')}°C\n"
        f"🌬️ Viento: {datos.get('viento')} km/h\n"
        f"☁️ Estado: {descripcion}"
    )