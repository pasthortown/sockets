# socket_client.py
import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:6060"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(f"Received: {data}")

if __name__ == "__main__":
    asyncio.run(receive_data())
