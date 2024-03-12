from .parameters import FeatureParams
from .FrameHandler import FrameHandler
from .FeaturePipe import FeaturePipe
from .pipe_events import InputEvent
from .FeatureState import FeatureState

class Feature(FeatureState, FeaturePipe):
    def __init__(self, params: FeatureParams):
        FeatureState.__init__(self, params)
        FeaturePipe.__init__(self)

        self.is_started = False
        self.params = params
        self.frames = FrameHandler(self.params)

    @property
    def frame_ids(self):
        return self.frames.frame_ids
    
    @property
    def active_frame_ids(self):
        return self.frames.active_frame_ids
    
    def start(self):
        if not self.is_started:
            self.open_pipe()
            self.frames.init()
            self.is_started = True

    async def stop(self):
        if self.is_started:
            await self.close_pipe()
            self.frames.cleanup()
            self.is_started = False

    def open_frame(self, frame_id: str):
        if self.is_started:
            new_frame_id = self.frames.open(frame_id)
            return new_frame_id if new_frame_id else frame_id
    
    def close_frame(self, id: str):
        if self.is_started: self.frames.close(id)

    async def handle_pipe_events(self, event: InputEvent, client_id: str):
        if self.pipe_is_opened:
            await self.handla_state_events(event, self.client_websockets[client_id], self.dispatch_event)