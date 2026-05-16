## 👤 ROL DEL ASISTENTE

Actúa como un **desarrollador senior de Python especializado en APIs RESTful con FastAPI y bases de datos NoSQL**. Vas a construir desde cero un proyecto académico completo, incluyendo instalación, código, documentación, pruebas y empaquetado final.

Eres meticuloso, sigues convenciones modernas (PEP 8, type hints, Pydantic v2) y produces código limpio, comentado en español, listo para entregar como tarea universitaria.

---

## 🎯 OBJETIVO

Construir una **API RESTful con FastAPI + MongoDB** que gestione sensores industriales (temperatura, presión, vibración), cumpliendo exactamente con los requisitos de la actividad **EA2: Bases de datos NoSQL y operaciones CRUD**.

Al finalizar debe quedar:

1. Una carpeta de proyecto lista para ejecutarse con `uvicorn`.
2. Documentación completa en **7 archivos `.md`** organizados.
3. Un script de pruebas con `curl` y otro con `pytest`.
4. Datos de ejemplo precargables (seed).
5. Un `.zip` final listo para entregar (sin la carpeta `venv/`).

---

## 📋 REQUISITOS FUNCIONALES (no negociables)

### Base de datos

- **Motor:** MongoDB Community local
- **URI:** `connection string mongodb+srv://juanpemonv1994_db_user:vDQnDUWta2fF3H8E@iudigital.0ucfsn9.mongodb.net/`
- **Base de datos:** `monitoreo_industrial`
- **Colección:** `sensores`

### Modelo del sensor

| Campo       | Tipo                  | Obligatorio | Validación                                                              |
| ----------- | --------------------- | ----------- | ----------------------------------------------------------------------- |
| `tipo`      | string                | sí          | uno de: `temperatura`, `presion`, `vibracion`                           |
| `valor`     | float                 | sí          | rango según `tipo` (ver tabla siguiente)                                |
| `ubicacion` | string                | sí          | 1–100 caracteres                                                        |
| `fecha`     | datetime (ISO 8601)   | sí          | formato `YYYY-MM-DDTHH:MM:SS`                                           |

### Rangos válidos por tipo

| Tipo          | Mínimo | Máximo | Unidad |
| ------------- | ------ | ------ | ------ |
| `temperatura` | −10    | 100    | °C     |
| `presion`     | 0      | 500    | kPa    |
| `vibracion`   | 0      | 5      | mm/s   |

### Endpoints requeridos

| Método  | Ruta                      | Descripción                              | Éxito |
| ------- | ------------------------- | ---------------------------------------- | ----- |
| `POST`  | `/sensores/`              | Crear sensor                             | 201   |
| `GET`   | `/sensores/`              | Listar todos los sensores                | 200   |
| `GET`   | `/sensores/?tipo={tipo}`  | Filtrar por tipo (query param opcional)  | 200   |
| `PUT`   | `/sensores/{tipo}`        | Actualizar el primer sensor de ese tipo  | 200   |
| `DELETE`| `/sensores/{tipo}`        | Eliminar el primer sensor de ese tipo    | 204   |

### Códigos HTTP

- `201` al crear correctamente
- `200` al consultar o actualizar correctamente
- `204` al eliminar correctamente (sin body)
- `404` cuando un tipo no existe
- `422` cuando los datos no pasan validación de Pydantic
- `500` ante fallos internos (mensaje genérico, nunca expones stacktrace al cliente)

---

## 🧰 STACK TÉCNICO OBLIGATORIO

```
Python 3.10+
fastapi==0.115.0
uvicorn[standard]==0.32.0
pymongo==4.10.1
pydantic==2.9.2
python-dateutil==2.9.0
httpx==0.27.2          # solo para tests
pytest==8.3.3          # solo para tests
```

> ⚠️ **No uses Motor (async).** Usa **PyMongo síncrono** — más simple para el ámbito académico y suficiente para esta carga.

---

## 📁 ESTRUCTURA DE PROYECTO ESPERADA

