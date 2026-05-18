# 🏭 API de Monitoreo de Sensores Industriales

> Una solución robusta y escalable basada en FastAPI y MongoDB para el monitoreo en tiempo real de variables críticas en plantas industriales.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📖 Descripción del Proyecto

Este proyecto nace de la necesidad de centralizar y automatizar el monitoreo de sensores críticos en entornos industriales (temperatura, presión y vibración). La inconsistencia de datos y lecturas fuera de límites seguros pueden provocar fallas catastróficas en maquinarias de alto valor (como calderas, turbinas y reactores).

Esta **API RESTful** proporciona una interfaz unificada y de alto rendimiento que no solo gestiona la persistencia de datos (CRUD), sino que actúa como una **barrera activa de validación**.

### 🛠️ ¿Por qué elegimos esta tecnología?
- **FastAPI:** Su velocidad de ejecución (comparable a NodeJS y Go) y su integración nativa con Pydantic v2 garantizan validación asíncrona inmediata en el punto de entrada de la red.
- **MongoDB NoSQL:** Las lecturas de sensores industriales son semiestructuradas, de alta frecuencia y propensas a cambios en el tiempo. La flexibilidad del esquema de MongoDB Atlas permite agregar lecturas heterogéneas sin necesidad de costosas migraciones de esquemas relacionales.
- **Pydantic v2:** Nos permitió construir esquemas auto-documentados que rechazan de inmediato datos inválidos antes de tocar la base de datos.

### 🧠 Retos Superados y Aprendizajes
- **Validación Cruzada Avanzada:** Desarrollamos un validador personalizado con `@field_validator` y `ValidationInfo` en Pydantic para validar los límites seguros de variables dinámicamente según el tipo de sensor (por ejemplo, rechazar lecturas de presión si son negativas o mayores a 500, pero permitiendo un rango diferente para vibraciones).
- **Problema de Codificación de Terminal (Windows cp1252):** Superamos las limitaciones de salida de la terminal de PowerShell en Windows al refactorizar los sistemas de registro para evitar que caracteres especiales y emojis arruinaran la ejecución de cargas automatizadas.
- **RESTful vs Query Params:** Balanceamos la API para responder tanto al estándar REST (`/sensores/{id}`) como a filtros por parámetros de consulta (`/sensores/?tipo=temperatura`) para facilitar la flexibilidad de cara al cliente.

---

