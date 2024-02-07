from .api import api, server
from .clients import clients_handler
from typing import Dict, List
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

@api.get('/client/{feature_name}/open')
async def open_feature(feature_name: str):
    data = clients_handler.open(feature_name)
    if isinstance(data, HTTPException): raise data
    return JSONResponse(data)

@api.get('/client/{client_id}/close')
async def close_client(client_id: str):
    websocket = client_websockets.client_websockets.get(client_id)

    if not websocket:
        raise HTTPException(
            status_code = 404,
            detail = f"Bad client id!"
        )
    else:
        await websocket.send_text('close-event')
        return JSONResponse({'message': f"Client '{client_id}' closed"})

@api.get('/client/{feature_name}/ids')
async def get_feature_client_ids(feature_name: str):
    data = clients_handler.get_feature_ids(feature_name)

    if not data:
        raise HTTPException(
            status_code = 404,
            detail = f"'{feature_name}' feature has no client!"
        )

    return JSONResponse(data)

@api.get('/client/ids')
async def get_client_ids():
    data = clients_handler.get_ids()

    if not data:
        raise HTTPException(
            status_code = 404,
            detail = f"No client ids found!"
        )

    return JSONResponse(data)

class ClientWebSockets:
    def __init__(self) -> None:
        self.connected_websockets: Dict[str, List[WebSocket]] = {}
        self.client_websockets: Dict[str, WebSocket] = {}

    def add_client(self, websocket: WebSocket, client_id: str):
        self.client_websockets[client_id] = websocket

    def remove_client(self, client_id: str):
        del self.client_websockets[client_id]
        self.connected_websockets[client_id] = []

    def add_connexion(self, websocket: WebSocket, client_id: str):
        if client_id in self.connected_websockets:
            self.connected_websockets[client_id].append(websocket)
        else:
            self.connected_websockets[client_id] = [websocket]

    def remove_connexion(self, websocket: WebSocket, client_id: str):
        self.connected_websockets[client_id].remove(websocket)
        if not self.connected_websockets[client_id]:
            del self.connected_websockets[client_id]

client_websockets = ClientWebSockets()

@api.websocket('/feature/{client_id}')
async def websocket_feature_client(current_websocket: WebSocket, client_id: str, client: bool = False):

    if client:
        await current_websocket.accept()
        client_websockets.add_client(current_websocket, client_id)
        print(f"Client '{client_id}' connected")
    else:
        if client_websockets.client_websockets.get(client_id):
            await current_websocket.accept()
            client_websockets.add_connexion(current_websocket, client_id)
            print(f"New connexion to '{client_id}' client")
        else: 
            await current_websocket.close(
                reason = 'No client initialized!'
            )
            return
        
    def remove_websocket():
        if client:
            client_websockets.remove_client(client_id)
            print(f"Client '{client_id}' disconnected...")
        else:
            client_websockets.remove_connexion(current_websocket, client_id)
            print(f"One connexion to '{client_id}' disconnected...")

    try:
        while True:
            data = await current_websocket.receive_text()

            if data == 'close-event':
                if client:
                    clients_handler.unsubscribe(client_id)
                    await current_websocket.send_text(data)
                    break
            else:
                # Diffusez le message à toutes les connexions du même client_id
                message = f"Message text from client {client_id}: {data}"

                if not client:
                    await client_websockets.client_websockets[client_id].send_text(message)

                for websocket in client_websockets.connected_websockets[client_id]:
                    if websocket != current_websocket:  # Ne pas envoyer le message à l'expéditeur d'origine
                        await websocket.send_text(message)

    except WebSocketDisconnect as e:
        if server.should_exit: pass
        
    finally:
        remove_websocket()