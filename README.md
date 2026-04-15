# 🌤️ Aplicación de Clima en Python

Aplicación de consola desarrollada en Python que permite consultar el clima actual de una ciudad utilizando la API de Open-Meteo.

Este proyecto está diseñado con fines educativos, aplicando buenas prácticas de desarrollo como validación de datos, separación de responsabilidades y manejo de errores, con el objetivo de evolucionar desde un nivel principiante hacia un desarrollo más profesional.

---

## 🚀 Características

- 🔍 Consulta de clima por nombre de ciudad
- 🌎 Obtención automática de ubicación (latitud y longitud)
- 🌡️ Temperatura actual
- 🌬️ Velocidad del viento
- ☁️ Descripción del estado del clima
- 🔁 Consultas múltiples sin reiniciar la aplicación
- 🚪 Salida controlada mediante comando `salir`

### 🛡️ Validaciones de entrada

- ❌ No permite números (`123`, `Santiago123`)
- ❌ No permite caracteres especiales inválidos (`@@@`, `###`)
- ❌ No permite entradas vacías
- ✅ Acepta mayúsculas y minúsculas (`Santiago`, `santiago`)
- ✅ Soporta tildes (`Bogotá`, `São Paulo`)

---

## 🧱 Estructura del proyecto
clima_app/
│
├─ app/
│ ├─ main.py # Lógica principal (interacción con el usuario)
│ ├─ servicio.py # Consumo de la API y lógica de negocio
│ ├─ formato.py # Formateo de datos para mostrar en consola
│ └─ config.py # Configuración (URLs, timeout)
│
├─ run.py # Punto de entrada
├─ requirements.txt # Dependencias
└─ README.md # Documentación

---

## ⚙️ Requisitos

- Python 3.10 o superior
- Librería `requests`

---

## 📦 Instalación

1. Clonar o descargar el proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd clima_app
Instalar dependencias:
pip install -r requirements.txt
▶️ Ejecución
python run.py
🧪 Ejemplo de uso
🌤️ Bienvenido a la aplicación del clima
Escribe una ciudad para consultar el clima.
Si deseas salir, escribe: salir

🌍 Ingresa una ciudad: Santiago

📍 Santiago, Chile
🌡️ Temperatura: 18.2°C
🌬️ Viento: 5.1 km/h
☁️ Estado: Parcialmente nublado ⛅

💡 Si deseas salir, escribe 'salir' en la próxima consulta.

⚠️ Manejo de errores

La aplicación maneja distintos escenarios:

❌ Ciudad no encontrada
❌ Problemas de conexión a internet
❌ Timeout del servicio
❌ Respuestas inválidas de la API

Los errores se muestran de forma clara y amigable para el usuario.

🧠 Arquitectura del proyecto

El proyecto está organizado en capas para facilitar su mantenimiento y escalabilidad:

main.py → Maneja la interacción con el usuario
servicio.py → Gestiona la lógica de negocio y llamadas a la API
formato.py → Convierte los datos en texto legible
config.py → Centraliza la configuración

Esta separación permite:

Mejorar la legibilidad
Facilitar pruebas
Escalar el proyecto a futuro (API, GUI, etc.)
🔧 Tecnologías utilizadas
Python
Requests (para consumo de APIs)
Open-Meteo API (datos meteorológicos)