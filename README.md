# 🧠 Outfit AI - Sistema Avanzado de Análisis de Imagen y Recomendación de Outfits

Un sistema inteligente de análisis de imágenes con **preprocesamiento avanzado**, análisis de colorimetría facial, y recomendaciones de outfit personalizadas. El núcleo del sistema es un motor de preprocesamiento que genera estadísticas completas, histogramas detallados y métricas de calidad en cada etapa del procesamiento.

## 🔥 Características Principales

### 📊 **Sistema de Preprocesamiento Avanzado** (Núcleo del Programa)
- **Análisis estadístico completo** en cada etapa del procesamiento
- **Tablas de estadísticas detalladas** con métricas de calidad
- **Histogramas evolutivos** de cada canal RGB por etapa
- **Gráficos de radar** comparando métricas de calidad
- **8 etapas de procesamiento** con optimización automática:
  1. **Original** - Análisis de imagen base
  2. **Resized** - Redimensionamiento inteligente con preservación de aspecto
  3. **Corrected** - Detección y corrección automática de problemas
  4. **CLAHE Enhanced** - Ecualización adaptativa de histograma
  5. **Denoised** - Reducción de ruido con preservación de bordes
  6. **Sharpened** - Mejora de nitidez controlada
  7. **Color Corrected** - Ajuste de saturación y brillo
  8. **Final** - Resultado optimizado

### 🎨 **Análisis Inteligente de Color**
- Detección facial automática con OpenCV
- Extracción de tono de piel y análisis de colorimetría
- Generación de paletas de colores personalizadas
- Análisis de colores dominantes con algoritmos avanzados

### 👔 **Sistema de Recomendaciones**
- Generación de 3 outfits diferentes por análisis
- Estilos: Profesional, Casual y Moderno/Trendy
- Recomendaciones basadas en teoría del color
- Consejos de estilo personalizados

### 📈 **Visualizaciones Avanzadas**
- Gráficos comparativos de métricas (brillo, contraste, nitidez)
- Histogramas evolutivos RGB por etapa
- Gráficos de radar de calidad (antes vs después)
- Visualizaciones 3D con Plotly
- Maniquí virtual 3D con Three.js

## 🏗️ Arquitectura del Proyecto

```
outfit_ai/
├── manage.py                    # Django management
├── requirements.txt             # Dependencias del proyecto
├── demo_preprocessing.py        # Demo del sistema de preprocesamiento
├── assets/                      # Modelos 3D, HDR, etc.
├── static/                      # CSS, JS estáticos
├── media/                       # Archivos subidos y procesados
├── outfit_ai/                   # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── outfits/                     # Aplicación principal
│   ├── models.py                # Modelos de datos
│   ├── views.py                 # Vistas y API endpoints
│   ├── urls.py                  # URLs de la aplicación
│   └── processing/              # Módulos de procesamiento
│       ├── preprocessing.py     # ⭐ NÚCLEO: Preprocesamiento avanzado
│       ├── analysis.py          # Análisis facial y colorimetría
│       ├── recommendation.py    # Sistema de recomendaciones
│       ├── render.py            # Renderizado y overlays
│       ├── mannequin3d.py       # Visualización 3D con Plotly
│       └── threejs.py           # Generador HTML para Three.js
└── templates/
    └── outfits/
        └── home.html            # Interfaz web avanzada
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Racio08/outfit-ai.git
cd outfit-ai
```

### 2. Instalar Dependencias
```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-tk libgl1-mesa-glx libglib2.0-0

# Instalar dependencias Python
pip install -r requirements.txt
```

### 3. Configurar Django
```bash
# Aplicar migraciones
python manage.py migrate

# (Opcional) Crear superusuario
python manage.py createsuperuser
```

### 4. Ejecutar el Sistema
```bash
# Ejecutar demo de preprocesamiento
python demo_preprocessing.py

# Iniciar servidor web
python manage.py runserver 0.0.0.0:8000
```

## 📊 Demostración del Sistema

### Ejecutar Demo Completa
```bash
python demo_preprocessing.py
```

**Salida esperada:**
```
🧠 DEMOSTRACIÓN DEL SISTEMA AVANZADO DE PREPROCESAMIENTO
=================================================================

📸 Creando imagen de muestra...
✅ Imagen guardada en: /tmp/tmpx__57zch.png

🔧 Inicializando procesador de imágenes...

🚀 Iniciando procesamiento completo...
✅ Procesamiento completado exitosamente!

📊 RESUMEN DEL PROCESAMIENTO:
----------------------------------------
📊 Etapas completadas: 8
📋 Secuencia: original → resized → corrected → clahe_enhanced → denoised → sharpened → color_corrected → final

📈 MEJORAS EN CALIDAD:
• Contraste: -2.81
• Nitidez: +2380.28
• Reducción de ruido: -3.59
• Saturación: +0.83

💾 CAMBIOS DE TAMAÑO:
• Original: 1.37 MB
• Final: 0.75 MB
• Cambio: -45.4%

📈 GRÁFICOS GENERADOS:
✅ Gráfico de comparación de métricas generado
✅ Histogramas de evolución generados
✅ Gráfico de radar de calidad generado
```

## 💻 Uso de la Interfaz Web

1. **Acceder a la aplicación**: `http://localhost:8000`
2. **Subir imagen**: Arrastra o selecciona una imagen (JPG, PNG, WEBP máx. 5MB)
3. **Ver procesamiento en tiempo real**: Barra de progreso con 6 etapas
4. **Explorar resultados**: 4 pestañas con análisis completo:
   - **Preprocesamiento y Estadísticas**: Tablas, gráficos comparativos, histogramas
   - **Resultados Visuales**: Imagen procesada y overlay de colores
   - **Análisis de Color**: Detección facial y paletas generadas
   - **Recomendaciones**: 3 outfits personalizados con consejos

