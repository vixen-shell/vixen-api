import json
from .FeatureSetting import FeatureSetting
from .FrameHandler import FrameHandler
from .FeaturePipe import FeaturePipe

class Feature:
    def __init__(self, setting_file_path: str):
        self.is_started = False
        self.setting_file_path = setting_file_path

        with open(self.setting_file_path, 'r') as file:
            setting_data: dict = json.load(file)

        self.setting = FeatureSetting(setting_data)
        self.frames = FrameHandler(self.setting.frames)
        self.pipe = FeaturePipe(setting_data.get('state'), self.setting_file_path)

    def start(self):
        if not self.is_started:
            self.pipe.open_pipe()
            self.frames.init()
            self.is_started = True

    async def stop(self):
        if self.is_started:
            await self.pipe.close_pipe(
                f"Feature '{self.setting.feature_name}' stopped"
            )
            self.frames.cleanup()
            self.is_started = False

    def open_frame(self, frame_id: str):
        if self.is_started:
            new_frame_id = self.frames.open(frame_id)
            return new_frame_id if new_frame_id else frame_id
    
    def close_frame(self, id: str):
        if self.is_started: self.frames.close(id)

    @property
    def frame_ids(self):
        return self.frames.frame_ids
    
    @property
    def active_frame_ids(self):
        return self.frames.active_frame_ids