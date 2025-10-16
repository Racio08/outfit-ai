# 🚀 Guía Rápida de Uso - Sistema de 15 Etapas

## ✅ Estado del Sistema
**🟢 SERVIDOR ACTIVO**: http://0.0.0.0:8000/

---

## 📋 Pasos para Probar el Sistema

### 1️⃣ Abrir la Aplicación
- **URL Local**: http://127.0.0.1:8000/
- **URL Codespace**: Usar el navegador simple de VS Code (ya abierto)

### 2️⃣ Cargar una Imagen

Tienes 3 opciones:

#### Opción A: Arrastrar y Soltar 🖱️
1. Busca una imagen en tu computadora
2. Arrástrala a la zona de carga (área con borde punteado)
3. Suelta la imagen

#### Opción B: Seleccionar Archivo 📁
1. Clic en el botón azul **"Seleccionar Archivo"**
2. Navega a tu imagen
3. Selecciona y abre

#### Opción C: Tomar Foto 📸
1. Clic en el botón verde **"Tomar Foto"**
2. Permite acceso a la cámara
3. Captura la foto
4. Confirma con **"Usar esta Foto"**

### 3️⃣ Ver el Procesamiento

Mientras se procesa verás:
- ⏳ Barra de progreso
- 📝 Lista de etapas completándose
- ✅ Checkmarks en cada etapa terminada

### 4️⃣ Explorar los Resultados

Una vez completado, verás **4 pestañas**:

#### 📊 Pestaña: Preprocesamiento
**¡AQUÍ ESTÁN LAS 15 ETAPAS!**

Desplázate hacia abajo y verás la **Galería de 15 Etapas**:

```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  1  📸 Original     │ │  2  📏 Redimensión  │ │  3  🎨 Normalizado  │
│  [Imagen]           │ │  [Imagen]           │ │  [Imagen]           │
│  📊 Estadísticas    │ │  📊 Estadísticas    │ │  📊 Estadísticas    │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘

┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  4  💡 Gamma        │ │  5  🖼️ Bordes       │ │  6  🌟 CLAHE        │
│  [Imagen]           │ │  [Imagen]           │ │  [Imagen]           │
│  📊 Estadísticas    │ │  📊 Estadísticas    │ │  📊 Estadísticas    │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘

... y así hasta la etapa 15
```

Cada tarjeta muestra:
- 🖼️ **Imagen procesada** de esa etapa
- 📝 **Descripción** con emoji
- 📊 **5-7 estadísticas**:
  - Media
  - Desviación estándar
  - Contraste
  - Nitidez
  - Densidad de bordes

Más abajo verás:
- 📈 **Gráficos comparativos** entre etapas
- 📊 **Histogramas** de evolución
- 🎯 **Gráfico de radar** con métricas de calidad

#### 🖼️ Pestaña: Imágenes
- Imagen procesada final
- Overlay de paleta de colores

#### 🔬 Pestaña: Análisis
- Detección facial
- Tono de piel
- Paleta de colores recomendada
- Colores dominantes

#### ✨ Pestaña: Recomendaciones
- Sugerencias de outfit personalizadas
- Tips de estilo
- Combinaciones de colores

---

## 🎨 Las 15 Etapas Explicadas

| # | Emoji | Nombre | Qué Hace |
|---|-------|--------|----------|
| 1 | 📸 | Original | Imagen sin modificar |
| 2 | 📏 | Redimensionado | Ajusta tamaño óptimo |
| 3 | 🎨 | Normalización | Equilibra colores RGB |
| 4 | 💡 | Gamma Adaptativo | Corrige brillo automáticamente |
| 5 | 🖼️ | Preservación Bordes | Suaviza sin perder contornos |
| 6 | 🌟 | CLAHE | Mejora contraste local |
| 7 | ✨ | Bilateral | Reduce ruido, mantiene bordes |
| 8 | 🔲 | Realce Contornos | Define bordes importantes |
| 9 | 🌈 | Saturación | Colores más vivos |
| 10 | ⚖️ | Balance Blancos | Corrige temperatura color |
| 11 | 🔪 | Nitidez | Detalles más definidos |
| 12 | 🧵 | Textura | Realza texturas de tela |
| 13 | 🧹 | Reducción Ruido | Limpia la imagen |
| 14 | 🎭 | Contraste Final | Ajusta claridad máxima |
| 15 | ✅ | Optimización | Normalización final |

---

## 🖼️ Imágenes Recomendadas para Probar

### ✅ Funcionan Mejor:
- 👔 Fotos de ropa sobre fondo liso
- 👕 Selfies con outfit completo
- 👗 Fotos de catálogos de moda
- 🧥 Imágenes con buena iluminación