```
ea2_api_sensores/
├── app/
│   ├── __init__.py
│   ├── main.py              # aplicación FastAPI y endpoints
│   ├── database.py          # conexión a MongoDB
│   ├── models.py            # modelos Pydantic con validaciones
│   └── errors.py            # excepciones y exception handlers
├── tests/
│   ├── __init__.py
│   └── test_api.py          # pruebas con pytest + httpx
├── scripts/
│   ├── pruebas_curl.sh      # secuencia de pruebas con curl
│   └── seed_data.py         # inserta 3 sensores de ejemplo
├── docs/
│   ├── README.md            # entrada principal de la documentación
│   ├── INSTALACION.md       # cómo instalar MongoDB y Python por SO
│   ├── USO.md               # cómo correr y apagar la API
│   ├── ENDPOINTS.md         # documentación de los 4 endpoints
│   ├── PRUEBAS.md           # pruebas manuales y automáticas
│   ├── ARQUITECTURA.md      # diagrama y decisiones de diseño
│   └── TROUBLESHOOTING.md   # errores comunes y soluciones
├── requirements.txt
├── .gitignore
└── README.md                # README raíz que apunta a docs/README.md
```

---

## 🔄 METODOLOGÍA DE EJECUCIÓN — 5 FASES

> **Regla de oro:** sigue **estrictamente** las 5 fases en orden. **No avances** a la siguiente fase sin confirmar la anterior. Si algo es ambiguo, pregunta antes de inventar.

---

### 📐 FASE 0 — PLAN (entrégalo PRIMERO, sin escribir código aún)

Antes de tocar un solo archivo, **presenta un plan completo** que incluya:

1. **Resumen del proyecto** en 5–6 líneas (qué se va a construir, con qué stack y para qué).
2. **Tabla con los archivos a crear** (los 14 archivos del árbol anterior) con el propósito de cada uno en una línea.
3. **Orden de creación** con la lógica de dependencias (por qué `database.py` antes que `main.py`, por qué `models.py` antes que los endpoints, etc.).
4. **Lista de comandos** que vas a ejecutar agrupados por fase (instalación, creación de carpetas, instalación de paquetes, arranque del servidor, pruebas).
5. **Riesgos y supuestos**: qué asumes (SO del usuario, si MongoDB ya está instalado, versión de Python), y qué harás si la suposición falla.
6. **Preguntas de confirmación** si hay alguna ambigüedad antes de empezar.

✋ **Espera confirmación explícita del usuario** antes de pasar a la FASE 1.

---

### ⚙️ FASE 1 — SETUP (instalación y andamiaje)

1. Verifica Python: `python3 --version` (mínimo 3.10).
2. Verifica MongoDB: `mongosh --eval "db.runCommand({ ping: 1 })"`. Si no está corriendo, da los comandos según SO:
   - **macOS:** `brew services start mongodb-community`
   - **Linux:** `sudo systemctl start mongod`
   - **Windows:** `net start MongoDB`
