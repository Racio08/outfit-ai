#!/usr/bin/env python3
"""
Demostración del sistema avanzado de preprocesamiento de imágenes
Este script crea una imagen de ejemplo y la procesa mostrando todas las estadísticas
"""

import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tempfile

# Configurar Django
sys.path.append('/workspaces/outfit-ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outfit_ai.settings')
django.setup()

from outfits.processing.preprocessing import ImagePreprocessor

def create_sample_image():
    """Crea una imagen de ejemplo para probar el sistema"""
    # Crear una imagen con gradientes y ruido
    width, height = 800, 600
    
    # Crear imagen base
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Agregar gradiente de fondo
    for y in range(height):
        # Crear gradiente de azul a blanco
        blue_value = int(255 * (1 - y / height))
        color = (100, 150, blue_value)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Agregar algunas formas geométricas
    # Círculo
    draw.ellipse([50, 50, 200, 200], fill=(255, 100, 100), outline=(0, 0, 0), width=2)
    
    # Rectángulo
    draw.rectangle([300, 100, 500, 300], fill=(100, 255, 100), outline=(0, 0, 0), width=2)
    
    # Triángulo
    draw.polygon([(600, 400), (700, 200), (750, 450)], fill=(255, 255, 100), outline=(0, 0, 0), width=2)
    
    # Agregar texto
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 450), "Outfit AI Demo", fill=(0, 0, 0), font=font)
    
    # Agregar ruido artificial
    img_array = np.array(img)
    noise = np.random.normal(0, 15, img_array.shape).astype(np.int16)
    noisy_img = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_img)

def demonstrate_preprocessing():
    """Demuestra el sistema completo de preprocesamiento"""
    print("🧠 DEMOSTRACIÓN DEL SISTEMA AVANZADO DE PREPROCESAMIENTO")
    print("=" * 65)
    
    # Crear imagen de muestra
    print("\n📸 Creando imagen de muestra...")
    sample_image = create_sample_image()
    
    # Guardar imagen temporal
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        sample_image.save(tmp_file.name)
        temp_path = tmp_file.name
    
    print(f"✅ Imagen guardada en: {temp_path}")
    
    # Inicializar procesador
    print("\n🔧 Inicializando procesador de imágenes...")
    preprocessor = ImagePreprocessor()
    
    # Procesar imagen
    print("\n🚀 Iniciando procesamiento completo...")
    try:
        with open(temp_path, 'rb') as f:
            processed_image, processing_summary = preprocessor.process_upload_complete(f)
        
        print("✅ Procesamiento completado exitosamente!")
        
        # Mostrar resumen
        print("\n📊 RESUMEN DEL PROCESAMIENTO:")
        print("-" * 40)
        print(preprocessor.get_processing_summary())
        
        # Generar tabla de estadísticas
        print("\n📋 TABLA DE ESTADÍSTICAS DETALLADAS:")
        print("-" * 45)
        stats_table = preprocessor.generate_statistics_table()
        print(stats_table.to_string(index=False))
        
        # Información sobre gráficos
        print("\n📈 GRÁFICOS GENERADOS:")
        print("-" * 25)
        
        try:
            # Generar gráficos (se guardarán en memoria)
            comparison_fig = preprocessor.generate_comparison_charts()
            if comparison_fig:
                print("✅ Gráfico de comparación de métricas generado")
            
            histograms_fig = preprocessor.generate_histograms_comparison()
            if histograms_fig:
                print("✅ Histogramas de evolución generados")
            
            radar_fig = preprocessor.generate_quality_metrics_radar()
            if radar_fig:
                print("✅ Gráfico de radar de calidad generado")
            
            # Cerrar figuras para liberar memoria
            import matplotlib.pyplot as plt
            plt.close('all')
            
        except Exception as e:
            print(f"⚠️  Error generando gráficos: {e}")
        
        # Estadísticas de procesamiento
        print(f"\n⏱️  ESTADÍSTICAS DE RENDIMIENTO:")
        print("-" * 35)
        print(f"• Tiempo total: {processing_summary['processing_time']:.2f} segundos")
        print(f"• Etapas completadas: {len(processing_summary['stages_completed'])}")
        print(f"• Correcciones aplicadas: {len(processing_summary['corrections_applied'])}")
        
        if processing_summary['corrections_applied']:
            print("\n🔧 CORRECCIONES APLICADAS:")
            for correction in processing_summary['corrections_applied']:
                print(f"  • {correction}")
        
        # Información sobre mejoras de calidad
        if 'quality_improvement' in processing_summary:
            improvements = processing_summary['quality_improvement']
            print(f"\n📈 MEJORAS DE CALIDAD:")
            print(f"  • Contraste: {improvements.get('contrast_improvement', 0):+.2f}")
            print(f"  • Nitidez: {improvements.get('sharpness_improvement', 0):+.2f}")  
            print(f"  • Reducción de ruido: {improvements.get('noise_reduction', 0):+.2f}")
            print(f"  • Saturación: {improvements.get('saturation_enhancement', 0):+.2f}")
        
        # Información del archivo
        print(f"\n💾 INFORMACIÓN DEL ARCHIVO:")
        if 'file_size_change' in processing_summary:
            size_info = processing_summary['file_size_change']
            print(f"  • Tamaño original: {size_info.get('original_mb', 0):.2f} MB")
            print(f"  • Tamaño final: {size_info.get('final_mb', 0):.2f} MB")
            print(f"  • Cambio: {size_info.get('size_change_percent', 0):+.1f}%")
        
        # Guardar imagen procesada
        output_path = "/workspaces/outfit-ai/media/demo_processed.png"
        processed_image.save(output_path)
        print(f"\n💾 Imagen procesada guardada en: {output_path}")
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(temp_path)
            print(f"\n🧹 Archivo temporal eliminado: {temp_path}")
        except:
            pass
    
    print("\n🎉 DEMOSTRACIÓN COMPLETADA")
    print("=" * 30)
    print("\n📌 El servidor Django está disponible en: http://localhost:8000")
    print("📌 Puedes subir tus propias imágenes para ver el análisis completo")

if __name__ == "__main__":
    demonstrate_preprocessing()