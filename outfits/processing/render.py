"""
Renderizado de overlays y previews
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64


class RenderEngine:
    """Motor de renderizado para overlays y previews"""
    
    def __init__(self):
        self.overlay_opacity = 0.7
    
    def create_color_palette_overlay(self, image, color_palette):
        """Crea un overlay con la paleta de colores sobre la imagen"""
        # Convertir PIL a OpenCV si es necesario
        if isinstance(image, Image.Image):
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            cv_image = image.copy()
        
        h, w = cv_image.shape[:2]
        
        # Crear área para paleta (lado derecho)
        palette_width = w // 4
        palette_height = h // 3
        
        # Posición del overlay
        x_start = w - palette_width - 20
        y_start = 20
        
        # Crear fondo semi-transparente
        overlay = cv_image.copy()
        cv2.rectangle(overlay, (x_start-10, y_start-10), 
                     (x_start + palette_width + 10, y_start + palette_height + 10), 
                     (0, 0, 0), -1)
        
        # Aplicar transparencia
        cv2.addWeighted(overlay, self.overlay_opacity, cv_image, 1 - self.overlay_opacity, 0, cv_image)
        
        # Dibujar colores de la paleta
        all_colors = []
        if 'primary' in color_palette:
            all_colors.extend(color_palette['primary'][:3])
        if 'accent' in color_palette:
            all_colors.extend(color_palette['accent'][:2])
        
        color_height = palette_height // len(all_colors) if all_colors else palette_height
        
        for i, color_hex in enumerate(all_colors):
            # Convertir hex a BGR
            color_rgb = tuple(int(color_hex.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
            color_bgr = (color_rgb[2], color_rgb[1], color_rgb[0])
            
            y_pos = y_start + i * color_height
            cv2.rectangle(cv_image, (x_start, y_pos), 
                         (x_start + palette_width, y_pos + color_height - 2), 
                         color_bgr, -1)
        
        # Convertir de vuelta a PIL
        result = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        return result
    
    def create_outfit_preview(self, base_image, outfit_data):
        """Crea un preview del outfit recomendado"""
        # Crear una imagen de preview con información del outfit
        preview_width = 400
        preview_height = 600
        
        # Crear canvas
        preview = Image.new('RGB', (preview_width, preview_height), 'white')
        draw = ImageDraw.Draw(preview)
        
        try:
            # Intentar cargar una fuente
            font_title = ImageFont.truetype("arial.ttf", 24)
            font_text = ImageFont.truetype("arial.ttf", 16)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            # Usar fuente por defecto si no se encuentra arial
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        y_pos = 20
        
        # Título del estilo
        draw.text((20, y_pos), outfit_data['style'], fill='black', font=font_title)
        y_pos += 40
        
        # Descripción
        draw.text((20, y_pos), outfit_data['description'], fill='gray', font=font_text)
        y_pos += 60
        
        # Dibujar piezas del outfit
        for piece_name, piece_info in outfit_data['pieces'].items():
            # Nombre de la pieza
            draw.text((20, y_pos), f"{piece_info['type']}:", fill='black', font=font_text)
            y_pos += 25
            
            # Color de la pieza (rectángulo)
            color_hex = piece_info['color']
            try:
                color_rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                draw.rectangle([40, y_pos, 80, y_pos + 20], fill=color_rgb, outline='black')
            except:
                draw.rectangle([40, y_pos, 80, y_pos + 20], fill='gray', outline='black')
            
            # Descripción de la pieza
            draw.text((90, y_pos), piece_info['description'], fill='gray', font=font_small)
            y_pos += 35
        
        # Consejos
        y_pos += 20
        draw.text((20, y_pos), "Consejos de estilo:", fill='black', font=font_text)
        y_pos += 30
        
        for tip in outfit_data.get('tips', [])[:2]:  # Solo los primeros 2 consejos
            # Wrap text si es muy largo
            if len(tip) > 40:
                tip = tip[:37] + "..."
            draw.text((20, y_pos), f"• {tip}", fill='gray', font=font_small)
            y_pos += 20
        
        return preview
    
    def create_face_detection_overlay(self, image, face_coords):
        """Crea overlay mostrando la detección facial"""
        if isinstance(image, Image.Image):
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            cv_image = image.copy()
        
        if face_coords is not None:
            for (x, y, w, h) in face_coords:
                # Dibujar rectángulo alrededor de la cara
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Agregar texto
                cv2.putText(cv_image, 'Face Detected', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        result = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        return result
    
    def image_to_base64(self, image):
        """Convierte imagen PIL a base64 para mostrar en web"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def create_comparison_grid(self, original_image, processed_results):
        """Crea una grilla comparativa con diferentes procesados"""
        # Redimensionar imágenes para la grilla
        target_size = (300, 300)
        
        images = [original_image]
        labels = ['Original']
        
        # Agregar imágenes procesadas
        if 'palette_overlay' in processed_results:
            images.append(processed_results['palette_overlay'])
            labels.append('Paleta de Colores')
        
        if 'face_detection' in processed_results:
            images.append(processed_results['face_detection'])
            labels.append('Detección Facial')
        
        # Crear grilla
        grid_width = len(images) * target_size[0]
        grid_height = target_size[1] + 40  # Espacio para labels
        
        grid = Image.new('RGB', (grid_width, grid_height), 'white')
        
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        for i, (img, label) in enumerate(zip(images, labels)):
            # Redimensionar imagen
            resized = img.resize(target_size)
            
            # Pegar en grilla
            x_pos = i * target_size[0]
            grid.paste(resized, (x_pos, 40))
            
            # Agregar label
            draw = ImageDraw.Draw(grid)
            text_width = draw.textlength(label, font=font)
            text_x = x_pos + (target_size[0] - text_width) // 2
            draw.text((text_x, 10), label, fill='black', font=font)
        
        return grid