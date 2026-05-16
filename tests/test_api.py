"""Batería de pruebas automatizadas para la API usando Pytest y TestClient."""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from app.main import app
from app.database import get_collection

client = TestClient(app)

# Fixture de limpieza: Se ejecuta antes y después de todas las pruebas (module scope)
# para asegurar que la base de datos de pruebas no se ensucie con datos anteriores.
@pytest.fixture(scope="module", autouse=True)
def limpiar_db():
    coleccion = get_collection()
    coleccion.delete_many({})
    yield
    coleccion.delete_many({})


def test_crear_sensor_valido():
    payload = {
        "tipo": "presion",
        "valor": 150.5,
        "ubicacion": "Test Lab",
        "fecha": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/sensores/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["tipo"] == "presion"


def test_crear_sensor_tipo_invalido():
    payload = {
        "tipo": "radiacion",  # Tipo NO listado en el Literal
        "valor": 10.0,
        "ubicacion": "Test Lab",
        "fecha": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/sensores/", json=payload)
    assert response.status_code == 422
    assert "Error de validación" in response.json()["mensaje"]


def test_crear_sensor_fuera_de_rango():
    payload = {
        "tipo": "temperatura",
        "valor": 150.0,  # Máximo es 100.0
        "ubicacion": "Test Lab",
        "fecha": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/sensores/", json=payload)
    assert response.status_code == 422
    detalles = str(response.json()["detalles"])
    assert "entre -10.0 y 100.0" in detalles


def test_listar_sensores():
    response = client.get("/sensores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtrar_por_tipo():
    # Asegurar que exista uno de vibración
    client.post("/sensores/", json={
        "tipo": "vibracion",
        "valor": 2.5,
        "ubicacion": "Motor 2",
        "fecha": datetime.now(timezone.utc).isoformat()
    })
    
    response = client.get("/sensores/?tipo=vibracion")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for sensor in data:
        assert sensor["tipo"] == "vibracion"


def test_actualizar_sensor_existente():
    # 1. Crear uno para actualizarlo
    crear_resp = client.post("/sensores/", json={
        "tipo": "temperatura",
        "valor": 20.0,
        "ubicacion": "Sala 1",
        "fecha": datetime.now(timezone.utc).isoformat()
    })
    sensor_id = crear_resp.json()["id"]
    
    # 2. Enviar actualización
    update_resp = client.put(f"/sensores/{sensor_id}", json={
        "valor": 25.0
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["valor"] == 25.0


def test_actualizar_sensor_inexistente():
    id_falso = "64c91a3e9c5f8e5f8f8b4d1a" # Formato válido de MongoID, pero no existe
    response = client.put(f"/sensores/{id_falso}", json={"valor": 50.0})
    assert response.status_code == 404


def test_eliminar_sensor_existente():
    # 1. Crear
    crear_resp = client.post("/sensores/", json={
        "tipo": "presion",
        "valor": 200.0,
        "ubicacion": "Sala 2",
        "fecha": datetime.now(timezone.utc).isoformat()
    })
    sensor_id = crear_resp.json()["id"]
    
    # 2. Eliminar
    delete_resp = client.delete(f"/sensores/{sensor_id}")
    assert delete_resp.status_code == 200
    
    # 3. Comprobar que es inalcanzable (usando el GET individual)
    get_resp = client.get(f"/sensores/{sensor_id}")
    assert get_resp.status_code == 404


def test_eliminar_sensor_inexistente():
    id_falso = "64c91a3e9c5f8e5f8f8b4d1a"
    response = client.delete(f"/sensores/{id_falso}")
    assert response.status_code == 404
