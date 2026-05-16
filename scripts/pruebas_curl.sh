#!/bin/bash
# Script para probar automáticamente la API de Sensores.
# Se recomienda ejecutar desde Git Bash en Windows.

BASE_URL="http://localhost:8000"

echo "=== 1. POST: Creando un sensor de temperatura ==="
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "temperatura",
    "valor": 75.5,
    "ubicacion": "Caldera Principal",
    "fecha": "2025-10-15T08:30:00Z"
  }')
echo $POST_RESPONSE

# Extraer el ID recién creado usando grep básico (compatible sin instalar jq)
SENSOR_ID=$(echo $POST_RESPONSE | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo -e "\n\n=== 2. GET: Listando todos los sensores ==="
curl -s -X GET "$BASE_URL/sensores/"

echo -e "\n\n=== 3. GET: Listando solo sensores de temperatura ==="
curl -s -X GET "$BASE_URL/sensores/?tipo=temperatura"

echo -e "\n\n=== 4. GET: Obteniendo un único sensor por su ID ==="
curl -s -X GET "$BASE_URL/sensores/$SENSOR_ID"

echo -e "\n\n=== 5. PUT: Actualizando el valor del sensor creado ==="
curl -s -X PUT "$BASE_URL/sensores/$SENSOR_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 80.0
  }'

echo -e "\n\n=== 6. DELETE: Eliminando el sensor ==="
curl -s -X DELETE "$BASE_URL/sensores/$SENSOR_ID"

echo -e "\n\n=== PRUEBAS COMPLETADAS ==="
