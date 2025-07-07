#!/bin/bash

export PYTHONPATH="$PYTHONPATH"

# Activar entorno virtual (ajusta si usas otro)
source env/bin/activate

# Cargar variables del archivo .env de forma segura
if [ -f .env ]; then
    echo "✅ Cargando variables desde .env..."
    while IFS='=' read -r key value; do
        # Saltar comentarios o líneas vacías
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        # Quitar comillas si existen
        value="${value%\"}"
        value="${value#\"}"
        export "$key=$value"
    done < <(grep -v '^#' .env)
else
    echo "❌ Archivo .env no encontrado"
    exit 1
fi

# Verificar que uvicorn esté instalado
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn no está instalado. Instálalo con: pip install uvicorn[standard]"
    exit 1
fi

# Confirmar PYTHONPATH cargado
echo "📦 PYTHONPATH: $PYTHONPATH"

# Lanzar el servidor
echo "🚀 Ejecutando Uvicorn..."
uvicorn app.main:app --reload