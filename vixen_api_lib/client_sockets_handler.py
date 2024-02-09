from typing import Dict, List
from fastapi import WebSocket

class ClientSocketsHandler:
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

client_sockets_handler = ClientSocketsHandler()