import asyncio

from fastapi import WebSocket
from .api import api
from .hypr_events import HYPR_SOCKET_PATH, SocketDataHandler

@api.websocket("/hypr/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    reader, writer = await asyncio.open_unix_connection(HYPR_SOCKET_PATH)

    try:
        while True:
            data = SocketDataHandler(await reader.readline())
            await websocket.send_json(data.to_json)
    except Exception as e:
        print(e)
    
    reader.feed_eof()
    writer.close()