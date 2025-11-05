#!/bin/bash

# 🔍 OUTFIT AI - Script de Verificación del Sistema
# =================================================

echo "🔍 VERIFICANDO SISTEMA OUTFIT AI"
echo "================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de verificaciones
TOTAL_CHECKS=0
PASSED_CHECKS=0

# Función para verificar
check() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if $1 > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $2"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $2"
        return 1
    fi
}

# Función para verificar comando
check_command() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if command -v $1 &> /dev/null; then
        VERSION=$($2 2>&1 | head -1)
        echo -e "${GREEN}✅${NC} $3: $VERSION"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $3 no encontrado"
        return 1
    fi
}

# Función para verificar módulo Python
check_python_module() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if python3 -c "import $1" 2>/dev/null; then
        VERSION=$(python3 -c "import $1; print(getattr($1, '__version__', 'installed'))" 2>/dev/null)
        echo -e "${GREEN}✅${NC} $2: $VERSION"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $2 no encontrado"
        return 1
    fi
}

echo "1. VERIFICANDO REQUISITOS DEL SISTEMA"
echo "--------------------------------------"
check_command "python3" "python3 --version" "Python3"
check_command "pip" "pip --version" "pip"
echo ""

echo "2. VERIFICANDO MÓDULOS PYTHON REQUERIDOS"
echo "-----------------------------------------"
check_python_module "django" "Django"
check_python_module "cv2" "OpenCV"
check_python_module "numpy" "NumPy"
check_python_module "PIL" "Pillow"
check_python_module "matplotlib" "Matplotlib"
check_python_module "pandas" "Pandas"
check_python_module "scipy" "SciPy"
check_python_module "seaborn" "Seaborn"
check_python_module "plotly" "Plotly"
check_python_module "skimage" "scikit-image"
echo ""

echo "3. VERIFICANDO MÓDULOS OPCIONALES"
echo "----------------------------------"
check_python_module "gradio" "Gradio (para main.py)"
echo ""

echo "4. VERIFICANDO ARCHIVOS DEL PROYECTO"
echo "-------------------------------------"
check "test -f manage.py" "manage.py encontrado"
check "test -f main.py" "main.py encontrado"
check "test -f ejecutar.sh" "ejecutar.sh encontrado"
check "test -f requirements.txt" "requirements.txt encontrado"
check "test -d outfit_ai" "Directorio outfit_ai/ existe"
check "test -d outfits" "Directorio outfits/ existe"
echo ""

echo "5. VERIFICANDO CONFIGURACIÓN DJANGO"
echo "------------------------------------"
if python3 manage.py check --deploy 2>/dev/null; then
    echo -e "${GREEN}✅${NC} Django check passed"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    if python3 manage.py check 2>/dev/null; then
        echo -e "${YELLOW}⚠️${NC}  Django check passed (con advertencias)"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "${RED}❌${NC} Django check failed"
    fi
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
echo ""

echo "6. VERIFICANDO DIRECTORIOS NECESARIOS"
echo "--------------------------------------"
# Crear directorios si no existen
mkdir -p media static 2>/dev/null
check "test -d media" "Directorio media/"
check "test -d static" "Directorio static/"
echo ""

echo "7. VERIFICANDO BASE DE DATOS"
echo "-----------------------------"
if test -f db.sqlite3; then
    echo -e "${GREEN}✅${NC} Base de datos existe (db.sqlite3)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${YELLOW}⚠️${NC}  Base de datos no existe (ejecutar: python3 manage.py migrate)"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
echo ""

# Resumen
echo "========================================"
echo "RESUMEN DE VERIFICACIÓN"
echo "========================================"
echo ""
echo "Verificaciones pasadas: $PASSED_CHECKS/$TOTAL_CHECKS"
echo ""

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}🎉 ¡SISTEMA COMPLETAMENTE CONFIGURADO!${NC}"
    echo ""
    echo "Puedes ejecutar el sistema con:"
    echo "  ./ejecutar.sh                    # Script automático"
    echo "  python3 manage.py runserver      # Solo Django"
    echo "  python3 main.py                  # Solo Gradio"
    exit 0
elif [ $PASSED_CHECKS -gt $((TOTAL_CHECKS * 2 / 3)) ]; then
    echo -e "${YELLOW}⚠️  SISTEMA PARCIALMENTE CONFIGURADO${NC}"
    echo ""
    echo "Algunas dependencias faltan. Ejecuta:"
    echo "  sudo apt-get install -y python3-django python3-opencv python3-numpy \\"
    echo "                          python3-pil python3-matplotlib python3-pandas \\"
    echo "                          python3-scipy python3-seaborn python3-plotly \\"
    echo "                          python3-skimage"
    echo "  pip install gradio"
    exit 1
else
    echo -e "${RED}❌ SISTEMA NO CONFIGURADO CORRECTAMENTE${NC}"
    echo ""
    echo "Por favor, revisa los errores arriba y ejecuta:"
    echo "  ./ejecutar.sh  # Intentará instalar dependencias"
    exit 2
fi