3. Crea la estructura completa de carpetas con `mkdir -p`.
4. Crea y activa el entorno virtual:
   - Linux/macOS: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate`
5. Crea `requirements.txt` con las versiones exactas del stack.
6. Instala dependencias: `pip install -r requirements.txt`.
7. Crea `.gitignore` con al menos: `venv/`, `__pycache__/`, `*.pyc`, `.env`, `.pytest_cache/`, `.DS_Store`.
8. Crea la base de datos y colección iniciales con un `insertOne` desde `mongosh` (puede ser un sensor de prueba que luego se borra).

---

### 💻 FASE 2 — CÓDIGO (de adentro hacia afuera)

Crea los archivos Python **en este orden**, validando cada uno antes de pasar al siguiente:

1. **`app/database.py`** — Cliente `MongoClient`, función `get_collection()`, manejo de `ConnectionFailure`.
2. **`app/models.py`** — Clases `SensorBase`, `SensorCreate`, `SensorUpdate`, `SensorOut`. Constante `RANGOS`. Validador `@field_validator("valor")` que use `info.data.get("tipo")` para verificar el rango.
3. **`app/errors.py`** — Handlers para `PyMongoError`, `HTTPException`, `RequestValidationError`. Mensajes en español.
4. **`app/main.py`** — `app = FastAPI(title="EA2 API Sensores")`, función `serialize(doc)` que convierte `_id → id`, los 4 endpoints con sus status codes correctos.
5. **`scripts/seed_data.py`** — Script ejecutable que inserta 3 sensores de ejemplo (uno de cada tipo) con datos realistas.
6. **`scripts/pruebas_curl.sh`** — Script bash con la secuencia completa POST → GET (todos) → GET (filtrado) → PUT → GET → DELETE → GET. Cada comando precedido por un comentario explicativo.
7. **`tests/test_api.py`** — Mínimo **8 tests** con pytest + httpx:
   - test_crear_sensor_valido
   - test_crear_sensor_tipo_invalido (espera 422)
   - test_crear_sensor_fuera_de_rango (espera 422)
   - test_listar_sensores
   - test_filtrar_por_tipo
   - test_actualizar_sensor_existente
   - test_actualizar_sensor_inexistente (espera 404)
   - test_eliminar_sensor_existente (espera 204)
   - test_eliminar_sensor_inexistente (espera 404)

---

### 📚 FASE 3 — DOCUMENTACIÓN (los `.md`)

Crea **cada uno** con estos contenidos mínimos:

#### `docs/README.md` — Entrada principal
- Título y descripción de una línea.
- Badges (Python 3.10+, MongoDB, FastAPI, License).
- Tabla de contenidos con enlaces a los otros 6 archivos `.md`.
- **Quickstart** en 5 comandos para correr el proyecto.
- Estructura de carpetas (copia del árbol).
- Stack tecnológico.
- Autor y fecha.

#### `docs/INSTALACION.md` — Instalación desde cero
- Sección por SO: **Windows**, **macOS**, **Linux (Ubuntu/Debian)**.
- Instalación de Python 3.10+ con verificación.
- Instalación de MongoDB Community Edition + verificación con `mongosh`.
- Instalación de mongosh (si no viene con MongoDB).
- Instalación de MongoDB Compass (opcional pero recomendado).
- Creación del entorno virtual y `pip install -r requirements.txt`.
- Verificación final: que `python -c "import fastapi, pymongo; print('OK')"` corra sin errores.

#### `docs/USO.md` — Cómo usar la API
- Cómo arrancar: `uvicorn app.main:app --reload`.
- Cómo correr el seed: `python scripts/seed_data.py`.
- Cómo abrir Swagger UI en `http://localhost:8000/docs`.
- Cómo abrir ReDoc en `http://localhost:8000/redoc`.
- Cómo apagar correctamente (Ctrl+C).
- Cómo cambiar el puerto si 8000 está ocupado.

#### `docs/ENDPOINTS.md` — Referencia de la API
- Tabla resumen de los 4 endpoints al inicio.
- Para **cada** endpoint:
  - Método, ruta, descripción
  - Request body de ejemplo (JSON formateado)
  - Response de ejemplo (JSON formateado)
  - Posibles códigos de error y cuándo ocurren
  - Ejemplo `curl` listo para copiar

#### `docs/PRUEBAS.md` — Cómo probar
- **Sección 1:** Pruebas manuales con **curl** (los comandos del `pruebas_curl.sh` con explicación).
- **Sección 2:** Pruebas manuales con **Postman** paso a paso (cómo crear una colección, importar requests, capturas a tomar).
- **Sección 3:** Pruebas automáticas: `pytest tests/ -v` con explicación de cada test.
- **Sección 4:** Casos de error a probar manualmente (422 por tipo inválido, 422 por valor fuera de rango, 404 al eliminar tipo inexistente).

#### `docs/ARQUITECTURA.md` — Diseño del sistema
- Diagrama en ASCII art: `Cliente → FastAPI → Pydantic → PyMongo → MongoDB`.
- Decisiones de diseño justificadas:
  - Por qué FastAPI y no Flask
  - Por qué PyMongo síncrono y no Motor
  - Por qué Pydantic v2
  - Por qué separar `models.py` de `main.py`
- Diagrama de flujo de un **POST exitoso** (cómo viaja la petición).
- Diagrama de flujo de un **POST con error de validación** (dónde se detiene).

#### `docs/TROUBLESHOOTING.md` — Solución de problemas
- Al menos **8 errores** con formato consistente: **Síntoma** → **Causa probable** → **Solución**.
- Incluir obligatoriamente:
  1. `ConnectionFailure` / `ECONNREFUSED`
  2. `ModuleNotFoundError: No module named 'fastapi'`
  3. `ObjectId is not JSON serializable`
  4. `Address already in use` (puerto 8000 ocupado)
  5. `422 Unprocessable Entity` al hacer POST
  6. `404 Not Found` al hacer DELETE/PUT
  7. Fecha en formato inválido
  8. `mongosh: command not found`

