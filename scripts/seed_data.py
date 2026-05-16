"""Script para poblar la base de datos con datos ficticios."""
import sys
import os
from datetime import datetime, timezone

# Añadir el directorio raíz del proyecto al sys.path para poder importar 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_collection

def seed_database():
    """Limpia la colección de sensores e inserta 3 sensores de prueba."""
    coleccion = get_collection()
    
    # 1. Limpiar datos existentes (para evitar duplicados cada que se corre)
    coleccion.delete_many({})
    print("Coleccion limpiada exitosamente.")
    
    # 2. Generar datos iniciales válidos
    ahora = datetime.now(timezone.utc).isoformat()
    
    sensores_ficticios = [
        {
            "tipo": "temperatura",
            "valor": 35.5,
            "ubicacion": "Planta Baja - Sector A",
            "fecha": ahora
        },
        {
            "tipo": "presion",
            "valor": 250.0,
            "ubicacion": "Tubería Principal de Gas",
            "fecha": ahora
        },
        {
            "tipo": "vibracion",
            "valor": 2.1,
            "ubicacion": "Motor Turbina 1",
            "fecha": ahora
        }
    ]
    
    # 3. Insertar datos en la base de datos
    resultado = coleccion.insert_many(sensores_ficticios)
    
    print(f"Se insertaron {len(resultado.inserted_ids)} sensores correctamente:")
    for idx, doc_id in enumerate(resultado.inserted_ids):
        print(f"   - {sensores_ficticios[idx]['tipo']} -> ID: {doc_id}")

if __name__ == "__main__":
    seed_database()
