#!/bin/bash
# Script de inicio rápido para Outfit AI

cd "$(dirname "$0")"

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
    .venv/bin/python manage.py runserver 0.0.0.0:8000
elif [ -d "venv" ]; then
    source venv/bin/activate
    venv/bin/python manage.py runserver 0.0.0.0:8000
else
    python3 manage.py runserver 0.0.0.0:8000
fi
