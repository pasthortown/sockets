import asyncio
import cv2
import base64
import websockets
import json
from mss import mss
import numpy as np

async def capture_and_send(websocket, path):
    # Crea un objeto mss para capturar la pantalla
    sct = mss()

    # Selecciona la pantalla principal para la captura
    monitor = sct.monitors[1]  # El índice 1 generalmente representa la pantalla principal

    try:
        while True:
            # Captura la pantalla
            screenshot = sct.grab(monitor)

            # Convierte la captura a un arreglo de numpy
            frame = np.array(screenshot)

            # Elimina el canal alfa si existe (si la captura es RGBA)
            frame = frame[..., :3]  # Solo los primeros 3 canales (RGB)

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
            await asyncio.sleep(0.001)  # Ajusta el tiempo para controlar la frecuencia de envío
    except websockets.ConnectionClosed:
        print("Conexión cerrada por el cliente.")
    except Exception as e:
        print(f"Error durante la captura y envío: {e}")
    finally:
        print("Finalizando la captura de pantalla.")

async def main():
    # Inicia el servidor WebSocket en el puerto 6060
    server = await websockets.serve(capture_and_send, "localhost", 6060)
    
    print("WebSocket server running on ws://localhost:6060")

    # Mantén el servidor en ejecución hasta que se cierre manualmente
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
