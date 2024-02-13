import os, subprocess, json
from ..constants import VX_CONFIG_DIRECTORY, DEFAULT_FEATURES_CONFIG_FILE

def open_feature_client(feature_name: str, client_id: str) -> bool:
    if not os.path.exists(f'{VX_CONFIG_DIRECTORY}/{feature_name}.json'):
        return False
    
    cmd = f'vx-client -f {feature_name} -i {client_id} &'
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

from .globals import feature_clients

def start_default_feature_clients():
    default_features_file_path = DEFAULT_FEATURES_CONFIG_FILE

    if os.path.exists(default_features_file_path):
        with open(default_features_file_path, 'r') as file:
            active_features = json.load(file)

        for feature in active_features:
            feature_clients.open(feature)