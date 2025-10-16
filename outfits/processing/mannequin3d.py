"""
Visualizador 3D usando Plotly para maniquí virtual
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json


class Mannequin3D:
    """Maniquí 3D para visualización de outfits"""
    
    def __init__(self):
        self.base_mannequin = self._create_base_mannequin()
    
    def _create_base_mannequin(self):
        """Crea la estructura base del maniquí"""
        # Coordenadas simplificadas para un maniquí básico
        # Cabeza (esfera)
        head = self._create_sphere(center=(0, 0, 1.7), radius=0.15)
        
        # Torso (cilindro)
        torso = self._create_cylinder(center=(0, 0, 1.2), 
                                    height=0.6, radius=0.2)
        
        # Brazos
        left_arm = self._create_cylinder(center=(-0.3, 0, 1.3), 
                                       height=0.5, radius=0.05, horizontal=True)
        right_arm = self._create_cylinder(center=(0.3, 0, 1.3), 
                                        height=0.5, radius=0.05, horizontal=True)
        
        # Piernas
        left_leg = self._create_cylinder(center=(-0.1, 0, 0.4), 
                                       height=0.8, radius=0.08)
        right_leg = self._create_cylinder(center=(0.1, 0, 0.4), 
                                        height=0.8, radius=0.08)
        
        return {
            'head': head,
            'torso': torso,
            'left_arm': left_arm,
            'right_arm': right_arm,
            'left_leg': left_leg,
            'right_leg': right_leg
        }
    
    def _create_sphere(self, center=(0, 0, 0), radius=1):
        """Crea una esfera"""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        
        return {'x': x, 'y': y, 'z': z, 'type': 'surface'}
    
    def _create_cylinder(self, center=(0, 0, 0), height=1, radius=0.1, horizontal=False):
        """Crea un cilindro"""
        theta = np.linspace(0, 2*np.pi, 20)
        
        if horizontal:
            # Cilindro horizontal (para brazos)
            y = np.linspace(-height/2, height/2, 20)
            x = radius * np.outer(np.cos(theta), np.ones(len(y))) + center[0]
            z = radius * np.outer(np.sin(theta), np.ones(len(y))) + center[2]
            y = np.outer(np.ones(len(theta)), y) + center[1]
        else:
            # Cilindro vertical (para torso y piernas)
            z = np.linspace(-height/2, height/2, 20)
            x = radius * np.outer(np.cos(theta), np.ones(len(z))) + center[0]
            y = radius * np.outer(np.sin(theta), np.ones(len(z))) + center[1]
            z = np.outer(np.ones(len(theta)), z) + center[2]
        
        return {'x': x, 'y': y, 'z': z, 'type': 'surface'}
    
    def create_outfit_visualization(self, outfit_data):
        """Crea visualización 3D del outfit"""
        fig = go.Figure()
        
        # Colores del outfit
        colors = self._extract_colors_from_outfit(outfit_data)
        
        # Agregar partes del maniquí con colores del outfit
        self._add_mannequin_part(fig, self.base_mannequin['head'], 
                                colors.get('skin', '#FDBCB4'), 'Cabeza')
        
        self._add_mannequin_part(fig, self.base_mannequin['torso'], 
                                colors.get('top', '#4682B4'), 'Top')
        
        self._add_mannequin_part(fig, self.base_mannequin['left_arm'], 
                                colors.get('top', '#4682B4'), 'Brazo Izq.')
        
        self._add_mannequin_part(fig, self.base_mannequin['right_arm'], 
                                colors.get('top', '#4682B4'), 'Brazo Der.')
        
        self._add_mannequin_part(fig, self.base_mannequin['left_leg'], 
                                colors.get('bottom', '#2F4F4F'), 'Pierna Izq.')
        
        self._add_mannequin_part(fig, self.base_mannequin['right_leg'], 
                                colors.get('bottom', '#2F4F4F'), 'Pierna Der.')
        
        # Configurar layout
        fig.update_layout(
            title=f"Visualización 3D - {outfit_data.get('style', 'Outfit')}",
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            width=600,
            height=600,
            margin=dict(r=0, b=0, l=0, t=40)
        )
        
        return fig
    
    def _extract_colors_from_outfit(self, outfit_data):
        """Extrae colores del outfit para aplicar al maniquí"""
        colors = {
            'skin': '#FDBCB4',  # Color de piel por defecto
        }
        
        pieces = outfit_data.get('pieces', {})
        
        if 'top' in pieces:
            colors['top'] = pieces['top'].get('color', '#4682B4')
        
        if 'bottom' in pieces:
            colors['bottom'] = pieces['bottom'].get('color', '#2F4F4F')
        
        if 'outer' in pieces:
            colors['outer'] = pieces['outer'].get('color', '#696969')
        
        return colors
    
    def _add_mannequin_part(self, fig, part_data, color, name):
        """Agrega una parte del maniquí a la figura"""
        fig.add_trace(go.Surface(
            x=part_data['x'],
            y=part_data['y'], 
            z=part_data['z'],
            colorscale=[[0, color], [1, color]],
            showscale=False,
            name=name,
            opacity=0.8
        ))
    
    def create_color_palette_3d(self, color_palette):
        """Crea visualización 3D de la paleta de colores"""
        fig = go.Figure()
        
        # Obtener todos los colores
        all_colors = []
        color_labels = []
        
        if 'primary' in color_palette:
            all_colors.extend(color_palette['primary'])
            color_labels.extend([f'Primario {i+1}' for i in range(len(color_palette['primary']))])
        
        if 'accent' in color_palette:
            all_colors.extend(color_palette['accent'])
            color_labels.extend([f'Acento {i+1}' for i in range(len(color_palette['accent']))])
        
        if 'neutral' in color_palette:
            all_colors.extend(color_palette['neutral'])
            color_labels.extend([f'Neutro {i+1}' for i in range(len(color_palette['neutral']))])
        
        # Crear esferas para cada color
        for i, (color, label) in enumerate(zip(all_colors, color_labels)):
            x_pos = (i % 4) * 2 - 3  # Distribución en grilla
            y_pos = (i // 4) * 2
            
            sphere = self._create_sphere(center=(x_pos, y_pos, 0), radius=0.5)
            
            fig.add_trace(go.Surface(
                x=sphere['x'],
                y=sphere['y'],
                z=sphere['z'],
                colorscale=[[0, color], [1, color]],
                showscale=False,
                name=label,
                opacity=0.9
            ))
        
        fig.update_layout(
            title="Paleta de Colores 3D",
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y', 
                zaxis_title='Z',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            width=500,
            height=500
        )
        
        return fig
    
    def export_to_html(self, fig, filename):
        """Exporta la visualización a HTML"""
        fig.write_html(filename, include_plotlyjs='cdn')
        return filename
    
    def get_plotly_json(self, fig):
        """Obtiene la configuración JSON para Plotly.js"""
        return fig.to_json()