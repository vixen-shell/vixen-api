import asyncio

from fastapi import WebSocket
from .api import api

@api.get("/hello/{name}")
async def hello(name: str):
    return {"hello": name}

# WebSocket Send events messages
@api.websocket("/websocket_events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        i += 1
        await websocket.send_text(f"Message {i}")
        await asyncio.sleep(1)

# WebSocket Send and receive messages
@api.websocket("/websocket_send_receive")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message textuel reçu : {data}")