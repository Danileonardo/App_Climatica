from app.servicio import obtener_clima
from app.formato import formatear_clima


def ejecutar_app():
    ciudad = input("🌍 Ingresa una ciudad: ").strip()

    if not ciudad:
        print("⚠️ Debes ingresar una ciudad.")
        return

    datos_clima = obtener_clima(ciudad)
    mensaje = formatear_clima(datos_clima)

    print(mensaje)