"""
Análisis facial y colorimetría
"""
import cv2
import numpy as np
from PIL import Image
import colorsys


class FacialAnalyzer:
    """Análisis facial y determinación de paleta de colores"""
    
    def __init__(self):
        # Cargar clasificador de rostros de OpenCV
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            self.face_cascade = None
    
    def detect_face(self, image):
        """Detecta rostros en la imagen"""
        if self.face_cascade is None:
            return None
            
        # Convertir a escala de grises
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Detectar rostros
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return faces if len(faces) > 0 else None
    
    def extract_skin_tone(self, image, face_coords=None):
        """Extrae el tono de piel predominante"""
        # Convertir imagen PIL a numpy array si es necesario
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        if face_coords is not None and len(face_coords) > 0:
            # Usar área de la cara
            x, y, w, h = face_coords[0]
            # Tomar región central de la cara (evitar bordes)
            margin = int(min(w, h) * 0.2)
            face_region = img_array[y+margin:y+h-margin, x+margin:x+w-margin]
        else:
            # Usar imagen completa
            face_region = img_array
        
        # Convertir a HSV para mejor análisis de color
        hsv = cv2.cvtColor(face_region, cv2.COLOR_RGB2HSV)
        
        # Máscara para tonos de piel (rangos HSV típicos)
        lower_skin = np.array([0, 20, 70])
        upper_skin = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Extraer píxeles de piel
        skin_pixels = face_region[mask > 0]
        
        if len(skin_pixels) > 0:
            # Calcular color promedio
            avg_color = np.mean(skin_pixels, axis=0)
            return tuple(avg_color.astype(int))
        
        return None
    
    def analyze_color_palette(self, skin_tone):
        """Determina la paleta de colores recomendada basada en el tono de piel"""
        if skin_tone is None:
            return self._get_neutral_palette()
        
        r, g, b = skin_tone
        
        # Convertir a HSV para análisis
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Clasificar subtono (frío, cálido, neutro)
        if h < 0.1 or h > 0.9:  # Rojos/rosas
            if s > 0.3:
                undertone = "warm"  # Cálido
            else:
                undertone = "neutral"
        elif 0.1 <= h <= 0.3:  # Amarillos/naranjas
            undertone = "warm"
        elif 0.3 < h < 0.7:  # Verdes/azules
            undertone = "cool"  # Frío
        else:
            undertone = "neutral"
        
        return self._get_palette_for_undertone(undertone, v)
    
    def _get_palette_for_undertone(self, undertone, brightness):
        """Obtiene paleta específica según subtono"""
        palettes = {
            "warm": {
                "primary": ["#8B4513", "#CD853F", "#DEB887", "#F4A460"],  # Marrones cálidos
                "accent": ["#DC143C", "#FF6347", "#FF4500", "#DAA520"],   # Rojos y dorados
                "neutral": ["#F5F5DC", "#FFFFF0", "#FDF5E6"]             # Cremas
            },
            "cool": {
                "primary": ["#2F4F4F", "#708090", "#4682B4", "#5F9EA0"],  # Azules y grises
                "accent": ["#8A2BE2", "#4B0082", "#6A5ACD", "#00CED1"],   # Púrpuras y azules
                "neutral": ["#F8F8FF", "#E6E6FA", "#D3D3D3"]             # Grises fríos
            },
            "neutral": {
                "primary": ["#696969", "#A0A0A0", "#C0C0C0", "#DCDCDC"],  # Grises neutros
                "accent": ["#800080", "#008080", "#808000", "#B22222"],   # Colores balanceados
                "neutral": ["#FFFFFF", "#F5F5F5", "#EEEEEE"]             # Blancos
            }
        }
        
        # Ajustar según brillo de la piel
        if brightness < 0.3:  # Piel oscura
            return palettes.get(undertone, palettes["neutral"])
        elif brightness > 0.7:  # Piel clara
            return palettes.get(undertone, palettes["neutral"])
        else:  # Piel media
            return palettes.get(undertone, palettes["neutral"])
    
    def _get_neutral_palette(self):
        """Paleta neutra por defecto"""
        return {
            "primary": ["#696969", "#A0A0A0", "#C0C0C0", "#DCDCDC"],
            "accent": ["#800080", "#008080", "#808000", "#B22222"],
            "neutral": ["#FFFFFF", "#F5F5F5", "#EEEEEE"]
        }


class ColorAnalyzer:
    """Análisis avanzado de colores en la imagen"""
    
    @staticmethod
    def extract_dominant_colors(image, k=5):
        """Extrae los k colores dominantes de la imagen usando método simplificado"""
        try:
            # Convertir imagen a array numpy
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image
            
            # Redimensionar para acelerar el procesamiento
            h, w = img_array.shape[:2]
            if h * w > 50000:  # Si es muy grande, redimensionar
                factor = int(np.sqrt((h * w) / 50000))
                img_array = img_array[::factor, ::factor]
            
            # Reshape para k-means
            data = img_array.reshape(-1, 3).astype(np.float32)
            
            # Usar sklearn si está disponible, sino método manual
            try:
                from sklearn.cluster import KMeans
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(data)
                centers = kmeans.cluster_centers_.astype(np.uint8)
                return centers.tolist()
            except ImportError:
                # Método manual simplificado - extraer colores por muestreo
                # Dividir imagen en regiones y tomar color promedio de cada una
                colors = []
                step_h = max(1, img_array.shape[0] // 3)
                step_w = max(1, img_array.shape[1] // 3)
                
                for i in range(0, img_array.shape[0], step_h):
                    for j in range(0, img_array.shape[1], step_w):
                        region = img_array[i:i+step_h, j:j+step_w]
                        if region.size > 0:
                            avg_color = np.mean(region.reshape(-1, 3), axis=0).astype(int)
                            colors.append(tuple(avg_color))
                        
                        if len(colors) >= k:
                            break
                    if len(colors) >= k:
                        break
                
                # Completar con colores por defecto si es necesario
                while len(colors) < k:
                    colors.append((128, 128, 128))
                
                return colors[:k]
        
        except Exception as e:
            # En caso de error, devolver colores por defecto
            print(f"Error en extracción de colores dominantes: {e}")
            return [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255)]
    
    @staticmethod
    def get_complementary_colors(color):
        """Obtiene colores complementarios para un color dado"""
        r, g, b = color
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Color complementario (opuesto en el círculo cromático)
        comp_h = (h + 0.5) % 1.0
        comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_h, s, v)
        
        return (int(comp_r * 255), int(comp_g * 255), int(comp_b * 255))