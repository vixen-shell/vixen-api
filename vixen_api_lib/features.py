import os, subprocess, json
from typing import Dict, List, Literal
from fastapi import HTTPException

home_directory = os.path.expanduser('~')

def open_feature(name: str, id: str) -> bool:
    if not os.path.exists(f'{home_directory}/.config/vixen/{name}.json'):
        return False
    
    cmd = f'vx-client -f {name} -i {id} &'
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

class FeaturesHandler:
    def __init__(self) -> None:
        self.features: Dict[str, List[str]] = {}

    def _new_client_id(self, feature_name: str):
        if feature_name in self.features:
            client_id = f'{feature_name}_{len(self.features[feature_name])}'
        else:
            client_id = f'{feature_name}_0'

        return client_id
    
    def _subscribe_feature(self, feature_name: str, client_id: str) -> str:
        if feature_name in self.features:
            self.features[feature_name].append(client_id)
        else:
            self.features[feature_name] = [client_id]

    def _get_feature_instance_mode(self, setting_file_path: str):
        try:
            with open(setting_file_path, 'r') as file:
                setting = json.load(file)
                single = setting['single'] if 'single' in setting else False
        except FileNotFoundError:
            return HTTPException(
                status_code = 404,
                detail = f"Setting file '{setting_file_path}' not found!"
            )
        except json.JSONDecodeError:
            return HTTPException(
                status_code = 400,
                detail = f"Unable to decode JSON file setting file '{setting_file_path}'"
            )

        return single

    def open(self, feature_name: str) -> Dict | None:
        error = None
        get_single_instance = self._get_feature_instance_mode(f'{home_directory}/.config/vixen/{feature_name}.json')

        if isinstance(get_single_instance, HTTPException): error = get_single_instance
        else: single_instance = get_single_instance

        client_state: Literal['created', 'existing'] = 'created'
        client_id: str | None = None
        
        def open_client_feature(client_id: str):
            if open_feature(feature_name, client_id):
                self._subscribe_feature(feature_name, client_id)
            else:
                return {'error': "Open feature failed!"}

        if not error:           
            if not single_instance:
                client_id = self._new_client_id(feature_name)
                error = open_client_feature(client_id)
            else:
                if not feature_name in self.features:
                    client_id = self._new_client_id(feature_name)
                    error = open_client_feature(client_id)
                else:
                    client_state = 'existing'
                    client_id = self.features[feature_name][0]

        return {
            'single_instance': single_instance,
            'client_state': client_state,
            'client_id': client_id
        } if not error else error
        
    def unsubscribe(self, client_id: str):
        feature_name = client_id.split('_')[0]
        self.features[feature_name].remove(client_id)
        if not self.features[feature_name]: del self.features[feature_name]

features_handler = FeaturesHandler()

def start_default_features():
    default_features_file_path = f'{home_directory}/.config/vixen/default_features.json'

    if os.path.exists(default_features_file_path):
        with open(default_features_file_path, 'r') as file:
            active_features = json.load(file)

        for feature in active_features:
            features_handler.open(feature)