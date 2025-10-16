# main.py

import gradio as gr
import cv2
import numpy as np
from PIL import Image


def procesar_imagen(img: Image.Image) -> Image.Image:
    np_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    salida = cv2.GaussianBlur(np_img, (15, 15), 0)
    return Image.fromarray(cv2.cvtColor(salida, cv2.COLOR_BGR2RGB))


iface = gr.Interface(
    fn=procesar_imagen,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(),
    title="Prueba Outfit AI",
    description="Aplicación de ejemplo para procesar imágenes",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
