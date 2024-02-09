import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from .api import api, server
from .clients_handler import clients_handler, client_sockets_handler
from .client_events import ClientEventObject

@api.websocket('/feature/{client_id}')
async def websocket_feature_client(current_websocket: WebSocket, client_id: str, client: bool = False):

    if client:
        await current_websocket.accept()
        client_sockets_handler.add_client(current_websocket, client_id)
    else:
        if client_sockets_handler.client_websockets.get(client_id):
            await current_websocket.accept()
            client_sockets_handler.add_connexion(current_websocket, client_id)
        else: 
            await current_websocket.close(
                reason = 'No client initialized!'
            )
            return
        
    def remove_websocket():
        if client:
            client_sockets_handler.remove_client(client_id)
        else:
            client_sockets_handler.remove_connexion(current_websocket, client_id)

    try:
        while True:
            event: ClientEventObject = await current_websocket.receive_json()

            if event['id'] == 'close_client':
                if client:
                    clients_handler.unsubscribe(client_id)
                    await current_websocket.send_json(event)
                    await asyncio.sleep(0.2)
                    break
            else:
                # Diffusez le message à toutes les connexions du même client_id
                message = f"Message text from client {client_id}: {event}"

                if not client:
                    await client_sockets_handler.client_websockets[client_id].send_text(message)

                if client_id in client_sockets_handler.connected_websockets:
                    for websocket in client_sockets_handler.connected_websockets[client_id]:
                        if websocket != current_websocket:  # Ne pas envoyer le message à l'expéditeur d'origine
                            await websocket.send_text(message)

    except WebSocketDisconnect as e:
        if server.should_exit: pass
        
    finally:
        remove_websocket()