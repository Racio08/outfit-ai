"""
Generador de HTML para visor Three.js
"""
import json
from typing import Dict, List


class ThreeJSGenerator:
    """Genera código HTML/JavaScript para visor Three.js"""
    
    def __init__(self):
        self.threejs_cdn = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
        self.orbit_controls_cdn = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"
    
    def generate_3d_viewer(self, outfit_data: Dict, model_path: str = None) -> str:
        """Genera HTML completo para visor 3D"""
        
        # Extraer colores del outfit
        colors = self._extract_colors(outfit_data)
        
        html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor 3D - {outfit_data.get('style', 'Outfit')}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
            overflow: hidden;
        }}
        
        #container {{
            position: relative;
            width: 100vw;
            height: 100vh;
        }}
        
        #canvas-container {{
            width: 100%;
            height: 100%;
        }}
        
        #ui-overlay {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 300px;
            z-index: 100;
        }}
        
        .outfit-info h3 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 18px;
        }}
        
        .outfit-info p {{
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }}
        
        .color-palette {{
            display: flex;
            gap: 5px;
            margin: 10px 0;
        }}
        
        .color-swatch {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 2px solid #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }}
        
        #controls {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: center;
            gap: 10px;
            z-index: 100;
        }}
        
        .control-btn {{
            background: rgba(255, 255, 255, 0.9);
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .control-btn:hover {{
            background: rgba(255, 255, 255, 1);
            transform: translateY(-2px);
        }}
        
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 18px;
            z-index: 200;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="loading">Cargando visor 3D...</div>
        
        <div id="canvas-container"></div>
        
        <div id="ui-overlay">
            <div class="outfit-info">
                <h3>{outfit_data.get('style', 'Outfit')}</h3>
                <p>{outfit_data.get('description', 'Descripción del outfit')}</p>
                
                <div class="color-palette">
                    {self._generate_color_swatches(colors)}
                </div>
                
                <p><strong>Armonía:</strong> {outfit_data.get('color_harmony', 'Combinación equilibrada')}</p>
            </div>
        </div>
        
        <div id="controls">
            <button class="control-btn" onclick="resetCamera()">Resetear Vista</button>
            <button class="control-btn" onclick="toggleWireframe()">Wireframe</button>
            <button class="control-btn" onclick="changeBackground()">Cambiar Fondo</button>
        </div>
    </div>

    <script src="{self.threejs_cdn}"></script>
    <script>
        {self._generate_threejs_code(outfit_data, colors)}
    </script>
</body>
</html>
        """
        
        return html_template
    
    def _extract_colors(self, outfit_data: Dict) -> Dict:
        """Extrae colores del outfit data"""
        colors = {{}}
        pieces = outfit_data.get('pieces', {{}})
        
        for piece_name, piece_info in pieces.items():
            if 'color' in piece_info:
                colors[piece_name] = piece_info['color']
        
        return colors
    
    def _generate_color_swatches(self, colors: Dict) -> str:
        """Genera HTML para los swatches de color"""
        swatches = []
        for color_value in colors.values():
            swatches.append(f'<div class="color-swatch" style="background-color: {color_value};"></div>')
        
        return ''.join(swatches)
    
    def _generate_threejs_code(self, outfit_data: Dict, colors: Dict) -> str:
        """Genera código JavaScript para Three.js"""
        
        js_code = f"""
        // Variables globales
        let scene, camera, renderer, mannequin;
        let controls;
        let wireframeMode = false;
        let backgroundIndex = 0;
        const backgrounds = [
            0x667eea,
            0x764ba2, 
            0x2c3e50,
            0xecf0f1,
            0x34495e
        ];
        
        // Colores del outfit
        const outfitColors = {json.dumps(colors)};
        
        // Inicializar
        init();
        animate();
        
        function init() {{
            // Ocultar loading después de un momento
            setTimeout(() => {{
                document.getElementById('loading').style.display = 'none';
            }}, 1000);
            
            // Crear escena
            scene = new THREE.Scene();
            scene.background = new THREE.Color(backgrounds[backgroundIndex]);
            
            // Crear cámara
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(3, 3, 3);
            
            // Crear renderer
            renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            document.getElementById('canvas-container').appendChild(renderer.domElement);
            
            // Controles de órbita (simulado)
            setupControls();
            
            // Crear luces
            createLights();
            
            // Crear maniquí
            createMannequin();
            
            // Manejar resize
            window.addEventListener('resize', onWindowResize, false);
        }}
        
        function setupControls() {{
            // Simulación básica de controles de órbita con mouse
            let mouseDown = false;
            let mouseX = 0;
            let mouseY = 0;
            
            renderer.domElement.addEventListener('mousedown', (event) => {{
                mouseDown = true;
                mouseX = event.clientX;
                mouseY = event.clientY;
            }});
            
            renderer.domElement.addEventListener('mouseup', () => {{
                mouseDown = false;
            }});
            
            renderer.domElement.addEventListener('mousemove', (event) => {{
                if (!mouseDown) return;
                
                const deltaX = event.clientX - mouseX;
                const deltaY = event.clientY - mouseY;
                
                // Rotar cámara alrededor del centro
                const spherical = new THREE.Spherical();
                spherical.setFromVector3(camera.position);
                
                spherical.theta -= deltaX * 0.01;
                spherical.phi += deltaY * 0.01;
                
                // Limitar phi
                spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));
                
                camera.position.setFromSpherical(spherical);
                camera.lookAt(0, 1, 0);
                
                mouseX = event.clientX;
                mouseY = event.clientY;
            }});
            
            // Zoom con scroll
            renderer.domElement.addEventListener('wheel', (event) => {{
                const scale = event.deltaY > 0 ? 1.1 : 0.9;
                camera.position.multiplyScalar(scale);
                
                // Limitar zoom
                const distance = camera.position.length();
                if (distance < 2) camera.position.normalize().multiplyScalar(2);
                if (distance > 10) camera.position.normalize().multiplyScalar(10);
            }});
        }}
        
        function createLights() {{
            // Luz ambiental
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);
            
            // Luz direccional principal
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            
            // Luz de relleno
            const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
            fillLight.position.set(-5, 0, -5);
            scene.add(fillLight);
        }}
        
        function createMannequin() {{
            mannequin = new THREE.Group();
            
            // Cabeza
            const headGeometry = new THREE.SphereGeometry(0.15, 16, 16);
            const headMaterial = new THREE.MeshLambertMaterial({{ color: 0xFFDBB6 }});
            const head = new THREE.Mesh(headGeometry, headMaterial);
            head.position.set(0, 1.7, 0);
            head.castShadow = true;
            mannequin.add(head);
            
            // Torso
            const torsoGeometry = new THREE.CylinderGeometry(0.2, 0.25, 0.6, 12);
            const torsoColor = outfitColors.top ? outfitColors.top : '#4682B4';
            const torsoMaterial = new THREE.MeshLambertMaterial({{ color: torsoColor }});
            const torso = new THREE.Mesh(torsoGeometry, torsoMaterial);
            torso.position.set(0, 1.2, 0);
            torso.castShadow = true;
            mannequin.add(torso);
            
            // Brazos
            const armGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.5, 8);
            const armMaterial = new THREE.MeshLambertMaterial({{ color: torsoColor }});
            
            const leftArm = new THREE.Mesh(armGeometry, armMaterial);
            leftArm.position.set(-0.3, 1.3, 0);
            leftArm.rotation.z = Math.PI / 2;
            leftArm.castShadow = true;
            mannequin.add(leftArm);
            
            const rightArm = new THREE.Mesh(armGeometry, armMaterial);
            rightArm.position.set(0.3, 1.3, 0);
            rightArm.rotation.z = -Math.PI / 2;
            rightArm.castShadow = true;
            mannequin.add(rightArm);
            
            // Piernas
            const legGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.8, 8);
            const legColor = outfitColors.bottom ? outfitColors.bottom : '#2F4F4F';
            const legMaterial = new THREE.MeshLambertMaterial({{ color: legColor }});
            
            const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
            leftLeg.position.set(-0.1, 0.4, 0);
            leftLeg.castShadow = true;
            mannequin.add(leftLeg);
            
            const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
            rightLeg.position.set(0.1, 0.4, 0);
            rightLeg.castShadow = true;
            mannequin.add(rightLeg);
            
            // Agregar chaqueta si existe
            if (outfitColors.outer) {{
                const jacketGeometry = new THREE.CylinderGeometry(0.22, 0.27, 0.4, 12);
                const jacketMaterial = new THREE.MeshLambertMaterial({{ 
                    color: outfitColors.outer,
                    transparent: true,
                    opacity: 0.8
                }});
                const jacket = new THREE.Mesh(jacketGeometry, jacketMaterial);
                jacket.position.set(0, 1.3, 0);
                jacket.castShadow = true;
                mannequin.add(jacket);
            }}
            
            scene.add(mannequin);
            
            // Crear suelo
            const floorGeometry = new THREE.PlaneGeometry(10, 10);
            const floorMaterial = new THREE.MeshLambertMaterial({{ color: 0xcccccc }});
            const floor = new THREE.Mesh(floorGeometry, floorMaterial);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            
            // Rotación sutil del maniquí
            if (mannequin) {{
                mannequin.rotation.y += 0.005;
            }}
            
            renderer.render(scene, camera);
        }}
        
        function onWindowResize() {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }}
        
        // Funciones de control
        function resetCamera() {{
            camera.position.set(3, 3, 3);
            camera.lookAt(0, 1, 0);
        }}
        
        function toggleWireframe() {{
            wireframeMode = !wireframeMode;
            
            mannequin.children.forEach(child => {{
                if (child.material) {{
                    child.material.wireframe = wireframeMode;
                }}
            }});
        }}
        
        function changeBackground() {{
            backgroundIndex = (backgroundIndex + 1) % backgrounds.length;
            scene.background = new THREE.Color(backgrounds[backgroundIndex]);
        }}
        """
        
        return js_code
    
    def generate_simple_3d_preview(self, colors: List[str]) -> str:
        """Genera un preview 3D simple solo con colores"""
        html = f"""
        <div id="simple-3d-preview" style="width: 300px; height: 200px; background: linear-gradient(45deg, {colors[0] if colors else '#ccc'}, {colors[1] if len(colors) > 1 else colors[0] if colors else '#ddd'});">
            <div style="text-align: center; padding-top: 80px; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                Preview 3D
            </div>
        </div>
        """
        return html
    
    def generate_color_sphere_viewer(self, color_palette: Dict) -> str:
        """Genera visor de esferas de colores"""
        colors_json = json.dumps(color_palette)
        
        html = f"""
        <div id="color-sphere-container" style="width: 100%; height: 400px;">
            <script>
                // Three.js code para esferas de colores
                const colorPalette = {colors_json};
                // ... código para crear esferas de colores
            </script>
        </div>
        """
        return html