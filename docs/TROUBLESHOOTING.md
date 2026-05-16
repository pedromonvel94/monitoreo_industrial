# 🚨 Troubleshooting (Solución de problemas)

Si te encuentras con un error durante la ejecución del proyecto, revisa las siguientes soluciones comunes.

### 1. `pymongo.errors.ServerSelectionTimeoutError`
- **Causa:** La aplicación no logra comunicarse con tu base de datos MongoDB en la nube.
- **Solución:** 
  - Verifica que tengas acceso a Internet si usas MongoDB Atlas.
  - Asegúrate de que el archivo `.env` exista en la raíz y la variable `MONGO_URI` esté correctamente escrita.
  - Comprueba que tu IP esté agregada en la *Network Access / IP Access List* de tu panel en Atlas.

### 2. `ModuleNotFoundError: No module named 'app'`
- **Causa:** Estás ejecutando un script (como `seed_data.py`) desde un contexto donde Python no encuentra el paquete raíz del proyecto.
- **Solución:** Ejecuta el script **siempre** estando parado en la raíz principal de tu proyecto (`monitoreo_industrial`), no navegues dentro de la carpeta scripts para hacerlo.
  ```bash
  python scripts/seed_data.py
  ```

### 3. Líneas rojas en los imports de PyMongo o Pydantic (En VS Code)
- **Causa:** Tu editor está utilizando el intérprete de Python global en lugar del que pertenece al entorno virtual `venv`.
- **Solución:** Hemos creado un archivo `.vscode/settings.json` para forzar la lectura. Si persiste, presiona `Ctrl + Shift + P` en VS Code, escribe `Python: Select Interpreter` y elige `.\venv\Scripts\python.exe`. Luego, reinicia la ventana de VS Code.

### 4. `422 Unprocessable Entity` al insertar datos
- **Causa:** El JSON que enviaste no cumple con las reglas del negocio definidas en `app/models.py`.
- **Solución:** Revisa que los campos numéricos como `valor` respeten su límite (ej. Temperatura máximo 100). Revisa el contenido del error en formato JSON; la API ha sido configurada en `app/errors.py` para devolverte un mensaje de error en español sumamente detallado con el campo exacto que falló.
