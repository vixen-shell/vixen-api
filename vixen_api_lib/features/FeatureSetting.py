from typing import Dict
from .frame_view import FrameSetting
from ..globals import SettingFile

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
    def __init__(self, path: str):
        self.file = SettingFile(path)
        self.feature_name: str = self.file.data['feature']
        self.frames: FrameSettingsDict = FrameSettingsDict(
            feature_name = self.feature_name,
            frames_data = self.file.data['frames']
        )