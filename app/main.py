import re
from app.servicio import obtener_clima, obtener_clima_por_ubicacion
from app.formato import formatear_clima, traducir_clima


def es_ciudad_valida(ciudad):
    if not ciudad:
        return False, "⚠️ Debes ingresar una ciudad."

    if any(char.isdigit() for char in ciudad):
        return False, "❌ La ciudad no debe contener números."

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$", ciudad):
        return False, "❌ La ciudad contiene caracteres no válidos."

    return True, ""


def mostrar_menu():
    print("\n🌤️ MENÚ PRINCIPAL")
    print("1. Pronóstico del clima")
    print("2. Comparación de clima")
    print("3. Salir")


def seleccionar_ubicacion(coincidencias, nombre_ingresado):
    print(f"\n🌍 Se encontraron varias opciones para '{nombre_ingresado}':\n")

    for i, opcion in enumerate(coincidencias, start=1):
        print(f"{i}. {opcion['nombre']}, {opcion['pais']}")

    print("\nEscribe el número de la opción correcta.")
    print("Si deseas volver, escribe: salir\n")

    while True:
        seleccion = input("Selecciona una opción: ").strip()

        if seleccion.lower() == "salir":
            return None

        if not seleccion.isdigit():
            print("❌ Debes ingresar un número válido.\n")
            continue

        indice = int(seleccion) - 1

        if 0 <= indice < len(coincidencias):
            return coincidencias[indice]

        print("❌ Opción fuera de rango.\n")


def resolver_clima_con_seleccion(ciudad):
    resultado = obtener_clima(ciudad)

    if not resultado["ok"]:
        return resultado

    if resultado.get("seleccion_requerida"):
        ubicacion = seleccionar_ubicacion(resultado["coincidencias"], ciudad)

        if ubicacion is None:
            return {
                "ok": False,
                "error": "↩️ Selección cancelada. Volviendo..."
            }

        return obtener_clima_por_ubicacion(ubicacion)

    return resultado


def ejecutar_pronostico():
    print("\n🌦️ MODO: Pronóstico del clima")
    print("Escribe una ciudad para consultar el clima.")
    print("Si deseas volver al menú, escribe: salir\n")

    while True:
        ciudad = input("🌍 Ingresa una ciudad: ").strip()

        if ciudad.lower() == "salir":
            print("↩️ Volviendo al menú principal...\n")
            break

        es_valida, mensaje_error = es_ciudad_valida(ciudad)
        if not es_valida:
            print(mensaje_error)
            print()
            continue

        resultado = resolver_clima_con_seleccion(ciudad)
        mensaje = formatear_clima(resultado)

        print(mensaje)
        print("\n💡 Si deseas volver al menú, escribe 'salir'.\n")


def ejecutar_comparacion():
    print("\n📊 MODO: Comparación de clima")
    print("Ingresa una ciudad a la vez.")
    print("Si una ciudad existe en más de un país, podrás elegir la opción correcta.")
    print("Si deseas volver al menú, escribe: salir\n")

    resultados = []

    while True:
        ciudad = input("🌍 Ingresa una ciudad: ").strip()

        if ciudad.lower() == "salir":
            print("↩️ Volviendo al menú principal...\n")
            break

        es_valida, mensaje_error = es_ciudad_valida(ciudad)
        if not es_valida:
            print(mensaje_error)
            print()
            continue

        resultado = resolver_clima_con_seleccion(ciudad)

        if resultado["ok"]:
            datos = resultado["datos"]
            resultados.append({
                "ciudad": datos.get("ciudad"),
                "pais": datos.get("pais"),
                "temperatura": datos.get("temperatura"),
                "viento": datos.get("viento"),
                "humedad": datos.get("humedad"),
                "estado": traducir_clima(datos.get("codigo_clima")),
            })
            print(f"✅ Se agregó: {datos.get('ciudad')}, {datos.get('pais')}\n")
        else:
            print(resultado["error"])
            print()
            continue

        while True:
            agregar_otra = input("¿Quieres agregar otra ciudad? (si/no): ").strip().lower()

            if agregar_otra == "si":
                print()
                break

            if agregar_otra == "no":
                if not resultados:
                    print("⚠️ No hay ciudades para comparar.\n")
                    return

                print("\n📋 COMPARACIÓN DEL CLIMA ACTUAL:\n")

                for item in resultados:
                    print(
                        f"📍 {item['ciudad']}, {item['pais']} | "
                        f"🌡️ {item['temperatura']}°C | "
                        f"🌬️ {item['viento']} km/h | "
                        f"💧 {item['humedad']}% | "
                        f"☁️ {item['estado']}"
                    )

                print("\n💡 Comparación finalizada. Volviendo al menú principal...\n")
                return

            if agregar_otra == "salir":
                print("↩️ Volviendo al menú principal...\n")
                return

            print("❌ Responde 'si', 'no' o 'salir'.\n")


def ejecutar_app():
    print("🌤️ Bienvenido a la aplicación del clima")

    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip().lower()

        if opcion == "1":
            ejecutar_pronostico()

        elif opcion == "2":
            ejecutar_comparacion()

        elif opcion == "3" or opcion == "salir":
            print("👋 Cerrando la aplicación. ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida. Intenta nuevamente.\n")