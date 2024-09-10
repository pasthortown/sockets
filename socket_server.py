# socket_server.py
import asyncio
import cv2
import base64
import websockets
import json

async def capture_and_send(websocket, path):
    # Inicia la captura de video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    try:
        while True:
            # Captura una imagen
            ret, frame = cap.read()
            
            if not ret:
                print("No se pudo capturar la imagen.")
                break

            # Codifica la imagen a formato JPEG
            _, buffer = cv2.imencode('.jpg', frame)

            # Convierte la imagen a base64
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # Crea un objeto JSON con la imagen en base64
            data = {
                'image': img_base64,
                'type': 'jpeg'  # Puedes agregar más información si es necesario
            }

            # Envía el objeto JSON al cliente a través del WebSocket
            await websocket.send(json.dumps(data))

            # Espera un breve momento antes de capturar la siguiente imagen
            await asyncio.sleep(0.01)  # Ajusta el tiempo para controlar la frecuencia de envío
    except websockets.ConnectionClosed:
        print("Conexión cerrada por el cliente.")
    except Exception as e:
        print(f"Error durante la captura y envío: {e}")
    finally:
        cap.release()

async def main():
    # Inicia el servidor WebSocket en el puerto 6060
    server = await websockets.serve(capture_and_send, "localhost", 6060)
    
    print("WebSocket server running on ws://localhost:6060")

    # Mantén el servidor en ejecución hasta que se cierre manualmente
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
