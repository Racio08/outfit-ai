# 🚀 Guía de Inicio Rápido - Outfit AI

## ✅ Estado del Sistema

El sistema **Outfit AI** está completamente configurado y listo para ejecutarse.

## 📋 Requisitos Previos

- **Sistema Operativo**: Ubuntu/Debian Linux
- **Python**: 3.8 o superior
- **Conexión a Internet**: Para instalar dependencias (primera ejecución)

## 🎯 Opciones de Ejecución

### Opción 1: Script Automático (Recomendado)

El método más simple es usar el script de ejecución automática:

```bash
./ejecutar.sh
```

Este script:
- ✅ Verifica dependencias
- ✅ Instala paquetes necesarios
- ✅ Configura Django
- ✅ Ejecuta demo de preprocesamiento
- ✅ Inicia el servidor web en http://localhost:8000

### Opción 2: Servidor Django (Manual)

Si prefieres ejecutar solo el servidor Django:

```bash
# 1. Instalar dependencias (solo primera vez)
sudo apt-get update
sudo apt-get install -y python3-django python3-opencv python3-numpy python3-pil \
                        python3-matplotlib python3-pandas python3-scipy \
                        python3-seaborn python3-plotly python3-skimage

# 2. Configurar Django
python3 manage.py migrate
mkdir -p media static

# 3. Iniciar servidor
python3 manage.py runserver 0.0.0.0:8000
```

**Acceso**: http://localhost:8000

### Opción 3: Aplicación Gradio (Alternativa)

Para la interfaz Gradio simple:

```bash
# 1. Instalar Gradio
pip install gradio

# 2. Ejecutar aplicación
python3 main.py
```

**Acceso**: http://localhost:7860

## 🌐 Interfaces Disponibles

### Interfaz Django (Puerto 8000)

**Características completas**:
- 📊 Sistema de preprocesamiento con 15 etapas
- 🎨 Análisis facial y colorimetría
- 👔 Recomendaciones de outfit personalizadas
- 📈 Gráficos y estadísticas detalladas
- 🌟 Visualización 3D interactiva

**URL**: http://localhost:8000

### Interfaz Gradio (Puerto 7860)

**Características básicas**:
- 🖼️ Procesamiento simple de imágenes
- 👁️ Demostración de visión por computadora
- ⚡ Interfaz rápida y ligera

**URL**: http://localhost:7860

## 📸 Cómo Usar

### Usando la Interfaz Django:

1. **Abrir navegador** en http://localhost:8000
2. **Cargar imagen**: Arrastra una foto o usa el botón "Seleccionar Archivo"
3. **Esperar procesamiento**: Verás una barra de progreso
4. **Explorar resultados** en las 4 pestañas:
   - **Preprocesamiento**: 15 etapas con estadísticas
   - **Imágenes**: Resultados visuales
   - **Análisis**: Detección facial y colores
   - **Recomendaciones**: Sugerencias de outfit

### Usando la Interfaz Gradio:

1. **Abrir navegador** en http://localhost:7860
2. **Subir imagen** usando el área de carga
3. **Ver resultado** procesado instantáneamente

## 🔧 Solución de Problemas

### Error: "No se encuentra manage.py"

**Solución**: Asegúrate de ejecutar desde el directorio del proyecto:

```bash
cd /ruta/al/proyecto/outfit-ai
./ejecutar.sh
```

### Error: "Module not found"

**Solución**: Instala las dependencias manualmente:

```bash
sudo apt-get install -y python3-django python3-opencv python3-numpy \
                        python3-pil python3-matplotlib python3-pandas \
                        python3-scipy python3-seaborn python3-plotly \
                        python3-skimage
```

### Puerto ya en uso

**Solución**: Detén procesos existentes:

```bash
# Detener Django
pkill -f "manage.py runserver"

# Detener Gradio
pkill -f "main.py"

# O usar otro puerto
python3 manage.py runserver 0.0.0.0:8080
```

### Error de permisos con apt-get

**Solución**: Usa sudo:

```bash
sudo ./ejecutar.sh
```

## 📊 Demo de Preprocesamiento

Para ejecutar solo la demostración de preprocesamiento:

```bash
python3 demo_preprocessing.py
```

Esto mostrará:
- Estadísticas de 8 etapas de procesamiento
- Mejoras de calidad
- Gráficos comparativos
- Histogramas de evolución

## 🎨 Tipos de Imágenes Recomendadas

### ✅ Funcionan Mejor:
- Fotos de personas con buena iluminación
- Selfies con outfit completo
- Fotos de catálogos de moda
- Fondos simples y limpios

### ⚠️ Evitar:
- Imágenes muy oscuras o borrosas
- Fondos muy complejos
- Archivos muy grandes (>5MB)

## 📝 Notas Importantes

1. **Primera ejecución**: La instalación de dependencias puede tomar 5-10 minutos
2. **Conexión a Internet**: Necesaria solo para la primera instalación
3. **Recursos**: Se recomienda al menos 2GB de RAM
4. **Navegadores**: Compatible con Chrome, Firefox, Safari, Edge

## 🎯 Siguiente Pasos

1. ✅ Ejecutar el sistema con `./ejecutar.sh`
2. 📸 Probar con algunas imágenes de prueba
3. 📊 Explorar las estadísticas de preprocesamiento
4. 🎨 Revisar las recomendaciones de outfit
5. 🌟 Experimentar con diferentes tipos de imágenes

## 💡 Tips Avanzados

- **Exportar resultados**: Los análisis se pueden exportar en formato JSON
- **Múltiples imágenes**: Procesa varias imágenes para comparar
- **Personalización**: Modifica `outfit_ai/settings.py` para ajustes avanzados

## 📞 Soporte

Para más información, consulta:
- `README.md` - Documentación completa
- `GUIA_RAPIDA_USO.md` - Guía detallada de uso
- `SYSTEM_CHECK.md` - Verificación del sistema

---

**¡Disfruta usando Outfit AI!** 🎉
