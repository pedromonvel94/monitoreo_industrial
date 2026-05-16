# 🏛️ Arquitectura del Proyecto

Este proyecto fue diseñado separando responsabilidades para facilitar su escalabilidad y comprensión. Se utiliza un enfoque de **Capas Lógicas**.

## Estructura de Directorios

```text
monitoreo_industrial/
├── app/
│   ├── __init__.py
│   ├── database.py   # Gestión y configuración del driver síncrono PyMongo.
│   ├── models.py     # Esquemas de Pydantic v2 (Validación de entrada y salida).
│   ├── errors.py     # Manejadores globales de excepciones.
│   └── main.py       # Instancia de FastAPI y definición de controladores (Endpoints).
├── docs/             # Archivos Markdown con documentación exhaustiva.
├── scripts/          # Utilidades para línea de comandos (Bash y Python).
├── tests/            # Batería de pruebas (Pytest).
├── venv/             # Entorno virtual de Python.
├── .env              # Variables sensibles (No traqueado en git).
├── .gitignore
└── requirements.txt
```

## Decisiones Técnicas
- **Base de Datos Síncrona:** A pesar de que FastAPI soporta asincronía nativa (`motor`), se optó por usar `pymongo` estándar en `app/database.py` por simplicidad didáctica y en estricto cumplimiento de la guía académica del proyecto.
- **Serialización ObjectId:** MongoDB utiliza un formato `ObjectId` en BSON que no es compatible nativamente con JSON. Por ello, en `app/main.py` se construyó el helper `serialize_mongo_doc()` que aplana el `_id` a un formato `string` estándar (`id`).
- **Validación con Pydantic v2:** Se usó el moderno decorador `@field_validator` apoyado del objeto `ValidationInfo` para comparar dinámicamente el valor insertado con el diccionario estático de rangos según el tipo de sensor.
