"""Módulo principal con la aplicación FastAPI y los endpoints CRUD."""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from bson import ObjectId
from bson.errors import InvalidId

from app.database import get_collection
from app.models import SensorCreate, SensorUpdate, SensorOut, RANGOS
from app.errors import configurar_handlers

# Inicializar aplicación FastAPI
app = FastAPI(
    title="API de Sensores Industriales",
    description="API RESTful para monitoreo de sensores (temperatura, presión, vibración).",
    version="1.0.0"
)

# Configurar manejadores de excepciones globales definidos en errors.py
configurar_handlers(app)


def serialize_mongo_doc(doc: dict) -> dict:
    """Convierte el documento BSON de MongoDB a un diccionario compatible con JSON/FastAPI."""
    if not doc:
        return doc
    doc["id"] = str(doc.pop("_id"))
    return doc


@app.post("/sensores/", response_model=SensorOut, status_code=201)
def crear_sensor(sensor: SensorCreate):
    """
    Crea una nueva lectura de sensor en la base de datos.
    """
    coleccion = get_collection()
    
    # Convertir el modelo Pydantic a diccionario
    nuevo_sensor = sensor.model_dump()
    resultado = coleccion.insert_one(nuevo_sensor)
    
    # Recuperar el documento recién insertado
    doc_insertado = coleccion.find_one({"_id": resultado.inserted_id})
    return serialize_mongo_doc(doc_insertado)


@app.get("/sensores/", response_model=List[SensorOut])
def listar_sensores(tipo: Optional[str] = Query(None, description="Filtrar opcionalmente por tipo de sensor")):
    """
    Obtiene la lista de todos los sensores. Permite filtrar opcionalmente por la query `?tipo=...`
    """
    coleccion = get_collection()
    filtro = {}
    if tipo:
        filtro["tipo"] = tipo
        
    cursor = coleccion.find(filtro)
    sensores = [serialize_mongo_doc(doc) for doc in cursor]
    return sensores


@app.get("/sensores/{id}", response_model=SensorOut)
def obtener_sensor(id: str):
    """
    Obtiene los datos de un único sensor utilizando su ID.
    (Implementado como Path Parameter /sensores/{id} siguiendo el estándar REST).
    """
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID de MongoDB inválido.")
        
    coleccion = get_collection()
    sensor = coleccion.find_one({"_id": obj_id})
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
        
    return serialize_mongo_doc(sensor)


@app.put("/sensores/{id}", response_model=SensorOut)
def actualizar_sensor(id: str, sensor_update: SensorUpdate):
    """
    Actualiza parcialmente los datos de un sensor existente usando PATCH-like behaviour (PUT parcial).
    """
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID de MongoDB inválido.")
        
    coleccion = get_collection()
    
    # Se debe buscar primero el sensor para conocer su tipo y hacer la validación de rango cruzada
    sensor_existente = coleccion.find_one({"_id": obj_id})
    if not sensor_existente:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
    
    update_data = sensor_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar.")
    
    # Validación manual de rango para actualizaciones
    if "valor" in update_data:
        tipo_actual = sensor_existente["tipo"]
        nuevo_valor = update_data["valor"]
        minimo, maximo = RANGOS[tipo_actual]
        if not (minimo <= nuevo_valor <= maximo):
            raise HTTPException(
                status_code=422,
                detail=f"Error de validación cruzada: El valor para un sensor de tipo '{tipo_actual}' debe estar entre {minimo} y {maximo}."
            )
            
    coleccion.update_one({"_id": obj_id}, {"$set": update_data})
    
    # Retornar el documento actualizado
    doc_actualizado = coleccion.find_one({"_id": obj_id})
    return serialize_mongo_doc(doc_actualizado)

@app.put("/sensores/tipo/{tipo}", response_model=SensorOut)
def actualizar_sensor_por_tipo(tipo: str, sensor_update: SensorUpdate):
    """
    Actualiza parcialmente el primer sensor que encuentre del tipo especificado.
    """
    # 1. Validar que el tipo solicitado exista en nuestros modelos permitidos
    if tipo not in RANGOS:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de sensor inválido. Opciones válidas: {list(RANGOS.keys())}"
        )
        
    coleccion = get_collection()
    
    # Se debe buscar primero el sensor para conocer su tipo y hacer la validación de rango cruzada
    sensor_existente = coleccion.find_one({"tipo": tipo})
    if not sensor_existente:
        raise HTTPException(status_code=404, detail="Tipo de sensor no encontrado.")
    
    update_data = sensor_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar.")
    
    # Validación manual de rango para actualizaciones
    if "valor" in update_data:
        tipo_actual = sensor_existente["tipo"]
        nuevo_valor = update_data["valor"]
        minimo, maximo = RANGOS[tipo_actual]
        if not (minimo <= nuevo_valor <= maximo):
            raise HTTPException(
                status_code=422,
                detail=f"Error de validación cruzada: El valor para un sensor de tipo '{tipo_actual}' debe estar entre {minimo} y {maximo}."
            )
            
    coleccion.update_one({"tipo": tipo}, {"$set": update_data})
    
    # Retornar el documento actualizado
    doc_actualizado = coleccion.find_one({"tipo": tipo})
    return serialize_mongo_doc(doc_actualizado)

@app.delete("/sensores/{id}")
def eliminar_sensor(id: str):
    """
    Elimina un sensor de la base de datos dado su ID.
    """
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID de MongoDB inválido.")
        
    coleccion = get_collection()
    resultado = coleccion.delete_one({"_id": obj_id})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
        
    return {"mensaje": "Sensor eliminado exitosamente."}


@app.delete("/sensores/tipo/{tipo}")
def eliminar_sensor_por_tipo(tipo: str):
    """
    Elimina el primer sensor que encuentre del tipo especificado en la base de datos.
    """
    if tipo not in RANGOS:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de sensor inválido. Opciones válidas: {list(RANGOS.keys())}"
        )
        
    coleccion = get_collection()
    resultado = coleccion.delete_one({"tipo": tipo})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tipo de sensor no encontrado para eliminar.")
        
    return {"mensaje": f"Sensor de tipo '{tipo}' eliminado exitosamente."}
