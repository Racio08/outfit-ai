#!/bin/bash

# 🧠 OUTFIT AI - Script de Ejecución del Sistema Completo
# ======================================================

echo "🚀 INICIANDO OUTFIT AI - SISTEMA AVANZADO DE PREPROCESAMIENTO"
echo "=============================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py. Ejecutar desde el directorio del proyecto."
    exit 1
fi

echo ""
echo "📋 VERIFICANDO ENTORNO..."
echo "-------------------------"

# Verificar Python
python3 --version 2>/dev/null || { echo "❌ Python3 no encontrado"; exit 1; }
echo "✅ Python3 disponible"

# Detectar y activar entorno virtual
VENV_PATH=""
if [ -d ".venv" ]; then
    VENV_PATH=".venv"
elif [ -d "venv" ]; then
    VENV_PATH="venv"
fi

if [ -n "$VENV_PATH" ]; then
    echo "✅ Entorno virtual encontrado: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    PYTHON_CMD="$VENV_PATH/bin/python"
    PIP_CMD="$VENV_PATH/bin/pip"
else
    echo "⚠️  No se encontró entorno virtual, usando Python del sistema"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Verificar pip
$PIP_CMD --version 2>/dev/null || { echo "❌ pip no encontrado"; exit 1; }
echo "✅ pip disponible"

# Instalar dependencias si es necesario
echo ""
echo "📦 VERIFICANDO DEPENDENCIAS..."
echo "------------------------------"
if ! $PYTHON_CMD -c "import django" 2>/dev/null; then
    echo "Instalando dependencias desde requirements.txt..."
    $PIP_CMD install -r requirements.txt -q
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "🔧 CONFIGURANDO DJANGO..."
echo "------------------------"

# Ejecutar verificación del sistema
$PYTHON_CMD manage.py check --deploy 2>/dev/null || $PYTHON_CMD manage.py check
echo "✅ Verificación del sistema completada"

# Ejecutar migraciones
$PYTHON_CMD manage.py migrate --noinput > /dev/null 2>&1
echo "✅ Migraciones aplicadas"

# Crear directorios necesarios
mkdir -p media static assets
echo "✅ Directorios creados"

echo ""
echo "🌐 INICIANDO SERVIDOR WEB..."
echo "---------------------------"
echo ""
echo "📌 El servidor se iniciará en: http://localhost:8000"
echo "📌 Puedes subir imágenes para ver el análisis completo"
echo "📌 Presiona Ctrl+C para detener el servidor"
echo ""
echo "🔥 CARACTERÍSTICAS PRINCIPALES:"
echo "  • 15+ etapas de preprocesamiento avanzado"
echo "  • Estadísticas detalladas con gráficos"
echo "  • Análisis facial y colorimetría"
echo "  • Recomendaciones de outfit inteligentes"
echo "  • Visualización 3D interactiva"
echo "  • Reportes exportables en JSON"
echo ""

# Esperar un momento antes de iniciar el servidor
sleep 1

# Iniciar servidor Django
echo "🚀 Iniciando servidor Django..."
$PYTHON_CMD manage.py runserver 0.0.0.0:8000
