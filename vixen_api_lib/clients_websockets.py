import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from .api import api, server
from .feature_clients import feature_clients, feature_client_connections, FeatureClientEventObject

@api.websocket('/client/{client_id}')
async def websocket_feature_client(current_websocket: WebSocket, client_id: str, main_client: bool = False):

    await feature_client_connections.connect_client(
        current_websocket, client_id, main_client
    )
        
    try:
        while True:
            event: FeatureClientEventObject = await current_websocket.receive_json()

            if event['id'] == 'close_client':
                if main_client:
                    feature_clients.unsubscribe(client_id)
                    await current_websocket.send_json(event)
                    await asyncio.sleep(0.2)
                    break
            else:
                # Diffusez le message à toutes les connexions du même client_id
                message = f"Message text from client {client_id}: {event}"

                if not main_client:
                    await feature_client_connections.main_clients[client_id].send_text(message)

                if client_id in feature_client_connections.clients:
                    for websocket in feature_client_connections.clients[client_id]:
                        if websocket != current_websocket:  # Ne pas envoyer le message à l'expéditeur d'origine
                            await websocket.send_text(message)

    except WebSocketDisconnect as e:
        if server.should_exit: pass
        
    finally:
        await feature_client_connections.remove_client(
            current_websocket, client_id, main_client
        )