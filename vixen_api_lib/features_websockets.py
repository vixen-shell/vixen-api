from fastapi import WebSocket
from .api import api
from .features import Features

@api.websocket('/feature/{feature_name}/pipe/{client_id}')
async def feature_pipe_websocket(websocket: WebSocket, feature_name: str, client_id: str):
    pipe = await Features.connect_client_to_pipe(
        feature_name, client_id, websocket
    )

    try:
        while True:
            await pipe.handle_event(
                await websocket.receive_json()
            )
    except:
        pipe.remove_client(client_id)