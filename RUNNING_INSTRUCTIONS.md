# 🚀 Cómo Correr el Programa - Outfit AI

## ✅ Estado Actual
**🟢 PROGRAMA FUNCIONANDO CORRECTAMENTE**

Este documento explica cómo ejecutar el sistema Outfit AI después de configurarlo.

---

## 📋 Requisitos Previos

Antes de correr el programa, asegúrate de tener:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

---

## 🔧 Instalación Inicial (Solo la Primera Vez)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Racio08/outfit-ai.git
cd outfit-ai
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

Este comando instalará todas las bibliotecas necesarias:
- Django 5.2.7 (framework web)
- OpenCV (procesamiento de imágenes)
- NumPy, SciPy (computación numérica)
- Matplotlib, Seaborn, Plotly (visualizaciones)
- MediaPipe (análisis facial)
- Y muchas más...

### 3. Configurar Base de Datos
```bash
python manage.py migrate
```

Este comando crea la base de datos SQLite necesaria para Django.

### 4. Crear Directorios Necesarios
```bash
mkdir -p media static
```

---

## 🎯 Cómo Correr el Programa

Tienes **3 opciones** para ejecutar el programa:

### Opción 1: 🚀 Script Automático (Recomendado)
El método más fácil - ejecuta todo automáticamente:

```bash
./ejecutar.sh
```

Este script:
- ✅ Verifica dependencias
- ✅ Aplica migraciones
- ✅ Ejecuta una demo del preprocesamiento
- ✅ Inicia el servidor web en http://localhost:8000

### Opción 2: 🌐 Solo el Servidor Web Django
Para solo iniciar la aplicación web:

```bash
python manage.py runserver 0.0.0.0:8000
```

Luego abre tu navegador en: **http://localhost:8000**

### Opción 3: 📊 Demo de Preprocesamiento
Para ver solo una demostración del sistema de preprocesamiento:

```bash
python demo_preprocessing.py
```

Esto genera:
- Estadísticas detalladas de procesamiento
- Gráficos comparativos
- Histogramas de evolución
- Análisis de calidad

---

## 💻 Usando la Aplicación Web

Una vez que el servidor esté corriendo (Opción 1 o 2):

### 1. Abrir la Aplicación
Abre tu navegador web y ve a:
- **http://localhost:8000** (para acceso local)
- **http://127.0.0.1:8000** (alternativa)

### 2. Subir una Imagen
Tienes 3 formas de cargar una imagen:

#### A. Arrastrar y Soltar 🖱️
1. Arrastra una imagen desde tu computadora
2. Suéltala en la zona de carga (área con borde punteado)

#### B. Seleccionar Archivo 📁
1. Haz clic en el botón **"Seleccionar Archivo"**
2. Busca tu imagen
3. Selecciónala y ábrela

#### C. Tomar Foto 📸
1. Haz clic en **"Abrir Cámara"**
2. Permite acceso a la cámara
3. Captura la foto
4. Confirma con **"Usar esta Foto"**

### 3. Ver los Resultados
El sistema procesará tu imagen a través de **15 etapas** y mostrará:

- **📊 Preprocesamiento**: Galería de 15 etapas con estadísticas
- **🖼️ Imágenes**: Resultado final y overlay de colores
- **🔬 Análisis**: Detección facial, tono de piel, paleta de colores
- **✨ Recomendaciones**: Sugerencias de outfit personalizadas

---

## 🎨 Formatos de Imagen Soportados

- ✅ **JPG/JPEG** (recomendado)
- ✅ **PNG**
- ✅ **WEBP**

**Tamaño máximo**: 5 MB

---

## 🛑 Detener el Servidor

Para detener el servidor web, presiona:
```
Ctrl + C
```
en la terminal donde está corriendo.

---

## 🐛 Solución de Problemas Comunes

### Problema: "ModuleNotFoundError"
**Causa**: Falta instalar dependencias

**Solución**:
```bash
pip install -r requirements.txt
```

### Problema: "No such table" o errores de base de datos
**Causa**: Base de datos no inicializada

**Solución**:
```bash
python manage.py migrate
```

