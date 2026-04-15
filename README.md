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

```text
clima_app/
│
├─ app/
│  ├─ main.py          # Lógica principal
│  ├─ servicio.py      # API y lógica
│  ├─ formato.py       # Salida en consola
│  └─ config.py        # Configuración
│
├─ run.py
├─ requirements.txt
└─ README.md

---

## ⚙️ Requisitos

- Python 3.10 o superior
- Librería `requests`

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd clima_app

2. Instalar dependencias:
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

## 📚 Dependencias y licencias de terceros

Este proyecto utiliza las siguientes bibliotecas y servicios de terceros:

- **requests** — Licencia Apache-2.0
- **Open-Meteo API** — Uso gratuito sin API key para fines no comerciales, sujeto a sus términos de uso y condiciones de licencia de datos

Referencias oficiales:
- Requests (PyPI): https://pypi.org/project/requests/
- Open-Meteo Terms: https://open-meteo.com/en/terms
- Open-Meteo Licence: https://open-meteo.com/en/licence

## 🔐 Seguridad y configuración

Actualmente este proyecto no requiere claves de API para funcionar con Open-Meteo.

Sin embargo, si en el futuro se integra otro proveedor que sí requiera credenciales:

- Las claves **no deben almacenarse** en `config.py`
- Las claves **no deben subirse** al repositorio
- Deben usarse **variables de entorno** o un archivo `.env` ignorado por Git

Archivos recomendados:
- `.env.example` → ejemplo de variables
- `.env` → archivo local no versionado
- `.gitignore` → debe incluir `.env`

## 🔒 Privacidad y uso de datos

Esta aplicación no almacena de forma persistente la información ingresada por el usuario, como nombres de ciudades o ubicaciones.

Sin embargo, para obtener datos meteorológicos:

- Las consultas de ciudades ingresadas por el usuario se envían a la API de Open-Meteo
- La API procesa estas consultas para obtener coordenadas geográficas y datos del clima

### Consideraciones

- No se guarda historial de ciudades consultadas
- No se almacenan coordenadas en archivos ni bases de datos
- No se recolecta información personal del usuario

### Futuras mejoras

En caso de que la aplicación evolucione para utilizar coordenadas precisas del usuario (por ejemplo, GPS):

- Se solicitará consentimiento explícito del usuario
- Se informará claramente el uso de dichos datos
- Se documentará si existe almacenamiento, duración y eliminación de los datos

📄 Documentación completa: [Google Docs](https://docs.google.com/document/d/1actyIjFGP0JM-KiQdbumeh7w2mzFX4NB/edit)