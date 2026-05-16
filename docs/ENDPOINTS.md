# 🔗 Documentación de Endpoints

La API expone los siguientes endpoints para la gestión de la colección `sensores`. Todos los cuerpos de las peticiones (Payloads) utilizan el formato `application/json`.

---

## 1. Crear un Sensor
- **Método:** `POST`
- **Ruta:** `/sensores/`
- **Descripción:** Crea un nuevo registro de sensor.
- **Validaciones:**
  - `tipo`: Solo permite "temperatura", "presion" o "vibracion".
  - `valor`: Temperatura (-10 a 100), Presión (0 a 500), Vibración (0 a 5).
- **Body de Ejemplo:**
  ```json
  {
    "tipo": "temperatura",
    "valor": 45.5,
    "ubicacion": "Reactor 1",
    "fecha": "2026-05-15T20:00:00Z"
  }
  ```

## 2. Listar Todos los Sensores
- **Método:** `GET`
- **Ruta:** `/sensores/`
- **Descripción:** Retorna un arreglo con todos los sensores. Permite filtrar opcionalmente por tipo.
- **Query Parameter:** `?tipo={temperatura|presion|vibracion}`

## 3. Obtener un Sensor Específico
- **Método:** `GET`
- **Ruta:** `/sensores/{id}`
- **Descripción:** Busca y retorna un único documento a partir de su ObjectId de MongoDB. Retorna 404 si no existe.

## 4. Actualizar Parcialmente un Sensor
- **Método:** `PUT`
- **Ruta:** `/sensores/{id}`
- **Descripción:** Actualiza de forma parcial (tipo PATCH) un documento existente. Mantiene validación de rangos según su tipo original.
- **Body de Ejemplo:**
  ```json
  {
    "valor": 55.0
  }
  ```

## 5. Eliminar un Sensor
- **Método:** `DELETE`
- **Ruta:** `/sensores/{id}`
- **Descripción:** Elimina definitivamente el sensor de la base de datos.
