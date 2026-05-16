# 📖 Guía de Uso

Una vez completada la [instalación](INSTALACION.md), puedes interactuar con la aplicación y poblarla con datos iniciales.

## 1. Sembrar Datos Iniciales (Seeding)
Para no iniciar con una base de datos vacía, puedes ejecutar el script preparado que carga 3 sensores válidos:

```bash
python scripts/seed_data.py
```
*Salida esperada:* Un mensaje indicando que la colección fue limpiada y 3 sensores fueron insertados.

## 2. Iniciar el Servidor de Desarrollo
Levanta la API usando Uvicorn con recarga automática:

```bash
uvicorn app.main:app --reload
```
La aplicación estará disponible en `http://localhost:8000`.

## 3. Acceder a Swagger UI
FastAPI genera automáticamente documentación interactiva. Visita la siguiente URL en tu navegador:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

Desde allí podrás probar y visualizar todos los endpoints directamente sin necesidad de usar herramientas externas como Postman.
