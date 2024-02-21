from typing import Dict
from .frame_view import FrameSetting

class FrameSettingsDict(Dict[str, FrameSetting]):
    def __init__(self, feature_name: str, frames_data: list):
        frame_settings: Dict[str, FrameSetting] = {}

        for data in frames_data:
            frame_settings[data['id']] = FrameSetting(
                feature_name = feature_name,
                frame_data = data
            )

        super().__init__(frame_settings)

    @property
    def single_frame_settings(self) -> Dict[str, FrameSetting]:
        return {id: setting for id, setting in self.items() if not setting.instantiable}
    
    @property
    def instance_frame_settings(self) -> Dict[str, FrameSetting]:
        return {id: setting for id, setting in self.items() if setting.instantiable}

class FeatureSetting:
    def __init__(self, feature_data: dict):
        self.feature_name: str = feature_data['feature']
        self.frames: FrameSettingsDict = FrameSettingsDict(
            feature_name = self.feature_name,
            frames_data = feature_data['frames']
        )