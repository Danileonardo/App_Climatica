from app.servicio import obtener_clima, validar_ciudad
from app.formato import formatear_clima


def ejecutar_app():
    print("🌤️ Bienvenido a la aplicación del clima")
    print("Consulta el clima actual y el pronóstico de hasta 7 días.")
    print("👉 Puedes escribir una ciudad o ubicación.")
    print("👉 Si deseas salir, escribe: salir\n")

    while True:
        ciudad = input("🌍 Ingresa una ciudad: ").strip()

        es_valida, mensaje_error = validar_ciudad(ciudad)

        if not es_valida:
            print(mensaje_error)
            print()
            continue

        if ciudad.lower() == "salir":
            print("👋 Cerrando la aplicación. ¡Hasta luego!")
            break

        datos_clima = obtener_clima(ciudad)
        mensaje = formatear_clima(datos_clima)

        print(mensaje)
        print("\n💡 Si deseas salir, escribe 'salir' en la próxima consulta.\n")