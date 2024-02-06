from .api import api
from fastapi import HTTPException, WebSocket
from fastapi.responses import JSONResponse
from .features import features_handler

@api.get('/feature/{feature_name}/open')
async def open_feature(feature_name: str):
    data = features_handler.open(feature_name)
    if isinstance(data, HTTPException): raise data
    return JSONResponse(data)

class ClientWebSockets:
    def __init__(self) -> None:
        self.websockets = {}

    def add(self, websocket: WebSocket, client_id: str):
        if client_id in self.websockets:
            self.websockets[client_id].append(websocket)
        else:
            self.websockets[client_id] = [websocket]

    def remove(self, websocket: WebSocket, client_id: str):
        self.websockets[client_id].remove(websocket)
        if not self.websockets[client_id]:
            del self.websockets[client_id]

client_websockets = ClientWebSockets()

@api.websocket('/feature/{client_id}')
async def websocket_feature_client(current_websocket: WebSocket, client_id: str, subject: bool = False):
    await current_websocket.accept()

    client_websockets.add(current_websocket, client_id)

    try:
        while True:
            data = await current_websocket.receive_text()

            if data == 'user-close-event':
                if subject:
                    features_handler.unsubscribe(client_id)
                    await current_websocket.send_text(data)
                    break
            else:
                # Diffusez le message à toutes les connexions du même client_id
                for websocket in client_websockets.websockets[client_id]:
                    if websocket != current_websocket:  # Ne pas envoyer le message à l'expéditeur d'origine
                        await websocket.send_text(f"Message text from client {client_id}: {data}")
    finally:
        client_websockets.remove(current_websocket, client_id)