from pydantic import BaseModel
from typing import List

class Models:
    class FrameState(BaseModel):
        feature_name: str
        frame_id: str
        frame_opened: bool

    class FrameIds(BaseModel):
        frame_ids: List[str]
        active_frame_ids: List[str]
