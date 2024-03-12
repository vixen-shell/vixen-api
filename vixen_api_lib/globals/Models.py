from pydantic import BaseModel
from typing import Dict, List, Literal, Any

class CommonsModels:
    class Error(BaseModel):
        message: str
        details: Any

    class KeyError(BaseModel):
        error: Literal['KeyError', 'KeyExists'] = 'KeyError'
        key: str

class FeatureModels:
    class FeatureNames(BaseModel):
        names: List[str]

    class FeatureBase(BaseModel):
        name: str
        is_started: bool = True

    class FeatureState(FeatureBase):
        state: Dict[str, None | str | int | float | bool]

class FrameModels:
    class FrameIds(BaseModel):
        ids: List[str]
        actives: List[str]

    class FrameBase(BaseModel):
        id: str
        is_opened: bool = True

    class FrameProperty(FrameBase):
        feature: FeatureModels.FeatureBase
