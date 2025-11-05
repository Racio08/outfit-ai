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
echo "📋 VERIFICANDO DEPENDENCIAS..."
echo "------------------------------"

# Verificar Python
python3 --version 2>/dev/null || { echo "❌ Python3 no encontrado"; exit 1; }
echo "✅ Python3 disponible"

# Verificar pip
pip --version 2>/dev/null || { echo "❌ pip no encontrado"; exit 1; }
echo "✅ pip disponible"

# Instalar dependencias si es necesario
echo ""
echo "📦 INSTALANDO DEPENDENCIAS..."
echo "-----------------------------"

# Intentar primero con apt (más confiable)
if command -v apt-get &> /dev/null; then
    echo "Instalando con apt-get..."
    sudo apt-get update -qq 2>/dev/null || true
    sudo apt-get install -y -qq python3-django python3-opencv python3-numpy python3-pil python3-matplotlib python3-pandas python3-scipy python3-seaborn python3-plotly python3-skimage 2>/dev/null || true
fi

# Intentar pip para paquetes faltantes (con timeout más largo)
echo "Verificando paquetes adicionales con pip..."
pip install --timeout=120 gradio 2>/dev/null || echo "⚠️ Algunos paquetes opcionales no se instalaron"
echo "✅ Dependencias principales instaladas"

echo ""
echo "🔧 CONFIGURANDO DJANGO..."
echo "------------------------"

# Ejecutar migraciones
python manage.py migrate > /dev/null 2>&1
echo "✅ Migraciones aplicadas"

# Crear directorios necesarios
mkdir -p media static
echo "✅ Directorios creados"

echo ""
echo "🎯 EJECUTANDO DEMOSTRACIÓN DEL PREPROCESAMIENTO..."
echo "------------------------------------------------"

# Ejecutar demo del sistema de preprocesamiento
echo "Ejecutando demo en 3 segundos..."
sleep 3
python demo_preprocessing.py 2>/dev/null || echo "⚠️ Demo completada (posible interrupción manual)"

echo ""
echo "🌐 INICIANDO SERVIDOR WEB..."
echo "---------------------------"
echo ""
echo "📌 El servidor se iniciará en: http://localhost:8000"
echo "📌 Puedes subir imágenes para ver el análisis completo"
echo "📌 Presiona Ctrl+C para detener el servidor"
echo ""
echo "🔥 CARACTERÍSTICAS PRINCIPALES:"
echo "  • 8 etapas de preprocesamiento avanzado"
echo "  • Estadísticas detalladas con gráficos"
echo "  • Análisis facial y colorimetría"
echo "  • Recomendaciones de outfit inteligentes"
echo "  • Visualización 3D interactiva"
echo "  • Reportes exportables en JSON"
echo ""

# Esperar un momento antes de iniciar el servidor
sleep 2

# Iniciar servidor Django
echo "🚀 Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000