### Problema: "Port already in use" (Puerto 8000 ocupado)
**Causa**: Otro proceso está usando el puerto 8000

**Solución 1** - Usar otro puerto:
```bash
python manage.py runserver 0.0.0.0:8080
```

**Solución 2** - Encontrar y detener el proceso:
```bash
# En Linux/Mac:
lsof -ti:8000 | xargs kill -9

# En Windows:
netstat -ano | findstr :8000
taskkill /PID <número_del_proceso> /F
```

### Problema: "STATICFILES_DIRS directory does not exist"
**Causa**: Falta crear el directorio static

**Solución**:
```bash
mkdir -p static media
```

### Problema: La página no carga o muestra errores
**Solución**:
1. Verifica que el servidor esté corriendo
2. Abre la consola del navegador (F12)
3. Busca errores en rojo
4. Refresca la página (F5)

---

## 📊 Características del Sistema

### Sistema de Preprocesamiento (15 Etapas)
1. 📸 Original
2. 📏 Redimensionado
3. 🎨 Normalización
4. 💡 Gamma Adaptativo
5. 🖼️ Preservación Bordes
6. 🌟 CLAHE
7. ✨ Bilateral
8. 🔲 Realce Contornos
9. 🌈 Saturación
10. ⚖️ Balance Blancos
11. 🔪 Nitidez
12. 🧵 Textura
13. 🧹 Reducción Ruido
14. 🎭 Contraste Final
15. ✅ Optimización

### Análisis de Color
- Detección facial automática con OpenCV
- Extracción de tono de piel
- Generación de paletas de colores personalizadas
- Análisis de colores dominantes

### Recomendaciones de Outfit
- 3 estilos diferentes: Profesional, Casual, Moderno
- Basado en teoría del color
- Consejos de estilo personalizados

---

## 🔄 Flujo de Trabajo Típico

```
1. Iniciar servidor ⚡
   python manage.py runserver

2. Abrir navegador 🌐
   http://localhost:8000

3. Cargar imagen 📤
   Arrastrar o seleccionar

4. Esperar procesamiento ⏳
   2-5 segundos (15 etapas)

5. Explorar resultados 🎉
   Ver las 4 pestañas

6. Descargar/Compartir 💾
   Exportar resultados
```

---

## 📝 Notas Importantes

- ⚠️ Este es un servidor de **desarrollo**. No usar en producción.
- 💡 Para mejor rendimiento, usa imágenes menores a 2 MB
- 🎯 Las mejores fotos son con buena iluminación y fondo simple
- 🔒 Todas las imágenes se procesan localmente en tu computadora

---

## 🆘 Obtener Ayuda

Si encuentras problemas:

1. **Revisar la documentación**:
   - README.md (información general)
   - GUIA_RAPIDA_USO.md (guía de usuario)
   - Este archivo (instrucciones de ejecución)

2. **Verificar los logs**:
   - La terminal donde corre el servidor muestra errores útiles

3. **Reportar issues**:
   - Usa GitHub Issues: https://github.com/Racio08/outfit-ai/issues

---

## ✅ Verificación de Instalación Exitosa

Para verificar que todo está correctamente instalado:

```bash
# 1. Verificar Python
python --version
# Debería mostrar: Python 3.8 o superior

# 2. Verificar dependencias principales
python -c "import django; import cv2; import numpy; print('✅ Todo instalado correctamente')"

# 3. Verificar migraciones
python manage.py showmigrations
# Debería mostrar todas las migraciones con [X]

# 4. Iniciar servidor de prueba
python manage.py check
# Debería mostrar: System check identified no issues
```

---

## 🎓 Próximos Pasos

Una vez que el programa esté corriendo:

1. **Lee** GUIA_RAPIDA_USO.md para aprender a usar todas las características
2. **Experimenta** con diferentes tipos de imágenes
3. **Explora** las 15 etapas de preprocesamiento
4. **Compara** los resultados de diferentes fotos
5. **Disfruta** del análisis y recomendaciones

---

**¡Listo! Ya puedes usar Outfit AI 🎉**

Para cualquier pregunta adicional, revisa la documentación o abre un issue en GitHub.
