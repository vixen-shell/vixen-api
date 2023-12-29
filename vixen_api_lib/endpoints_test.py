import asyncio, socket, os
from fastapi import WebSocket
from .api import api

HYPR_SOCKET_PATH = "/tmp/hypr/{}/.socket2.sock".format(os.getenv('HYPRLAND_INSTANCE_SIGNATURE'))

class DataEntity:
    def __init__(self, data_bytes):
        data_line = data_bytes.decode('utf-8')
        data_line = data_line.rstrip('\n')
        split_line = data_line.split('>>')
        self._id = split_line[0]
        self._data = split_line[1].split(',') if len(split_line) > 1 else []

    @property
    def to_json(self):
        return {
            "id": self._id,
            "data": self._data
        }

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

@api.websocket("/hypr_events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    reader, writer = await asyncio.open_unix_connection(HYPR_SOCKET_PATH)

    try:
        while True:
            data = DataEntity(await reader.readline())
            await websocket.send_json(data.to_json)
    except Exception as e:
        print(e)
    
    reader.feed_eof()
    writer.close()