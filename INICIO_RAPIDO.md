# 🚀 Inicio Rápido - Outfit AI

## Formas de ejecutar el servidor

### Opción 1: Script completo con verificaciones (Recomendado)
```bash
./ejecutar.sh
```

Este script:
- ✅ Verifica el entorno Python
- ✅ Detecta y activa automáticamente el entorno virtual (.venv o venv)
- ✅ Verifica e instala dependencias si es necesario
- ✅ Ejecuta migraciones de Django
- ✅ Crea directorios necesarios
- ✅ Inicia el servidor en http://localhost:8000

### Opción 2: Inicio rápido sin verificaciones
```bash
./start.sh
```

Este script simplemente:
- Activa el entorno virtual (si existe)
- Inicia el servidor directamente

### Opción 3: Comando directo (si ya tienes todo configurado)
```bash
.venv/bin/python manage.py runserver 0.0.0.0:8000
```

## Acceder a la aplicación

Una vez iniciado el servidor, abre tu navegador en:
- **http://localhost:8000/** - Página principal
- **http://localhost:8000/outfits/** - Sistema de análisis de outfit

## Detener el servidor

Presiona `Ctrl+C` en el terminal donde está ejecutándose el servidor.

## Características principales

🔥 **Sistema de Análisis de Outfit con IA:**
- 15+ etapas de preprocesamiento avanzado
- Análisis facial y colorimetría automática
- Detección de tono de piel y características faciales
- Recomendaciones inteligentes de outfit
- Visualización 3D interactiva
- Estadísticas detalladas con gráficos
- Exportación de reportes en JSON

## Requisitos

- Python 3.12+
- Entorno virtual configurado (.venv)
- Dependencias instaladas (ver requirements.txt)

## Solución de problemas

### Si el script no se ejecuta:
```bash
chmod +x ejecutar.sh start.sh
```

### Si faltan dependencias:
```bash
.venv/bin/pip install -r requirements.txt
```

### Si hay errores de migración:
```bash
.venv/bin/python manage.py migrate
```

### Si el puerto 8000 está ocupado:
```bash
.venv/bin/python manage.py runserver 0.0.0.0:8080
```
(Cambia 8000 por otro puerto disponible)

## Documentación adicional

- `GUIA_RAPIDA_USO.md` - Guía de uso del sistema
- `SISTEMA_COMPLETO.md` - Documentación completa del sistema
- `README.md` - Información general del proyecto
