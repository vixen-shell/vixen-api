from typing import Dict, List
from fastapi import WebSocket

class FeatureClientConnections:
    def __init__(self) -> None:
        self.clients: Dict[str, List[WebSocket]] = {}
        self.main_clients: Dict[str, WebSocket] = {}

    async def connect_client(self, websocket: WebSocket, client_id: str, main_client: bool):
        if main_client:
            await websocket.accept()
            self.main_clients[client_id] = websocket
        else:
            if self.main_clients.get(client_id):
                await websocket.accept()

                if client_id in self.clients:
                    self.clients[client_id].append(websocket)
                else:
                    self.clients[client_id] = [websocket]
            else: 
                await websocket.close(
                    code = 1000,
                    reason = 'Main client not initialized!'
                )
    
    async def remove_client(self, websocket: WebSocket, client_id: str, main_client: bool):
        if main_client:
            del self.main_clients[client_id]

            if client_id in self.clients:
                for _websocket in self.clients[client_id]:
                    await _websocket.close(
                        code = 1000,
                        reason = 'Main client disconnected!'
                    )

                del self.clients[client_id]
        else:
            if client_id in self.clients:
                self.clients[client_id].remove(websocket)
                if not self.clients[client_id]:
                    del self.clients[client_id]