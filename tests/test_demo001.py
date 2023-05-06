import asyncio

import websockets

async def send_text_message():
    async with websockets.connect('ws://localhost:15010/ws') as websocket:
        # message = input("Enter message: ")
        message = "test message"
        await websocket.send(message)
        x = await websocket.recv()
        print(f"recv message: {x}")

asyncio.get_event_loop().run_until_complete(send_text_message())