## 🧪 API Endpoints

### POST `/process/`
Procesa una imagen completa con análisis avanzado.

**Request:**
```javascript
FormData: {
  image: File // Imagen a procesar
}
```

**Response:**
```javascript
{
  "success": true,
  "processing_summary": {
    "processing_time": 1.45,
    "corrections_applied": ["Mejora de nitidez", "Corrección de saturación"],
    "stages_completed": ["original", "resized", "corrected", ...],
    "quality_improvement": {
      "contrast_improvement": -2.76,
      "sharpness_improvement": 2452.25,
      "noise_reduction": -3.82,
      "saturation_enhancement": 1.11
    }
  },
  "preprocessing_stats": {
    "summary_text": "Resumen detallado...",
    "statistics_table": "<table>...</table>",
    "charts": {
      "comparison_charts": "base64_image",
      "histograms": "base64_image", 
      "quality_radar": "base64_image"
    }
  },
  "analysis_results": {
    "face_detected": true,
    "skin_tone": [183, 151, 126],
    "color_palette": {
      "primary": ["#8B4513", "#CD853F"],
      "accent": ["#DC143C", "#FF6347"],
      "neutral": ["#F5F5DC", "#FFFFF0"]
    }
  },
  "outfit_recommendations": [...],
  "images": {
    "processed": "data:image/png;base64,...",
    "palette_overlay": "data:image/png;base64,..."
  }
}
```

## 📋 Dependencias Principales

```
Django==5.2.7              # Framework web
opencv-python-headless      # Procesamiento de imagen
numpy>=1.24.0              # Operaciones numéricas
scikit-image>=0.21.0       # Algoritmos de imagen avanzados
matplotlib>=3.7.0          # Generación de gráficos
seaborn>=0.12.0           # Visualizaciones estadísticas
pandas>=2.0.0             # Manipulación de datos
plotly>=5.15.0            # Gráficos interactivos 3D
PIL (Pillow)              # Manipulación de imagen
mediapipe>=0.10.0         # ML para análisis facial
scipy>=1.11.0             # Algoritmos científicos
```

## 📈 Métricas y Estadísticas

El sistema genera métricas detalladas en cada etapa:

### Métricas de Calidad
- **Brillo Promedio**: Luminosidad general (0-255)
- **Contraste (Std)**: Variabilidad de intensidades
- **Nitidez (Laplacian)**: Claridad de bordes y detalles
- **Nivel de Ruido**: Cantidad de artefactos indeseados
- **Saturación Promedio**: Intensidad de colores

### Estadísticas RGB
- Valores promedio, mínimo, máximo y mediana por canal
- Desviación estándar para análisis de distribución
- Histogramas de 256 bins por canal RGB

### Métricas de Archivo
- Tamaño en MB por etapa
- Cambio porcentual de tamaño
- Dimensiones de imagen

## 🎨 Sistema de Paletas de Color

### Análisis de Subtono de Piel
- **Cálido**: Rojos, amarillos, dorados
- **Frío**: Azules, púrpuras, plateados  
- **Neutro**: Grises balanceados, colores mixtos

### Generación de Paletas
- **Colores Primarios**: Base versátil para looks diarios
- **Colores de Acento**: Para destacar y añadir personalidad
- **Colores Neutros**: Fundamento equilibrado

## 🏷️ Estilos de Outfit

### 👔 Profesional/Formal
- Líneas limpias y estructuradas
- Colores neutros con acentos sutiles
- Proporciones equilibradas

### 👕 Casual/Diario  
- Comodidad sin sacrificar estilo
- Juego con texturas y capas
- Flexibilidad en combinaciones

### 🌟 Moderno/Trendy
- Combinaciones audaces de color
- Mezcla de patrones y texturas
- Accesorios statement como focal point

## 🛠️ Contribución

### Estructura de Commits
```
feat: nueva funcionalidad de análisis de color
fix: corregir error en detección facial  
docs: actualizar documentación de API
style: mejorar formato de código
refactor: optimizar algoritmo de preprocesamiento
test: agregar tests de integración
```

### Desarrollo Local
```bash
# Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# Instalar dependencias de desarrollo
pip install ipython jupyter

# Ejecutar tests
python manage.py test

# Verificar estilo de código
flake8 outfits/

# Commit y push
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Racio08** - Desarrollo principal y arquitectura del sistema

## 🔮 Roadmap

### v2.0 Planificado
- [ ] Integración con modelos ML de reconocimiento de ropa
- [ ] Sistema de recomendaciones basado en ML
- [ ] Análisis de tendencias de moda
- [ ] API REST completa con documentación OpenAPI
- [ ] Aplicación móvil React Native
- [ ] Sistema de usuarios y favoritos
- [ ] Integración con tiendas online

### v2.1 Futuro
- [ ] Análisis de tipo de cuerpo
- [ ] Recomendaciones por ocasión y clima
- [ ] Realidad aumentada para probarse outfits
- [ ] Sistema de calificaciones y reviews
- [ ] Integración con redes sociales

---

## 📞 Soporte

Para reportar bugs o solicitar features, por favor usa [GitHub Issues](https://github.com/Racio08/outfit-ai/issues).

Para preguntas de desarrollo, consulta la [documentación de la API](./docs/api.md) o contacta al equipo.

---

**⭐ Si este proyecto te ha sido útil, ¡considera darle una estrella en GitHub!**
Desarrollar un sistema (usando Python y herramientas web) que, a partir de una imagen de una persona, analice sus características faciales (ojos, facciones, forma de cara, peinado) y sugiera un atuendo completo (con tipos de prendas y colores) adaptado a su género.
