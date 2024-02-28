import os
from typing import List, Dict
from fastapi import WebSocket
from .Gtk_main_loop import Gtk_main_loop
from .Feature import Feature, FeaturePipe
from ..globals import FEATURE_SETTINGS_DIRECTORY

class Features:
    _features: Dict[str, Feature] = {}

    @staticmethod
    def init():
        Gtk_main_loop.run()

        directory = FEATURE_SETTINGS_DIRECTORY
        setting_file_paths = []

        for file_name in os.listdir(directory):
            if file_name.endswith('.json'):
                file_path = os.path.join(directory, file_name)

                if os.path.isfile(file_path):
                    setting_file_paths.append(file_path)

        for setting_file_path in setting_file_paths:
            feature = Feature(setting_file_path)
            Features._features[feature.setting.feature_name] = feature

    @staticmethod
    async def cleanup():
        for feature_name in Features._features:
            feature = Features.get(feature_name)
            if feature.is_started: await feature.stop()

        Features._features = {}
        Gtk_main_loop.quit()

    @staticmethod
    def keys() -> List[str]:
        return list(Features._features.keys())

    @staticmethod
    def key_exists(feature_name: str) -> bool:
        return feature_name in Features._features

    @staticmethod
    def get(feature_name: str) -> Feature | None:
        if Features.key_exists(feature_name):
            return Features._features[feature_name]
    
    @staticmethod
    async def connect_client_to_pipe(
        feature_name: str,
        client_id: str,
        websocket: WebSocket
    ) -> FeaturePipe | None:
        reason_for_closure = None

        if not Features.key_exists(feature_name):
            reason_for_closure = f"Feature '{feature_name}' not found"
        else:
            feature = Features.get(feature_name)
            if not feature.pipe.is_open:
                reason_for_closure = f"Feature '{feature_name}' pipe is closed"

        if reason_for_closure:
            await websocket.close(
                reason = reason_for_closure
            )
            return None
        
        await feature.pipe.connect_client(client_id, websocket)
        return feature.pipe