## 📑 Tabla de Contenido
1. [Instalación y Configuración](#-instalación-y-configuración)
2. [Estructura del Proyecto](#-estructura-del-proyecto)
3. [Cómo utilizar la API](#-cómo-utilizar-la-api)
4. [Documentación de Endpoints](#-documentación-de-endpoints)
5. [Batería de Pruebas](#-batería-de-pruebas)
6. [Cómo Contribuir](#-cómo-contribuir)
7. [Créditos y Licencia](#-créditos-y-licencia)

---

## ⚙️ Instalación y Configuración

Siga esta guía paso a paso para levantar el entorno de desarrollo local en su máquina Windows.

### 1. Prerrequisitos
- Python instalado (versión 3.10 o superior recomendada; este proyecto se construyó con la **3.12.3**).
- Conexión a internet (para sincronizarse con el clúster en la nube de MongoDB Atlas).

### 2. Configurar el Entorno Virtual
Abre tu consola de comandos en la carpeta raíz del proyecto y ejecuta:

```powershell
# 1. Crear el entorno virtual limpio
python -m venv venv

# 2. Activar el entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1
```
*Si estás en Git Bash o Linux usa:* `source venv/bin/activate`

### 3. Instalar Dependencias
Una vez activado el entorno virtual (verás el prefijo `(venv)` en tu consola), ejecuta:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto (este archivo está excluido en el `.gitignore` por seguridad) y añade tus credenciales de MongoDB Atlas:

```env
MONGO_URI="mongodb+srv://juanpemonv1994_db_user:vDQnDUWta2fF3H8E@iudigital.0ucfsn9.mongodb.net/"
DB_NAME="monitoreo_industrial"
COLLECTION_NAME="sensores"
```

---

## 🏛️ Estructura del Proyecto

El desarrollo sigue una estricta separación de responsabilidades en capas:

```text
monitoreo_industrial/
├── app/
│   ├── __init__.py
│   ├── database.py   # Controlador de base de datos síncrona PyMongo
│   ├── models.py     # Esquemas de Pydantic v2 (Validaciones y tipos)
│   ├── errors.py     # Manejador global de excepciones traducidas
│   └── main.py       # Endpoints de la API y lógica de control
├── docs/             # Reportes de validación y guías extendidas
├── scripts/
│   ├── seed_data.py  # Script para sembrar datos semilla (limpia e inserta)
│   └── pruebas_curl.sh # Pruebas funcionales rápidas en Bash
├── tests/
│   ├── __init__.py
│   └── test_api.py   # Suite de 9 pruebas automatizadas con Pytest
├── .env              # Configuración local sensible
├── requirements.txt  # Lista de dependencias del proyecto
└── README.md         # Manual de usuario principal
```

---

## 📖 Cómo utilizar la API

Siga esta secuencia lógica para ver la aplicación funcionando al 100%:

### 1. Poblar la Base de Datos (Sembrado)
Antes de interactuar con la API, puedes cargar datos de prueba reales para sensores de temperatura, presión y vibración. Ejecuta en tu terminal:

```bash
python scripts/seed_data.py
```
*Salida esperada:*
```text
INFO:app.database:Conexión exitosa a MongoDB Atlas.
Coleccion limpiada exitosamente.
Se insertaron 3 sensores correctamente.
```

### 2. Iniciar el Servidor de Desarrollo
Levanta la API usando Uvicorn:

```bash
uvicorn app.main:app --reload
```
Verás que la consola reporta el éxito del arranque y te indicará que el servidor está escuchando en **`http://127.0.0.1:8000`**.

### 3. Probar con Swagger UI (Recomendado)
FastAPI auto-documenta la API al instante. Abre tu navegador web y visita:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Desde aquí puedes probar de forma visual e interactiva todos los métodos HTTP sin herramientas externas.

### 4. Probar desde Postman
Si prefieres usar Postman, asegúrate de configurar los Headers con `Content-Type: application/json` y usa payloads con fechas en formato estándar **ISO 8601** (`AAAA-MM-DDTHH:MM:SSZ`):

**Ejemplo de creación de sensor (POST a `http://127.0.0.1:8000/sensores/`):**
```json
{
  "tipo": "temperatura",
  "valor": 38.6,
  "ubicacion": "Planta Norte - Reactor 2",
  "fecha": "2026-05-18T14:30:00Z"
}
```

---

## 🔗 Documentación de Endpoints

| Método | Ruta | Descripción | Parámetros / Payload |
| :--- | :--- | :--- | :--- |
| **POST** | `/sensores/` | Registra una nueva lectura de sensor | Recibe un `SensorCreate` JSON. |
| **GET** | `/sensores/` | Obtiene todas las lecturas de sensores | Opcional: Query param `?tipo=temperatura` |
| **GET** | `/sensores/{id}` | Busca un sensor específico por su ObjectId | Path param `{id}` hexadecimal. |
| **PUT** | `/sensores/{id}` | Actualización parcial de un sensor por ID | Recibe valores opcionales en JSON. |
| **PUT** | `/sensores/tipo/{tipo}`| Actualiza el primer sensor del tipo dado | Path param `{tipo}` ("temperatura", etc). |
| **DELETE**| `/sensores/{id}` | Elimina un sensor de la base de datos | Path param `{id}` hexadecimal. |
| **DELETE**| `/sensores/tipo/{tipo}`| Elimina el primer sensor de ese tipo | Path param `{tipo}` |

---

## 🧪 Batería de Pruebas

El código cuenta con una robustez probada y validada mediante **9 tests unitarios e integrales** que garantizan que el sistema reaccione correctamente ante payloads corruptos.

Para ejecutar las pruebas en tu máquina, con tu entorno `(venv)` activo, corre:

```bash
pytest tests/ -v
```

### Cobertura de las Pruebas:
- ✅ **`test_crear_sensor_valido`:** Envío correcto de datos devuelve HTTP 201 y el ID de MongoDB.
- ✅ **`test_crear_sensor_tipo_invalido`:** Envío de un tipo no soportado (ej. "radiacion") es rechazado con HTTP 422.
- ✅ **`test_crear_sensor_fuera_de_rango`:** Valores que violan los límites (ej. temperatura de 150°C) son rechazados en español (HTTP 422).
- ✅ **`test_listar_sensores`:** Comprobación del retorno de la lista de base de datos (HTTP 200).
- ✅ **`test_filtrar_por_tipo`:** Valida que el query param filtre adecuadamente en MongoDB.
- ✅ **`test_actualizar_sensor_existente`:** Validación del flujo de edición (HTTP 200).
- ✅ **`test_actualizar_sensor_inexistente`:** IDs correctos en forma pero inexistentes en Atlas devuelven HTTP 404.
- ✅ **`test_eliminar_sensor_existente` & `test_eliminar_sensor_inexistente`:** Prueba el flujo de remoción de registros y el rechazo ante IDs falsos.

---

## 🤝 Cómo Contribuir

¡Las contribuciones de la comunidad son muy bienvenidas! Si deseas mejorar este sistema de monitoreo industrial:

1. Haz un **Fork** de este repositorio.
2. Crea una rama para tu característica: `git checkout -b feature/nueva-mejora`.
3. Realiza tus cambios y asegúrate de que todos los tests sigan pasando ejecutando `pytest`.
4. Sube tus cambios a tu repositorio: `git commit -am 'Añadir nueva mejora' && git push origin feature/nueva-mejora`.
5. Abre un **Pull Request** explicando detalladamente qué problemas resuelve tu código.

---

## 🎓 Créditos y Licencia

Este proyecto fue desarrollado como parte de la Actividad Académica **EA2: Bases de datos NoSQL y operaciones CRUD** para la institución **IUDigital**.

- **Desarrollador:** Juan Pedro Montero ([GitHub](https://github.com/pedromonvel94))
- **Licencia:** Este proyecto se distribuye bajo la **Licencia MIT**. Siéntete libre de clonarlo, modificarlo y usarlo para fines educativos o comerciales respetando los derechos de autor.
