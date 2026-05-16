# 🧪 Ejecución de Pruebas

El proyecto cuenta con dos mecanismos para comprobar el correcto funcionamiento de los endpoints.

## 1. Pruebas End-to-End con cURL (Bash)
Hemos preparado un script ejecutable que hace una ronda secuencial por cada uno de los métodos HTTP. 

**Cómo ejecutar:**
Si estás en Windows, te recomendamos abrir **Git Bash** para correrlo:
```bash
bash scripts/pruebas_curl.sh
```
*Este script simulará un usuario real realizando un POST, varios GET, un PUT y finalmente un DELETE sobre un mismo ID extraído dinámicamente.*

## 2. Batería de Pruebas Automatizadas (Pytest)
Hemos programado 9 tests automatizados que ponen a prueba las validaciones de límite, tipos y fallos controlados usando `TestClient`.

**Cómo ejecutar:**
Asegúrate de tener el entorno virtual activado y ejecuta en la raíz del proyecto:
```bash
pytest tests/ -v
```

**Cobertura de los Tests:**
- Inserciones válidas.
- Rechazo (422) de tipos inválidos y rangos excedidos.
- Búsqueda (200) de listas globales y filtradas por query.
- Actualización exitosa conservando validaciones cruzadas.
- Errores (404) al intentar borrar o modificar IDs inexistentes.