### ⚠️ Evitar:
- ❌ Imágenes muy oscuras o borrosas
- ❌ Fondos muy complejos o desordenados
- ❌ Fotos con mucho movimiento
- ❌ Archivos muy grandes (>5MB)

---

## 🔍 Qué Buscar en los Resultados

### Comparar Etapas
Observa cómo cada etapa mejora:
1. **Etapas 1-5**: Preparación básica
2. **Etapas 6-10**: Mejora de calidad visual
3. **Etapas 11-15**: Refinamiento y optimización

### Estadísticas Clave
- **Media alta** (>100): Imagen clara
- **Contraste alto** (>0.7): Buena definición
- **Nitidez alta** (>200): Detalles nítidos
- **Baja densidad bordes** (<0.05): Imagen limpia

### Progreso Visual
Desplázate por las 15 tarjetas y nota:
- Cómo mejora el brillo (etapas 3-4)
- Cómo se definen los bordes (etapas 5-8)
- Cómo se intensifican los colores (etapa 9)
- Cómo se limpia el ruido (etapa 13)

---

## 🎯 Ejemplo de Flujo Completo

```
1. Abrir http://127.0.0.1:8000/ ✅
   ↓
2. Cargar imagen de prueba (ej: foto de camisa) ✅
   ↓
3. Esperar 2-5 segundos (procesamiento) ⏳
   ↓
4. Ver barra de progreso completarse ✅
   ↓
5. Hacer scroll en pestaña "Preprocesamiento" 📊
   ↓
6. Ver galería con 15 tarjetas de etapas 🎨
   ↓
7. Comparar imágenes y estadísticas 🔍
   ↓
8. Explorar gráficos debajo 📈
   ↓
9. Cambiar a otras pestañas 🖼️
   ↓
10. ¡Disfrutar los resultados! 🎉
```

---

## 🐛 Solución de Problemas

### Problema: No veo las 15 etapas
**Solución**: 
- Refresca la página (F5)
- Asegúrate de estar en la pestaña "Preprocesamiento"
- Haz scroll hacia abajo hasta ver "Galería de 15 Etapas"

### Problema: Error al cargar imagen
**Solución**:
- Verifica que sea JPG, PNG o WEBP
- Asegúrate que pese menos de 5MB
- Intenta con otra imagen más simple

### Problema: Procesamiento muy lento
**Solución**:
- Usa imágenes más pequeñas (<1MB)
- Cierra otras pestañas del navegador
- Espera pacientemente, 15 etapas toman tiempo

### Problema: No se ven las imágenes
**Solución**:
- Abre la consola del navegador (F12)
- Busca errores en rojo
- Verifica que el servidor esté corriendo
- Refresca la página

---

## 📊 Verificar que Funciona

### Checklist de Verificación:
- [ ] Servidor corriendo en puerto 8000
- [ ] Página web se carga correctamente
- [ ] Puedo cargar una imagen
- [ ] Veo barra de progreso con 15 etapas
- [ ] Aparece la galería de 15 etapas
- [ ] Cada etapa tiene su imagen
- [ ] Cada etapa tiene estadísticas
- [ ] Los gráficos se muestran correctamente

---

## 🎓 Tips Avanzados

### Compara Etapas Específicas
1. Abre dos ventanas del navegador lado a lado
2. Carga la misma imagen en ambas
3. Enfócate en diferentes etapas en cada ventana
4. Compara visualmente las diferencias

### Analiza el Progreso
- Etapa 1 vs 5: ¿Mejoró el brillo?
- Etapa 5 vs 10: ¿Los colores son más vivos?
- Etapa 10 vs 15: ¿Se ve más nítido?

### Prueba Diferentes Tipos de Ropa
- 👔 Formal: Trajes, camisas
- 👕 Casual: Camisetas, jeans
- 👗 Elegante: Vestidos, faldas
- 🧥 Exterior: Chaquetas, abrigos

---

## 📱 Responsive Design

El sistema funciona en:
- 💻 **Desktop**: 3 columnas de etapas
- 📱 **Tablet**: 2 columnas de etapas
- 📱 **Móvil**: 1 columna de etapas

Prueba redimensionar la ventana del navegador!

---

## 🎉 ¡Disfruta el Sistema!

Ya tienes todo listo para explorar las **15 etapas de preprocesamiento de imágenes**.

**Características destacadas:**
- ✨ Interfaz moderna con glassmorphism
- 🎨 Animaciones suaves y atractivas
- 📊 Datos estadísticos detallados
- 🖼️ Visualización completa paso a paso
- 🚀 Procesamiento rápido y eficiente

---

**Fecha**: 16 de Octubre, 2025  
**Versión**: 1.0  
**Estado**: 🟢 Completamente Funcional
