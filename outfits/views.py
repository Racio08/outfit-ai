from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import json
import base64
import io
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para servidor
import matplotlib.pyplot as plt
import pandas as pd

from .processing.preprocessing import ImagePreprocessor
from .processing.analysis import FacialAnalyzer, ColorAnalyzer  
from .processing.recommendation import OutfitRecommender
from .processing.render import RenderEngine
from .processing.mannequin3d import Mannequin3D


def convert_numpy_types(obj):
    """Convierte tipos NumPy a tipos Python nativos para serialización JSON"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    else:
        return obj


def home(request):
    """Vista principal para subida de imagen"""
    return render(request, 'outfits/home.html')


@csrf_exempt
def process_image(request):
    """Vista principal para procesamiento completo de imagen"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No se encontró imagen'}, status=400)
    
    try:
        # Inicializar procesadores
        preprocessor = ImagePreprocessor()
        facial_analyzer = FacialAnalyzer()
        color_analyzer = ColorAnalyzer()
        recommender = OutfitRecommender()
        render_engine = RenderEngine()
        
        # Procesar imagen
        uploaded_file = request.FILES['image']
        
        # 1. PREPROCESAMIENTO COMPLETO
        processed_image, processing_summary = preprocessor.process_upload_complete(uploaded_file)
        
        # 2. ANÁLISIS FACIAL
        face_coords = facial_analyzer.detect_face(processed_image)
        skin_tone = facial_analyzer.extract_skin_tone(processed_image, face_coords)
        color_palette = facial_analyzer.analyze_color_palette(skin_tone)
        
        # 3. ANÁLISIS DE COLOR
        dominant_colors = color_analyzer.extract_dominant_colors(processed_image)
        
        # 4. GENERACIÓN DE RECOMENDACIONES
        outfit_recommendations = recommender.generate_recommendations(color_palette)
        style_tips = recommender.get_style_tips(color_palette)
        
        # 5. RENDERIZADO Y VISUALIZACIONES
        palette_overlay = render_engine.create_color_palette_overlay(processed_image, color_palette)
        
        # 6. GENERAR ESTADÍSTICAS Y GRÁFICOS
        stats_table = preprocessor.generate_statistics_table()
        
        # Generar gráficos y guardarlos
        charts_fig = preprocessor.generate_comparison_charts()
        histograms_fig = preprocessor.generate_histograms_comparison()  
        radar_fig = preprocessor.generate_quality_metrics_radar()
        
        # Convertir gráficos a base64
        charts_base64 = _fig_to_base64(charts_fig)
        histograms_base64 = _fig_to_base64(histograms_fig)
        radar_base64 = _fig_to_base64(radar_fig)
        
        # Convertir imágenes a base64
        processed_image_base64 = render_engine.image_to_base64(processed_image)
        palette_overlay_base64 = render_engine.image_to_base64(palette_overlay)
        
        # Convertir todas las imágenes de las 15 etapas a base64
        stage_descriptions = {
            'original': '📸 Imagen Original',
            'resized': '📏 Redimensionado Inteligente',
            'normalized': '🎨 Colores Normalizados',
            'gamma_corrected': '💡 Corrección Gamma Adaptativa',
            'edge_preserved': '🖼️ Preservación de Bordes',
            'clahe': '🌟 CLAHE - Ecualización Adaptativa',
            'bilateral': '✨ Filtro Bilateral Suavizado',
            'edges_enhanced': '🔲 Realce de Contornos',
            'saturation_enhanced': '🌈 Saturación Mejorada',
            'white_balanced': '⚖️ Balance de Blancos',
            'sharpened': '🔪 Nitidez Mejorada',
            'texture_enhanced': '🧵 Textura Realzada',
            'denoised': '🧹 Reducción de Ruido',
            'final_contrast': '🎭 Contraste Final Ajustado',
            'final_optimization': '✅ Optimización Final'
        }
        
        stage_images_base64 = {}
        for stage_name, stage_image in preprocessor.stage_images.items():
            stage_img_pil = Image.fromarray(stage_image)
            stage_images_base64[stage_name] = {
                'image': render_engine.image_to_base64(stage_img_pil),
                'description': stage_descriptions.get(stage_name, stage_name),
                'stats': convert_numpy_types(preprocessor.processing_stats.get(stage_name, {}))
            }
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'processing_summary': convert_numpy_types(processing_summary),
            'preprocessing_stats': {
                'summary_text': preprocessor.get_processing_summary(),
                'statistics_table': stats_table.to_html(classes='table table-striped', table_id='stats-table'),
                'charts': {
                    'comparison_charts': charts_base64,
                    'histograms': histograms_base64,
                    'quality_radar': radar_base64
                }
            },
            'analysis_results': {
                'face_detected': face_coords is not None,
                'skin_tone': convert_numpy_types(skin_tone),
                'color_palette': convert_numpy_types(color_palette),
                'dominant_colors': convert_numpy_types(dominant_colors)
            },
            'outfit_recommendations': convert_numpy_types(outfit_recommendations),
            'style_tips': convert_numpy_types(style_tips),
            'images': {
                'processed': processed_image_base64,
                'palette_overlay': palette_overlay_base64
            },
            'preprocessing_stages': {
                'total_stages': len(stage_images_base64),
                'stages': stage_images_base64,
                'stage_order': list(preprocessor.stage_images.keys())
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error procesando imagen: {str(e)}'
        }, status=500)


def _fig_to_base64(fig):
    """Convierte figura matplotlib a base64"""
    if fig is None:
        return None
        
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)  # Liberar memoria
    
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


def get_processing_statistics(request):
    """Vista para obtener estadísticas detalladas del último procesamiento"""
    try:
        preprocessor = ImagePreprocessor()
        stats = preprocessor.processing_stats
        
        # Convertir tipos NumPy en las estadísticas
        converted_stats = convert_numpy_types(stats)
        
        return JsonResponse({
            'success': True,
            'statistics': converted_stats,
            'message': 'Estadísticas del último procesamiento'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error obteniendo estadísticas: {str(e)}'
        }, status=500)


def download_statistics_report(request):
    """Vista para descargar reporte completo de estadísticas"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        # Crear procesador temporal para generar reporte
        preprocessor = ImagePreprocessor()
        
        # Generar archivo de reporte
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            report_path = preprocessor.export_statistics_report(tmp_file.name)
        
        # Leer archivo y enviarlo como respuesta
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = f.read()
        
        # Limpiar archivo temporal
        os.unlink(report_path)
        
        response = HttpResponse(report_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="preprocessing_report.json"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error generando reporte: {str(e)}'
        }, status=500)


def get_3d_visualization(request):
    """Vista para generar visualización 3D"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        # Obtener datos del outfit de la sesión o request
        outfit_data = json.loads(request.body) if request.body else {}
        
        # Generar visualización 3D
        mannequin = Mannequin3D()
        
        if outfit_data:
            fig = mannequin.create_outfit_visualization(outfit_data)
        else:
            # Usar datos de ejemplo
            example_outfit = {
                'style': 'Casual',
                'pieces': {
                    'top': {'color': '#4682B4'},
                    'bottom': {'color': '#2F4F4F'}
                }
            }
            fig = mannequin.create_outfit_visualization(example_outfit)
        
        # Convertir a JSON para Plotly.js
        plotly_json = mannequin.get_plotly_json(fig)
        
        # Convertir plotly_json si no es None
        plotly_data = json.loads(plotly_json) if plotly_json else {}
        
        return JsonResponse({
            'success': True,
            'plotly_json': convert_numpy_types(plotly_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error generando visualización 3D: {str(e)}'
        }, status=500)
