from pydantic import BaseModel
from typing import Literal

class Models:
    class FeatureState(BaseModel):
        frame_name: str
        is_loaded: bool

    class FileNotFoundError(BaseModel):
        message: str
        error: str
        filename: str