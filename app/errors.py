"""Manejadores de errores personalizados para la aplicación FastAPI."""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)

def configurar_handlers(app: FastAPI):
    """Configura los manejadores de excepciones globales de la aplicación."""

    @app.exception_handler(PyMongoError)
    async def pymongo_exception_handler(request: Request, exc: PyMongoError):
        """Manejador para errores internos de la base de datos MongoDB."""
        logger.error(f"Error de base de datos: {exc}")
        return JSONResponse(
            status_code=500,
            content={"mensaje": "Error interno del servidor al acceder a la base de datos."}
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Manejador para errores HTTP estándar (como 404 No encontrado, 400 Bad Request)."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"mensaje": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Manejador para los errores de validación arrojados por Pydantic (422)."""
        errores = exc.errors()
        mensajes = []
        
        # Formatear cada error de pydantic a español legible
        for error in errores:
            campo = " -> ".join(str(loc) for loc in error.get("loc", []) if loc != "body")
            mensaje = error.get("msg", "")
            mensajes.append(f"Error en '{campo}': {mensaje}")
            
        return JSONResponse(
            status_code=422,
            content={
                "mensaje": "Error de validación en los datos enviados.",
                "detalles": mensajes
            }
        )
