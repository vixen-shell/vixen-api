from pydantic import BaseModel
from typing import Literal

class SharedModels:
    class KeyError(BaseModel):
        message: str
        error: Literal['KeyError', 'KeyExists']
        key: str