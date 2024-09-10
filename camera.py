import cv2
import base64
from flask import Flask, Response

app = Flask(__name__)

def capture_image():
    # Inicia la captura de video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return None

    # Captura una sola imagen
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("No se pudo capturar la imagen.")
        return None

    # Codifica la imagen a formato JPEG
    _, buffer = cv2.imencode('.jpg', frame)

    # Convierte la imagen a base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return img_base64

@app.route('/capture')
def capture():
    # Captura y convierte la imagen a base64
    img_base64 = capture_image()
    if img_base64:
        # Construye la respuesta HTML para mostrar la imagen
        html_content = f"""
        <html>
            <head>
                <title>Imagen Capturada</title>
            </head>
            <body>
                <h1>Imagen Capturada desde la Cámara</h1>
                <img src="data:image/jpeg;base64,{img_base64}" alt="Imagen capturada"/>
            </body>
        </html>
        """
        return Response(html_content, mimetype='text/html')
    else:
        return Response("Error al capturar la imagen.", status=500)

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
