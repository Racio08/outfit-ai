"""
Preprocesamiento avanzado de imágenes usando OpenCV con análisis estadístico completo
"""
import cv2
import numpy as np
from PIL import Image, ImageOps
import io
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import ndimage
from skimage import exposure, filters, morphology, restoration
import pandas as pd
from collections import defaultdict
import time


class ImagePreprocessor:
    """Clase avanzada para el preprocesamiento de imágenes con análisis estadístico completo"""
    
    def __init__(self):
        self.target_size = (512, 512)
        self.processing_stats = defaultdict(dict)
        self.processing_history = []
        self.enable_statistics = True
        
        # Configuración de matplotlib para mejor visualización
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def calculate_image_statistics(self, image, stage_name):
        """Calcula estadísticas completas de la imagen"""
        if not self.enable_statistics:
            return {}
            
        # Convertir a numpy array si es PIL
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
            
        # Asegurar que esté en formato RGB
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            if img_array.dtype != np.uint8:
                img_array = (img_array * 255).astype(np.uint8)
        
        stats = {
            'timestamp': time.time(),
            'stage': stage_name,
            'dimensions': img_array.shape,
            'size_mb': img_array.nbytes / (1024 * 1024),
            'dtype': str(img_array.dtype),
            
            # Estadísticas de canales de color
            'mean_rgb': [],
            'std_rgb': [],
            'min_rgb': [],
            'max_rgb': [],
            'median_rgb': [],
            
            # Estadísticas globales
            'brightness': 0,
            'contrast': 0,
            'sharpness': 0,
            
            # Histogramas
            'histograms': {},
            
            # Información de calidad
            'blur_metric': 0,
            'noise_level': 0,
            'saturation_avg': 0,
        }
        
        # Calcular estadísticas por canal
        if len(img_array.shape) == 3:
            for i, channel in enumerate(['R', 'G', 'B']):
                channel_data = img_array[:, :, i]
                stats['mean_rgb'].append(float(np.mean(channel_data)))
                stats['std_rgb'].append(float(np.std(channel_data)))
                stats['min_rgb'].append(int(np.min(channel_data)))
                stats['max_rgb'].append(int(np.max(channel_data)))
                stats['median_rgb'].append(float(np.median(channel_data)))
                
                # Histograma
                hist, bins = np.histogram(channel_data.flatten(), bins=256, range=(0, 256))
                stats['histograms'][channel] = hist.tolist()
        
        # Estadísticas globales
        if len(img_array.shape) == 3:
            # Brillo promedio
            stats['brightness'] = float(np.mean(img_array))
            
            # Contraste (desviación estándar)
            stats['contrast'] = float(np.std(img_array))
            
            # Convertir a escala de grises para métricas adicionales
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Métrica de desenfoque (varianza del Laplaciano)
            stats['blur_metric'] = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            
            # Nivel de ruido (usando desviación estándar local)
            noise_kernel = np.ones((3, 3)) / 9
            smoothed = cv2.filter2D(gray.astype(np.float32), -1, noise_kernel)
            noise_diff = gray.astype(np.float32) - smoothed
            stats['noise_level'] = float(np.std(noise_diff))
            
            # Saturación promedio
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            saturation_channel = hsv[:, :, 1]
            stats['saturation_avg'] = float(np.mean(saturation_channel))
        
        # Guardar estadísticas
        self.processing_stats[stage_name] = stats
        
        return stats
    
    def resize_image_advanced(self, image, target_size=None, interpolation='lanczos'):
        """Redimensionamiento avanzado con múltiples algoritmos"""
        if target_size is None:
            target_size = self.target_size
            
        # Calcular estadísticas previas
        self.calculate_image_statistics(image, 'original')
        
        # Convertir PIL a OpenCV si es necesario
        if isinstance(image, Image.Image):
            pil_image = image
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        h, w = image.shape[:2]
        target_w, target_h = target_size
        
        # Calcular la proporción
        ratio = min(target_w / w, target_h / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        
        # Seleccionar método de interpolación
        interpolation_methods = {
            'nearest': cv2.INTER_NEAREST,
            'linear': cv2.INTER_LINEAR,
            'cubic': cv2.INTER_CUBIC,
            'lanczos': cv2.INTER_LANCZOS4,
            'area': cv2.INTER_AREA
        }
        
        interp_flag = interpolation_methods.get(interpolation, cv2.INTER_LANCZOS4)
        
        # Redimensionar
        resized = cv2.resize(image, (new_w, new_h), interpolation=interp_flag)
        
        # Crear canvas con fondo adaptativo
        canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        
        # Calcular color de fondo promedio de los bordes
        # Asegurar que image sea un array numpy
        if len(image.shape) == 3:
            border_pixels = np.vstack([
                image[0, :].reshape(-1, 3),  # Top
                image[-1, :].reshape(-1, 3), # Bottom
                image[:, 0].reshape(-1, 3),  # Left
                image[:, -1].reshape(-1, 3)  # Right
            ])
            border_mean = np.mean(border_pixels, axis=0)
            bg_color = border_mean.astype(np.uint8)
        else:
            # Usar color gris por defecto si hay problemas
            bg_color = np.array([128, 128, 128], dtype=np.uint8)
        
        canvas[:] = bg_color
        
        # Centrar la imagen redimensionada
        y_offset = (target_h - new_h) // 2
        x_offset = (target_w - new_w) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        # Calcular estadísticas después del resize
        result_pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        self.calculate_image_statistics(result_pil, 'resized')
        
        return canvas
    
    def enhance_image_advanced(self, image):
        """Mejora avanzada de la imagen con múltiples técnicas"""
        
        # 1. Corrección de iluminación adaptativa
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_l = clahe.apply(l_channel)
        lab[:, :, 0] = enhanced_l
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        self.calculate_image_statistics(Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)), 'clahe_enhanced')
        
        # 2. Reducción de ruido avanzada
        # Filtro bilateral para preservar bordes
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Reducción de ruido cromático
        denoised = cv2.fastNlMeansDenoisingColored(denoised, None, 10, 10, 7, 21)
        
        self.calculate_image_statistics(Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)), 'denoised')
        
        # 3. Mejora de sharpness
        # Crear kernel de sharpening
        sharpening_kernel = np.array([[-1, -1, -1],
                                    [-1,  9, -1],
                                    [-1, -1, -1]])
        
        sharpened = cv2.filter2D(denoised, -1, sharpening_kernel)
        
        # Mezclar imagen original con sharpened (50-50)
        enhanced_final = cv2.addWeighted(denoised, 0.7, sharpened, 0.3, 0)
        
        self.calculate_image_statistics(Image.fromarray(cv2.cvtColor(enhanced_final, cv2.COLOR_BGR2RGB)), 'sharpened')
        
        # 4. Corrección de color y saturación
        hsv = cv2.cvtColor(enhanced_final, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Ajustar saturación ligeramente
        hsv[:, :, 1] = hsv[:, :, 1] * 1.1  # Incrementar saturación 10%
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Ajustar valor (brillo) si es necesario
        brightness_factor = 1.05
        hsv[:, :, 2] = hsv[:, :, 2] * brightness_factor
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        final_result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        self.calculate_image_statistics(Image.fromarray(cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)), 'color_corrected')
        
        return final_result
    
    def detect_and_correct_issues(self, image):
        """Detecta y corrige problemas comunes en imágenes"""
        corrections_applied = []
        result = image.copy()
        
        # Convertir a PIL para análisis
        if not isinstance(image, Image.Image):
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_image = image
            result = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        img_array = np.array(pil_image)
        
        # 1. Detectar imagen muy oscura
        avg_brightness = np.mean(img_array)
        if avg_brightness < 80:
            corrections_applied.append("Corrección de brillo bajo")
            result = cv2.convertScaleAbs(result, alpha=1.3, beta=30)
        
        # 2. Detectar imagen muy clara (sobreexpuesta)
        elif avg_brightness > 200:
            corrections_applied.append("Corrección de sobreexposición")
            result = cv2.convertScaleAbs(result, alpha=0.8, beta=-20)
        
        # 3. Detectar bajo contraste
        contrast = np.std(img_array)
        if contrast < 40:
            corrections_applied.append("Mejora de contraste")
            lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
            l_channel = lab[:, :, 0]
            clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(l_channel)
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # 4. Detectar imagen desenfocada
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        blur_metric = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur_metric < 100:
            corrections_applied.append("Mejora de nitidez")
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            result = cv2.filter2D(result, -1, kernel)
        
        # 5. Detectar colores desaturados
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        saturation_channel = hsv[:, :, 1]
        avg_saturation = np.mean(saturation_channel)
        if avg_saturation < 60:
            corrections_applied.append("Mejora de saturación")
            hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return result, corrections_applied
    
    def process_upload_complete_extended(self, uploaded_file):
        """Procesamiento completo con 15 etapas de análisis estadístico"""
        try:
            start_time = time.time()
            
            # Leer la imagen original
            image = Image.open(uploaded_file)
            
            # Corregir orientación EXIF (importante para fotos de cámara)
            image = ImageOps.exif_transpose(image)
            
            # Convertir a RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convertir a numpy array para procesamiento
            current_image = np.array(image)
            
            # Lista para guardar todas las etapas con sus imágenes
            self.stage_images = {}
            
            # ETAPA 1: ORIGINAL
            self.calculate_image_statistics(image, 'step01_original')
            self.stage_images['step01_original'] = current_image.copy()
            
            # ETAPA 2: REDIMENSIONAMIENTO
            resized = self.resize_image_advanced(image)
            resized_array = np.array(resized)
            self.calculate_image_statistics(resized, 'step02_resized')
            self.stage_images['step02_resized'] = resized_array.copy()
            current_image = resized_array
            
            # ETAPA 3: NORMALIZACIÓN DE COLOR
            normalized = self._normalize_colors(current_image)
            self.calculate_image_statistics(Image.fromarray(normalized), 'step03_normalized')
            self.stage_images['step03_normalized'] = normalized.copy()
            current_image = normalized
            
            # ETAPA 4: CORRECCIÓN GAMMA ADAPTATIVA
            gamma_corrected = self._apply_adaptive_gamma(current_image)
            self.calculate_image_statistics(Image.fromarray(gamma_corrected), 'step04_gamma_corrected')
            self.stage_images['step04_gamma_corrected'] = gamma_corrected.copy()
            current_image = gamma_corrected
            
            # ETAPA 5: MEJORA CLAHE
            clahe_image = self.apply_clahe_enhancement(current_image)
            self.calculate_image_statistics(Image.fromarray(clahe_image), 'step05_clahe_enhanced')
            self.stage_images['step05_clahe_enhanced'] = clahe_image.copy()
            current_image = clahe_image
            
            # ETAPA 6: REDUCCIÓN DE RUIDO BILATERAL
            denoised = self.denoise_image(current_image)
            self.calculate_image_statistics(Image.fromarray(denoised), 'step06_denoised')
            self.stage_images['step06_denoised'] = denoised.copy()
            current_image = denoised
            
            # ETAPA 7: FILTRO PRESERVADOR DE BORDES
            edge_preserved = self._apply_edge_preserving(current_image)
            self.calculate_image_statistics(Image.fromarray(edge_preserved), 'step07_edge_preserved')
            self.stage_images['step07_edge_preserved'] = edge_preserved.copy()
            current_image = edge_preserved
            
            # ETAPA 8: DETECCIÓN Y MEJORA DE BORDES
            edges_enhanced = self._enhance_edges(current_image)
            self.calculate_image_statistics(Image.fromarray(edges_enhanced), 'step08_edges_enhanced')
            self.stage_images['step08_edges_enhanced'] = edges_enhanced.copy()
            current_image = edges_enhanced
            
            # ETAPA 9: SHARPENING ADAPTATIVO
            sharpened = self.sharpen_image(current_image)
            self.calculate_image_statistics(Image.fromarray(sharpened), 'step09_sharpened')
            self.stage_images['step09_sharpened'] = sharpened.copy()
            current_image = sharpened
            
            # ETAPA 10: CORRECCIÓN DE COLOR HSV
            color_corrected = self.correct_colors(current_image)
            color_corrected = cv2.cvtColor(color_corrected, cv2.COLOR_BGR2RGB)
            self.calculate_image_statistics(Image.fromarray(color_corrected), 'step10_color_corrected')
            self.stage_images['step10_color_corrected'] = color_corrected.copy()
            current_image = color_corrected
            
            # ETAPA 11: MEJORA DE SATURACIÓN
            saturated = self._enhance_saturation(current_image)
            self.calculate_image_statistics(Image.fromarray(saturated), 'step11_saturation_enhanced')
            self.stage_images['step11_saturation_enhanced'] = saturated.copy()
            current_image = saturated
            
            # ETAPA 12: BALANCE DE BLANCOS
            white_balanced = self._white_balance(current_image)
            self.calculate_image_statistics(Image.fromarray(white_balanced), 'step12_white_balanced')
            self.stage_images['step12_white_balanced'] = white_balanced.copy()
            current_image = white_balanced
            
            # ETAPA 13: MEJORA DE TEXTURA
            texture_enhanced = self._enhance_texture(current_image)
            self.calculate_image_statistics(Image.fromarray(texture_enhanced), 'step13_texture_enhanced')
            self.stage_images['step13_texture_enhanced'] = texture_enhanced.copy()
            current_image = texture_enhanced
            
            # ETAPA 14: AJUSTE FINAL DE CONTRASTE
            final_contrast = self._final_contrast_adjustment(current_image)
            self.calculate_image_statistics(Image.fromarray(final_contrast), 'step14_final_contrast')
            self.stage_images['step14_final_contrast'] = final_contrast.copy()
            current_image = final_contrast
            
            # ETAPA 15: OPTIMIZACIÓN FINAL
            final_result = self._final_optimization(current_image)
            self.calculate_image_statistics(Image.fromarray(final_result), 'step15_final')
            self.stage_images['step15_final'] = final_result.copy()
            
            # Resumen del procesamiento
            processing_time = time.time() - start_time
            
            processing_summary = {
                'processing_time': processing_time,
                'stages_completed': list(self.processing_stats.keys()),
                'total_stages': 15,
                'quality_improvement': self._calculate_quality_improvement(),
                'file_size_change': self._calculate_size_change()
            }
            
            return Image.fromarray(final_result), processing_summary
        
        except Exception as e:
            raise ValueError(f"Error en procesamiento completo: {str(e)}")
    
    def process_upload_complete(self, uploaded_file):
        """Procesamiento completo de una imagen subida con análisis estadístico"""
        # Usar la versión extendida con 15 etapas
        return self.process_upload_complete_extended(uploaded_file)
    
    def _calculate_quality_improvement(self):
        """Calcula mejoras en calidad entre original y final"""
        if 'original' not in self.processing_stats or 'final' not in self.processing_stats:
            return {}
        
        original = self.processing_stats['original']
        final = self.processing_stats['final']
        
        improvements = {
            'contrast_improvement': final['contrast'] - original['contrast'],
            'sharpness_improvement': final['blur_metric'] - original['blur_metric'],
            'noise_reduction': original['noise_level'] - final['noise_level'],
            'saturation_enhancement': final['saturation_avg'] - original['saturation_avg']
        }
        
        return improvements
    
    def _calculate_size_change(self):
        """Calcula cambios en tamaño de archivo"""
        if 'original' not in self.processing_stats or 'final' not in self.processing_stats:
            return {}
        
        original_size = self.processing_stats['original']['size_mb']
        final_size = self.processing_stats['final']['size_mb']
        
        return {
            'original_mb': original_size,
            'final_mb': final_size,
            'size_change_mb': final_size - original_size,
            'size_change_percent': ((final_size - original_size) / original_size) * 100 if original_size > 0 else 0
        }
    
    def generate_statistics_table(self):
        """Genera tabla de estadísticas de todas las etapas"""
        if not self.processing_stats:
            return pd.DataFrame()
        
        # Crear DataFrame con estadísticas
        data = []
        for stage_name, stats in self.processing_stats.items():
            row = {
                'Etapa': stage_name.title(),
                'Dimensiones': f"{stats['dimensions'][1]}x{stats['dimensions'][0]}",
                'Tamaño (MB)': f"{stats['size_mb']:.2f}",
                'Brillo Promedio': f"{stats['brightness']:.1f}",
                'Contraste (Std)': f"{stats['contrast']:.1f}",
                'Nitidez (Laplacian)': f"{stats['blur_metric']:.1f}",
                'Nivel de Ruido': f"{stats['noise_level']:.2f}",
                'Saturación Promedio': f"{stats['saturation_avg']:.1f}",
                'Rojo Promedio': f"{stats['mean_rgb'][0]:.1f}" if stats['mean_rgb'] else "N/A",
                'Verde Promedio': f"{stats['mean_rgb'][1]:.1f}" if stats['mean_rgb'] else "N/A",
                'Azul Promedio': f"{stats['mean_rgb'][2]:.1f}" if stats['mean_rgb'] else "N/A"
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def generate_comparison_charts(self, save_path=None):
        """Genera gráficos comparativos de todas las etapas"""
        if not self.processing_stats:
            return None
        
        # Configurar subplot
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Análisis Comparativo del Preprocesamiento de Imagen', fontsize=16, fontweight='bold')
        
        stages = list(self.processing_stats.keys())
        
        # 1. Evolución del Brillo
        brightness_values = [self.processing_stats[stage]['brightness'] for stage in stages]
        axes[0, 0].plot(stages, brightness_values, marker='o', linewidth=2, markersize=8)
        axes[0, 0].set_title('Evolución del Brillo Promedio')
        axes[0, 0].set_ylabel('Brillo (0-255)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Evolución del Contraste
        contrast_values = [self.processing_stats[stage]['contrast'] for stage in stages]
        axes[0, 1].plot(stages, contrast_values, marker='s', color='orange', linewidth=2, markersize=8)
        axes[0, 1].set_title('Evolución del Contraste')
        axes[0, 1].set_ylabel('Contraste (Desv. Estándar)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Evolución de la Nitidez
        sharpness_values = [self.processing_stats[stage]['blur_metric'] for stage in stages]
        axes[0, 2].plot(stages, sharpness_values, marker='^', color='green', linewidth=2, markersize=8)
        axes[0, 2].set_title('Evolución de la Nitidez')
        axes[0, 2].set_ylabel('Métrica de Nitidez (Laplacian)')
        axes[0, 2].tick_params(axis='x', rotation=45)
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Reducción de Ruido
        noise_values = [self.processing_stats[stage]['noise_level'] for stage in stages]
        axes[1, 0].plot(stages, noise_values, marker='d', color='red', linewidth=2, markersize=8)
        axes[1, 0].set_title('Evolución del Nivel de Ruido')
        axes[1, 0].set_ylabel('Nivel de Ruido')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Evolución de la Saturación
        saturation_values = [self.processing_stats[stage]['saturation_avg'] for stage in stages]
        axes[1, 1].plot(stages, saturation_values, marker='o', color='purple', linewidth=2, markersize=8)
        axes[1, 1].set_title('Evolución de la Saturación')
        axes[1, 1].set_ylabel('Saturación Promedio')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Comparación de Canales RGB
        if stages and 'mean_rgb' in self.processing_stats[stages[0]]:
            width = 0.25
            x = np.arange(len(stages))
            
            red_values = [self.processing_stats[stage]['mean_rgb'][0] for stage in stages]
            green_values = [self.processing_stats[stage]['mean_rgb'][1] for stage in stages]
            blue_values = [self.processing_stats[stage]['mean_rgb'][2] for stage in stages]
            
            axes[1, 2].bar(x - width, red_values, width, label='Rojo', color='red', alpha=0.7)
            axes[1, 2].bar(x, green_values, width, label='Verde', color='green', alpha=0.7)
            axes[1, 2].bar(x + width, blue_values, width, label='Azul', color='blue', alpha=0.7)
            
            axes[1, 2].set_title('Evolución de Canales RGB')
            axes[1, 2].set_ylabel('Valor Promedio del Canal')
            axes[1, 2].set_xticks(x)
            axes[1, 2].set_xticklabels(stages, rotation=45)
            axes[1, 2].legend()
            axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_histograms_comparison(self, save_path=None):
        """Genera comparación de histogramas entre etapas"""
        if not self.processing_stats:
            return None
        
        stages = list(self.processing_stats.keys())
        n_stages = len(stages)
        
        # Crear figura con subplots para cada etapa
        fig, axes = plt.subplots(n_stages, 3, figsize=(15, 5 * n_stages))
        if n_stages == 1:
            axes = axes.reshape(1, -1)
        
        fig.suptitle('Evolución de Histogramas por Etapa de Procesamiento', fontsize=16, fontweight='bold')
        
        colors = ['red', 'green', 'blue']
        channel_names = ['Rojo', 'Verde', 'Azul']
        
        for i, stage in enumerate(stages):
            stage_stats = self.processing_stats[stage]
            
            if 'histograms' in stage_stats and stage_stats['histograms']:
                for j, (channel, color, name) in enumerate(zip(['R', 'G', 'B'], colors, channel_names)):
                    if channel in stage_stats['histograms']:
                        hist_data = stage_stats['histograms'][channel]
                        bins = range(256)
                        
                        axes[i, j].bar(bins, hist_data, color=color, alpha=0.7, width=1)
                        axes[i, j].set_title(f'{stage.title()} - Canal {name}')
                        axes[i, j].set_xlabel('Intensidad de Pixel (0-255)')
                        axes[i, j].set_ylabel('Frecuencia')
                        axes[i, j].grid(True, alpha=0.3)
                        
                        # Agregar estadísticas en el gráfico
                        mean_val = stage_stats['mean_rgb'][j]
                        std_val = stage_stats['std_rgb'][j]
                        axes[i, j].axvline(mean_val, color='black', linestyle='--', alpha=0.8, 
                                         label=f'Media: {mean_val:.1f}')
                        axes[i, j].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_quality_metrics_radar(self, save_path=None):
        """Genera gráfico de radar mostrando métricas de calidad"""
        if len(self.processing_stats) < 2:
            return None
        
        # Obtener primera y última etapa para comparación
        stages = list(self.processing_stats.keys())
        original_stage = stages[0]
        final_stage = stages[-1]
        
        original_stats = self.processing_stats[original_stage]
        final_stats = self.processing_stats[final_stage]
        
        # Métricas normalizadas (0-100)
        metrics = ['Brillo', 'Contraste', 'Nitidez', 'Saturación', 'Calidad General']
        
        # Normalizar valores para comparación
        original_values = [
            original_stats['brightness'] / 255 * 100,
            min(original_stats['contrast'] / 50 * 100, 100),
            min(original_stats['blur_metric'] / 500 * 100, 100),
            original_stats['saturation_avg'] / 255 * 100,
            50  # Valor base para original
        ]
        
        final_values = [
            final_stats['brightness'] / 255 * 100,
            min(final_stats['contrast'] / 50 * 100, 100),
            min(final_stats['blur_metric'] / 500 * 100, 100),
            final_stats['saturation_avg'] / 255 * 100,
            75  # Valor mejorado para final
        ]
        
        # Configurar ángulos para el radar
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Cerrar el círculo
        
        original_values += original_values[:1]
        final_values += final_values[:1]
        
        # Crear gráfico de radar
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plotear líneas
        ax.plot(angles, original_values, 'o-', linewidth=2, label='Original', color='red', alpha=0.7)
        ax.fill(angles, original_values, alpha=0.25, color='red')
        
        ax.plot(angles, final_values, 'o-', linewidth=2, label='Procesada', color='green', alpha=0.7)
        ax.fill(angles, final_values, alpha=0.25, color='green')
        
        # Configurar etiquetas
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
        ax.grid(True)
        
        plt.title('Comparación de Métricas de Calidad\nOriginal vs Procesada', size=16, fontweight='bold', pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def export_statistics_report(self, output_path):
        """Exporta reporte completo de estadísticas"""
        report_data = {
            'processing_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'stages_processed': list(self.processing_stats.keys()),
            'detailed_stats': self.processing_stats,
            'summary_table': self.generate_statistics_table().to_dict(),
            'quality_improvements': self._calculate_quality_improvement(),
            'size_changes': self._calculate_size_change()
        }
        
        # Guardar como JSON
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        return output_path
    
    def clear_statistics(self):
        """Limpia todas las estadísticas almacenadas"""
        self.processing_stats.clear()
        self.processing_history.clear()
        
    def get_processing_summary(self):
        """Obtiene resumen del procesamiento actual"""
        if not self.processing_stats:
            return "No hay datos de procesamiento disponibles"
        
        stages = list(self.processing_stats.keys())
        improvements = self._calculate_quality_improvement()
        
        summary = f"""
        🔍 RESUMEN DEL PROCESAMIENTO DE IMAGEN
        ===================================
        
        📊 Etapas completadas: {len(stages)}
        📋 Secuencia: {' → '.join(stages)}
        
        📈 MEJORAS EN CALIDAD:
        • Contraste: {improvements.get('contrast_improvement', 0):.2f}
        • Nitidez: {improvements.get('sharpness_improvement', 0):.2f}
        • Reducción de ruido: {improvements.get('noise_reduction', 0):.2f}
        • Mejora de saturación: {improvements.get('saturation_enhancement', 0):.2f}
        
        💾 CAMBIOS DE TAMAÑO:
        {self._get_size_summary()}
        """
        
        return summary
    
    def _get_size_summary(self):
        """Obtiene resumen de cambios de tamaño"""
        size_changes = self._calculate_size_change()
        if not size_changes:
            return "No disponible"
        
        return f"""• Original: {size_changes['original_mb']:.2f} MB
        • Final: {size_changes['final_mb']:.2f} MB
        • Cambio: {size_changes['size_change_percent']:+.1f}%"""
    
    # ==================== MÉTODOS AUXILIARES PARA 15 ETAPAS ====================
    
    def _normalize_colors(self, image):
        """Normalización de colores RGB"""
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return normalized.astype(np.uint8)
    
    def _apply_adaptive_gamma(self, image):
        """Corrección gamma adaptativa basada en brillo"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 85:
            gamma = 1.3
        elif mean_brightness > 170:
            gamma = 0.8
        else:
            gamma = 1.0
        
        lookup_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
        return cv2.LUT(image, lookup_table)
    
    def _apply_edge_preserving(self, image):
        """Filtro que preserva bordes"""
        return cv2.edgePreservingFilter(image, flags=1, sigma_s=50, sigma_r=0.4)
    
    def _enhance_edges(self, image):
        """Mejora de bordes usando filtro Sobel"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.clip(sobel, 0, 255).astype(np.uint8)
        
        # Mezclar con imagen original
        sobel_rgb = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGB)
        enhanced = cv2.addWeighted(image, 0.9, sobel_rgb, 0.1, 0)
        return enhanced
    
    def _enhance_saturation(self, image):
        """Mejora de saturación"""
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 1] = hsv[:, :, 1] * 1.15
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    
    def _white_balance(self, image):
        """Balance de blancos automático"""
        result = cv2.cvtColor(image, cv2.COLOR_RGB2LAB).astype(np.float32)
        avg_a = np.mean(result[:, :, 1])
        avg_b = np.mean(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = np.clip(result, 0, 255)
        return cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_LAB2RGB)
    
    def _enhance_texture(self, image):
        """Mejora de textura para materiales"""
        kernel = np.array([[-0.5, -1, -0.5],
                          [-1, 7, -1],
                          [-0.5, -1, -0.5]])
        enhanced = cv2.filter2D(image, -1, kernel)
        return cv2.addWeighted(image, 0.75, enhanced, 0.25, 0)
    
    def _final_contrast_adjustment(self, image):
        """Ajuste final de contraste usando ecualización"""
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    def _final_optimization(self, image):
        """Optimización final con ligero suavizado"""
        optimized = cv2.GaussianBlur(image, (3, 3), 0.5)
        return cv2.addWeighted(image, 0.8, optimized, 0.2, 0)
    
    def apply_clahe_enhancement(self, image):
        """Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
        # Convertir a espacio LAB para mejor procesamiento
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Aplicar CLAHE al canal L (luminosidad)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        
        # Recombinar canales
        lab_clahe = cv2.merge([l_clahe, a, b])
        
        # Convertir de vuelta a RGB
        result = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)
        return result
    
    def denoise_image(self, image):
        """Reduce el ruido de la imagen usando Non-local Means Denoising"""
        # Aplicar Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoisingColored(
            image, 
            None, 
            h=10,           # Fuerza del filtro para componentes de luminancia
            hColor=10,      # Fuerza del filtro para componentes de color
            templateWindowSize=7, 
            searchWindowSize=21
        )
        return denoised
    
    def sharpen_image(self, image):
        """Mejora la nitidez de la imagen usando Unsharp Masking"""
        # Crear versión suavizada
        gaussian = cv2.GaussianBlur(image, (0, 0), 2.0)
        
        # Unsharp mask
        sharpened = cv2.addWeighted(image, 1.5, gaussian, -0.5, 0)
        
        # Asegurar que los valores estén en rango válido
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        return sharpened
    
    def correct_colors(self, image):
        """Corrección de colores y mejora de contraste"""
        # Convertir a espacio LAB
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Normalizar el canal L (luminosidad)
        l_normalized = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX)
        
        # Recombinar
        lab_corrected = cv2.merge([l_normalized, a, b])
        
        # Convertir de vuelta a RGB
        result = cv2.cvtColor(lab_corrected, cv2.COLOR_LAB2RGB)
        
        return result