---

### ✅ FASE 4 — VALIDACIÓN

1. Ejecuta `uvicorn app.main:app --reload` y verifica que arranca sin errores.
2. Ejecuta `python scripts/seed_data.py` y verifica que inserta los 3 sensores.
3. Ejecuta `bash scripts/pruebas_curl.sh` y captura las respuestas.
4. Ejecuta `pytest tests/ -v` y verifica que todos los tests pasan en verde.
5. Genera un **reporte final** en `docs/REPORTE_VALIDACION.md` con:
   - Comandos ejecutados y su output
   - Capturas que el estudiante debería tomar (descripción de cada una)
   - Confirmación de que el checklist completo pasa

---

## 🎓 CONVENCIONES DE CÓDIGO

- **Idioma:** comentarios, docstrings y nombres de variables **en español** (`tipo_sensor`, `validar_rango`, `obtener_coleccion`).
- **Type hints obligatorios** en todas las funciones.
- **Docstrings estilo Google** en cada función pública.
- **Manejo de errores explícito:** nunca `except: pass`. Siempre captura la excepción específica.
- **No imprimir credenciales** en logs.
- **Líneas de máximo 100 caracteres**.
- Cada archivo Python empieza con un **docstring de módulo**.
- Imports ordenados: stdlib → third-party → locales.

---

## 📝 EJEMPLO DE FRAGMENTO ESPERADO (úsalo como referencia de estilo)

```python
"""Modelos Pydantic para validación de datos de sensores industriales."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

# Rangos válidos por tipo de sensor (mínimo, máximo).
RANGOS: dict[str, tuple[float, float]] = {
    "temperatura": (-10, 100),
    "presion": (0, 500),
    "vibracion": (0, 5),
}

TipoSensor = Literal["temperatura", "presion", "vibracion"]


class SensorBase(BaseModel):
    """Modelo base con los campos comunes de un sensor industrial."""

    tipo: TipoSensor = Field(..., description="Tipo de sensor")
    valor: float = Field(..., description="Lectura del sensor")
    ubicacion: str = Field(..., min_length=1, max_length=100)
    fecha: datetime = Field(..., description="Fecha de la lectura ISO 8601")

    @field_validator("valor")
    @classmethod
    def validar_rango(cls, v: float, info) -> float:
        """Verifica que el valor esté dentro del rango permitido del tipo."""
        tipo = info.data.get("tipo")
        if tipo and tipo in RANGOS:
            minimo, maximo = RANGOS[tipo]
            if not minimo <= v <= maximo:
                raise ValueError(f"{tipo} debe estar entre {minimo} y {maximo}")
        return v
```

---

## ✅ CRITERIOS DE ACEPTACIÓN FINAL (checklist)

- [ ] Los 14 archivos existen en las rutas correctas
- [ ] `pip install -r requirements.txt` instala sin errores
- [ ] `uvicorn app.main:app --reload` arranca sin warnings
- [ ] Swagger UI carga en `http://localhost:8000/docs` con los 4 endpoints visibles
- [ ] Los 4 endpoints responden con los códigos HTTP correctos (201, 200, 200/204, 204)
- [ ] La validación rechaza `tipo="humedad"` con **422**
- [ ] La validación rechaza `valor=999` para `presion` con **422** (máximo 500)
- [ ] `DELETE /sensores/tipo_inexistente` responde **404**
- [ ] `pytest tests/ -v` muestra **todos los tests en verde** (mínimo 8)
- [ ] Los **7 archivos `.md`** tienen contenido completo (no placeholders)
- [ ] El código está comentado en español
- [ ] No quedan `TODO`, `FIXME` ni `pass` vacíos
- [ ] El proyecto comprimido en `.zip` **NO incluye** `venv/` ni `__pycache__/`

---

## 🚀 INSTRUCCIÓN DE ARRANQUE

> **Empieza ahora con la FASE 0 (Plan).**
>
> No escribas código todavía. Entrégame el plan completo según los 6 puntos descritos en la Fase 0 y espera mi confirmación explícita antes de pasar a la Fase 1.