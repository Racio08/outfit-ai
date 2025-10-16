"""
Sistema de recomendación de outfits
"""
import random
from typing import Dict, List, Tuple


class OutfitRecommender:
    """Genera recomendaciones de outfit basadas en análisis"""
    
    def __init__(self):
        self.outfit_database = self._initialize_outfit_database()
        self.style_rules = self._initialize_style_rules()
    
    def generate_recommendations(self, color_palette: Dict, season: str = "all", 
                               occasion: str = "casual", style_preference: str = "versatile") -> List[Dict]:
        """Genera recomendaciones de outfit"""
        
        recommendations = []
        
        # Obtener colores base
        primary_colors = color_palette.get("primary", [])
        accent_colors = color_palette.get("accent", [])
        neutral_colors = color_palette.get("neutral", [])
        
        # Generar 3 outfits diferentes
        for i in range(3):
            outfit = self._create_outfit(
                primary_colors, accent_colors, neutral_colors,
                occasion, style_preference, i
            )
            recommendations.append(outfit)
        
        return recommendations
    
    def _create_outfit(self, primary_colors: List, accent_colors: List, 
                      neutral_colors: List, occasion: str, style: str, variant: int) -> Dict:
        """Crea un outfit específico"""
        
        outfit_styles = {
            0: "professional",  # Profesional/formal
            1: "casual",        # Casual/diario
            2: "trendy"         # Moderno/trendy
        }
        
        current_style = outfit_styles.get(variant, "casual")
        
        if current_style == "professional":
            return self._create_professional_outfit(primary_colors, neutral_colors, accent_colors)
        elif current_style == "casual":
            return self._create_casual_outfit(primary_colors, accent_colors, neutral_colors)
        else:  # trendy
            return self._create_trendy_outfit(accent_colors, primary_colors, neutral_colors)
    
    def _create_professional_outfit(self, primary_colors: List, neutral_colors: List, accent_colors: List) -> Dict:
        """Outfit profesional/formal"""
        return {
            "style": "Profesional",
            "description": "Look elegante y sofisticado para el trabajo",
            "pieces": {
                "top": {
                    "type": "Blusa/Camisa",
                    "color": random.choice(neutral_colors) if neutral_colors else "#FFFFFF",
                    "description": "Blusa clásica en tono neutro"
                },
                "bottom": {
                    "type": "Pantalón/Falda",
                    "color": random.choice(primary_colors) if primary_colors else "#2F4F4F",
                    "description": "Pantalón de vestir o falda midi"
                },
                "outer": {
                    "type": "Blazer",
                    "color": random.choice(primary_colors) if primary_colors else "#2F4F4F",
                    "description": "Blazer estructurado"
                },
                "accessories": {
                    "type": "Accesorios",
                    "color": random.choice(accent_colors) if accent_colors else "#800080",
                    "description": "Reloj, bolso y zapatos coordinados"
                }
            },
            "color_harmony": "Colores neutros con un toque de color en accesorios",
            "tips": [
                "Mantén líneas limpias y siluetas estructuradas",
                "Los accesorios pueden añadir personalidad sin comprometer la elegancia",
                "Asegúrate de que las proporciones sean equilibradas"
            ]
        }
    
    def _create_casual_outfit(self, primary_colors: List, accent_colors: List, neutral_colors: List) -> Dict:
        """Outfit casual/diario"""
        return {
            "style": "Casual",
            "description": "Look cómodo y versátil para el día a día",
            "pieces": {
                "top": {
                    "type": "Camiseta/Suéter",
                    "color": random.choice(accent_colors) if accent_colors else "#4682B4",
                    "description": "Top cómodo en color llamativo"
                },
                "bottom": {
                    "type": "Jeans/Pantalón casual",
                    "color": random.choice(neutral_colors) if neutral_colors else "#2F4F4F",
                    "description": "Pantalón cómodo en tono neutro"
                },
                "outer": {
                    "type": "Chaqueta/Cardigan",
                    "color": random.choice(primary_colors) if primary_colors else "#696969",
                    "description": "Capa adicional versátil"
                },
                "accessories": {
                    "type": "Accesorios casuales",
                    "color": random.choice(primary_colors) if primary_colors else "#A0A0A0",
                    "description": "Sneakers, mochila o bolso casual"
                }
            },
            "color_harmony": "Combinación relajada con equilibrio entre neutros y colores",
            "tips": [
                "Juega con texturas para añadir interés visual",
                "Los accesorios casuales pueden cambiar completamente el look",
                "Comodidad sin sacrificar estilo"
            ]
        }
    
    def _create_trendy_outfit(self, accent_colors: List, primary_colors: List, neutral_colors: List) -> Dict:
        """Outfit moderno/trendy"""
        return {
            "style": "Moderno",
            "description": "Look actual y con personalidad",
            "pieces": {
                "top": {
                    "type": "Top statement",
                    "color": random.choice(accent_colors) if accent_colors else "#DC143C",
                    "description": "Pieza llamativa como focal point"
                },
                "bottom": {
                    "type": "Pantalón/Falda moderna",
                    "color": random.choice(primary_colors) if primary_colors else "#4682B4",
                    "description": "Silueta contemporánea"
                },
                "outer": {
                    "type": "Chaqueta trendy",
                    "color": random.choice(neutral_colors) if neutral_colors else "#696969",
                    "description": "Chaqueta con diseño actual"
                },
                "accessories": {
                    "type": "Accesorios modernos",
                    "color": random.choice(accent_colors) if accent_colors else "#8A2BE2",
                    "description": "Accesorios que complementen el look trendy"
                }
            },
            "color_harmony": "Combinación audaz con colores de acento prominentes",
            "tips": [
                "No tengas miedo de mezclar patrones y texturas",
                "Un accesorio statement puede transformar todo el look",
                "Equilibra piezas llamativas con básicos"
            ]
        }
    
    def _initialize_outfit_database(self) -> Dict:
        """Inicializa base de datos de outfits"""
        return {
            "categories": ["formal", "casual", "sport", "evening"],
            "pieces": {
                "tops": ["blusa", "camisa", "camiseta", "suéter", "top"],
                "bottoms": ["pantalón", "falda", "shorts", "jeans"],
                "outerwear": ["blazer", "chaqueta", "abrigo", "cardigan"],
                "accessories": ["zapatos", "bolso", "joyería", "cinturón"]
            }
        }
    
    def _initialize_style_rules(self) -> Dict:
        """Inicializa reglas de estilo"""
        return {
            "color_combinations": {
                "monochromatic": "Un color en diferentes tonos",
                "analogous": "Colores adyacentes en el círculo cromático",
                "complementary": "Colores opuestos",
                "triadic": "Tres colores equidistantes"
            },
            "proportions": {
                "fitted_top_loose_bottom": "Top ajustado con bottom holgado",
                "loose_top_fitted_bottom": "Top holgado con bottom ajustado",
                "balanced": "Proporciones equilibradas"
            }
        }
    
    def get_style_tips(self, color_palette: Dict) -> List[str]:
        """Genera consejos de estilo personalizados"""
        tips = [
            "Usa la regla del 60-30-10: 60% color dominante, 30% secundario, 10% acento",
            "Los accesorios son una forma fácil de incorporar tendencias",
            "Invierte en básicos de calidad en colores neutros",
        ]
        
        # Agregar tips específicos basados en la paleta
        if color_palette.get("primary"):
            tips.append("Tus colores primarios son versátiles para looks diarios")
        
        if color_palette.get("accent"):
            tips.append("Usa los colores de acento para destacar y añadir personalidad")
        
        return tips