# ⚙️ Guía de Instalación

Sigue estos pasos para levantar el proyecto de forma local en tu máquina Windows.

## 1. Prerrequisitos
- **Python 3.10 o superior** (Desarrollado y probado bajo la versión 3.12.3).
- **Git Bash** (opcional, pero recomendado para correr el script de curl).
- Conexión a internet (para comunicarse con el clúster remoto de MongoDB Atlas).

## 2. Configurar el Entorno Virtual
Abre tu terminal en la carpeta raíz del proyecto y ejecuta:

```bash
# Crear el entorno virtual
py -3.12 -m venv venv

# Activar el entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1
```

## 3. Instalación de Dependencias
Una vez activado el entorno `(venv)`, instala el stack requerido:

```bash
pip install -r requirements.txt
```

## 4. Configurar Variables de Entorno
Asegúrate de contar con el archivo `.env` en la raíz del proyecto. Si no existe, créalo con este formato:

```env
MONGO_URI="tu_cadena_de_conexion_de_atlas"
DB_NAME="monitoreo_industrial"
COLLECTION_NAME="sensores"
```
*(Nota: El archivo `.env` no se incluye en el control de versiones por seguridad).*
