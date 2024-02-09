import os, subprocess, json
from typing import Dict, List, Literal
from fastapi import HTTPException
from .client_events import ClientEventObject
from .constants import HOME_DIRECTORY
from .client_sockets_handler import client_sockets_handler

def open_client(feature_name: str, client_id: str) -> bool:
    if not os.path.exists(f'{HOME_DIRECTORY}/.config/vixen/{feature_name}.json'):
        return False
    
    cmd = f'vx-client -f {feature_name} -i {client_id} &'
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

class ClientsHandler:
    def __init__(self) -> None:
        self.clients: Dict[str, List[str]] = {}
        self.client_ids: Dict[str, List[int]] = {}

    def _new_client_id(self, feature_name: str):
        if feature_name in self.clients:
            self.client_ids[feature_name] += 1
        else:
            self.client_ids[feature_name] = 0

        client_id = f'{feature_name}_{self.client_ids[feature_name]}'

        return client_id
    
    def _subscribe(self, feature_name: str, client_id: str) -> str:
        if feature_name in self.clients:
            self.clients[feature_name].append(client_id)
        else:
            self.clients[feature_name] = [client_id]

    def _get_instance_mode(self, feature_setting_file_path: str):
        try:
            with open(feature_setting_file_path, 'r') as file:
                setting = json.load(file)
                single = setting['single'] if 'single' in setting else False
        except FileNotFoundError:
            return HTTPException(
                status_code = 404,
                detail = f"Setting file '{feature_setting_file_path}' not found!"
            )
        except json.JSONDecodeError:
            return HTTPException(
                status_code = 400,
                detail = f"Unable to decode JSON file setting file '{feature_setting_file_path}'"
            )

        return single

    def open(self, feature_name: str) -> Dict | None:
        error = None
        instance_mode = self._get_instance_mode(f'{HOME_DIRECTORY}/.config/vixen/{feature_name}.json')

        if isinstance(instance_mode, HTTPException): error = instance_mode
        else: single_instance = instance_mode

        client_state: Literal['created', 'existing'] = 'created'
        client_id: str | None = None
        
        def open_feature_client(client_id: str):
            if open_client(feature_name, client_id):
                self._subscribe(feature_name, client_id)
            else:
                return HTTPException(
                    status_code = 400,
                    detail = f"Open '{feature_name}' feature failed!"
                )

        if not error:           
            if not single_instance:
                client_id = self._new_client_id(feature_name)
                error = open_feature_client(client_id)
            else:
                if not feature_name in self.clients:
                    client_id = self._new_client_id(feature_name)
                    error = open_feature_client(client_id)
                else:
                    client_state = 'existing'
                    client_id = self.clients[feature_name][0]

        return {
            'single_instance': single_instance,
            'client_state': client_state,
            'client_id': client_id
        } if not error else error
    
    async def close(self, client_id: str):
        error = None
        websocket = client_sockets_handler.client_websockets.get(client_id)

        if not websocket:
            error = HTTPException(
                        status_code = 404,
                        detail = f"Bad client id!"
                    )
        if not error:
            event: ClientEventObject = {'id': 'close_client'}
            await websocket.send_json(event)

        return {
            'message': f"Client '{client_id}' closed"
        } if not error else error
    
    def unsubscribe(self, client_id: str):
        feature_name = client_id.split('_')[0]
        self.clients[feature_name].remove(client_id)

        if not self.clients[feature_name]:
            del self.clients[feature_name]
            del self.client_ids[feature_name]

    def get_feature_ids(self, feature_name: str):
        return self.clients.get(feature_name)
    
    def get_ids(self):
        ids: List[str] = []
        for feature in self.clients:
            ids.extend(self.clients[feature])
        return ids if ids else None

def start_default_clients():
    default_features_file_path = f'{HOME_DIRECTORY}/.config/vixen/default_features.json'

    if os.path.exists(default_features_file_path):
        with open(default_features_file_path, 'r') as file:
            active_features = json.load(file)

        for feature in active_features:
            clients_handler.open(feature)

clients_handler = ClientsHandler()